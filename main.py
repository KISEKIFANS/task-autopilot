from util import *

load_conf_file()

for game in Conf.games:

    print_and_log(f'开始执行{game}脚本')

    first_mission=init(game)
    mission_result = process_mission(first_mission)
    while mission_result != "ALL_MISSION_COMPLETED":
        if mission_result == "exit":
            break
        else:
            mission_result = process_mission(mission_result)
    print_and_log(f'{game}脚本所有任务完成，执行完毕')

