"""
KrikNN is a library that includes various components for neural network operations and tensor manipulations. This README provides an overview of the `Tensor` class and its functionality, as well as instructions for running the tests.

![PyPI - Version](https://img.shields.io/pypi/v/kriknn?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/kriknn?style=for-the-badge)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/andykr1k/kriknn/publish.yaml?style=for-the-badge&label=Publish)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/andykr1k/kriknn/ci.yaml?style=for-the-badge&label=CI)
![PyPI - License](https://img.shields.io/pypi/l/kriknn?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/andykr1k/kriknn?style=for-the-badge)

Documentation: https://andykr1k.github.io/KrikNN/

## Tensor Class

The `Tensor` class is a fundamental component of the KrikNN library, allowing you to perform various operations on multidimensional arrays. 

## Features

- **Initialization**: Create tensors from data with support for different data types.
- **Matrix Multiplication**: Use the `@` operator to perform matrix multiplication.
- **Addition/Subtract**: Use the `+` or the `-` operator to perform element-wise addition and subtraction.
- **Shape**: Retrieve the shape of the tensor.

## Usage

Here’s a brief guide on how to use the `Tensor` class:

```python
import numpy as np
from kriknn.engine.tensor import Tensor

# Create tensors
tensor1 = Tensor([[1.0, 2.0], [3.0, 4.0]])
tensor2 = Tensor([[2.0, 0.0], [1.0, 2.0]])

# Matrix multiplication
result = tensor1 @ tensor2
print(result.data)  # Output: [[4.0, 4.0], [10.0, 8.0]]

# Addition
tensor3 = Tensor([[5.0, 6.0], [7.0, 8.0]])
result_add = tensor1 + tensor3
print(result_add.data)  # Output: [[6.0, 8.0], [10.0, 12.0]]

# Subtraction
tensor4 = Tensor([[5.0, 6.0], [7.0, 8.0]])
result_sub = tensor4 - tensor1
print(result_sub.data)  # Output: [[4.0, 4.0], [4.0, 4.0]]
```

## Running Tests

The KrikNN library includes tests for the `Tensor` class to ensure its functionality. The tests are written using `unittest` and can be run using the following command:

```bash
python -m tests/run.py
```

### Test Cases

1. **Initialization Tests**: Verify that tensors are initialized correctly with various data types.
2. **Shape Tests**: Ensure that the shape property returns the correct dimensions.
3. **Matrix Multiplication Tests**: Check that matrix multiplication is performed correctly.
4. **Addition/Subtraction Tests**: Validate that tensor addition and subtraction is working as expected.
5. **Error Handling Tests**: Ensure that appropriate errors are raised for invalid operations.

## Examples

The KrikNN library provides several examples to help you get started with tensor operations:

- **[Basic Tensor Operations](examples/basic_tensor_operations.py)**: Demonstrates basic tensor operations like matrix multiplication and addition/subtraction.

```bash
python examples/basic_tensor_operations.py
```

## Contribution

Contributions to the KrikNN library are welcome. Please fork the repository, make your changes, and submit a pull request. Ensure that your changes are covered by tests and adhere to the existing code style.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
"""