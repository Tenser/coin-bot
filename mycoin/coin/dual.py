from mycoin.coin.unit import DualPositionUnit
import time
from datetime import datetime

class DualPosition:
    def __init__(self, infos, usdt, importance, leverage):
        self.dpus = []
        for info in infos:
            self.dpus.append(DualPositionUnit(info, usdt, importance, leverage))
        self.turn = False
        self.log = ""
    
    def run(self):
        print(self.turn)
        while self.turn:
            time.sleep(30)
            tmp_log = ""
            for dpu in self.dpus:
                time.sleep(0.5)
                tmp_log += dpu.update()
            now = datetime.time(datetime.now())
            tmp_log += 'time ' + str(now.hour) + ':' + str(now.minute)
            self.log = tmp_log
        self.log = ""
