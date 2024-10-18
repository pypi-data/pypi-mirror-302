
class League:
    def __init__(self, league_id, name, country=None):
        self.league_id = league_id
        self.name = name
        self.country = country

    @classmethod
    def from_dict(cls, response):
        data = response['data']
        return cls(
            league_id=data['league']['id'],
            name=data['league']['name'],
            country=data['country']['name']
        )
