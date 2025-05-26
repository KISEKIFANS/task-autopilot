from util import *

def run_script(game):
    Util.print_and_log(f'开始执行{game}脚本')
    init_result=Util.init(game)
    if init_result == 'ERR_SCRIPT_NOT_FOUND':
        Util.print_and_log(f'{game}脚本文件不存在，跳过脚本')
        #Conf.game_script_status_dict[game] = 'ERR_OCCURRED'
        return 'ERR_OCCURRED'
    if init_result == 'ERR_GAME_NOT_RUNNING':
        Util.print_and_log(f'{game}游戏未运行，跳过脚本')
        #Conf.game_script_status_dict[game] = 'WAIT_TO_RETRY'
        return 'WAIT_TO_RETRY'
    else:
        mission_result = Util.process_mission(init_result)
        while mission_result != "ALL_MISSION_COMPLETED":
            if mission_result == "SCRIPT_ABORTED":
                break
            else:
                mission_result = Util.process_mission(mission_result)
        if mission_result == "ALL_MISSION_COMPLETED":
            Util.print_and_log(f'{game}脚本所有任务完成，执行完毕')
            #Conf.game_script_status_dict[game] = 'COMPLETED'
            return 'COMPLETED'
        if mission_result == "SCRIPT_ABORTED":
            Util.print_and_log(f'{game}脚本手动退出，放弃后续执行')
            #Conf.game_script_status_dict[game] = 'ABORTED'
            return 'ABORTED'
        #time.sleep(2)

Util.load_conf_file()
for game in Conf.games:
    Conf.game_script_status_dict[game] = run_script(game)

SCRIPTS_NEED_RETRY="NO"
game_retry=[]
for game in Conf.games:
    if Conf.game_script_status_dict[game] == 'WAIT_TO_RETRY':
        SCRIPTS_NEED_RETRY = "YES"
        game_retry.append(game)
if SCRIPTS_NEED_RETRY=="NO":
    Util.print_and_log(f'本日所有脚本执行完毕，无脚本需要重试，按回车键退出')
    Util.send_qq_channel_message(f'本日所有手游日活脚本执行完毕')
else:
    retry_count=1
    while retry_count < 4 and SCRIPTS_NEED_RETRY=="YES":
        Util.print_and_log(f'本日除{game_retry}之外的脚本执行完毕，进行第{retry_count}次自动尝试')
        for game in Conf.games:
            if Conf.game_script_status_dict[game] == 'WAIT_TO_RETRY':
                Conf.game_script_status_dict[game] = run_script(game)

        SCRIPTS_NEED_RETRY = "NO"
        retry_count+=1
        game_retry=[]
        for game in Conf.games:
            if Conf.game_script_status_dict[game] == 'WAIT_TO_RETRY':
                SCRIPTS_NEED_RETRY = "YES"
                game_retry.append(game)
    if retry_count == 4:
        Util.print_and_log(f'本日除{game_retry}之外的脚本执行完毕，重试次数超过3次，结束执行，按回车键退出')
input()

