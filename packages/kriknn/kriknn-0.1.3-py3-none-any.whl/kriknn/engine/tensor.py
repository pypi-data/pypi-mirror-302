import numpy as np


class Tensor:
    """
    A class that represents a tensor (multidimensional array) for numerical operations.

    Attributes:
    -----------
    data : np.ndarray
        A NumPy array that holds the numerical data of the tensor.
    
    dtype : data-type (default: np.float32)
        The data type of the tensor elements.
    
    shape : tuple
        The shape (dimensions) of the tensor.
    """

    def __init__(self, data, dtype=np.float32):
        """
        Initializes a Tensor object.

        Parameters:
        -----------
        data : list, np.ndarray, int, or float
            The input data to create the tensor. It can be a Python list, NumPy array, or scalar (int/float).
        
        dtype : data-type (default: np.float32)
            The desired data type of the tensor elements.

        Raises:
        -------
        TypeError
            If the provided data is not a list, NumPy array, or scalar.
        """
        if isinstance(data, list):
            self.data = np.array(data, dtype=dtype)
        elif isinstance(data, np.ndarray):
            self.data = data
        elif isinstance(data, (int, float)):
            self.data = np.array(data, dtype=dtype)
        else:
            raise TypeError(
                "Data must be a list, a numpy array, or a scalar (int/float).")
        self.dtype = dtype
        self.shape = self.data.shape

    def __repr__(self):
        """
        Returns a string representation of the Tensor object for easy debugging.

        Returns:
        --------
        str
            The string representation of the tensor, displaying its shape, data type, and content.
        """
        return f"Tensor(shape={self.shape}, dtype={self.dtype}, data={self.data})"

    def __matmul__(self, other):
        """
        Implements the matrix multiplication operator (`@`) for two tensors.

        Parameters:
        -----------
        other : Tensor
            The other tensor to perform matrix multiplication with.

        Returns:
        --------
        Tensor
            A new Tensor representing the result of the matrix multiplication.

        Raises:
        -------
        TypeError
            If the operand is not of type Tensor.
        """
        if not isinstance(other, Tensor):
            raise TypeError(
                f"Unsupported operand type(s) for @: 'Tensor' and '{type(other).__name__}'")
        return Tensor(np.matmul(self.data, other.data))

    def __add__(self, other):
        """
        Implements the addition operator (`+`) for two tensors.

        Parameters:
        -----------
        other : Tensor
            The other tensor to add to the current tensor.

        Returns:
        --------
        Tensor
            A new Tensor representing the result of the addition.

        Raises:
        -------
        TypeError
            If the operand is not of type Tensor.
        """
        if not isinstance(other, Tensor):
            raise TypeError(
                f"Unsupported operand type(s) for +: 'Tensor' and '{type(other).__name__}'")
        return Tensor(self.data + other.data)

    def get_data(self):
        """
        Retrieves the raw NumPy array data of the tensor.

        Returns:
        --------
        np.ndarray
            The data stored in the tensor.
        """
        return self.data

    @staticmethod
    def zeros(shape, dtype=np.float32):
        """
        Creates a Tensor initialized with all zeros.

        Parameters:
        -----------
        shape : tuple
            The shape of the tensor.
        
        dtype : data-type (default: np.float32)
            The desired data type of the tensor elements.

        Returns:
        --------
        Tensor
            A new Tensor filled with zeros.
        """
        return Tensor(np.zeros(shape, dtype=dtype))

    @staticmethod
    def ones(shape, dtype=np.float32):
        """
        Creates a Tensor initialized with all ones.

        Parameters:
        -----------
        shape : tuple
            The shape of the tensor.
        
        dtype : data-type (default: np.float32)
            The desired data type of the tensor elements.

        Returns:
        --------
        Tensor
            A new Tensor filled with ones.
        """
        return Tensor(np.ones(shape, dtype=dtype))

    @staticmethod
    def uniform(shape, low=0.0, high=1.0, dtype=np.float32):
        """
        Creates a Tensor initialized with random values drawn from a uniform distribution.

        Parameters:
        -----------
        shape : tuple
            The shape of the tensor.
        
        low : float (default: 0.0)
            The lower bound of the uniform distribution.
        
        high : float (default: 1.0)
            The upper bound of the uniform distribution.
        
        dtype : data-type (default: np.float32)
            The desired data type of the tensor elements.

        Returns:
        --------
        Tensor
            A new Tensor filled with random values.
        """
        return Tensor(np.random.uniform(low, high, size=shape).astype(dtype))

    def add(self, other):
        """
        Element-wise addition of two tensors.

        Parameters:
        -----------
        other : Tensor
            The other tensor to add to the current tensor.

        Returns:
        --------
        Tensor
            A new Tensor representing the element-wise addition of the two tensors.

        Raises:
        -------
        TypeError
            If the operand is not of type Tensor.
        """
        if isinstance(other, Tensor):
            return Tensor(self.data + other.data, dtype=self.dtype)
        else:
            raise TypeError("Operand must be a Tensor.")

    def subtract(self, other):
        """
        Element-wise subtraction of two tensors.

        Parameters:
        -----------
        other : Tensor
            The other tensor to subtract from the current tensor.

        Returns:
        --------
        Tensor
            A new Tensor representing the element-wise subtraction of the two tensors.

        Raises:
        -------
        TypeError
            If the operand is not of type Tensor.
        """
        if isinstance(other, Tensor):
            return Tensor(self.data - other.data, dtype=self.dtype)
        else:
            raise TypeError("Operand must be a Tensor.")

    def mul(self, other):
        """
        Element-wise multiplication of two tensors.

        Parameters:
        -----------
        other : Tensor
            The other tensor to multiply with the current tensor.

        Returns:
        --------
        Tensor
            A new Tensor representing the element-wise multiplication of the two tensors.

        Raises:
        -------
        TypeError
            If the operand is not of type Tensor.
        """
        if isinstance(other, Tensor):
            return Tensor(self.data * other.data, dtype=self.dtype)
        else:
            raise TypeError("Operand must be a Tensor.")

    def dot(self, other):
        """
        Computes the dot product of two tensors.

        Parameters:
        -----------
        other : Tensor
            The other tensor to perform the dot product with.

        Returns:
        --------
        Tensor
            A new Tensor representing the result of the dot product.

        Raises:
        -------
        TypeError
            If the operand is not of type Tensor.
        """
        if isinstance(other, Tensor):
            return Tensor(np.dot(self.data, other.data), dtype=self.dtype)
        else:
            raise TypeError("Operand must be a Tensor.")

    def transpose(self):
        """
        Returns the transposed version of the tensor (flips the dimensions).

        Returns:
        --------
        Tensor
            A new Tensor with transposed dimensions.
        """
        return Tensor(self.data.T, dtype=self.dtype)
