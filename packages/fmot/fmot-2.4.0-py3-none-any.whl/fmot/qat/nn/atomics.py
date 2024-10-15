"""
Defining the atomic operators. These operators are generally parameter-less,
instead taking as input activation/parameter tensors.
"""
from typing import List
from functools import partial
import torch
from torch import nn, Tensor
import numpy as np
from copy import copy
import fmot

from ..annotated_tensors import (
    check_for_annotations,
    copy_annotations,
    annotate,
    copy_dim_annotations,
    set_dim_annotations,
    get_dim_annotations,
    asint,
)
from . import quantizers
from ..fake_quantization import fake_quantize
from ...nn import atomics as nn_atomics
from ._utils import intitem
from ..bitwidths import fqint4, fqint8, fqint16
import torch.nn.functional as F
from fmot.functional import _apply_varname
from fmot import CONFIG, ROUND_CONFIG


class AtomicModule(nn.Module):
    def __init__(self, round=False):
        super().__init__()
        self.quantize = False
        self.round = round

    @check_for_annotations
    def forward(self, *args):
        """
        All atomic modules should implement this
        """
        raise NotImplementedError

    def __repr__(self):
        inset = ""
        if hasattr(self, "_extra_repr"):
            inset += self._extra_repr
        if hasattr(self, "quantizer"):
            if len(inset) > 0:
                inset += ", "
            inset += f"bw={self.quantizer.bitwidth}"
        return f"Quant{type(self).__name__}({inset})"

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate, observer, **observer_kwargs):
        raise NotImplementedError

    def _get_constants(self, *args):
        return dict()


ACC_BW = 32


def transpose_dim(x, dim0, dim1):
    dimensions = list(x.dimensions)
    dimensions[dim0], dimensions[dim1] = dimensions[dim1], dimensions[dim0]
    x.__setattr__("dimensions", dimensions)
    return


######################################
"""
Addition Operators
"""


def _get_add_constants(x, y, z):
    """
    Get constants for expression:
    z = x + y

    shamt_x: (left) shift amount for operand x
    shamt_y: (left) shift amount for operand y
    shamt_bwred: (left) shift amount for output buffer when reducing bitwidth
    """
    constants = {}
    if all([w.quantized for w in [x, y, z]]):
        xq, yq, zq = x.quanta, y.quanta, z.quanta
        if CONFIG.lshift_qmax:
            q = torch.min(xq, yq)
            # q = torch.min(q, zq)
        else:
            q = torch.max(xq, yq)
            # q = torch.max(q, zq)
        constants["shamt_x"] = intitem(xq - q)
        constants["shamt_y"] = intitem(yq - q)
        constants["shamt_bwred"] = intitem(q - zq)
        constants["bw"] = z.bitwidth.bitwidth
        constants["bw_x"] = x.bitwidth.bitwidth
        constants["bw_y"] = y.bitwidth.bitwidth
    return constants


class VVAdd(AtomicModule):
    def __init__(self, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]):
        super().__init__(round=ROUND_CONFIG.vvadd)
        self.quantizer = quantizers.Quantizer(
            bitwidth, observer=observer, rounded=self.round
        )

    @check_for_annotations
    def forward(self, x, y):
        dimensions = get_dim_annotations(x, y)
        if self.quantize:
            xq, yq = x.quanta, y.quanta
            _, zq = self.quantizer.get_bits_quanta()
            if CONFIG.lshift_qmax:
                q = torch.min(xq, yq)
                # q = torch.min(q, zq)
            else:
                q = torch.max(xq, yq)
                # q = torch.max(q, zq)

            y = fake_quantize(y, q, ACC_BW, rounded=False)
            x = fake_quantize(x, q, ACC_BW, rounded=False)
        return self.quantizer(set_dim_annotations(dimensions, x + y))

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(bitwidth=bw_conf.activations, observer=observer)

    def _get_constants(self, x, y):
        z = self.forward(x, y)
        constants = _get_add_constants(x, y, z)
        constants.update({"rounded": self.round})
        return constants


class VIAdd(AtomicModule):
    def __init__(self, imm, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]):
        super().__init__(round=ROUND_CONFIG.viadd)
        if isinstance(imm, torch.Tensor):
            imm = imm.clone().detach()
        else:
            imm = torch.tensor(imm)
        self.imm = nn.Parameter(imm, requires_grad=False)
        self.imm_quantizer = quantizers.ParameterQuantizer(bitwidth)
        self.quantizer = quantizers.Quantizer(
            bitwidth, observer=observer, rounded=self.round
        )

        self.q_group = quantizers.PrecisionConstraint()
        self.q_group.recursively_add(self)

    @check_for_annotations
    def forward(self, x):
        dimensions = get_dim_annotations(x)
        device = x.device
        y = self.imm_quantizer(copy_dim_annotations(x, self.imm.to(device)))
        if self.quantize:
            xq, yq = x.quanta, y.quanta
            _, zq = self.quantizer.get_bits_quanta()
            if CONFIG.lshift_qmax:
                q = torch.min(xq, yq)
                # q = torch.min(q, zq)
            else:
                q = torch.max(xq, yq)
                # q = torch.max(q, zq)
            y = fake_quantize(y, q, y.bitwidth.bitwidth, rounded=False)
            x = fake_quantize(x, q, x.bitwidth.bitwidth, rounded=False)
        return self.quantizer(set_dim_annotations(dimensions, x + y))

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(imm=parent.imm, bitwidth=bw_conf.activations, observer=observer)

    @property
    def _extra_repr(self):
        return f"imm={self.imm.item():.3f}"

    def _get_constants(self, x):
        y = self.imm_quantizer(self.imm)
        z = self.forward(x)
        constants = _get_add_constants(x, y, z)
        if y.quantized:
            constants["y"] = asint(y).cpu().item()
        constants["rounded"] = self.round
        return constants


class VVSub(AtomicModule):
    def __init__(self, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]):
        super().__init__(round=ROUND_CONFIG.vvadd)
        self.quantizer = quantizers.Quantizer(
            bitwidth, observer=observer, rounded=self.round
        )

    @check_for_annotations
    def forward(self, x, y):
        dimensions = get_dim_annotations(x, y)
        if self.quantize:
            xq, yq = x.quanta, y.quanta
            _, zq = self.quantizer.get_bits_quanta()
            if CONFIG.lshift_qmax:
                q = torch.min(xq, yq)
                # q = torch.min(q, zq)
            else:
                q = torch.max(xq, yq)
                # q = torch.max(q, zq)
            x, y = tuple(fake_quantize(arg, q, ACC_BW, rounded=False) for arg in (x, y))
        return self.quantizer(set_dim_annotations(dimensions, x - y))

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(bitwidth=bw_conf.activations, observer=observer)

    def _get_constants(self, x, y):
        z = self.forward(x, y)
        constants = _get_add_constants(x, y, z)
        constants["rounded"] = self.round
        return constants


class Neg(AtomicModule):
    @check_for_annotations
    def forward(self, x):
        y = -x
        if self.quantize:
            y = fake_quantize(y, x.quanta, x.bitwidth.bitwidth, rounded=self.round)
        copy_annotations(x, y)
        y.avg_sparsity = 0.0
        y.density_per_element = None
        y.prev_relu = False
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls()

    def _get_constants(self, x):
        constants = {}
        if x.quantized:
            constants["bw"] = x.bitwidth.bitwidth
        return constants


#######################################
"""
Multiply Operators
"""


def _get_mul_constants(x, y, z):
    constants = {}
    if all([w.quantized for w in [x, y, z]]):
        xq, yq, zq = [w.quanta for w in [x, y, z]]
        buffer_quanta = xq + yq
        constants["shamt_bwred"] = intitem(buffer_quanta - zq)
        constants["bw"] = z.bitwidth.bitwidth
    return constants


class VVMul(AtomicModule):
    def __init__(self, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]):
        super().__init__(round=ROUND_CONFIG.vvmul)
        self.quantizer = quantizers.Quantizer(
            bitwidth, observer=observer, rounded=self.round
        )

    @check_for_annotations
    def forward(self, x, y):
        dimensions = get_dim_annotations(x, y)
        return self.quantizer(set_dim_annotations(dimensions, x * y))

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(bitwidth=bw_conf.activations, observer=observer)

    def _get_constants(self, x, y):
        z = self.forward(x, y)
        constants = _get_mul_constants(x, y, z)
        constants.update({"rounded": self.round})
        return constants


class VIMul(AtomicModule):
    def __init__(self, imm, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]):
        super().__init__(round=ROUND_CONFIG.vimul)
        if isinstance(imm, torch.Tensor):
            imm = imm.clone().detach()
        else:
            imm = torch.tensor(imm)
        self.imm = nn.Parameter(imm, requires_grad=False)
        self.imm_quantizer = quantizers.ParameterQuantizer(
            bitwidth, observer=quantizers.MinMaxObserver
        )
        self.quantizer = quantizers.Quantizer(
            bitwidth, observer=observer, rounded=self.round
        )

        self.q_group = quantizers.PrecisionConstraint()
        self.q_group.recursively_add(self)

    @check_for_annotations
    def forward(self, x):
        device = x.device
        y = self.imm_quantizer(copy_dim_annotations(x, self.imm.to(device)))
        return self.quantizer(copy_dim_annotations(x, x * y))

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(imm=parent.imm, bitwidth=bw_conf.activations, observer=observer)

    def _get_constants(self, x):
        z = self.forward(x)
        y = self.imm_quantizer(self.imm)
        constants = _get_mul_constants(x, y, z)
        if y.quantized:
            constants["y"] = asint(y).cpu().item()
        constants["rounded"] = self.round
        return constants


def is_sparse(*tensors):
    return [x.avg_sparsity != 0 for x in tensors]


class _diffable_pos(torch.autograd.Function):
    """
    Returns the mask x > 0 as a FloatTensor.
    Uses a surrogate gradient equivalent to the gradient w.r.t. ReLU
    """

    @staticmethod
    def forward(ctx, x):
        nz = x > 0
        ctx.save_for_backward(nz)
        return nz.float()

    @staticmethod
    def backward(ctx, grad):
        grad_nz = None
        if ctx.needs_input_grad[0]:
            (nz,) = ctx.saved_tensors
            grad_nz = nz.float() * grad
        return grad_nz


####################################
"""
Reduction
"""


class Sum(AtomicModule):
    def __init__(
        self, dim, keepdim, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]
    ):
        super().__init__(round=False)
        self.quantizer = quantizers.Quantizer(
            bitwidth, observer=observer, rounded=self.round
        )
        self.dim = dim
        self.keepdim = keepdim

    @check_for_annotations
    def forward(self, x):
        y = torch.sum(x, dim=self.dim, keepdim=self.keepdim)
        y = self.quantizer(copy_dim_annotations(x, y))
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(
            dim=parent.dim,
            keepdim=parent.keepdim,
            bitwidth=bw_conf.activations,
            observer=observer,
        )

    def _get_constants(self, x):
        dim = self.dim
        if isinstance(dim, list):
            dim = tuple(dim)
        constants = {"dim": dim, "keepdim": self.keepdim}
        y = self.forward(x)
        if x.quantized and y.quantized:
            xq, yq = x.quanta, y.quanta
            constants["shamt_bwred"] = intitem(xq - yq)
            constants["bw"] = y.bitwidth.bitwidth
        return constants

    @property
    def _extra_repr(self):
        return f"dim={self.dim}"


####################################
"""
Activation Functions
"""


class ReLU(AtomicModule):
    def __init__(self, alpha=0.95):
        super().__init__(round=False)
        self.alpha = alpha
        self.register_buffer("avg_sparsity", None)
        # self.register_buffer('density_per_element', None)

    @torch.no_grad()
    def update_sparsity(self, x):
        if x.dimensions is not None:
            f_dim = x.dimensions.index("F")
            dims = list(range(x.ndim))
            dims.remove(f_dim)
            density_per_element = (x != 0).float().mean(dims)
            sparsity = 1 - density_per_element.mean()
            if self.avg_sparsity is None:
                self.avg_sparsity = sparsity
                self.density_per_element = density_per_element
            else:
                self.avg_sparsity = ReLU._lpf_update(
                    self.alpha, self.avg_sparsity, sparsity
                )
                # self.density_per_element = ReLU._lpf_update(
                #     self.alpha, self.density_per_element, density_per_element)
        else:
            sparsity = (x == 0).float().mean()
            if self.avg_sparsity is None:
                self.avg_sparsity = sparsity
            else:
                self.avg_sparsity = ReLU._lpf_update(
                    self.alpha, self.avg_sparsity, sparsity
                )

    @staticmethod
    def _lpf_update(s, old, new):
        return s * old + (1 - s) * new

    @check_for_annotations
    def forward(self, x):
        y = x.relu()
        y.dimensions = x.dimensions
        self.update_sparsity(y)
        y = copy_annotations(x, y)
        y.avg_sparsity = self.avg_sparsity
        y.density_per_element = None
        y.prev_relu = True
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls()

    def __repr__(self):
        repr = super().__repr__()
        if self.avg_sparsity is not None:
            repr += " (Act. Sparsity: {:.0f}%)".format(self.avg_sparsity * 100)

        return repr


class Identity(AtomicModule):
    @check_for_annotations
    def forward(self, x):
        return x

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls()


class TagVarname(AtomicModule):
    def __init__(self, varname: str):
        super().__init__()
        self.varname = varname

    @check_for_annotations
    def forward(self, x):
        return _apply_varname(x, self.varname)

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(parent.varname)


class OnesLike(AtomicModule):
    def __init__(self, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"]):
        super().__init__(round=False)
        self.quantizer = quantizers.Quantizer(bitwidth, observer=observer)

    @check_for_annotations
    def forward(self, x):
        y = torch.ones_like(x)
        return self.quantizer(copy_dim_annotations(x, y))

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(bitwidth=bw_conf.activations, observer=observer)

    def _get_constants(self, x):
        y = self.forward(x)
        constants = {}
        if x.quantized:
            constants = {"imm": asint(y).flatten()[0].cpu().item()}
        return constants


class Table:
    def __init__(self, x, y, name):
        assert len(x) == len(y)
        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)
        self.name = name
        self.x = x
        self.y = y
        self.N = len(self.x)

    def __eq__(self, other):
        assert isinstance(other, Table)
        if self.N == other.N:
            return np.all(self.y == other.y)
        else:
            return False

    def __lt__(self, other):
        if self.__eq__(other):
            return False
        else:
            return self.name < other.name

    def __gt__(self, other):
        if self.__eq__(other):
            return False
        else:
            return self.name > other.name

    def __repr__(self):
        return f"<{self.name}>"


class BareLUT(AtomicModule):
    def __init__(
        self,
        function,
        bitwidth,
        limits=None,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
    ):
        super().__init__(round=False)
        self.function = function
        self.quantizer = quantizers.Quantizer(bitwidth, observer=observer)

    @check_for_annotations
    def forward(self, x):
        if x.quantized:
            assert x.bitwidth == fqint8
        y = self.function(x)
        return self.quantizer(copy_dim_annotations(x, y))

    def get_table(self, x):
        bits, quanta = x.bitwidth.bitwidth, x.quanta
        levels = 2**bits
        min_x = -(2 ** (bits + quanta - 1))
        max_x = (2 ** (bits - 1) - 1) * 2**quanta
        y = torch.linspace(min_x, max_x, levels, device=x.device)
        y = self.quantizer(copy_dim_annotations(x, self.function(y)))
        x_int = np.linspace(-levels // 2, levels // 2 - 1, levels, dtype=int)
        y_int = asint(y).cpu().numpy()
        return Table(x=x_int, y=y_int, name=self.function.__name__)

    def _get_constants(self, x):
        constants = {}
        if x.quantized:
            constants["shamt_address"] = 0
            constants["bw_address"] = 8
            constants["table"] = self.get_table(x)
        constants["function"] = self.function.__name__
        return constants


####################
"""
Tensor slicing and joining
"""


class Chunk(nn.Module):
    def __init__(self, chunks, dim=0):
        super().__init__()
        self.round = False
        self.chunks = chunks
        self.dim = dim

    @check_for_annotations
    def forward(self, x):
        z = torch.chunk(x, self.chunks, self.dim)
        return [copy_annotations(x, zz) for zz in z]

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(chunks=parent.chunks, dim=parent.dim)

    def _get_constants(self, x):
        return {"chunks": self.chunks, "dim": self.dim}

    @property
    def _extra_repr(self):
        return f"chunks={self.chunks}, dim={self.dim}"


class Split(AtomicModule):
    def __init__(self, split_sizes: List[int], dim=0):
        super().__init__(round=False)
        self.split_sizes = split_sizes
        self.dim = dim

    @check_for_annotations
    def forward(self, x):
        z = torch.split(x, self.split_sizes, self.dim)
        return [copy_annotations(x, zz + 0) for zz in z]

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(split_sizes=parent.split_sizes, dim=parent.dim)

    def _get_constants(self, x):
        return {"lengths": self.split_sizes, "dim": self.dim}

    @property
    def _extra_repr(self):
        return f"split_sizes={self.split_sizes}, dim={self.dim}"


class BareCat(AtomicModule):
    def __init__(self, dim=0):
        super().__init__(round=False)
        self.dim = dim

    @check_for_annotations
    def forward(self, *tensors):
        z = torch.cat(tensors, self.dim)
        return copy_annotations(tensors[0], z)

    def _get_constants(self, *x):
        return {"dim": self.dim}

    def _getargnames(self):
        i = 0
        while True:
            yield f"x{i}"
            i += 1


class Cat(nn.Module):
    def __init__(self, dim, bitwidth, observer):
        super().__init__()
        self.cat = BareCat(dim)
        self.requantizers = nn.ModuleList()
        self.q_group = quantizers.PrecisionConstraint()
        self._built = False
        self._obs = observer
        self._bw = bitwidth

    def _build(self, N):
        for __ in range(N):
            req = Requantize(self._bw, self._obs)
            self.requantizers.append(req)
            self.q_group.recursively_add(req)
        quantizers.share_observer(self.requantizers)
        self._built = True

    @check_for_annotations
    def forward(self, tensors):
        if not self._built:
            N = len(tensors)
            self._build(N)
        new_tensors = [req(t) for req, t in zip(self.requantizers, tensors)]
        return self.cat(*new_tensors)

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(dim=parent.dim, bitwidth=bw_conf.activations, observer=observer)


class Stack(AtomicModule):
    def __init__(self, dim=0):
        super().__init__(round=False)
        self.dim = dim

    @check_for_annotations
    def forward(self, tensors: List[Tensor]):
        t0 = tensors[0]
        if t0.quantized:
            assert all(
                [t.quanta == t0.quanta for t in tensors]
            ), "Cannot concatenate tensors with different quanta"
        z = torch.stack(tensors, self.dim)
        return copy_annotations(tensors[0], z)

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(dim=parent.dim)

    def _get_constants(self, x):
        return {"dim": self.dim}

    @property
    def _extra_repr(self):
        return f"dim={self.dim}"

    def _getargnames(self):
        i = 0
        while True:
            yield f"x{i}"
            i += 1


class Transpose(AtomicModule):
    """
    Performs a transpose on a matrix.
    """

    def __init__(self):
        super().__init__(round=False)

    @check_for_annotations
    def forward(self, x):
        z = x.t()
        return copy_annotations(x, z)

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls()

    def _get_constants(self, x):
        return {"dim0": 0, "dim1": 1}


class Reshape(AtomicModule):
    """
    Performs a transpose on a matrix.
    """

    def __init__(self, shape):
        super().__init__(round=False)
        self.shape = shape

    @check_for_annotations
    def forward(self, x):
        z = torch.reshape(x, self.shape)
        return copy_annotations(x, z)

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(parent.shape)

    def _get_constants(self, x):
        return {"shape": self.shape}


"""
Requantize
"""


class Requantize(AtomicModule):
    def __init__(
        self, bitwidth, observer=quantizers.DEFAULT_OBSERVERS["default"], **kwargs
    ):
        super().__init__(round=ROUND_CONFIG.vshift)
        self.quantizer = quantizers.Quantizer(bitwidth, observer=observer, **kwargs)

    @check_for_annotations
    def forward(self, x):
        prev_relu = x.prev_relu
        avg_sparsity = x.avg_sparsity
        x_clone = x + 0
        copy_annotations(x, x_clone)
        y = self.quantizer(x_clone)
        y.avg_sparsity = avg_sparsity
        y.prev_relu = prev_relu
        y.density_per_element = x.density_per_element
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        observer = partial(observer, **kwargs)
        return cls(bitwidth=bw_conf.activations, observer=observer)

    def _get_constants(self, x):
        y = self.forward(x)
        constants = {"shamt": intitem(x.quanta - y.quanta), "bw": y.bitwidth.bitwidth}
        constants["rounded"] = self.round
        return constants


class Shift(AtomicModule):
    def __init__(self, shamt, bitwidth):
        super().__init__(round=ROUND_CONFIG.vshift)
        self.shamt = shamt
        self.bitwidth = bitwidth

    @check_for_annotations
    def forward(self, x):
        prev_relu = x.prev_relu
        quanta = x.quanta
        avg_sparsity = x.avg_sparsity
        density_per_element = x.density_per_element
        if self.quantize:
            quanta = quanta - self.shamt
            y = fake_quantize(x, quanta, self.bitwidth.bitwidth, rounded=self.round)
        else:
            mv = torch.max(torch.abs(x))
            mvq = torch.ceil(torch.log2(mv))
            mv = 2.0**mvq
            y = torch.clamp(x, -mv * 2**-self.shamt, mv * 2**-self.shamt)
        y = annotate(
            y,
            bitwidth=self.bitwidth,
            quanta=quanta,
            quantized=True,
            avg_sparsity=avg_sparsity,
            density_per_element=density_per_element,
            prev_relu=prev_relu,
        )
        copy_dim_annotations(x, y)
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(shamt=parent.shamt, bitwidth=bw_conf.activations)

    def _get_constants(self, x):
        constants = {"shamt": self.shamt, "bw": self.bitwidth.bitwidth}
        constants["rounded"] = self.round
        return constants


class Gt0(AtomicModule):
    def __init__(self, bitwidth, pseudo_derivative=True):
        super().__init__(round=False)
        self.bitwidth = bitwidth
        self.pseudo_derivative = pseudo_derivative

    @check_for_annotations
    def forward(self, x):
        quanta = x.quanta
        quantized = x.quantized
        avg_sparsity = x.avg_sparsity
        if not self.pseudo_derivative:
            x = x.detach()
        y = nn_atomics._diffable_gt0.apply(x)
        if self.quantize:
            quanta = quanta * 0
        y = annotate(
            y,
            bitwidth=self.bitwidth,
            quanta=quanta,
            quantized=quantized,
            avg_sparsity=avg_sparsity,
            prev_relu=True,
        )
        copy_dim_annotations(x, y)
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(
            bitwidth=bw_conf.activations, pseudo_derivative=parent.pseudo_derivative
        )

    def _get_constants(self, x):
        return {"bw": self.bitwidth.bitwidth}


class FTranspose(AtomicModule):
    """
    Performs a functional transpose on a matrix.
    """

    def __init__(self, dim0, dim1):
        super().__init__(round=False)
        self.dim0 = dim0
        self.dim1 = dim1
        self.tracing_mode = False

    @check_for_annotations
    def forward(self, x):
        # In tracing mode, we assume that we only have an input of shape
        # (batch_size, feature_size)
        if self.tracing_mode:
            z = x
        else:
            dimensions = list(x.dimensions)
            if set([dimensions[self.dim0], dimensions[self.dim1]]) == {"B", "F"}:
                raise Exception("We don't support Batch-Feature dimension swap")
            z = torch.transpose(x, self.dim0, self.dim1)
            z = copy_annotations(x, z)
            transpose_dim(z, self.dim0, self.dim1)
        return z

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(parent.dim0, parent.dim1)

    def _get_constants(self, x):
        return {"dim0": self.dim0, "dim1": self.dim1}


class Permute(AtomicModule):
    """
    Performs a permutation on a tensor.
    """

    def __init__(self, dims):
        super().__init__(round=False)
        self.dims = dims
        self.tracing_mode = False

    @check_for_annotations
    def forward(self, x):
        # In tracing mode, we assume that we only have an input of shape
        # (batch_size, feature_size)
        if self.tracing_mode:
            z = x
        else:
            dimensions = x.dimensions
            if set([dimensions[self.dim0], dimensions[self.dim1]]) == {"B", "F"}:
                raise Exception("We don't support Batch-Feature dimension swap")
            z = torch.transpose(x, self.dim0, self.dim1)
            z = copy_annotations(x, z)
            transpose_dim(z, self.dim0, self.dim1)
        return z

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(parent.dim0, parent.dim1)

    def _get_constants(self, x):
        return {"dim0": self.dim0, "dim1": self.dim1}


class Dropout(AtomicModule):
    def __init__(self, p, training, inplace):
        super().__init__(round=False)
        self.p = p
        self.training = training
        self.inplace = inplace

    @check_for_annotations
    def forward(self, x):
        if self.training:
            device = x.device
            mask = torch.bernoulli(torch.zeros(x.shape) + (1 - self.p)).to(device)
            z = mask * x / (1 - self.p)
            return copy_annotations(x, z)
        else:
            return x

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(p=parent.p, training=parent.training, inplace=parent.inplace)


class Squeeze(AtomicModule):
    def __init__(self, dim):
        super().__init__(round=False)
        self.dim = dim

    def forward(self, x):
        y = x.squeeze(self.dim)
        y = copy_annotations(x, y)
        dims = copy(get_dim_annotations(x))
        if dims is not None:
            del dims[self.dim]
            set_dim_annotations(dims, y)
        return y

    @classmethod
    def _from_float(
        cls,
        parent,
        bw_conf,
        interpolate,
        observer=quantizers.DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        return cls(parent.dim)

    def _get_constants(self, x):
        return {"dim": self.dim}
