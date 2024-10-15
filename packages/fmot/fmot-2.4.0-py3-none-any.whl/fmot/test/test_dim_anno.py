import torch
from torch import nn
import fmot

# We need to import these for explicit type annotations
from typing import List, Tuple
from torch import Tensor

from fmot.nn import (
    RNNCell,
    LSTMCell,
    GRUCell,
    RNN,
    LSTM,
    GRU,
    MultiLayerRNN,
    Sequential,
)
from fmot.nn.conv1d import TemporalConv1d, SequencedTemporalConv1d
from fmot.nn import rgetattr, rsetattr, map_param_name, get_trailing_number
from fmot.nn import default_torch2seq_param_mapping
from fmot.nn import BasicRNN, SuperBasic

from fmot import qat as Q


class TestDimAnnotations:
    def test_conv2lin(self):
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.tcn = TemporalConv1d(8, 6, 4)  # output: B*6
                self.linear = nn.Linear(6, 3)

            def forward(self, x):
                y = self.tcn(x)
                y = torch.transpose(y, 1, 2)
                output = self.linear(y)

                return output

        model = Net()
        batch_size = 5
        timesteps = 10
        n_features = 8

        cmodel = fmot.ConvertedModel(model, batch_dim=0, seq_dim=-1)
        inputs = [torch.randn(batch_size, n_features, timesteps) for _ in range(5)]
        cmodel.quantize(inputs)

        x = torch.randn(batch_size, n_features, timesteps)
        x.dimensions = ["B", "F", "T"]
        output = cmodel(x)

        assert output.dimensions == ["B", "T", "F"]

    def test_conv2rnn(self):
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.tcn = TemporalConv1d(8, 6, 4)  # output: B*6
                self.rnn = RNN(6, 3, batch_first=True)

            def forward(self, x):
                y = self.tcn(x)
                y = torch.transpose(y, 1, 2)
                output, _ = self.rnn(y)

                return output

        model = Net()
        batch_size = 5
        timesteps = 10
        n_features = 8

        cmodel = fmot.ConvertedModel(model, batch_dim=0, seq_dim=-1)
        inputs = [torch.randn(batch_size, n_features, timesteps) for _ in range(5)]
        cmodel.quantize(inputs)

        x = torch.randn(batch_size, n_features, timesteps)
        output = cmodel(x)

        assert output.dimensions == ["B", "T", "F"]

    # def test_4d_propag(self):
    #     import torch
    #     import fmot

    #     model = torch.nn.Conv2d(1, 16, 2, 2)
    #     x = torch.randn(1, 1, 96, 96)

    #     # convert, quantize
    #     named_dims = ['B', 'F', 'H', 'W']
    #     cmodel = fmot.ConvertedModel(model, named_dims=named_dims)  # cannot tag dims yet...
    #     cmodel.quantize([torch.randn(5, 1, 4, 4) for _ in range(2)])
    #     y = cmodel(x)
    #     assert y.dimensions == named_dims

    def test_torch_1_9(self):
        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.linears = nn.ModuleList([nn.Linear(4, 4), nn.Linear(4, 4)])

            def forward(self, x):
                for l in self.linears:
                    y = l(x)

                return y

        model = Net()
        batch_size = 5
        timesteps = 10
        n_features = 8

        cmodel = fmot.ConvertedModel(model, batch_dim=0, seq_dim=-1)


if __name__ == "__main__":
    my_test = TestDimAnnotations()
    my_test.test_conv2lin()
