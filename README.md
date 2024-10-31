# Estimated Performance Rating, and Performance Rating Equilibrium
## Estimated Performance Rating

Assume that player 1 scores `m` points in `n` games against players with an average rating `R_a`, where `m` is an integer. Note that in chess, a win is worth 1 point, a draw 0.5 points, and a loss 0 points. Let `S(w,m,n)` denote the player 1's **probability of scoring** exactly `m` points in `n` games, given player 1's win probability `w` against players with an average rating `R_a`. 

S(w,m,n) = {n choose m} w^m (1-w)^(n-m).

For a given threshold `t` in `[0,1]`, define the following maximization problem to find `w` that maximizes `S(w,m,n)`.

maximize S(w,m,n) subject to S(w,m,n) <= t.

Unless otherwise noted, set `t=0.75`, indicating a 75% likelihood that player 1 scores `S(w,m,n)`.

Let `w*` be the value that solves the optimization problem. Then, given `R_a`, find the value `A*` such that 

W(A*,R_a) = w* = 1 / (1 + 10^((R_a - A*) / 400)).


In this context, `A*` is called the **Estimated Performance Rating** (PR^e) of player 1, given the score `m` in `n` games and the average rating `R_a` of the opposition. `PR^e(w*,R_a)` denotes the performance rating of player 1 given `w*` and `R_a`. Note that `w*` is dependent on `t`, `m`, and `n`. 

Solving Equation for `A*`we obtain:
A* = R_a - 400 * log10((1 - w*) / w*).


### Illustrative Example

| `R_a` | `m` | `n` | `w*` | `S(w*,m,n)` | **PR^e** | **TPR** |
|-------|-----|-----|------|-------------|----------|---------|
| 2700  | 0   | 2   | 0.13 | 0.75        | 2376     | N/A     |
| 2700  | 0.5 | 2   | 0.25 | 0.42        | 2509     | 2509    |
| 2700  | 1   | 2   | 0.50 | 0.50        | 2700     | 2700    |
| 2700  | 1.5 | 2   | 0.75 | 0.42        | 2891     | 2891    |
| 2700  | 2   | 2   | 0.87 | 0.75        | 3024     | N/A     |

To illustrate the difference between TPR and PR^e, consider the example where player 1 has an average rating of 2700 and plays 2 games against players with an average rating of 2700. `S(w*,m,n)` shows the probability of scoring `m` points in `n` games given `w*`.

For the given score `m = 1` and `n = 2`, I calculate the TPR and PR^e. For TPR, I use the standard formula and for PR^e, I use the W(A*,R_a) formula above. 
Solving the following equation for TPR

1/2 = 1 / (1 + 10^((2700 - TPR) / 400)),

yields TPR = 2700. Now, calculate the PR^e. For `m=1` and `n=2`, we have `w* = 0.5`. Then, plugging 
`w* = 0.5` and `R_a = 2700` into the formula for PR^e, we obtain PR^e = 2700.

Next, calculate PR^e for `m=0` and `n=2`. (Note that TPR is undefined for `m=0` and `m=n`.) 
For `m=0` and `n=2`, solving the optimization problem yields `w* = 0.29`. Then, plugging 
`w* = 0.29` and `R_a = 2700` into the formula for PR^e, we obtain PR^e = 2546.89. The remaining values of 
PR^e and TPR are calculated similarly.

## Complete Performance Rating

For situations where a computer is unavailable, I propose a second novel rating system: the Complete Performance Rating (CPR). The CPR is defined as the hypothetical rating R such that if the player were assigned this rating at the start of a tournament where she scored m points in n games, and additionally drew a game against an opponent with a rating R, the player’s initial rating R would remain unchanged. The CPR makes use of the fact that drawing a game against an opponent with the same rating does not change a player’s rating.

## Performance Rating Equilibrium

Performance Rating Equilibrium (PRE) is a sequence of hypothetical ratings r_i for every player i in a tournament such that after scoring m_i points in n rounds, every player's initial rating r_i remains unchanged. PRE is the fixed point of the 'ratings' mapping. Numerically, the PRE can be calculated iteratively starting from the initial ratings and updating initial ratings after each iteration.

For example, in the 2017 FIDE Grand Prix Palma de Mallorca, Jakovenko was ranked 1st according to the TPR tiebreak, but Aronian's PRE was higher because his opponents performed better in the tournament. For similar reasons, Nakamura's and Svidler's PREs are also noticeably higher than their TPRs.

| Rk. | Name                   | Rtg  | Pts. | TPR  | PRE  |
| --- | ---------------------- | ---- | ---- | ---- | ---- |
| 1   | Jakovenko Dmitry       | 2721 | 5.5  | 2823 | 2841 |
| 2   | Aronian Levon          | 2801 | 5.5  | 2821 | 2857 |
| 3   | Radjabov Teimour       | 2741 | 5    | 2764 | 2743 |
| 4   | Rapport Richard        | 2692 | 5    | 2762 | 2744 |
| 5   | Tomashevsky Evgeny     | 2702 | 5    | 2791 | 2813 |
| 6   | Nakamura Hikaru        | 2780 | 5    | 2792 | 2830 |
| 7   | Svidler Peter          | 2763 | 5    | 2782 | 2815 |
| 8   | Ding Liren             | 2774 | 5    | 2771 | 2783 |
| 9   | Harikrishna P.         | 2738 | 5    | 2767 | 2789 |
| 10  | Inarkiev Ernesto       | 2683 | 4.5  | 2734 | 2699 |
| 11  | Vachier-Lagrave Maxime | 2796 | 4.5  | 2741 | 2768 |
| 12  | Eljanov Pavel          | 2707 | 4.5  | 2724 | 2706 |
| 13  | Li Chao B              | 2741 | 4    | 2656 | 2624 |
| 14  | Vallejo Pons Francisco | 2705 | 4    | 2679 | 2644 |
| 15  | Giri Anish             | 2762 | 4    | 2693 | 2696 |
| 16  | Riazantsev Alexander   | 2651 | 3.5  | 2640 | 2623 |
| 17  | Gelfand Boris          | 2719 | 3    | 2580 | 2555 |
| 18  | Hammer Jon Ludvig      | 2629 | 3    | 2586 | 2562 |

For more details of PRE, see https://github.com/drmehmetismail/Perfect-Performance-Ratings
For the research papers, see: 
https://kclpure.kcl.ac.uk/portal/en/publications/performance-rating-in-chess-tennis-and-other-contexts
and
https://kclpure.kcl.ac.uk/portal/en/publications/performance-rating-equilibrium
