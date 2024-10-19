from typing import List, Dict

from buco_db_controller import FixtureService, Fixture
from buco_db_controller.models.teams_stats import TeamStats
from buco_db_controller.repositories.fixture_repository import FixtureRepository
from buco_db_controller.repositories.team_stats_repository import TeamStatsRepository


class TeamStatsService:
    def __init__(self):
        self.team_repository = TeamStatsRepository()
        self.fixture_service = FixtureService()

    def upsert_many_team_stats(self, team_stats: List[dict]):
        self.team_repository.upsert_many_team_stats(team_stats)

    def get_team_stats(self, fixture: Fixture) -> Dict[str, TeamStats]:
        response = self.team_repository.get_team_stats(fixture.fixture_id)

        ht_stats = next((team_stats for team_stats in response if team_stats['team_id'] == fixture.home_team.team_id), None)
        at_stats = next((team_stats for team_stats in response if team_stats['team_id'] == fixture.away_team.team_id), None)

        ht_stats = TeamStats.from_dict(ht_stats)
        at_stats = TeamStats.from_dict(at_stats)

        teams_stats = {
            'home': ht_stats,
            'away': at_stats
        }
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



