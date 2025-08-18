import requests
import pandas as pd
import time
import os

schedule_file = "data/game_schedule_2024.csv"
output_file = "data/batting_team_2024.csv"

# Load schedule
schedule_df = pd.read_csv(schedule_file)

# Resume functionality
if os.path.exists(output_file):
    team_batting_df = pd.read_csv(output_file)
    already_fetched_games = set(team_batting_df['gamePk'].unique())
    print(f"Resuming. Already fetched {len(already_fetched_games)} games.")
else:
    team_batting_df = pd.DataFrame()
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
        game_data_count = 0

        for team_side in ['away', 'home']:
            team = data['teams'][team_side]
            team_id = team['team']['id']
            team_name = team['team']['name']
            batting_stats = team.get('teamStats', {}).get('batting', {})
            if not batting_stats:
                continue
            
            team_row = {
                'gamePk': gamePk,
                'team_side': team_side,
                'team_id': team_id,
                'team_name': team_name,
                'atBats': batting_stats.get('atBats'),
                'hits': batting_stats.get('hits'),
                'doubles': batting_stats.get('doubles'),
                'triples': batting_stats.get('triples'),
                'homeRuns': batting_stats.get('homeRuns'),
                'rbi': batting_stats.get('rbi'),
                'strikeOuts': batting_stats.get('strikeOuts'),
                'baseOnBalls': batting_stats.get('baseOnBalls'),
                'avg': batting_stats.get('avg'),
                'obp': batting_stats.get('obp'),
                'slg': batting_stats.get('slg'),
                'ops': batting_stats.get('ops'),
                'stolenBases': batting_stats.get('stolenBases'),
                'caughtStealing': batting_stats.get('caughtStealing'),
                'plateAppearances': batting_stats.get('plateAppearances'),
                'leftOnBase': batting_stats.get('leftOnBase')
            }

            team_batting_df = pd.concat([team_batting_df, pd.DataFrame([team_row])], ignore_index=True)
            game_data_count += 1

        # Save after each game
        team_batting_df.to_csv(output_file, index=False)
        print(f"GamePk {gamePk}: Fetched {game_data_count} team records.")

        time.sleep(0.2)
        
    except Exception as e:
        print(f"Error fetching game {gamePk}: {e}")
        # Save whatever data fetched till now
        team_batting_df.to_csv(output_file, index=False)
        continue

print("All games processed. Data saved.", team_batting_df.shape)