def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    if (b==0):
        raise ValueError("Denominator cannot be zero")
    return a/b
def maximum(a):
    return max(a)
def minimum(a):
    return min(a)
def mean(a):
    return sum(a)/len(a)
def median(a):
    a.sort()
    n = len(a)
    if n%2 == 0:
        return (a[n//2-1]+a[n//2])/2
    else:
        return a[n//2]
def mode(a):
    d = {}
    for i in a:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    max_count = max(d.values())
    mode = [k for k,v in d.items() if v == max_count]
    return mode[0]
def variance(a):
    n = len(a)
    mean = sum(a)/n
    variance = sum((x-mean)**2 for x in a)/n
    return variance
def subarray(arr):
    subarrays = []
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            subarrays.append(arr[i:j+1])
    return subarrays
def factorial(n):
    if n == 0:
        return 1
    return n*factorial(n-1)
def permutation(n,r):
    return factorial(n)/factorial(n-r)
def combination(n,r):
    return factorial(n)/(factorial(n-r)*factorial(r))
def gcd(a,b):
    if b == 0:
        return a
    return gcd(b, a%b)
def lcm(a,b):
    return a*b//gcd(a,b)
def isprime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n%i == 0:
            return False
    return True
def primes(n):
    primes = []
    for i in range(2,n+1):
        if isprime(i):
            primes.append(i)
    return primes
def factors(n):
    factors = []
    for i in range(1,n+1):
        if n%i == 0:
            factors.append(i)
    return factors
def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for i in range(len(matrix)):
        det += ((-1)**i)*matrix[0][i]*determinant([row[:i]+row[i+1:] for row in matrix[1:]])
    return det
def inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    if len(matrix) == 2:
        return [[matrix[1][1]/det, -matrix[0][1]/det], [-matrix[1][0]/det, matrix[0][0]/det]]
    cofactors = []
    for i in range(len(matrix)):
        cofactor_row = []
        for j in range(len(matrix)):
            minor = [row[:j]+row[j+1:] for row in (matrix[:i]+matrix[i+1:])]
            cofactor_row.append(((-1)**(i+j)) * determinant(minor))
        cofactors.append(cofactor_row)
    cofactors = transpose(cofactors)
    for i in range(len(cofactors)):
        for j in range(len(cofactors)):
            cofactors[i][j] = cofactors[i][j]/det
    return cofactors
def dotproduct(a,b):
    return sum([a[i]*b[i] for i in range(len(a))])