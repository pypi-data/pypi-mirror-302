from typing import List

from buco_db_controller.models.fixture_teams_stats import TeamStats
from buco_db_controller.repositories.fixture_repository import FixtureRepository
from buco_db_controller.repositories.team_stats_repository import TeamStatsRepository


class TeamStatsService:
    def __init__(self):
        self.team_repository = TeamStatsRepository()
        self.fixture_repository = FixtureRepository()

    def upsert_many_team_stats(self, team_stats: List[dict]):
        self.team_repository.upsert_many_team_stats(team_stats)

    def get_team_stats(self, team_id: int, league_id: int, season) -> List[TeamStats]:
        response = self.team_repository.get_team_stats(team_id, league_id, season)
        fixtures = self.fixture_repository.get_team_fixtures(team_id, league_id, season)

        if len(response) == 0:
            raise ValueError(f'No team stats found for team {team_id}, league {league_id} and season {season}')

        teams_stats = []
        for team1_stats in response:
            fixture = next((fixture for fixture in fixtures if fixture.fixture_id == team1_stats.fixture_id), None)
            team2_stats = self.team_repository.get_team_stats(fixture.away_team.team_id, league_id, season)

            team_stats = TeamStats.from_dict(fixture, team1_stats, team2_stats)
            teams_stats.append(team_stats)

        teams_stats.sort(key=lambda x: x.date)
        return teams_stats

    def get_h2h_team_stats(self, team1_id, team2_id, league_id, seasons) -> List[TeamStats]:
        team1_stats = self.get_team_stats(team1_id, league_id, seasons)
        team2_stats = self.get_team_stats(team2_id, league_id, seasons)

        team2_stats_fixture_ids = [fixture.fixture_id for fixture in team2_stats]
        team1_stats_fixture_ids = [fixture.fixture_id for fixture in team1_stats]

        team1_stats = [fixture for fixture in team1_stats if fixture.fixture_id in team2_stats_fixture_ids]
        team2_stats = [fixture for fixture in team2_stats if fixture.fixture_id in team1_stats_fixture_ids]

        h2h_stats = {
            'team1': team1_stats,
            'team2': team2_stats
        }
        return h2h_stats



