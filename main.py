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
    parameters = load_parameters('31860')
    for parameter in parameters:
        print(parameter)

    gen = Generator(length_points=6001,
                    dots_per_minute=600,
                    bias_left_border=1000,
                    bias_right_border=2650,
                    bias_max_intensity=0.3,
                    bias_min_intensity=0.03,
                    bias_peaks_number=10,
                    bias_max_peak_width=50,
                    bias_min_peak_width=30,
                    peaks_probe_number=1,
                    widths_probe=np.array([[250], [250], [250], [250], [250], [250], [250], [250]]),
                    intensities_probe_peaks=np.array([[9.7], [9.7], [9.7], [9.7], [9.7], [9.7], [9.7], [9.7]]),
                    times_probe_peaks=np.array([[3100], [3100], [3100], [3100], [3100], [3100], [3100], [3100]]),
                    repeatability=0.04,
                    reproducibility=0.05,
                    dead_time=1200,
                    dead_width=200,
                    dead_intensity=2,
                    intensities_stability_check=np.array([[6], [6]]),
                    number_chr_for_stability_check=2,
                    number_chromatograms_in_series=2,
                    noise_intensity=0.3,
                    probes_count=8,
                    start_time='13:06',
                    interval_between_chromatograms=13,
                    cyctime=0.1,
                    coef=0.0003,
                    units='mV',
                    analysis_date='25.12.2024')
    gen.get_exported_chromatograms()
    gen.generate_bats("25.12.2024")


if __name__ == '__main__':
    generate()

