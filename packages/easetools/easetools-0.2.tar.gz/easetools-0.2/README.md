# Math and Matrix Operations

This Python package provides a collection of functions for basic mathematical operations, statistical computations, number theory, and matrix operations. The package is designed to simplify calculations for common use cases, including arithmetic, statistical analysis, combinatorics, and linear algebra.

## Features

### Basic Operations
- `add(a, b)`: Returns the sum of `a` and `b`.
- `sub(a, b)`: Returns the difference of `a` and `b`.
- `mul(a, b)`: Returns the product of `a` and `b`.
- `div(a, b)`: Returns the division of `a` by `b`. Raises a `ValueError` if `b` is zero.

### Statistical Operations
- `maximum(a)`: Returns the maximum value in the array `a`.
- `minimum(a)`: Returns the minimum value in the array `a`.
- `mean(a)`: Returns the mean (average) of the array `a`.
- `median(a)`: Returns the median of the array `a`.
- `mode(a)`: Returns the most frequent element in the array `a`.
- `variance(a)`: Returns the variance of the array `a`.

### Number Theory
- `gcd(a, b)`: Returns the greatest common divisor of `a` and `b`.
- `lcm(a, b)`: Returns the least common multiple of `a` and `b`.
- `isprime(n)`: Checks if `n` is a prime number.
- `primes(n)`: Returns all prime numbers less than or equal to `n`.
- `factors(n)`: Returns the factors of `n`.
- `factorial(n)`: Returns the factorial of `n`.
- `permutation(n, r)`: Returns the number of permutations of `n` objects taken `r` at a time.
- `combination(n, r)`: Returns the number of combinations of `n` objects taken `r` at a time.

### Array Operations
- `subarray(arr)`: Returns all possible subarrays of the array `arr`.

### Matrix Operations
- `transpose(matrix)`: Returns the transpose of a matrix.
- `determinant(matrix)`: Returns the determinant of a matrix.
- `inverse(matrix)`: Returns the inverse of a matrix. Raises a `ValueError` if the matrix is not invertible.
- `dotproduct(a, b)`: Returns the dot product of two vectors `a` and `b`.

## Installation

You can install this package using `pip`:

```bash
pip install easetools
