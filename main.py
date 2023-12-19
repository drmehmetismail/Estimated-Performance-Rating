from pr_calculator import (calculate_win_probability, adjust_mn, optimize_w, calculate_EPR, 
                            calculate_score_probability, calculate_TPR, 
                            calculate_score_plus_probability, optimize_w_plus, calculate_FPR)


def main():
    B = 2700  # Average rating of the opponents
    m, n = 10, 10  # Scoring m points in n games
    t = 0.75         # Threshold probability

    m, n = adjust_mn(m, n)
    w_star = optimize_w(m, n, t)
    score_optimized_probability = calculate_score_probability(w_star, m, n)

    EPR = calculate_EPR(w_star, B)
    TPR = calculate_TPR(m, n, B)
    FPR = calculate_FPR(m, n, B)
    FIDE_score_probability = calculate_score_probability(0.99, m, n)

    w_star_plus = optimize_w_plus(m, n, t)
    EPR_plus = calculate_EPR(w_star_plus, B)
    score_plus_optimized_probability = calculate_score_plus_probability(w_star_plus, m, n)

    # Print B
    print(f"B: {B}")
    # Print m score in n games
    print(f"Score: {m} / {n}")
    # Print the threshold
    print(f"Threshold: {t}")
    # Print w_star
    print(f"w_star: {w_star}")
    print(f"Optimized probability of scoring {m} points: {score_optimized_probability}")
    # calculate_score_probability w_star, m, n
    # print(f"Score Probability: {calculate_score_probability(w, m, n)}")
    print(f"Estimated Performance Rating (EPR): {EPR}")
    print(f"Tournament Performance Rating (TPR): {TPR}")
    print("FIDE Performance Rating: ", FPR)
    print("FIDE score probability: ", FIDE_score_probability)
    print()
    print(f"w_star_plus: {w_star_plus}")
    print(f"EPR_plus: {EPR_plus}")
    print(f"Optimized probability of scoring {m} points or more: {score_plus_optimized_probability}")
    print("Calculate win probability 2800 + 800: ", calculate_win_probability(3600,2800 ))


if __name__ == "__main__":
    main()
