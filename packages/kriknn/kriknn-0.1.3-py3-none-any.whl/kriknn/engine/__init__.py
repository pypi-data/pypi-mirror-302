"""
The `engine` submodule of KrikNN provides the core components and classes for tensor operations.

This submodule includes the following classes:

- **Tensor**: A class that represents multidimensional arrays (tensors) and supports a variety of numerical operations such as matrix multiplication, addition, and element-wise operations.

Main Features:
- Tensor creation from various data types.
- Matrix multiplication using the `@` operator.
- Element-wise operations (addition, subtraction, multiplication).
- Static methods for creating zero, one, and randomly initialized tensors.
- Transpose, dot product, and shape retrieval for tensor manipulations.

Example usage:

```python
from kriknn.engine import Tensor

tensor1 = Tensor([[1.0, 2.0], [3.0, 4.0]])
tensor2 = Tensor([[2.0, 0.0], [1.0, 2.0]])

# Matrix multiplication
result = tensor1 @ tensor2
print(result.data)
```

This module serves as the foundation for building and managing neural network structures within KrikNN.

"""