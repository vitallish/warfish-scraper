from pathlib import Path
import hashlib

class WarfishGame:
    def __init__(self, game_id, username=None, WarfishUser=None, global_cache = "~/.cache/warfish"):
        self.game_id = game_id
        self.username = username # overwritten by WarfishUser if provided

        if(WarfishUser is not None):
            self.add_WarfishUser(WarfishUser)
        else:
            self.WarfishUser = None
            self.br = None

        if(global_cache is not None):
            self.set_cache(global_cache)
        else:
            self.set_cache(Path.cwd()) # use current directory otherwise

    def add_WarfishUser(self, WarfishUser):
        self.WarfishUser = WarfishUser
        self.br = WarfishUser.br
        self.username = WarfishUser.username

        return self

    def set_cache(self, cache):

        full_path = Path(cache).expanduser()
        if(self.username is not None):
            full_path = full_path.joinpath(hashlib.md5(self.username.encode()).hexdigest())

        self.cache = full_path
        self.game_cache = self.cache.joinpath(self.game_id)

        Path(self.game_cache).mkdir(parents=True, exist_ok=True)

        return self

    def check_logged_in(self):
        if not self.WarfishUser.logged_in:
            print("You are not logged in - this won't work")

    def dl_game_details(self):
        self.check_logged_in()
        details_file = 'details_' + self.game_id + '.html'
        details_file = self.game_cache.joinpath(details_file)
        self.WarfishUser.open('war','play','gamedetails', gid = self.game_id)
        details_text = self.WarfishUser.resp.get_data()
        with open(details_file, 'w') as f:
            f.write(details_text.decode())









