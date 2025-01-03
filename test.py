import signal
import subprocess
import time
import os

# sp = subprocess.Popen("D:/Hotta/WmGpLaunch/WmgpLauncher.exe")
#
#
# print(sp.pid)
# time.sleep(5)
# # sp.kill()
#
# subprocess.call(["taskkill","/F","/T","/IM","WmgpMobileGame.exe"])

# date = time.strftime('%Y-%m-%d', time.localtime())
#
#
# def load_conf_file():
#
#     with open(Conf.conf_file, "r", encoding='utf-8') as file:
#         lines = file.readlines()
#
#     load_area = "NOT_AREA"
#     load_global_dict={}
#     load_game_dict={}
#
#     # load txt to dict
#     for line in lines:
#         line = line.strip()
#         if line.startswith("#") or line == "":
#             continue
#         if line.startswith("["):
#             load_area = line
#         else:
#             line_key, line_value = line.split('#')[0].split('=')
#             if load_area=='[global]':
#                load_global_dict[line_key.strip()]=line_value.strip()
#                #rint(f"global:key[{line_key.strip()}], value[{line_value.strip()}]")
#             if load_area=='[game]':
#                load_game_dict[line_key.strip()]=line_value.strip()
#                #print(f"game:key[{line_key.strip()}], value[{line_value.strip()}]")
#
#
#     # load dict to conf
#     # for key in load_game_dict.keys():
#     #     Conf.games.append(key)
#     Conf.exec_mode = load_global_dict.get('exec_mode')
#     Conf.capture_mode = load_global_dict.get('capture_mode')
#     Conf.score_threshold = float(load_global_dict.get('score_threshold'))
#     Conf.screenshot_path = load_global_dict.get('screenshot_path')
#     Conf.log_path = load_global_dict.get('log_path')
#     Conf.log_file = f"{Conf.log_path}/log.{date}.txt"
#     Conf.script_path = load_global_dict.get('script_path')
#     Conf.game_launcher_dict = dict(load_game_dict)
#
#     for key in load_game_dict.keys():
#         Conf.games.append(key)
#
#     for ele in load_global_dict["games_exclude"].split(','):
#         if Conf.games.count(ele) > 0:
#             Conf.games.remove(ele)
#             Conf.game_launcher_dict.pop(ele)
#
#     for ele in Conf.games:
#         Conf.game_script_status_dict[ele]='READY'
#
#     print(f"配置文件加载完成")
#     print(f"执行模式：{Conf.exec_mode}")
#     print(f"截图模式：{Conf.capture_mode}")
#     print(f"评分阈值：{Conf.score_threshold}")
#     print(f"截图文件夹路径：{Conf.screenshot_path}")
#     print(f"日志文件夹路径：{Conf.log_path}")
#     print(f"脚本文件夹路径：{Conf.script_path}")
#     print(f"游戏：{Conf.games}")
#     print(f"游戏程序目录：{Conf.game_launcher_dict}")
#     #print(f"游戏脚本执行状态：{Conf.game_script_status_dict}")
#
# class Conf:
#
#     conf_file = f"./conf.txt"
#
#     # exec_mode = ""
#     # capture_mode = ""
#     # score_threshold = 0
#     # screenshot_path = ""
#     # log_path = ""
#     # log_file = ""
#     games = []
#     games_exclude = []
#     game_script_status_dict = {}
#     game_launcher_dict = {}
#
#     script_path = ""
#     game = ""
#     game_launcher = ""
#     img_target_path = f"./img/{game}"
#     script_file = f"{script_path}/script_{game}.txt"
#
#     @staticmethod
#     def refresh():
#         Conf.script_file = f"{Conf.script_path}/script_{Conf.game}.txt"
#         Conf.img_target_path = f"./img/{Conf.game}"
#         Conf.game_launcher = Conf.game_launcher_dict.get(Conf.game)
#
#     # Conf.log_file = f"{Conf.log_path}/{Conf.game}.log"
#
# load_conf_file()