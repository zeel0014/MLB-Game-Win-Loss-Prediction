import requests
import pandas as pd
import time
import os

schedule_file = "data/game_schedule_2024.csv"
output_file = "data/pitchers_player_2024.csv"

# Load schedule
schedule_df = pd.read_csv(schedule_file)

# Resume functionality
if os.path.exists(output_file):
    pitcher_df = pd.read_csv(output_file)
    already_fetched_games = set(pitcher_df['gamePk'].unique())
    print(f"Resuming. Already fetched {len(already_fetched_games)} games.")
else:
    pitcher_df = pd.DataFrame()
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
            players = team.get('players', {})

            for player_id, player_info in players.items():
                # Filter only pitchers
                if player_info['position']['type'] != 'Pitcher':
                    continue
                pitching_stats = player_info.get('stats', {}).get('pitching', {})
                if not pitching_stats:
                    continue

                player_row = {
                    'gamePk': gamePk,
                    'team_side': team_side,
                    'team_id': team_id,
                    'team_name': team_name,
                    'player_id': player_info['person']['id'],
                    'player_name': player_info['person']['fullName'],
                    'jerseyNumber': player_info.get('jerseyNumber'),
                    'position': player_info['position']['type'],
                    'status': player_info['status']['description'],
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
                    'rbi': pitching_stats.get('rbi')
                }

                pitcher_df = pd.concat([pitcher_df, pd.DataFrame([player_row])], ignore_index=True)
                game_data_count += 1

        # Save after each game
        pitcher_df.to_csv(output_file, index=False)
        print(f"GamePk {gamePk}: Fetched {game_data_count} pitcher records.")

        time.sleep(0.2)
        
    except Exception as e:
        print(f"Error fetching game {gamePk}: {e}")
        # Save whatever data fetched till now
        pitcher_df.to_csv(output_file, index=False)
        continue

print("All games processed. Data saved.", pitcher_df.shape)
