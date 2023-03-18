import yaml
import os
import numpy as np


class bSSFP:
    def __init__(
        self,
        TR: float,
        FA: float,
        NFlip: int,
        SA: bool,
        preparation: bool
    ):
        '''
        TR: repetition time
        FA: flip angle
        NFlip: number of flip angles (excluding preparation)
        SA: sign alternation
        preparation: preparation pulse (half TR and half FA)
        '''
        self. TR, self.FA, self.NFlip, self.SA, self.preparation = TR, FA, NFlip, SA, preparation
        self.seq = dict()

    def generate(self, name):
        # Generate sequence
        self.seq[name] = []
        t_prep = 0
        if self.preparation:
            t_prep = self.TR / 2
            self.seq[name].append(
                {
                    "FA": self.FA/2,
                    "t": 0
                }
            )
        for flip_idx in range(self.NFlip):
            self.seq[name].append(
                {
                    "FA": self.FA*(((flip_idx % 2)*2-1) if self.SA else 1),
                    "t": t_prep+self.TR * flip_idx,
                }
            )
            self.preparation = False
        with open(os.path.join("sequences", name+".yaml"), "w") as f:
            yaml.dump(self.seq, f)


if __name__ == "__main__":
    ssfp = bSSFP(2.8, 10, 75, True, True)
    ssfp.generate("bSSFP_TR2.8_FA10_N75_SA_prep")
