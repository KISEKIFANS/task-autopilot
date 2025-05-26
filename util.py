import cv2
import pyautogui
import os
import pydirectinput
from conf import *
import subprocess
import requests
import json

class Util:


    @staticmethod
    def print_and_log(txt):
        current_time = time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime())
        print(f'[{current_time}] {txt}')
        log_writer.writelines(f'[{current_time}] {txt}\n')
        log_writer.flush()

    @staticmethod
    def log(txt):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log_writer.writelines(f'[{current_time}] {txt}\n')
        log_writer.flush()

    @staticmethod
    def send_qq_channel_message(txt):
        try:
            #get token
            url = "https://bots.qq.com/app/getAppAccessToken"
            header = {'Content-Type': 'application/json'}
            data = {"appId": Conf.bot_appid,
                    "clientSecret": Conf.bot_secret
                    }
            access_token = json.loads(requests.post(url=url, headers=header, data=json.dumps(data)).text)[
                "access_token"]

            #use token to send qq channel message
            url = f"https://api.sgroup.qq.com/channels/{Conf.bot_channel_id}/messages"
            header = {'Content-Type': 'application/json',
                  'Authorization': f'QQBot {access_token}'
                  }
            data = {
                "content": txt,
                "msg_type": 0
            }
            result = requests.post(url=url, headers=header, data=json.dumps(data)).text
            Util.print_and_log(result)

        except Exception as e:
            Util.print_and_log("ERR in send qq channel message: " + str(e))

    @staticmethod
    def init(new_game):
        Conf.game = new_game
        Conf.refresh()
        pyautogui.FAILSAFE = False
        Util.print_and_log('初始化开始，当前目录' + os.getcwd())
        if not os.path.exists(Conf.screenshot_path):
            os.makedirs(Conf.screenshot_path, exist_ok=True)
            Util.print_and_log(f'检测到截图文件夹{Conf.screenshot_path}不存在，创建完成')
        if not os.path.exists(Conf.script_path):
            os.makedirs(Conf.script_path, exist_ok=True)
            Util.print_and_log(f'检测到脚本文件夹{Conf.script_path}不存在，创建完成')
        if not os.path.exists(Conf.script_file):
            Util.print_and_log(f'检测到脚本文件{Conf.script_file}不存在，程序退出')
            return "ERR_SCRIPT_NOT_FOUND"
        else:
            Util.print_and_log(f'脚本文件为：{Conf.script_file}')
        if Conf.game_launcher:
            try_count = 0
            while try_count <3 :
                try:
                    subprocess.Popen(Conf.game_launcher)
                    break
                except Exception as e:
                    Util.print_and_log(f"未成功打开游戏，稍后重试: {e}")
                    time.sleep(2)
                    try_count += 1
            if try_count == 3:
                Util.print_and_log(f'重试3次后未成功打开游戏，程序退出')
                return "ERR_GAME_NOT_RUNNING"
        seqs = Util.get_all_seq()
        Util.print_and_log(f'初始化完成，第一个任务为{seqs[0]}')
        Conf.game_script_status_dict[Conf.game] = 'RUNNING'
        return seqs[0]

    @staticmethod
    def load_conf_file():

        with open(Conf.conf_file, "r", encoding='utf-8') as file:
            lines = file.readlines()

        load_area = "NOT_AREA"
        load_global_dict={}
        load_game_dict={}

        # load txt to dict
        for line in lines:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            if line.startswith("["):
                load_area = line
            else:
                line_key, line_value = line.split('#')[0].split('=')
                if load_area=='[global]':
                   load_global_dict[line_key.strip()]=line_value.strip()
                   #rint(f"global:key[{line_key.strip()}], value[{line_value.strip()}]")
                if load_area=='[game]':
                   load_game_dict[line_key.strip()]=line_value.strip()
                   #print(f"game:key[{line_key.strip()}], value[{line_value.strip()}]")


        # load dict to conf
        Conf.exec_mode = load_global_dict.get('exec_mode')
        Conf.capture_mode = load_global_dict.get('capture_mode')
        Conf.score_threshold = float(load_global_dict.get('score_threshold'))
        Conf.screenshot_path = load_global_dict.get('screenshot_path')
        Conf.log_path = load_global_dict.get('log_path')
        Conf.log_file = f"{Conf.log_path}/log.{date}.txt"
        Conf.script_path = load_global_dict.get('script_path')
        Conf.game_launcher_dict = dict(load_game_dict)

        Conf.bot_appid = load_global_dict.get("bot_appid")
        Conf.bot_secret = load_global_dict.get("bot_secret")
        Conf.bot_channel_id = load_global_dict.get("bot_channel_id")

        for key in load_game_dict.keys():
            Conf.games.append(key)

        for ele in load_global_dict["games_exclude"].split(','):
            if Conf.games.count(ele) > 0:
                Conf.games.remove(ele)
                Conf.game_launcher_dict.pop(ele)

        for ele in Conf.games:
            Conf.game_script_status_dict[ele]='READY'


        # open log file
        global log_writer
        warn_info=""
        if not os.path.exists(Conf.log_path):
            os.makedirs(Conf.log_path, exist_ok=True)
            warn_info = f'检测到日志文件夹{Conf.log_path}不存在，创建完成'
        log_writer = open(Conf.log_file, "a", encoding='utf-8')
        if warn_info:
            Util.print_and_log(warn_info)


        Util.print_and_log(f"配置文件加载完成")
        Util.print_and_log(f"执行模式：{Conf.exec_mode}")
        Util.print_and_log(f"截图模式：{Conf.capture_mode}")
        Util.print_and_log(f"评分阈值：{Conf.score_threshold}")
        Util.print_and_log(f"截图文件夹路径：{Conf.screenshot_path}")
        Util.print_and_log(f"日志文件夹路径：{Conf.log_path}")
        Util.print_and_log(f"脚本文件夹路径：{Conf.script_path}")
        Util.print_and_log(f"游戏：{Conf.games}")
        Util.print_and_log(f"游戏程序目录：{Conf.game_launcher_dict}")
        #print(f"游戏脚本执行状态：{Conf.game_script_status_dict}")

    @staticmethod
    def load_script_file():
        with open(Conf.script_file, "r", encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    @staticmethod
    def get_all_seq():
        lines = Util.load_script_file()
        seqs = []
        for line in lines:
            if line.startswith('#') or line.strip() == '':
                continue
            seqs.append(line.split(",")[0])
        return seqs

    @staticmethod
    def get_img_center(seq, img_target):
        # 屏幕截图
        pyautogui.screenshot().save(f"{Conf.screenshot_path}/{Conf.game}_{seq}_screenshot.png")

        # 载入屏幕截图
        img_current_screen = cv2.imread(f"{Conf.screenshot_path}/{Conf.game}_{seq}_screenshot.png")

        # 目标图片
        img_target = cv2.imread(img_target)
        # 读取宽高
        height, width, channel = img_target.shape

        # 匹配结果
        result = cv2.matchTemplate(img_current_screen, img_target, cv2.TM_SQDIFF_NORMED)

        # 匹配分数，使用TM_SQDIFF_NORMED时越低越准确
        score = cv2.minMaxLoc(result)[0]

        # 获取匹配区域左上角坐标
        x_upper_left, y_upper_left = cv2.minMaxLoc(result)[2]

        # 计算匹配区域右下角坐标
        x_lower_right, y_lower_right = x_upper_left + width, y_upper_left + height

        # 计算匹配区域中心坐标
        target_center = int((x_upper_left + x_lower_right) / 2), int((y_upper_left + y_lower_right) / 2)

        return target_center, score

    @staticmethod
    def mouse_click(position):
        pyautogui.mouseDown(position[0], position[1])
        time.sleep(0.2)
        pyautogui.mouseUp(position[0], position[1])

        # pydirectinput.mouseDown(position[0], position[1])
        # time.sleep(0.2)
        # pydirectinput.mouseUp(position[0], position[1])

        time.sleep(1)

    @staticmethod
    def mouse_slip_around(position, dis_x, dis_y):
        x0 = int(position[0])
        y0 = int(position[1])
        point_01 = x0 - dis_x, y0 - dis_y
        point_02 = x0 + dis_x, y0 - dis_y
        point_03 = x0 + dis_x, y0
        point_04 = x0 - dis_x, y0
        point_05 = x0 - dis_x, y0 + dis_y
        point_06 = x0 + dis_x, y0 + dis_y
        pyautogui.mouseDown(point_01[0], point_01[1])
        pyautogui.moveTo(point_02[0], point_02[1], duration=0.5)
        pyautogui.moveTo(point_03[0], point_03[1], duration=0.5)
        pyautogui.moveTo(point_04[0], point_04[1], duration=0.5)
        pyautogui.moveTo(point_05[0], point_05[1], duration=0.5)
        pyautogui.moveTo(point_06[0], point_06[1], duration=0.5)
        pyautogui.mouseUp(point_06[0], point_06[1])

    @staticmethod
    def mouse_slip(position, dis_x, dis_y):
        point_start = int(position[0]), int(position[1])
        point_end = point_start[0] + dis_x, point_start[1] + dis_y
        pyautogui.mouseDown(point_start[0], point_start[1])
        pyautogui.moveTo(point_end[0], point_end[1], duration=0.5)
        pyautogui.mouseUp(point_end[0], point_end[1])

    @staticmethod
    def press_key(key):
        key_press = key.split('+')[0]
        key_next = ""
        if len(key.split('+')) > 1:
            key_next = key.split('+', 1)[1]
        if key_press.startswith('*'):
            key_press = key_press[1:]
            pydirectinput.keyDown(key_press)
            time.sleep(0.5)
            if len(key_next) > 0:
                Util.press_key(key_next)
            pydirectinput.keyUp(key_press)
            time.sleep(1)
        else:
            pyautogui.keyDown(key_press)
            time.sleep(0.5)
            if key_next:
                Util.press_key(key_next)
            pyautogui.keyUp(key_press)
            time.sleep(1)

        # pydirectinput.keyDown(key)
        # time.sleep(0.5)
        # pydirectinput.keyUp(key)
        # time.sleep(1)

    @staticmethod
    def find_img(seq, img_target, timeout, mission):
        if img_target == "MATCH_YES":
            time.sleep(timeout)
            return "DIRECT_YES"
        elif img_target == "MATCH_NO":
            time.sleep(timeout)
            return "DIRECT_NO"
        else:

            img_target = f'{Conf.img_target_path}/{img_target}'

            count = 0
            while count < timeout:
                center, score = Util.get_img_center(seq, img_target)
                if score > Conf.score_threshold:
                    Util.print_and_log(f'任务{seq}正在进行第{count + 1}次匹配，score={score}，未检测到有效目标')
                    count += 1
                    time.sleep(1)
                else:
                    Util.print_and_log(f'任务{seq}正在进行第{count + 1}次匹配，score={score}，检测到有效目标，{mission}')
                    return center
            Util.print_and_log(f'任务{seq}超过重试次数')
            return "IMG_TARGET_NOTFOUND"

    @staticmethod
    def process_mission(seq_start):
        lines = Util.load_script_file()
        seqs = Util.get_all_seq()
        seq_is_found = False
        for line in lines:
            if line.startswith('#') or line.strip() == '':
                continue

            seq = line.split(",")[0]

            if Conf.exec_mode == "step":
                input(f"当前处于逐步模式，回车以继续执行任务{seq}")

            if seq == seq_start:
                seq_is_found = True
            if seq_is_found:
                img_target = line.split(",")[1]
                action_img_found = line.split(",")[2]
                action_img_not_found = line.split(",")[3]
                timeout = int(line.split(",")[4])
                mission = line.split(",")[5].replace('\n', '')
                Util.print_and_log(f'seq={seq},img_target={img_target},action_y={action_img_found},action_n={action_img_not_found},timeout={timeout},mission={mission}')

                # if not os.path.exists(f'{img_target_path}/{img_target}'):
                #     print(f"目标图片{img_target}不存在，请检查名称")
                #     find_img_result="IMG_TARGET_NOTFOUND"
                # else:
                find_img_result = Util.find_img(seq, img_target, timeout, mission)
                if find_img_result == "IMG_TARGET_NOTFOUND" or find_img_result == "DIRECT_NO":
                    if action_img_not_found == 'block':
                        Util.send_qq_channel_message(f'执行{Conf.game}日活脚本的任务{seq}时无法匹配到图片，请进行相关检查~')
                        seq_new = input(f"程序已挂起，请调整脚本及图片。调整完毕后输入任务序号以继续执行（或直接回车执行最近一次任务{seq}，或输入exit退出）： ")
                        Util.log(f"程序已挂起，请调整脚本及图片。调整完毕后输入任务序号以继续执行（或直接回车执行最近一次任务{seq}，或输入exit退出）： {seq_new}")
                        seqs = Util.get_all_seq()
                        if seq_new == "exit" :
                            return "SCRIPT_ABORTED"
                        if seq_new == "" :
                            return seq
                        while seqs.count(seq_new) <= 0 :
                            seq_new = input(f"任务{seq_new}不存在，请重新输入： ")
                            Util.log(f"任务不存在，请重新输入：  {seq_new}")
                        return seq_new
                    else:
                        return action_img_not_found
                else:
                    if seqs.count(action_img_found) > 0:
                        return action_img_found

                    # 当有click关键字
                    elif action_img_found.find('click') != -1:

                        # 当是*click，表时需要用alt呼出鼠标
                        if action_img_found.startswith('*'):
                            pydirectinput.keyDown('alt')

                        # 当不带有@，直接点图标中央
                        if action_img_found.find('@') == -1:
                            # 此时不能为DIRECT_YES
                            if find_img_result == 'DIRECT_YES':
                                Util.print_and_log('MATCH_YES时不能直接click')
                            else:
                                Util.mouse_click(find_img_result)

                        # 当带有@，点相对坐标或绝对坐标
                        else:
                            # 获取坐标子串
                            pos_str = action_img_found.split('(')[1].split(')')[0]
                            abs_x = pos_str.split('@')[0]
                            abs_y = pos_str.split('@')[1]

                            # 相对坐标且为直接成功事件时：
                            if not abs_x.startswith('*') and not abs_y.startswith('*') and find_img_result == 'DIRECT_YES':
                                Util.print_and_log('MATCH_YES时click不能跟相对座标')

                            # 非直接成功事件或绝对坐标：
                            else:
                                if abs_x.startswith('*') and abs_y.startswith('*'):
                                    find_img_result = 0, 0
                                    abs_x = abs_x[1:]
                                    abs_y = abs_y[1:]
                                find_img_result = find_img_result[0] + int(abs_x), find_img_result[1] + int(abs_y)
                                Util.mouse_click(find_img_result)
                                Util.print_and_log(f'{find_img_result}')

                        if action_img_found.startswith('*'):
                            pydirectinput.keyUp('alt')
                        continue
                    elif action_img_found.startswith('slipAround'):
                        distance = action_img_found.split('(')[1].split(')')[0]
                        dis_x = int(distance.split('@')[0])
                        dis_y = int(distance.split('@')[1])
                        Util.mouse_slip_around(find_img_result, dis_x, dis_y)
                        continue
                    elif action_img_found.startswith('slip'):
                        distance = action_img_found.split('(')[1].split(')')[0]
                        dis_x = int(distance.split('@')[0])
                        dis_y = int(distance.split('@')[1])
                        Util.mouse_slip(find_img_result, dis_x, dis_y)
                        continue
                    else:
                        #press key
                        Util.press_key(action_img_found)
                        continue

        #kill client if exists
        return "ALL_MISSION_COMPLETED"
