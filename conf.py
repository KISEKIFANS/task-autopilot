import time

date = time.strftime('%Y-%m-%d', time.localtime())

class Conf:

    conf_file = f"./conf.txt"

    exec_mode = ""
    capture_mode = ""
    score_threshold = 0
    screenshot_path = ""
    log_path="./logs" #
    log_file = f"{log_path}/log.{date}.txt" #
    games = []
    games_exclude = []
    game_script_status_dict = {} # READY RUNNING WAIT_TO_RETRY ERR_OCCURRED COMPLETED
    game_launcher_dict = {}

    script_path = ""
    game = ""
    game_launcher = ""
    img_target_path = f"./img/{game}"
    script_file = f"{script_path}/script_{game}.txt"

    @staticmethod
    def refresh():
        Conf.script_file = f"{Conf.script_path}/script_{Conf.game}.txt"
        Conf.img_target_path = f"./img/{Conf.game}"
        Conf.game_launcher = Conf.game_launcher_dict.get(Conf.game)

    # Conf.log_file = f"{Conf.log_path}/{Conf.game}.log"