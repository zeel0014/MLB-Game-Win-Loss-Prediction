import requests
import pandas as pd
import time
import os

schedule_file = "data/game_schedule_2024.csv"
output_file = "data/pitching_team_2024.csv"

# Load schedule
schedule_df = pd.read_csv(schedule_file)

# Resume functionality
if os.path.exists(output_file):
    team_pitching_df = pd.read_csv(output_file)
    already_fetched_games = set(team_pitching_df['gamePk'].unique())
    print(f"Resuming. Already fetched {len(already_fetched_games)} games.")
else:
    team_pitching_df = pd.DataFrame()
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
            pitching_stats = team.get('teamStats', {}).get('pitching', {})
            if not pitching_stats:
                continue

            team_row = {
                'gamePk': gamePk,
                'team_side': team_side,
                'team_id': team_id,
                'team_name': team_name,
                'inningsPitched': pitching_stats.get('inningsPitched'),
                'outs': pitching_stats.get('outs'),
                'runs': pitching_stats.get('runs'),
                'earnedRuns': pitching_stats.get('earnedRuns'),
                'hits': pitching_stats.get('hits'),
                'homeRuns': pitching_stats.get('homeRuns'),
                'strikeOuts': pitching_stats.get('strikeOuts'),
                'baseOnBalls': pitching_stats.get('baseOnBalls'),
                'hitBatsmen': pitching_stats.get('hitBatsmen'),
                'numberOfPitches': pitching_stats.get('numberOfPitches'),
                'balls': pitching_stats.get('balls'),
                'strikes': pitching_stats.get('strikes'),
                'strikePercentage': pitching_stats.get('strikePercentage'),
                'groundOuts': pitching_stats.get('groundOuts'),
                'flyOuts': pitching_stats.get('flyOuts'),
                'completeGames': pitching_stats.get('completeGames'),
                'shutouts': pitching_stats.get('shutouts'),
                'saveOpportunities': pitching_stats.get('saveOpportunities'),
            }

            team_pitching_df = pd.concat([team_pitching_df, pd.DataFrame([team_row])], ignore_index=True)
            game_data_count += 1

        # Save after each game
        team_pitching_df.to_csv(output_file, index=False)
        print(f"GamePk {gamePk}: Fetched {game_data_count} team pitching records.")

        time.sleep(0.2)
        
    except Exception as e:
        print(f"Error fetching game {gamePk}: {e}")
        # Save whatever data fetched till now
        team_pitching_df.to_csv(output_file, index=False)
        continue

print("All games processed. Data saved.", team_pitching_df.shape)
