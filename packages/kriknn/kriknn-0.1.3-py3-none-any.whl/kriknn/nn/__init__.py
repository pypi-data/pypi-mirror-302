import numpy as np
from kriknn.engine.tensor import Tensor

class Linear:
    """
    Implements a fully connected (linear) layer for a neural network.

    Attributes:
    -----------
    weight : Tensor
        A 2D tensor containing the weights of the layer with shape (features_in, features_out).
        The weights are initialized with random values drawn from a uniform distribution 
        in the range [-bound, bound], where bound is the inverse of the square root of features_in.
    
    bias : Tensor
        A 1D tensor containing the biases of the layer with shape (features_out,).
        The biases are also initialized with random values from the same uniform distribution.
    """

    def __init__(self, features_in: int, features_out: int):
        """
        Initializes the Linear layer.

        Parameters:
        -----------
        features_in : int
            The number of input features (size of the input layer).
        
        features_out : int
            The number of output features (size of the output layer).

        Initialization:
        ---------------
        - The weight matrix is initialized using a uniform distribution over the range 
          [-bound, bound], where `bound = 1 / sqrt(features_in)`.
        - The bias vector is also initialized with a uniform distribution over the same range.
        """
        bound = 1 / np.sqrt(features_in)
        self.weight = Tensor.uniform(
            (features_in, features_out), -bound, bound)
        self.bias = Tensor.uniform((features_out,), -bound, bound)

    def __call__(self, x: Tensor) -> Tensor:
        """
        Forward pass of the linear layer. Computes the output by applying the 
        linear transformation: output = x @ weight + bias.

        Parameters:
        -----------
        x : Tensor
            A tensor of shape (batch_size, features_in) representing the input data.

        Returns:
        --------
        Tensor
            The transformed output tensor with shape (batch_size, features_out).
        """
        return x @ self.weight + self.bias
