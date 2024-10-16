"""Main module."""
# pymatica/basic_statistics.py
PI = 3.141592653589793
E = 2.718281828459045
PHI = 1.618033988749895  # Golden ratio
GOLDEN_RATIO = PHI      # Alias for PHI
SQRT2 = 1.4142135623730951  # Square root of 2
SQRT3 = 1.7320508075688772  # Square root of 3
SQRT5 = 2.23606797749979  # Square root of 5
LOG2E = 1.4426950408889634  # log base 2 of e
LOG10E = 0.4342944819032518  # log base 10 of e
SQRTPI = 1.772453850905516  # Square root of π

def get_constant(name):
        constants = {
            'pi': PI,
            'e': E,
            'phi': PHI,
            'golden_ratio': GOLDEN_RATIO,
            'sqrt2': SQRT2,
            'sqrt3': SQRT3,
            'sqrt5': SQRT5,
            'log2e': LOG2E,
            'log10e': LOG10E,
            'sqrtpi': SQRTPI,
        }
        return constants.get(name.lower(), None)


def mean(data):
    return sum(data) / len(data)

def median(data):
    n = len(data)
    if n == 0:
        return None
    sorted_data = sorted(data)
    mid = n // 2
    return (sorted_data[mid] + sorted_data[mid - 1]) / 2 if n % 2 == 0 else sorted_data[mid]

def mode(data):
    frequency = {}
    for value in data:
        frequency[value] = frequency.get(value, 0) + 1
    max_count = max(frequency.values())
    return [key for key, count in frequency.items() if count == max_count]

def variance(data):
    n = len(data)
    if n < 2:
        return None
    mean = mean(data)
    return sum((x - mean) ** 2 for x in data) / n

def std_deviation(data):
    variance_value = variance(data)
    return variance_value ** 0.5 if variance_value is not None else None


    
def factorial(n):
        """Calculate the factorial of a non-negative integer n."""
        if n < 0:
            raise ValueError("Negative values are not allowed.")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    
def combinations(n, r):
        """Calculate the number of combinations of n items taken r at a time."""
        if r > n:
            return 0
        return factorial(n) // (factorial(r) * factorial(n - r))

    
def permutations(n, r):
        """Calculate the number of permutations of n items taken r at a time."""
        if r > n:
            return 0
        return factorial(n) // factorial(n - r)

    
def comb_with_repetition(n, r):
        """Calculate the number of combinations of n items taken r at a time with repetition allowed."""
        return combinations(n + r - 1, r)

    
def binomial_coefficient(n, k):
        """Calculate the binomial coefficient C(n, k), also known as "n choose k"."""
        if k < 0 or k > n:
            return 0
        return combinations(n, k)

    
def generate_combinations(elements, r):
        """Generate all combinations of r elements from a list of elements."""
        from itertools import combinations
        return list(combinations(elements, r))

    
def generate_permutations(elements, r):
        """Generate all permutations of r elements from a list of elements."""
        from itertools import permutations
        return list(permutations(elements, r))





    
def area_circle(radius):
        """Calculate the area of a circle given its radius."""
        return PI * radius ** 2

    
def perimeter_circle(radius):
        """Calculate the perimeter (circumference) of a circle given its radius."""
        return 2 * PI * radius

    
def area_rectangle(length, width):
        """Calculate the area of a rectangle given its length and width."""
        return length * width

    
def perimeter_rectangle(length, width):
        """Calculate the perimeter of a rectangle given its length and width."""
        return 2 * (length + width)

    
def area_triangle(base, height):
        """Calculate the area of a triangle given its base and height."""
        return 0.5 * base * height

    
def perimeter_triangle(a, b, c):
        """Calculate the perimeter of a triangle given its three sides."""
        return a + b + c

    
def area_square(side):
        """Calculate the area of a square given its side length."""
        return side ** 2

    
def perimeter_square(side):
        """Calculate the perimeter of a square given its side length."""
        return 4 * side

    
def distance(x1, y1, x2, y2):
        """Calculate the distance between two points in 2D space."""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    
def distance_3d(x1, y1, z1, x2, y2, z2):
        """Calculate the distance between two points in 3D space."""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5

    
def volume_cylinder(radius, height):
        """Calculate the volume of a cylinder given its radius and height."""
        return PI * radius ** 2 * height

    
def volume_sphere(radius):
        """Calculate the volume of a sphere given its radius."""
        return (4 / 3) * PI * radius ** 3

    
def volume_cone(radius, height):
        """Calculate the volume of a cone given its radius and height."""
        return (1 / 3) * PI * radius ** 2 * height


   
def gcd(a, b):
        """Calculate the greatest common divisor (GCD) of a and b."""
        while b:
            a, b = b, a % b
        return abs(a)

   
def lcm(a, b):
        """Calculate the least common multiple (LCM) of a and b."""
        return abs(a * b) //gcd(a, b)

   
def is_prime(n):
        """Check if a number n is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

   
def prime_factors(n):
        """Return a list of all prime factors of n."""
        factors = []
        # Check for number of 2s that divide n
        while n % 2 == 0:
            if 2 not in factors:
                factors.append(2)
            n //= 2
        # Check for odd factors from 3 onwards
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                if i not in factors:
                    factors.append(i)
                n //= i
        if n > 2:
            factors.append(n)
        return factors

   
def generate_primes(limit):
        """Generate a list of all prime numbers up to a specified limit using the Sieve of Eratosthenes."""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False  # 0 and 1 are not prime numbers
        for start in range(2, int(limit**0.5) + 1):
            if sieve[start]:
                for multiple in range(start * start, limit + 1, start):
                    sieve[multiple] = False
        return [num for num, is_prime in enumerate(sieve) if is_prime]

   
def fibonacci(n):
        """Return the nth Fibonacci number."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

   
def euler_totient(n):
        """Calculate the Euler's Totient function φ(n), which counts the integers up to n that are coprime to n."""
        result = n  # Initialize result as n
        p = 2
        while p * p <= n:
            # Check if p divides n
            if n % p == 0:
                # If it does, subtract multiples of p from the result
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        # If n has a prime factor greater than sqrt(n)
        if n > 1:
            result -= result // n
        return result


