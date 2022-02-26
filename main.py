import NHL_API
import Visualizer


def main():
    Visualizer.shooting_data_visual(2000, 2020, 2)
    player = NHL_API.get_player(8477474)
    print(player)


if __name__ == '__main__':
    main()
