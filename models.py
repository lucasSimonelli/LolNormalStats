from elixir import *

metadata.bind = "sqlite:///database.sqlite"
metadata.bind.echo = False


class Match(Entity):
    champion = Field(Unicode(20))
    gameID = Field(Integer, default=0)
    gameType = Field(Unicode(30))
    won = Field(Boolean)
    kills = Field(Integer, default=0)
    deaths = Field(Integer, default=0)
    assists = Field(Integer, default=0)
    gold = Field(Float, default=0.0)
    minions = Field(Integer, default=0)

class NormalStats(Entity):
    champion = Field(Unicode(20))
    kills = Field(Integer, default=0)
    deaths = Field(Integer, default=0)
    assists = Field(Integer, default=0)
    wins = Field(Integer, default=0)
    losses = Field(Integer, default=0)
    gold = Field(Float, default=0.0)
    minions = Field(Integer, default=0)

class AramStats(Entity):
    champion = Field(Unicode(20))
    kills = Field(Integer, default=0)
    deaths = Field(Integer, default=0)
    assists = Field(Integer, default=0)
    wins = Field(Integer, default=0)
    losses = Field(Integer, default=0)
    gold = Field(Float, default=0.0)
    minions = Field(Integer, default=0)

class RankedTeamStats(Entity):
    champion = Field(Unicode(20))
    kills = Field(Integer, default=0)
    deaths = Field(Integer, default=0)
    assists = Field(Integer, default=0)
    wins = Field(Integer, default=0)
    losses = Field(Integer, default=0)
    gold = Field(Float, default=0.0)
    minions = Field(Integer, default=0)

class SoloQStats(Entity):
    champion = Field(Unicode(20))
    kills = Field(Integer, default=0)
    deaths = Field(Integer, default=0)
    assists = Field(Integer, default=0)
    wins = Field(Integer, default=0)
    losses = Field(Integer, default=0)
    gold = Field(Float, default=0.0)
    minions = Field(Integer, default=0)

