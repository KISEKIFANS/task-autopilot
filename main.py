from util import *

load_conf_file()

for game in Conf.games:

    print_and_log(f'开始执行{game}脚本')

    init_result=init(game)
    if init_result == 'ERR_SCRIPT_NOT_FOUND' :
        print_and_log(f'{game}脚本文件不存在，跳过脚本')
        continue
    if init_result == 'ERR_GAME_NOT_FOUND' :
        print_and_log(f'{game}游戏未运行，跳过脚本')
        continue
    else:
        mission_result = process_mission(init_result)
        while mission_result != "ALL_MISSION_COMPLETED":
            if mission_result == "exit":
                break
            else:
                mission_result = process_mission(mission_result)
        print_and_log(f'{game}脚本所有任务完成，执行完毕')
        time.sleep(2)
print_and_log(f'本日所有脚本执行完毕，按回车键退出')
input()

