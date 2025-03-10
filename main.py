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

    gen = Generator(length_points=18001,
                    dots_per_minute=600,
                    bias_left_border=2000,
                    bias_right_border=9000,
                    bias_max_intensity=20.1,
                    bias_min_intensity=0.03,
                    bias_peaks_number=30,
                    bias_max_peak_width=150,
                    bias_min_peak_width=30,
                    peaks_probe_number=1,
                    widths_probe=np.array([[200], [200], [200], [200], [200], [200], [200], [200],
                    [200], [200], [200], [200], [200], [200], [200], [200], [200], [200], [200], [200], [200], [200], [200], [200],
                    [200], [200], [200], [200], [200], [200], [200], [200]]),
                    intensities_probe_peaks=np.array([
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75],
                    [0], [18.75], [208], [226.75]]),
                    times_probe_peaks=np.array([[14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900],
                    [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900],
                    [14900], [14900], [14900], [14900], [14900], [14900], [14900], [14900]]),
                    repeatability=0.04,
                    reproducibility=0.06,
                    dead_time=1200,
                    dead_width=200,
                    dead_intensity=2,
                    intensities_stability_check=np.array([[375], [375]]),
                    number_chr_for_stability_check=2,
                    number_chromatograms_in_series=2,
                    noise_intensity=0.3,
                    probes_count=32,
                    start_time='08:45',
                    interval_between_chromatograms=32,
                    cyctime=0.1,
                    coef=0.0003,
                    units='mV',
                    analysis_date='27.01.2025')
    gen.get_exported_chromatograms()
    gen.generate_bats("27.01.2025")


if __name__ == '__main__':
    generate()

