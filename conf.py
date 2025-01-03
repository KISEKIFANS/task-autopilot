import time

date = time.strftime('%Y-%m-%d', time.localtime())

class Conf:
    mode = "normal"  # step
    game="empty"
    games=[]
    score_threshold = 0.05

    game_status_dict = {}
    game_launcher_dict = {}
    screenshot_path = "./screenshot"
    script_path="./scripts"
    log_path="./logs"

    img_target_path = f"./img/{game}"
    conf_file = f"./conf.txt"
    script_file = f"{script_path}/script_{game}.txt"
    log_file = f"{log_path}/log.{date}.txt"
    game_launcher = game_launcher_dict.get(game)

    @staticmethod
    def refresh():
        Conf.script_file = f"{Conf.script_path}/script_{Conf.game}.txt"
        Conf.img_target_path = f"./img/{Conf.game}"
        Conf.game_launcher = Conf.game_launcher_dict.get(Conf.game)
       #Conf.log_file = f"{Conf.log_path}/{Conf.game}.log"
