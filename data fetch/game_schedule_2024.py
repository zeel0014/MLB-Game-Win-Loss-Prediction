import requests
import pandas as pd

# API endpoint
url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2024&gameType=R"

# Fetch data
response = requests.get(url)
data = response.json()

games_data = []

# Loop through dates and games
for date_info in data.get("dates", []):
    game_date = date_info.get("date")
    for game in date_info.get("games", []):
        game_info = {
            "gamePk": game.get("gamePk"),
            "gameGuid": game.get("gameGuid"),
            "gameType": game.get("gameType"),
            "season": game.get("season"),
            "gameDate": game.get("gameDate"),
            "officialDate": game.get("officialDate"),
            "status": game.get("status", {}).get("detailedState"),
            "away_team_id": game.get("teams", {}).get("away", {}).get("team", {}).get("id"),
            "away_team_name": game.get("teams", {}).get("away", {}).get("team", {}).get("name"),
            "away_team_wins": game.get("teams", {}).get("away", {}).get("leagueRecord", {}).get("wins"),
            "away_team_losses": game.get("teams", {}).get("away", {}).get("leagueRecord", {}).get("losses"),
            "away_team_pct": game.get("teams", {}).get("away", {}).get("leagueRecord", {}).get("pct"),
            "away_score": game.get("teams", {}).get("away", {}).get("score"),
            "away_isWinner": game.get("teams", {}).get("away", {}).get("isWinner"),
            "home_team_id": game.get("teams", {}).get("home", {}).get("team", {}).get("id"),
            "home_team_name": game.get("teams", {}).get("home", {}).get("team", {}).get("name"),
            "home_team_wins": game.get("teams", {}).get("home", {}).get("leagueRecord", {}).get("wins"),
            "home_team_losses": game.get("teams", {}).get("home", {}).get("leagueRecord", {}).get("losses"),
            "home_team_pct": game.get("teams", {}).get("home", {}).get("leagueRecord", {}).get("pct"),
            "home_score": game.get("teams", {}).get("home", {}).get("score"),
            "home_isWinner": game.get("teams", {}).get("home", {}).get("isWinner"),
            "venue_id": game.get("venue", {}).get("id"),
            "venue_name": game.get("venue", {}).get("name"),
            "description": game.get("description"),
            "seriesDescription": game.get("seriesDescription"),
            "seriesGameNumber": game.get("seriesGameNumber"),
            "gamesInSeries": game.get("gamesInSeries"),
            "dayNight": game.get("dayNight"),
            "scheduledInnings": game.get("scheduledInnings"),
            "isTie": game.get("isTie")
        }
        games_data.append(game_info)

# Convert to DataFrame
df = pd.DataFrame(games_data)

# Save to CSV
df.to_csv("game_schedule_2024.csv", index=False, encoding="utf-8-sig")

print(f"Saved {len(df)} games to game_schedule_2024.csv")
