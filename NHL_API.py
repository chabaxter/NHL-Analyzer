import requests as rq
import json

url_prefix = 'https://statsapi.web.nhl.com/api'
season_type_lookup = {
    1: "Pre",
    2: "Regular",
    3: "Post",
    4: "Star"
}


def for_season(year, season_type, func):
    things = []
    i = 1
    while True:
        try:
            print(f'{year}: Getting {i}')
            game = get_game(year=year, season_type=season_type, game_id=i)
            things.append(func(game))
            i += 1
        except rq.exceptions.HTTPError as e:
            break
    return things


def get_season(year, season_type):
    season = []
    i = 1
    while True:
        try:
            game = get_game(year=year, season_type=season_type, game_id=i)
            season.append(game)
            i += 1
        except rq.exceptions.HTTPError as e:
            break
    return season


def get_game(year, season_type, game_id):
    url = url_prefix+'/v1/game/'+str(year)+str(season_type).zfill(2)+str(game_id).zfill(4)+'/feed/live'
    r = rq.get(url=url)
    if r.status_code == 404:
        raise rq.exceptions.HTTPError
    return r.json()


def get_player(player_id):
    url = url_prefix+'/v1/people/'+str(player_id)
    r = rq.get(url=url)
    if r.status_code == 404:
        raise rq.exceptions.HTTPError
    return r.json()


def get_player_season(player_id, year=None):
    url = url_prefix+'/v1/people/'+str(player_id)+'&stats=statsSingleSeason'
    if year is not None:
        url += '&season='+str(year)+str(year+1)
    r = rq.get(url=url)
    if r.status_code == 404:
        raise rq.exceptions.HTTPError
    return r.json()


def get_shooting_plays(game_data):
    # loop through all plays in the game
    shot_types = ['Shot', 'Goal', 'Blocked Shot', 'Missed Shot']
    shots = []
    for play in game_data['liveData']['plays']['allPlays']:
        if play['result']['event'] in shot_types:
            shots.append(play)
    return shots


def update_season_data(year, season_type):
    season = get_season(year, season_type)
    f = open(str(year)+season_type_lookup[int(season_type)]+"season.json", "w")
    json.dump(season, f, indent=4)