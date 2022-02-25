import numpy as np
from matplotlib import pyplot as plt
import json
import NHL_API


def shooting_data_visual():
    first_year = 2000
    second_year = 2020
    season_type = 2
    shooting_data_seasons = []

    # for year in range(first_year, second_year + 1):
    #     shooting_plays_by_game = for_season(year, season_type, get_shooting_plays)
    #     shooting_data_seasons.append(shooting_plays_by_game)
    #
    # f = open(str(first_year)+'-'+str(second_year)+'_'+str(season_type)+'_'+"shooting.json", "w")
    # json.dump(shooting_data_seasons, f, indent=4)

    f = open(str(first_year)+'-'+str(second_year)+'_'+str(season_type)+'_'+"shooting.json", "r")
    shooting_data_seasons = json.load(f)

    length = 200
    l_2 = length / 2
    width = 100
    w_2 = width / 2

    goals = np.zeros((width, length))
    saves = np.zeros((width, length))
    misses = np.zeros((width, length))
    goal_percent = np.zeros((width, length))
    for season in shooting_data_seasons:
        for game in season:
            for play in game:
                try:
                    if play['result']['event'] == 'Shot':
                        saves[int(play['coordinates']['y'] + w_2)][int(play['coordinates']['x'] + l_2)] += 1
                    elif play['result']['event'] == 'Goal':
                        goals[int(play['coordinates']['y'] + w_2)][int(play['coordinates']['x'] + l_2)] += 1
                    elif play['result']['event'] == 'Miss':
                        misses[int(play['coordinates']['y'] + w_2)][int(play['coordinates']['x'] + l_2)] += 1
                except KeyError as e:
                    pass

    for i in range(width):
        for j in range(length):
            if goals[i][j] == 0:
                goal_percent[i][j] = 0
            elif saves[i][j] == 0:
                goal_percent[i][j] = 1
            else:
                goal_percent[i][j] = goals[i][j] / (saves[i][j] + goals[i][j])

    plt.title('saves')
    plt.imshow(saves)
    plt.show()

    plt.title('goals')
    plt.imshow(goals)
    plt.show()

    plt.title('percent')
    plt.imshow(goal_percent)
    plt.show()


def main():
    player = NHL_API.get_player(8477474)
    print(player)


if __name__ == '__main__':
    main()
