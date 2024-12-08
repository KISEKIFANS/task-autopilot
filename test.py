import signal
import subprocess
import time
import os

sp = subprocess.Popen("D:/Hotta/WmGpLaunch/WmgpLauncher.exe")


print(sp.pid)
time.sleep(5)
# sp.kill()

subprocess.call(["taskkill","/F","/T","/IM","WmgpMobileGame.exe"])