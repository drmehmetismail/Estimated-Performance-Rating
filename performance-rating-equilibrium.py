"""
Performance Rating Equilibrium (PRE) Numerical Calculator:
PRE is a sequence of hypothetical ratings r_i for every player i in a tournament, 
such that after scoring m_i points in n rounds, every player's initial rating 
r_i remains unchanged. PRE is the fixed point of the 'ratings' mapping. Numerically,
the PRE can be calculated iteratively starting from the initial ratings and 
updating initial ratings after each iteration.
"""

import pandas as pd
import re
from scipy.optimize import root_scalar

# Function to parse round results for Swiss tournaments
def parse_swiss_round_result(round_entry):
    if isinstance(round_entry, str):
        try:
            # Match pattern: opponent number, result
            match = re.match(r'^(\d+)([wb])([01½])$', round_entry.strip())
            if match:
                opponent_num = int(match.group(1))
                result_part = match.group(3)

                # Determine the result
                if result_part == '½':
                    result = 0.5
                elif result_part == '1':
                    result = 1.0
                elif result_part == '0':
                    result = 0.0
                else:
                    result = None

                return opponent_num, result
            else:
                return None, None
        except:
            pass
    return None, None

# Function to parse round results for (single) Round-robin tournaments
def parse_round_robin_result(round_entry):
    if isinstance(round_entry, str):
        round_entry = round_entry.strip()
        if round_entry == '*' or round_entry == '':
            return None, None  # No game played or bye
        elif round_entry == '½':
            return 'draw', 0.5
        elif round_entry == '1':
            return 'win', 1.0
        elif round_entry == '0':
            return 'loss', 0.0
    return None, None

# Function to get opponent info for Swiss tournaments
def get_opponent_info_swiss(row, df, num_rounds):
    opponents = []
    results = []
    opponent_ratings = []
    opponent_nums = []  # Store opponent numbers for future reference

    for i in range(1, num_rounds + 1):
        round_col = f'{i}.Rd'
        round_entry = row.get(round_col, '*')
        opponent_num, result = parse_swiss_round_result(round_entry)
        if opponent_num is None or result is None:
            continue  # Skip if no game played or invalid format

        # Find the opponent's row based on rank (assuming 'Rk.' is the rank)
        opponent_row = df[df['Rk.'] == opponent_num]
        if not opponent_row.empty:
            opponent_name = opponent_row['Name'].values[0]
            opponent_rating = opponent_row['Rtg'].values[0]

            opponents.append(opponent_name)
            results.append(result)
            opponent_ratings.append(opponent_rating)
            opponent_nums.append(opponent_num)

    return opponents, results, opponent_ratings, opponent_nums

# Function to get opponent info for Round-robin tournaments
def get_opponent_info_round_robin(row, df, num_rounds):
    opponents = []
    results = []
    opponent_ratings = []
    opponent_nums = []  # Store opponent numbers for future reference

    player_rk = row['Rk.']

    for i in range(1, num_rounds + 1):
        round_col = f'{i}'
        round_entry = row.get(round_col, '*')
        
        if i == player_rk:
            continue  # Skip self

        opponent_row = df[df['Rk.'] == i]
        if opponent_row.empty:
            continue  # Opponent not found

        opponent_name = opponent_row['Name'].values[0]
        opponent_rating = opponent_row['Rtg'].values[0]
        opponent_num = opponent_row['Rk.'].values[0]

        outcome, result = parse_round_robin_result(round_entry)
        if outcome is None or result is None:
            continue  # Skip if no game played or invalid format

        opponents.append(opponent_name)
        results.append(result)
        opponent_ratings.append(opponent_rating)
        opponent_nums.append(opponent_num)

    return opponents, results, opponent_ratings, opponent_nums

def expected_score(opponent_ratings, own_rating):
    return sum(1 / (1 + 10 ** ((r - own_rating) / 400)) for r in opponent_ratings)

def performance_rating(opponent_ratings, score):
    result = root_scalar(lambda r: expected_score(opponent_ratings, r) - score, bracket=[0, 4000], method='brentq')
    return round(result.root,1) if result.converged else None

# Function to process each player's data based on tournament type
def process_player_data(df, tournament_type, num_rounds):
    player_data = {}

    if tournament_type == 'Swiss':
        get_opponent_info = lambda row: get_opponent_info_swiss(row, df, num_rounds)
    elif tournament_type == 'Round-robin':
        get_opponent_info = lambda row: get_opponent_info_round_robin(row, df, num_rounds)
    else:
        raise ValueError("Unsupported tournament type")

    # Initialize player_data with initial opponent info and ratings
    for index, row in df.iterrows():
        player_name = row['Name']
        player_rating = row['Rtg']

        opponents, results, opponent_ratings, opponent_nums = get_opponent_info(row)

        player_dict = {
            'Rk.': row['Rk.'],
            'Name': player_name,
            'Rtg': player_rating,
            'Pts.': sum(results),
            'opponents': opponents,
            'results': results,
            'opponent_ratings': opponent_ratings,
            'opponent_nums': opponent_nums,  # Store opponent numbers
            'PRs': []  # List to store PRs for each iteration
        }

        player_data[player_name] = player_dict

    converged = False
    iteration = 1

    while not converged:
        # Create a mapping from player names to their PRs
        if iteration == 1:
            # First iteration uses initial ratings
            pr_map = {player: data['Rtg'] for player, data in player_data.items()}
        else:
            # Subsequent iterations use the previous iteration's PRs
            pr_map = {player: data['PRs'][-1] for player, data in player_data.items()}

        converged = True  # Assume convergence, check if any PR changes

        # Recalculate PRs for each player
        for player, data in player_data.items():
            opponent_ratings = []
            for opp_num in data['opponent_nums']:
                # Find opponent by rank
                opponent_row = df[df['Rk.'] == opp_num]
                if not opponent_row.empty:
                    opponent_name = opponent_row['Name'].values[0]
                    opponent_pr = pr_map.get(opponent_name, data['Rtg'])  # Default to initial rating if not found
                    opponent_ratings.append(opponent_pr)
                else:
                    opponent_ratings.append(data['Rtg'])  # Default to player's own rating if opponent not found

            m = sum(data['results'])  # Total score
            n = len(data['results'])  # Number of games

            # Calculate new PR
            new_pr = performance_rating(opponent_ratings, m)

            # Check for convergence
            if iteration == 1:
                # No previous PR to compare
                data['PRs'].append(new_pr)
                converged = False  # Need at least two iterations
            else:
                previous_pr = data['PRs'][-1]
                data['PRs'].append(new_pr)
                if round(new_pr) != round(previous_pr):
                    converged = False  # PR changed, so not yet converged

        if not converged:
            iteration += 1

    return player_data, iteration

# Function to detect tournament type based on column headers
def detect_tournament_type(df, num_rounds):
    swiss_columns = [f'{i}.Rd' for i in range(1, num_rounds + 1)]
    round_robin_columns = [str(i) for i in range(1, num_rounds + 2)]

    if all(col in df.columns for col in swiss_columns):
        return 'Swiss'
    elif all(col in df.columns for col in round_robin_columns):
        return 'Round-robin'
    else:
        raise ValueError("Cannot determine tournament type based on column headers")

# Main function to read CSV, process data, and export PRs
def main(csv_file_path, num_rounds):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Strip whitespace from 'Name' column
    df['Name'] = df['Name'].str.strip()
    
    # Ensure 'Rk.', 'Name', 'Rtg' columns exist
    required_columns = {'Rk.', 'Name', 'Rtg'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain the following columns: {required_columns}")

    # Detect tournament type
    tournament_type = detect_tournament_type(df, num_rounds)
    # print(f"Tournament Type Detected: {tournament_type}")

    # Process player data with iterative PR calculations until convergence
    player_data, total_iterations = process_player_data(df, tournament_type, num_rounds)

    # Prepare data for CSV export
    export_data = []
    for player, data in player_data.items():
        row = {
            'Rk.': data['Rk.'],
            'Name': player,
            'Rtg': data['Rtg'],
            'Pts.': data['Pts.'],
            'PRE': round(data['PRs'][-1]),  # Final PRE after convergence
        }
        export_data.append(row)

    # Convert to DataFrame
    export_df = pd.DataFrame(export_data)

    # Sort by rank
    export_df.sort_values('Rk.', inplace=True)

    # Export to CSV
    output_csv_path = 'pre_results.csv'
    export_df.to_csv(output_csv_path, index=False)
    # print(f"Exported PR results to {output_csv_path}")

    # Print the DataFrame
    print(export_df)

if __name__ == "__main__":
    # Enter the path to the CSV file. See the attached example (GrandSwissPalma2017.csv) for the format.
    csv_file_path = ''
    # Enter the number of rounds in the tournament
    num_rounds = 9
    main(csv_file_path, num_rounds)
