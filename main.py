from pr_calculator import (calculate_win_probability, adjust_mn, optimize_w, calculate_EPR, 
                            calculate_score_probability, calculate_TPR, 
                            calculate_score_plus_probability, optimize_w_plus, calculate_FPR)
from calculate_cpr import calculate_cpr

def main():
    B = 2705 # Average rating of the opponents 2480, 3094
    m, n = 20, 20 # Scoring m points in n games
    t = 0.75       # Threshold probability
    # To calculat expected score between two players enter: A = 2800
    # Calculate the win probability
    # print("Expected score:", calculate_win_probability(A, B))
    # print(f"Expected score^{m}:", calculate_win_probability(A, B)**m)

    m, n = adjust_mn(m, n)
    w_star = optimize_w(m, n, t)
    score_optimized_probability = calculate_score_probability(w_star, m, n)

    EPR = calculate_EPR(w_star, B)
    CPR = calculate_cpr(m, n, B)
    TPR = calculate_TPR(m, n, B)
    FPR = calculate_FPR(m, n, B)
    FIDE_score_probability = calculate_score_probability(0.99, m, n)

    # w_star_plus = optimize_w_plus(m, n, t)
    # EPR_plus = calculate_EPR(w_star_plus, B)
    # score_plus_optimized_probability = calculate_score_plus_probability(w_star_plus, m, n)

    # Print B
    print(f"B: {B}")
    # Print m score in n games
    print(f"Score: {m} / {n}")
    # Print the threshold
    # print(f"Threshold: {t}")
    # Print w_star
    print(f"w_star: {w_star}")
    print(f"Optimized probability of scoring {m} points: {score_optimized_probability}")
    print("FIDE score probability: ", FIDE_score_probability)
    print("--------------------")
    # calculate_score_probability w_star, m, n
    # print(f"Score Probability: {calculate_score_probability(w, m, n)}")
    print(f"Estimated Performance Rating (EPR): {EPR}")
    print(f"Complete Performance Rating (CPR): {CPR}")
    print(f"Tournament Performance Rating (TPR): {TPR}")
    print("FIDE Performance Rating: ", FPR)
    print("--------------------")
    # print(f"w_star_plus: {w_star_plus}")
    # print(f"EPR_plus: {EPR_plus}")
    # print(f"Optimized probability of scoring {m} points or more: {score_plus_optimized_probability}")


if __name__ == "__main__":
    main()
