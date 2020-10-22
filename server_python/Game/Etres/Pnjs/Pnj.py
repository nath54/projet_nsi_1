import os
import sys
import Etre
import json
# import ../Etre.py

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Triés par leurs id
data_pnjs = [
    "Data/pnjs/paysan_tergaron_vieu1.json"
]


class Pnj(Etre):
    def __init__(self, index):
        super.__init__(self)
        self.index = index

    def load(self):
        f = open(data_pnjs[self.index])
        data = json.loads(f.read())
        f.close()
