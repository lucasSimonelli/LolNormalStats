from elixir import *

metadata.bind = "sqlite:///database.sqlite"
metadata.bind.echo = True


class Match(Entity):
    champion = Field(Unicode(20))
    gameID = Field(Integer, default=0)
    gameType = Field(Unicode(30))
    winLoss = Field(Unicode(30))
    kills = Field(Integer, default=0)
    deaths = Field(Integer, default=0)
    assists = Field(Integer, default=0)
    gold = Field(Float, default=0.0)
    minions = Field(Integer, default=0)

