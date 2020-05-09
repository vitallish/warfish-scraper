import warfish.user
from os import environ

me = warfish.user.WarfishUser('vdruker@gmail.com', password=environ['WARFISH_PASSWORD'])

me.fetch_total_games()
me.total_games

me.fetch_all_game_ids()
len(me.all_games_ids) == me.total_games