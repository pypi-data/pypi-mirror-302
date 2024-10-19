from datetime import datetime

from buco_db_controller.models.league import League
from buco_db_controller.models.team import Team


class TeamStats:
    def __init__(
            self,
            fixture_id,
            season,
            date,
            league,
            home_team,
            away_team,
            league_round,

            home_team_stats,
            away_team_stats,
    ):
        self.fixture_id = fixture_id
        self.date = date
        self.season = season
        self.home_team = home_team
        self.away_team = away_team
        self.league = league
        self.league_round = league_round

        self.home_team_stats = home_team_stats
        self.away_team_stats = away_team_stats

    @classmethod
    def from_dict(cls, fixture, team1_stats, team2_stats):
        fixture_id = fixture.fixture_id

        date = team1_stats['parameters']['date']
        season = team1_stats['parameters']['season']
        league_round = team1_stats['parameters']['round']

        if fixture.home_team.team_id == team1_stats['parameters']['team']:
            home_team_data = team1_stats['data']
            away_team_data = team2_stats['data']
        else:
            home_team_data = team2_stats['data']
            away_team_data = team1_stats['data']

        return cls(
            fixture_id=fixture_id,
            season=season,
            date=datetime.strptime(date, '%Y-%m-%d'),
            league=League(
                league_id=home_team_data['league']['id'],
                name=home_team_data['league']['name']
            ),
            league_round=league_round,
            home_team=fixture.home_team,
            away_team=fixture.away_team,
            home_team_stats=home_team_data,
            away_team_stats=away_team_data
        )
