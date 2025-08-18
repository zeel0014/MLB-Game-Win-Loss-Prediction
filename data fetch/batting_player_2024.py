import requests
import pandas as pd
import time
import os

schedule_file = "data/game_schedule_2024.csv"
output_file = "data/batting_player_2024.csv"

# Load schedule
schedule_df = pd.read_csv(schedule_file)

# Check if output CSV exists (for resume functionality)
if os.path.exists(output_file):
    batting_df = pd.read_csv(output_file)
    already_fetched_games = set(batting_df['gamePk'].unique())
    print(f"Resuming. Already fetched {len(already_fetched_games)} games.")
else:
    batting_df = pd.DataFrame()
    already_fetched_games = set()

# Loop through schedule
for idx, row in schedule_df.iterrows():
    gamePk = row['gamePk']

    if gamePk in already_fetched_games:
        print(f"Skipping gamePk {gamePk} (already fetched).")
        continue

    boxscore_url = f"https://statsapi.mlb.com/api/v1/game/{gamePk}/boxscore"
    
    try:
        resp = requests.get(boxscore_url)
        data = resp.json()
        game_data_count = 0  # counter for this game

        # Teams: away and home
        for team_side in ['away', 'home']:
            team = data['teams'][team_side]
            team_id = team['team']['id']
            team_name = team['team']['name']
            
            players = team.get('players', {})
            for player_id, player_info in players.items():
                person = player_info['person']
                stats = player_info.get('stats', {}).get('batting', {})
                if not stats:
                    continue  # skip if no batting stats
                
                player_row = {
                    'gamePk': gamePk,
                    'team_id': team_id,
                    'team_name': team_name,
                    'player_id': person['id'],
                    'player_name': person['fullName'],
                    'position': player_info['position']['code'],
                    'atBats': stats.get('atBats'),
                    'hits': stats.get('hits'),
                    'doubles': stats.get('doubles'),
                    'triples': stats.get('triples'),
                    'homeRuns': stats.get('homeRuns'),
                    'rbi': stats.get('rbi'),
                    'strikeOuts': stats.get('strikeOuts'),
                    'baseOnBalls': stats.get('baseOnBalls'),
                    'hitByPitch': stats.get('hitByPitch'),
                    'stolenBases': stats.get('stolenBases'),
                    'caughtStealing': stats.get('caughtStealing'),
                    'plateAppearances': stats.get('plateAppearances'),
                    'leftOnBase': stats.get('leftOnBase'),
                    'sacBunts': stats.get('sacBunts'),
                    'sacFlies': stats.get('sacFlies'),
                    'groundIntoDoublePlay': stats.get('groundIntoDoublePlay'),
                    'groundIntoTriplePlay': stats.get('groundIntoTriplePlay'),
                    'flyOuts': stats.get('flyOuts'),
                    'lineOuts': stats.get('lineOuts'),
                    'popOuts': stats.get('popOuts'),
                    'groundOuts': stats.get('groundOuts'),
                    'airOuts': stats.get('airOuts')
                }
                
                batting_df = pd.concat([batting_df, pd.DataFrame([player_row])], ignore_index=True)
                game_data_count += 1
        
        # Save after each game
        batting_df.to_csv(output_file, index=False)
        print(f"GamePk {gamePk}: Fetched {game_data_count} player records.")

        # Respect API
        time.sleep(0.2)
        
    except Exception as e:
        print(f"Error fetching game {gamePk}: {e}")
        # Save whatever data has been fetched till now
        batting_df.to_csv(output_file, index=False)
        continue

print("All games processed. Data saved.", batting_df.shape)
