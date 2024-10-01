import math

"""
Calculate the Complete Performance Rating (CPR).

Parameters:
    - m: Score obtained (number of points).
    - n: Number of games played.
    - e: Average Elo rating of the opponents.
Returns:
    - The CPR value.
The intuition is that the CPR is the hypothetical rating, R, such that 
if the player were assigned this rating at the start of the tournament, 
where she scored $m$ points in $n$ games against opponents with an average rating $R_a$, 
and additionally drew a game against a hypothetical opponent of rating $R$, 
the player's initial rating $R$ would not change. 
The CPR makes uses of the fact that drawing a game against an opponent 
with the same rating does not change a player's rating.
"""

def calculate_cpr(m, n, e):

    if m < 0 or m > n:
        raise ValueError("Score m must be between 0 and n.")
    if n <= 0:
        raise ValueError("Number of games n must be positive.")

    return e - ((n+1)/n) * 400 * math.log10((n + 0.5 - m) / (m + 0.5))

if __name__ == "__main__":
    # Example inputs
    m = 2  # Score
    n = 2   # Number of games
    e = 2600  # Average opponent rating

    cpr = calculate_cpr(m, n, e)
    print(f"The CPR is: {cpr}")
