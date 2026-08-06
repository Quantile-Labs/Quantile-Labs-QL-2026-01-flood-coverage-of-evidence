"""Uncertainty helpers. No bare proportions leave this laboratory."""
from math import sqrt


def wilson(k, n, z=1.96):
    """Wilson score interval for a proportion. Correct where the normal
    approximation breaks, which is wherever counts are small.

    Returns (point, low, high). n == 0 -> (nan, 0.0, 1.0).
    """
    if n == 0:
        return float("nan"), 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, centre - half), min(1.0, centre + half)


def fmt(k, n, pct=True, dp=1):
    """Render a proportion the way it must appear in every Note:
    point estimate, interval, denominator.

    >>> fmt(36, 84)
    '42.9% (95% CI 32.7-53.6%, n=84)'
    """
    p, lo, hi = wilson(k, n)
    if n == 0:
        return "undefined (n=0)"
    s = 100 if pct else 1
    u = "%" if pct else ""
    return (f"{p*s:.{dp}f}{u} (95% CI {lo*s:.{dp}f}-{hi*s:.{dp}f}{u}, n={n})")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
