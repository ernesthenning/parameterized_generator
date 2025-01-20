from generator import Generator
import numpy as np
from tkinter import *
from tkinter import ttk

def load_parameters(method_name):
    f = open(method_name + '.txt', 'r')
    raw_parameters = []
    for line in f.readlines():
        parameter = line.replace('\n', '').split(': ')[-1]
        if ', ' in parameter:
            probes = parameter.split(', ')
            decoded_probes = []
            for probe in probes:
                probe = probe.replace('[', '')
                probe = probe.replace(']', '')
                numbers = probe.split(',')
                decoded_probe = []
                for number in numbers:
                    if '.' in number:
                        a = float(number)
                    else:
                        a = int(number)
                    decoded_probe.append(a)
                np_probe = np.array(decoded_probe)
                decoded_probes.append(np_probe)
            raw_parameters.append(decoded_probes)
        elif ':' in parameter:
            raw_parameters.append(parameter)
        elif not parameter.isnumeric():
            raw_parameters.append(parameter)
        elif parameter.count('.') == 2:
            raw_parameters.append(parameter)
        else:
            if '.' in parameter:
                b = float(parameter)
            else:
                b = int(parameter)
        raw_parameters.append(b)
    return raw_parameters


def generate():
   # parameters = load_parameters('31860')
    #for parameter in parameters:
     #   print(parameter)

    gen = Generator(length_points=15001,
                    dots_per_minute=600,
                    bias_left_border=1000,
                    bias_right_border=3900,
                    bias_max_intensity=15,
                    bias_min_intensity=0.5,
                    bias_peaks_number=12,
                    bias_max_peak_width=50,
                    bias_min_peak_width=20,
                    peaks_probe_number=3,
                    widths_probe=np.array([[120, 150, 110], [120, 150, 110], [120, 150, 110], [120, 150, 110], [120, 150, 110], [120, 150, 110], [120, 150, 110], [120, 150, 110]]),
                    intensities_probe_peaks=np.array([[147, 98, 121], [147, 98, 121], [147, 98, 121], [147, 98, 121], [147, 98, 121], [147, 98, 121], [147, 98, 121], [147, 98, 121]]),
                    times_probe_peaks=np.array([[5700, 6600, 12000], [5700, 6600, 12000], [5700, 6600, 12000], [5700, 6600, 12000], [5700, 6600, 12000], [5700, 6600, 12000], [5700, 6600, 12000], [5700, 6600, 12000]]),
                    repeatability=0.02,
                    reproducibility=0.04,
                    dead_time=1200,
                    dead_width=100,
                    dead_intensity=2,
                    intensities_stability_check=np.array([[6], [6]]),
                    number_chr_for_stability_check=0,
                    number_chromatograms_in_series=2,
                    noise_intensity=0.3,
                    probes_count=8,
                    start_time='11:41',
                    interval_between_chromatograms=26,
                    cyctime=0.1,
                    coef=0.0003,
                    units='mV',
                    analysis_date='20.01.2025')
    gen.get_exported_chromatograms()
    gen.generate_bats("20.01.2025")


if __name__ == '__main__':
    generate()

