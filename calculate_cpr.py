import math
from itertools import combinations

"""
Calculate the Complete Performance Rating (CPR) and evaluate the best CPR for perfect scores across subsets of opponent ratings.

Functions:
    - calculate_cpr(m, n, e):
        Compute the CPR value given score m, games n, and average opponent rating e.
    - perfect_score_pr(ratings):
        For every non-empty subset of opponent ratings, assume a perfect score
        (m = size of subset, n = size of subset), compute CPR, and return the maximum CPR.
"""

def calculate_cpr(m, n, e):
    """
    Compute the Complete Performance Rating (CPR).

    Parameters:
        m (int or float): Score obtained (number of points).
        n (int): Number of games played.
        e (float): Average Elo rating of the opponents.
    Returns:
        float: The CPR value.

    Raises:
        ValueError: If m is not within [0, n], or n is not positive.
    """
    if m < 0 or m > n:
        raise ValueError("Score m must be between 0 and n.")
    if n <= 0:
        raise ValueError("Number of games n must be positive.")

    return e - ((n+1)/n) * 400 * math.log10((n + 0.5 - m) / (m + 0.5))


def perfect_score_pr(ratings):
    if not ratings:
        raise ValueError("ratings list must contain at least one element")

    max_cpr = float('-inf')
    total_games = len(ratings)

    # Iterate over all non-empty subsets of opponent ratings
    for size in range(1, total_games + 1):
        for subset in combinations(ratings, size):
            avg_rating = sum(subset) / size
            # Perfect score: m = n = size of subset
            cpr = calculate_cpr(size, size, avg_rating)
            max_cpr = max(max_cpr, cpr)

    return max_cpr


if __name__ == "__main__":
    # Example usage
    m, n, e = 9, 9, 2585
    print(f"CPR for score m={m}, n={n}, avg opponent rating e={e}: {calculate_cpr(m, n, e):.0f}")

    # Example opponent rating list
    Carlsen_opponent_ratings = [2718, 2657, 2684, 2692, 2227, 2501, 2640, 2633, 2513]
    Fischer_opponent_ratings = [2628, 2643, 2648, 2678, 2531, 2608, 2579, 2530, 2565, 2501, 2607]
    Beliavsky_opponent_ratings = [2520, 2440, 2455, 2425, 2485, 2435, 2425, 2330, 2345, 2310, 2390, 2340, 2200]
    opponent_ratings = Carlsen_opponent_ratings
    best_cpr = perfect_score_pr(opponent_ratings)
    print(f"Perfect score Performance Rating against opponents in {opponent_ratings}: {best_cpr:.0f}")
