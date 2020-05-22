from warfish.user import WarfishUser
from warfish.game import WarfishGame
from os import environ

me = WarfishUser('vdruker@gmail.com', password=environ['WARFISH_PASSWORD'])

me.fetch_total_games()
me.total_games

me.fetch_all_game_ids()
len(me.all_games_ids) == me.total_games

# This creates a .cache folder in your working directory - default is in ~/.cache/warfish
game = WarfishGame(me.all_games_ids[0], WarfishUser=me, global_cache='.cache')
game.dl_game_details()
