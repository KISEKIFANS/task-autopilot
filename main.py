from util import *

load_conf_file()

for game in Conf.games:

    print_and_log(f'开始执行{game}脚本')

    init_result=init(game)
    if init_result == 'ERR_SCRIPT_NOT_FOUND' :
        print_and_log(f'{game}脚本文件不存在，跳过脚本')
        Conf.game_script_status_dict[game] = 'ERR_OCCURRED'
        continue
    if init_result == 'ERR_GAME_NOT_RUNNING' :
        print_and_log(f'{game}游戏未运行，跳过脚本')
        Conf.game_script_status_dict[game] = 'WAIT_TO_RETRY'
        continue
    else:
        mission_result = process_mission(init_result)
        while mission_result != "ALL_MISSION_COMPLETED":
            if mission_result == "SCRIPT_ABORTED":
                break
            else:
                mission_result = process_mission(mission_result)
        if mission_result == "ALL_MISSION_COMPLETED":
            print_and_log(f'{game}脚本所有任务完成，执行完毕')
            Conf.game_script_status_dict[game] = 'COMPLETED'
        if mission_result == "SCRIPT_ABORTED":
            print_and_log(f'{game}脚本手动退出，放弃后续执行')
            Conf.game_script_status_dict[game] = 'ABORTED'
        time.sleep(2)

SCRIPTS_NEED_RETRY="NO"
game_retry=[]
for game in Conf.games:
    if Conf.game_script_status_dict[game] == 'WAIT_TO_RETRY':
        SCRIPTS_NEED_RETRY = "YES"
        game_retry.append(game)
if SCRIPTS_NEED_RETRY=="NO":
    print_and_log(f'本日所有脚本执行完毕，无脚本需要重试，按回车键退出')
else:
    print_and_log(f'本日所有脚本执行完毕，{game_retry}脚本需要重试，按回车键退出')

input()

