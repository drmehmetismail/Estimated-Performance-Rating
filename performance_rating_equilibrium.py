"""
Performance Rating Equilibrium (PRE) Numerical Calculator:
PRE is a sequence of hypothetical ratings r_i for every player i in a tournament, 
such that after scoring m_i points in n rounds, every player's initial rating 
r_i remains unchanged. PRE is the fixed point of the 'ratings' mapping. Numerically,
the PRE can be calculated iteratively starting from the initial ratings and 
updating initial ratings after each iteration.
"""

import pandas as pd
import numpy as np
from scipy.optimize import root_scalar
import os
import chess.pgn

def expected_score(opponent_ratings, own_rating):
    # Filter out None values from opponent_ratings
    opponent_ratings = [r for r in opponent_ratings if r is not None]
    if own_rating is None or not opponent_ratings:
        # Cannot compute expected score without own_rating or opponent_ratings
        return None
    return sum(1 / (1 + 10 ** ((r - own_rating) / 400)) for r in opponent_ratings)

# performance rating formula
def performance_rating(opponent_ratings, score):
    opponent_ratings = [r for r in opponent_ratings if r is not None]
    
    if not opponent_ratings:
        # Cannot compute performance rating without opponent ratings
        return None
    
    # if score is 0 or perfect score, then ask CPR
    if score == 0 or score == len(opponent_ratings):
        return round(complete_performance_rating(opponent_ratings, score), 1)
    else:
        try:
            result = root_scalar(
                lambda r: expected_score(opponent_ratings, r) - score,
                bracket=[1000, 4000],
                method='brentq'
            )
            return round(result.root, 1) if result.converged else None
        except (ValueError, TypeError) as e:
            # Handle cases where the root-finding algorithm fails
            return None

# linear performance rating
def linear_performance_rating(opponent_ratings, score):
    # Calculate the average ratings of the opponents for i, sum x_j's for j != i
    sum_term = np.sum(opponent_ratings)
    k = len(opponent_ratings)
    return sum_term / (k) + 800*(score/(k)) - 400

def complete_performance_rating(opponent_ratings, score):
    sum_term = np.sum(opponent_ratings)
    k = len(opponent_ratings)
    average_opponent_rating = sum_term / k
    return average_opponent_rating - ((k+1)/k) * 400 * math.log10((k + 0.5 - score) / (score + 0.5))

def process_pgn_files(pgn_input_dir):
    player_data = {}
    player_indices = {}
    player_counter = 1  # To assign unique numbers to players
    all_ratings = []

    for dirpath, dirnames, filenames in os.walk(pgn_input_dir):
        for filename in filenames:
            if filename.endswith('.pgn'):
                pgn_file_path = os.path.join(dirpath, filename)
                with open(pgn_file_path) as pgn:
                    while True:
                        game = chess.pgn.read_game(pgn)
                        if game is None:
                            break
                        # Get the headers of the game
                        white_player = game.headers.get('White', 'Unknown')
                        black_player = game.headers.get('Black', 'Unknown')
                        result_str = game.headers.get('Result', '*')
                        white_rating = game.headers.get('WhiteElo', '0')
                        black_rating = game.headers.get('BlackElo', '0')
                        
                        # Convert ratings to int
                        try:
                            white_rating = int(white_rating)
                        except:
                            white_rating = 0
                        try:
                            black_rating = int(black_rating)
                        except:
                            black_rating = 0

                        # Collect valid ratings
                        if white_rating > 0:
                            all_ratings.append(white_rating)
                        if black_rating > 0:
                            all_ratings.append(black_rating)

                        # Convert result string to numeric results
                        if result_str == '1-0':
                            white_result = 1.0
                            black_result = 0.0
                        elif result_str == '0-1':
                            white_result = 0.0
                            black_result = 1.0
                        elif result_str == '1/2-1/2' or result_str == '½-½':
                            white_result = 0.5
                            black_result = 0.5
                        else:
                            # In case of unknown result
                            continue

                        # Assign unique numbers to players if not already assigned
                        if white_player not in player_indices:
                            player_indices[white_player] = player_counter
                            player_counter += 1
                        if black_player not in player_indices:
                            player_indices[black_player] = player_counter
                            player_counter += 1

                        # Update white player's data
                        if white_player not in player_data:
                            player_data[white_player] = {
                                'Rank': player_indices[white_player],
                                'Name': white_player,
                                'Rating': white_rating,
                                'Points': 0.0,
                                'opponents': [],
                                'results': [],
                                'opponent_ratings': [],
                                'opponent_nums': [],
                                'PRs': []  # For storing PRs in iterations
                            }
                        player_data[white_player]['Points'] += white_result
                        player_data[white_player]['opponents'].append(black_player)
                        player_data[white_player]['results'].append(white_result)
                        player_data[white_player]['opponent_ratings'].append(black_rating)
                        player_data[white_player]['opponent_nums'].append(player_indices[black_player])

                        # Update black player's data
                        if black_player not in player_data:
                            player_data[black_player] = {
                                'Rank': player_indices[black_player],
                                'Name': black_player,
                                'Rating': black_rating,
                                'Points': 0.0,
                                'opponents': [],
                                'results': [],
                                'opponent_ratings': [],
                                'opponent_nums': [],
                                'PRs': []
                            }
                        player_data[black_player]['Points'] += black_result
                        player_data[black_player]['opponents'].append(white_player)
                        player_data[black_player]['results'].append(black_result)
                        player_data[black_player]['opponent_ratings'].append(white_rating)
                        player_data[black_player]['opponent_nums'].append(player_indices[white_player])

    # After processing all games, compute average rating
    average_rating = int(sum(all_ratings) / len(all_ratings)) if all_ratings else 0

    # Now, set missing or None ratings to average_rating
    for player in player_data:
        if not player_data[player]['Rating'] or player_data[player]['Rating'] == 0:
            player_data[player]['Rating'] = average_rating
        # Update opponent ratings where ratings are zero or None
        player_data[player]['opponent_ratings'] = [
            rating if rating else average_rating for rating in player_data[player]['opponent_ratings']
        ]

    return player_data, average_rating

def process_player_data(player_data, average_rating, performance_rating_type):
    # Remove players with no games
    player_data = {player: data for player, data in player_data.items() if len(data['opponents']) > 0}

    converged = False
    iteration = 1

    while not converged:
        # Create a mapping from player names to their PRs
        if iteration == 1:
            # First iteration uses initial ratings
            pr_map = {player: data['Rating'] for player, data in player_data.items()}
        else:
            # Subsequent iterations use the previous iteration's PRs
            pr_map = {player: data['PRs'][-1] if data['PRs'][-1] is not None else data['Rating']
                      for player, data in player_data.items()}

        converged = True  # Assume convergence, check if any PR changes

        # Recalculate PRs for each player
        for player, data in player_data.items():
            opponent_ratings = []
            for opp_name in data['opponents']:
                # Get opponent's PR or fallback to their initial rating
                opponent_pr = pr_map.get(opp_name, player_data[opp_name]['Rating'])
                if opponent_pr is None:
                    # If still None, use average_rating
                    opponent_pr = average_rating
                opponent_ratings.append(opponent_pr)

            m = sum(data['results'])  # Total score

            # Calculate new PR
            if performance_rating_type == 'linear':
                new_pr = linear_performance_rating(opponent_ratings, m)
            else:
                new_pr = performance_rating(opponent_ratings, m)

            # Check for convergence
            if iteration == 1:
                # No previous PR to compare
                data['PRs'].append(new_pr)
                converged = False  # Need at least two iterations
            else:
                previous_pr = data['PRs'][-1]
                data['PRs'].append(new_pr)
                if new_pr is None or previous_pr is None:
                    converged = False
                elif round(new_pr) != round(previous_pr):
                    converged = False  # PR changed, so not yet converged

        if not converged:
            iteration += 1

    return player_data, iteration

# Main function to read PGN, process data, and export
def main_pre(pgn_input_dir, performance_rating_type):
    # Process PGN files
    player_data, average_rating = process_pgn_files(pgn_input_dir)

    # Process player data with iterative PR calculations until convergence
    player_data, total_iterations = process_player_data(player_data, average_rating, performance_rating_type)

    # Prepare data for CSV export
    export_data = []
    for player, data in player_data.items():
        row = {
            'Rank': data['Rank'],
            'Name': player,
            'Rating': data['Rating'],
            'Points': data['Points'],
            'TPR': round(data['PRs'][0]),
            'PRE': round(data['PRs'][-1]),
        }
        export_data.append(row)

    # Convert to DataFrame
    export_df = pd.DataFrame(export_data)

    # Sort by Points
    export_df = export_df.sort_values(by='Points', ascending=False)

    # Export to CSV
    output_csv_path = 'performance_rating_equilibrium.csv'
    export_df.to_csv(output_csv_path, index=False)

    # Print the DataFrame
    print(export_df)

if __name__ == "__main__":
    # performance_rating_type: input 'linear' or 'standard'. For very big tournaments use linear as it's much faster.
    performance_rating_type = 'standard'
    pgn_input_dir = ''
    main_pre(pgn_input_dir, performance_rating_type)
