import yaml
import numpy as np
import os

gamma = 42.577478518e6  # Hz/T


class bSSFP:
    def __init__(
        self,
        TR: float,
        FA: float,
        FOV: list,  # mm
        k_shape: list,
        slice_thickness: float,  # TODO: change it into bandwidth
        sign_alter: bool,
        preparation: bool
    ):
        self.seq = []
        self.TR, self.FA, self.FOV, self.k_shape, self.slice_thickness, self.sign_alter, self.preparation = TR, FA, np.array(
            FOV), np.array(k_shape), slice_thickness, sign_alter, preparation
        self.data_process()

    def data_process(self):
        self.NFlip = self.k_shape[0]+1
        self.NADCsamples = self.k_shape[1]
        self.kFOV = np.array(
            [self.k_shape[0]/self.FOV[0], self.k_shape[1]/self.FOV[1]])
        self.dw = 1/self.kFOV
        # TODO: THERES something weird here
        # gamma*Gx*dw*TR/4=pi
        self.GX = 1/(gamma*self.dw[0]*self.TR/4)
        self.GY_max = 1/(gamma*self.dw[1]*self.TR/4)

    def add_readout(self, t_start, FA, TR, GX, GY, kY_idx):
        FA,  GX, GY, kY_idx = float(FA),  float(GX), float(GY), int(kY_idx)
        # timestamp
        PULSE_ts = {
            "t": t_start,
            "type": "PULSE",
            "FA": FA,
            "slice_thickness": self.slice_thickness
        }
        GY_ts_0 = {
            "t": t_start,
            "type": "GY",
            "G": -GY
        }
        GX_ts_0 = {
            "t": t_start,
            "type": "GX",
            "G": GX
        }
        GY_ts_1 = {
            "t": t_start+TR/4,
            "type": "GY",
            "G": 0
        }
        GX_ts_1 = {
            "t": t_start+TR/4,
            "type": "GX",
            "G": GX
        }
        self.seq.append(PULSE_ts)
        self.seq.append(GY_ts_0)
        self.seq.append(GX_ts_0)
        self.seq.append(GY_ts_1)
        self.seq.append(GX_ts_1)
        for adc_idx in range(self.NADCsamples):
            ADC_ts = {
                "t": float(t_start+TR/4+adc_idx*TR/(self.NADCsamples-1)),
                "type": "ADC",
                "kx": adc_idx,
                "ky": kY_idx
            }
            self.seq.append(ADC_ts)
        GY_tx_2 = {
            "t": t_start+TR/4+TR/2,
            "type": "GY",
            "G": -GY
        }
        GX_tx_2 = {
            "t": t_start+TR/4+TR/2,
            "type": "GX",
            "G": -GX
        }
        self.seq.append(GY_tx_2)
        self.seq.append(GX_tx_2)

    def generate(self, name):
        t_prep = 0
        if self.preparation:
            t_prep = self.TR/2
            self.seq.append({
                "t": 0,
                "type": "PULSE",
                "FA": self.FA/2,
            })
        for readout_idx in range(self.NFlip):
            t_start = t_prep+self.TR*readout_idx
            self.add_readout(
                t_start,
                self.FA*(((readout_idx % 2)*2-1) if self.sign_alter else 1),
                self.TR,
                self.GX,
                -self.GY_max+readout_idx*2*self.GY_max/(self.NFlip-1),
                readout_idx
            )
        with open(os.path.join("sequences_ssfp", name+".yaml"), "w") as f:
            yaml.dump(self.seq, f)


if __name__ == "__main__":
    ssfp = bSSFP(2.8, 30, [320, 320], [128, 128], 5, True, True)
    ssfp.generate("TR2.8_FA30")
