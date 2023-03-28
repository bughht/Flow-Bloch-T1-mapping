import yaml
import os
import numpy as np


class MOLLI:
    def __init__(
        self,
        reverse_t=[0, 8000],
        readout_t=[100, 1100, 2100, 3100, 4100, 8200, 9200, 10200],
        readout_seq="bSSFP_TR2.8_FA25_N75_SA",
        dt=None
    ):
        '''
        reverse_t: list of time points for reverse readout
        readout_t: list of time points for readout
        readout_seq: name of readout sequence
        dt: time step for free precession simulation
        '''
        self.reverse_t = reverse_t
        self.readout_t = readout_t
        self.load_readout(readout_seq=readout_seq)
        self.seq = dict()
        self.dt = dt

    def load_readout(self, readout_seq):
        # Load readout sequence
        with open(os.path.join("sequences_old", readout_seq+".yaml"), "r") as f:
            self.readout_seq = yaml.load(
                f, Loader=yaml.FullLoader)[readout_seq]
        self.readout_time = self.readout_seq[-1]["t"]

    def generate(self, name):
        # Generate sequence
        self.seq[name] = []
        for t in self.reverse_t:
            self.seq[name].append(
                {
                    "FA": 180,
                    "t": t
                }
            )
        prev_t = 0
        for t in self.readout_t:
            for flip in self.readout_seq:
                self.seq[name].append(
                    {
                        "FA": flip["FA"],
                        "t": t+flip["t"]
                    }
                )
            if self.dt is not None:
                for dt_idx in range(1, int((t-prev_t)/self.dt)):
                    self.seq[name].append(
                        {
                            "FA": 0,
                            "t": prev_t+dt_idx*self.dt
                        }
                    )
            prev_t = t

        # sort by time
        self.seq[name] = sorted(self.seq[name], key=lambda k: k["t"])
        with open(os.path.join("sequences", name+".yaml"), "w") as f:
            yaml.dump(self.seq, f)


if __name__ == "__main__":
    molli = MOLLI(readout_seq="bSSFP_TR2.8_FA10_N75_SA_prep", dt=1)
    molli.generate("MOLLI_533_dt_TR2.8_FA10_N75_SA_prep")
