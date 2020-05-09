import urllib
import mechanize
import re
from lxml import etree
from io import StringIO


class WarfishUser:
    def __init__(self, username, password=None):
        self.base_url = 'http://warfish.net/'
        self.username = username
        self.logged_in = False
        self.resp = None
        self.url = None
        self.br = None
        self.htmlparser = etree.HTMLParser()
        self.site_text = None
        self.tree = None
        self.url_parsed = None
        self.total_games = None
        self.all_games_ids = None

        self.setup_browser()
        if password is not None:
            self.login(password=password)

    def __repr__(self):
        login_string = "  Logged in" if self.logged_in else "  Not logged in"

        output = "WarfishUser\n" \
                 "  Username: " + self.username + "\n" + \
                 login_string

        return output

    def setup_browser(self):
        # initiate browser connection
        br = mechanize.Browser()
        cj = mechanize.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Chrome')]
        self.br = br

        self.check_login()

        return self

    def open(self, *paths, **params):
        url = self.base_url

        for p in paths:
            url = urllib.parse.urljoin(url + '/', p)

        if params:
            built_params = urllib.parse.urlencode(params)
            url = url + '?' + built_params

        resp = self.br.open(url)

        if resp.code == 200:
            self.url = resp.geturl()
            self.resp = resp
            self.url_parsed = False
        # TODO add error handling

        return self

    def parse(self):

        self.site_text = self.resp.read().decode()
        site_io = StringIO(self.site_text)
        self.tree = etree.parse(site_io, self.htmlparser)
        self.url_parsed = True

        return self

    def open_and_parse(self, *paths, **params):
        self.open(*paths, **params)
        self.parse()

        return self

    def login(self, password=None):

        self.open('war', 'login', ret='home')

        g_form = self.br.global_form()
        self.br.select_form(nr=0)
        g_form.find_control('login').add_to_form(self.br.form)
        g_form.find_control('password').add_to_form(self.br.form)

        self.br.form['login'] = self.username
        self.br.form['password'] = password
        self.br.submit()
        self.check_login()

        if self.logged_in:
            self.resp = self.br.response()
            self.url = self.resp.geturl()
        else:
            print("Not logged in")

        return self

    def check_login(self):
        self.open('war', 'home')
        self.logged_in = self.resp.info()['Content-Location'] == 'home.py'

        return self

    def fetch_total_games(self, filter=3):

        self.open_and_parse('war', 'play', f=filter, pp=25)

        total_game_xpath = '/html/body/center/table[3]/tr[3]/td[1]/b/text()'

        total_games = re.search('^([0-9]*)',
                                self.tree.xpath(total_game_xpath)[0]).group(1)

        self.total_games = int(total_games)
        return self

    def fetch_all_game_ids(self):
        if self.total_games is None:
            self.fetch_total_games()

        output = []
        for i in range(int(self.total_games / 100) + 1):
            self.open_and_parse('war', 'play', f=3, pp=100, p=i)
            game_id_xpath = '/html/body/center/table[3]/tr[2]/td/table[2]/tr/td/table//tr/td[3]/nobr/a[1]/@href'
            game_ids = self.tree.xpath(game_id_xpath)
            game_id_full = [re.search('gid=(.+)', game_id).group(1) for game_id in game_ids]

            output.extend(game_id_full)

        self.all_games_ids = output

        return self
