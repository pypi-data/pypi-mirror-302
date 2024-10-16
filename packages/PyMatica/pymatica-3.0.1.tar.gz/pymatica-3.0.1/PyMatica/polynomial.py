# pymatica/polynomial.py



def evaluate(coefficients, x):
        return sum(coef * (x ** i) for i, coef in enumerate(reversed(coefficients)))

def add(coeff1,coeff2):
        length = max(len(coeff1), len(coeff2))
        result = [0] * length
        for i in range(length):
            a = coeff1[i] if i < len(coeff1) else 0
            b = coeff2[i] if i < len(coeff2) else 0
            result[i] = a + b
        return (result)

def subtract(coeff1,coeff2):
        length = max(len(coeff1), len(coeff2))
        result = [0] * length
        for i in range(length):
            a = coeff1[i] if i < len(coeff1) else 0
            b = coeff2[i] if i < len(coeff2) else 0
            result[i] = a - b
        return (result)

def multiply(coeff1,coeff2):
        result = [0] * (len(coeff1) + len(coeff2) - 1)
        for i, a in enumerate(coeff1):
            for j, b in enumerate(coeff2):
                result[i + j] += a * b
        return (result)

def differentiate(coefficients):
        if len(coefficients) == 1:
            return [0]  # Derivative of a constant is zero
        result = [coef * (len(coefficients) - 1 - i) for i, coef in enumerate(coefficients[:-1])]
        return result

def polynomial_str(coefficients):
    """Return the polynomial as a string."""
    terms = []
    for i, coef in enumerate(reversed(coefficients)):
        if coef:
            term = f"{coef}x^{len(coefficients) - 1 - i}" if len(coefficients) - 1 - i > 0 else str(coef)
            terms.append(term)
    return " + ".join(terms)



def roots(coefficients):
        """Finds the roots of the polynomial using numpy's roots method."""
        if len(coefficients) == 0:
            return []
        # For polynomials of degree 2 or higher
        from numpy import roots
        return roots(coefficients)
