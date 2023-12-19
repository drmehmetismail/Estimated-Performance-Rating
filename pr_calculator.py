import math
from scipy.optimize import minimize_scalar

def calculate_win_probability(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))

def adjust_mn(m, n):
    if not float(m).is_integer():
        m, n = int(m * 2), int(n * 2)
    else:
        m, n = int(m), int(n)
    return m, n

def calculate_score_probability(w, m, n):
    # Ensure m and n are treated as integers for comb function
    return math.comb(n, m) * w ** m * (1 - w) ** (n - m)

def calculate_score_plus_probability(w, m, n):
    if n < m:
        raise ValueError("n must be greater than or equal to m")

    total_probability = 0
    for k in range(m, n + 1):
        total_probability += math.comb(n, k) * w ** k * (1 - w) ** (n - k)
    return total_probability

def optimize_w(m, n, t):
    def objective(w):
        score_prob = calculate_score_probability(w, m, n)
        if score_prob <= t:
            return -score_prob
        else:
            return float('inf')  # Return a large value if constraint is not met
    
    result = minimize_scalar(objective, bounds=(0, 1), method='bounded')
    return result.x

def optimize_w_plus(m, n, t):
    def objective(w):
        score_plus_prob = calculate_score_plus_probability(w, m, n)
        if score_plus_prob <= t:
            return -score_plus_prob
        else:
            return float('inf')  # Return a large value if constraint is not met

    result = minimize_scalar(objective, bounds=(0, 1), method='bounded')
    return result.x


# def calculate_EPR_old(w_star, B):
#    return 400 * math.log10(-w_star * math.exp((B * math.log(10)) / 400) / (w_star - 1))

def calculate_EPR(w_star, B):
    return B - 400 * math.log10((1 - w_star) / w_star)

def calculate_TPR(m, n, B):
    if m == 0:
        return "TPR cannot be calculated: Player lost all games."
    elif m == n:
        return "TPR cannot be calculated: Player won all games."
    return B - 400 * math.log10((n - m) / m)

def calculate_FPR(m, n, B):
    # Performance score (p) as a percentage, rounded to 2 decimal places
    p = round(m / n, 2)

    # Table for dp values
    dp_table = {
        1.0: 800, 0.99: 677, 0.98: 589, 0.97: 538, 0.96: 501, 0.95: 470, 0.94: 444, 0.93: 422,
        0.92: 401, 0.91: 383, 0.90: 366, 0.89: 351, 0.88: 336, 0.87: 322, 0.86: 309, 0.85: 296,
        0.84: 284, 0.83: 273, 0.82: 262, 0.81: 251, 0.80: 240, 0.79: 230, 0.78: 220, 0.77: 211,
        0.76: 202, 0.75: 193, 0.74: 184, 0.73: 175, 0.72: 166, 0.71: 158, 0.70: 149, 0.69: 141,
        0.68: 133, 0.67: 125, 0.66: 117, 0.65: 110, 0.64: 102, 0.63: 95, 0.62: 87, 0.61: 80,
        0.60: 72, 0.59: 65, 0.58: 57, 0.57: 50, 0.56: 43, 0.55: 36, 0.54: 29, 0.53: 21, 0.52: 14,
        0.51: 7, 0.50: 0, 0.49: -7, 0.48: -14, 0.47: -21, 0.46: -29, 0.45: -36, 0.44: -43, 0.43: -50,
        0.42: -57, 0.41: -65, 0.40: -72, 0.39: -80, 0.38: -87, 0.37: -95, 0.36: -102, 0.35: -110,
        0.34: -117, 0.33: -125, 0.32: -133, 0.31: -141, 0.30: -149, 0.29: -158, 0.28: -166, 0.27: -175,
        0.26: -184, 0.25: -193, 0.24: -202, 0.23: -211, 0.22: -220, 0.21: -230, 0.20: -240, 0.19: -251,
        0.18: -262, 0.17: -273, 0.16: -284, 0.15: -296, 0.14: -309, 0.13: -322, 0.12: -336, 0.11: -351,
        0.10: -366, 0.09: -383, 0.08: -401, 0.07: -422, 0.06: -444, 0.05: -470, 0.04: -501, 0.03: -538,
        0.02: -589, 0.01: -677, 0.00: -800
    }

    # Find dp from the table, rounding p to nearest key in the table
    dp = dp_table.get(p, "Not Found")
    if dp == "Not Found":
        # If p is not found exactly, find the closest key
        closest_p = min(dp_table.keys(), key=lambda x: abs(x - p))
        dp = dp_table[closest_p]

    # Calculate FIDE Performance Rating
    FPR = B + dp
    return FPR
