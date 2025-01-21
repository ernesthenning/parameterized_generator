import numpy as np
from datetime import timedelta, datetime
from os import path, mkdir


class Generator:

    def __init__(self,
                 length_points,
                 dots_per_minute,
                 bias_left_border,
                 bias_right_border,
                 bias_max_intensity,
                 bias_min_intensity,
                 bias_peaks_number,
                 bias_max_peak_width,
                 bias_min_peak_width,
                 peaks_probe_number,
                 widths_probe,
                 intensities_probe_peaks,
                 times_probe_peaks,
                 repeatability,
                 reproducibility,
                 dead_time,
                 dead_width,
                 dead_intensity,
                 intensities_stability_check,
                 number_chr_for_stability_check,
                 number_chromatograms_in_series,
                 noise_intensity,
                 probes_count,
                 start_time,
                 interval_between_chromatograms,
                 cyctime,
                 coef,
                 units,
                 analysis_date):

        self.length_points = length_points
        self.dots_per_minute = dots_per_minute
        self.bias_left_border = bias_left_border
        self.bias_right_border = bias_right_border
        self.bias_max_intensity = bias_max_intensity
        self.bias_min_intensity = bias_min_intensity
        self.bias_peaks_number = bias_peaks_number
        self.bias_max_peak_width = bias_max_peak_width
        self.bias_min_peak_width = bias_min_peak_width
        self.peaks_probe_number = peaks_probe_number
        self.widths_probe = widths_probe
        self.intensities_probe_peaks = intensities_probe_peaks
        self.times_probe_peaks = times_probe_peaks
        self.repeatability = repeatability
        self.reproducibility = reproducibility
        self.dead_time = dead_time
        self.dead_width = dead_width
        self.dead_intensity = dead_intensity
        self.intensities_stability_check = intensities_stability_check
        self.number_chr_for_stability_check = number_chr_for_stability_check
        self.number_chromatograms_in_series = number_chromatograms_in_series
        self.noise_intensity = noise_intensity
        self.probes_count = probes_count
        self.start_time = start_time
        self.interval_between_chromatograms = interval_between_chromatograms
        self.cyctime = cyctime
        self.coef = coef
        self.units = units
        self.analysis_date = analysis_date

    def generate_baseline(self, intensity, length_points):
        base_line_y = np.random.uniform(-intensity, intensity, length_points)
        return base_line_y

    def generate_peak(self, base_line, width, intensity, peak_time):
        base_line = base_line + intensity * np.exp(-((np.arange(0, self.length_points, 1) - peak_time) / width) ** 2)
        return base_line

    def generate_peaks(self, y, peaks_number, widths, intensities, times):
        for i in range(peaks_number):
            y = self.generate_peak(y, widths[i], intensities[i], times[i])
        return y

    def generate_bias(self, y, parameters):
        widths = parameters[0]
        intensities = parameters[1]
        times = parameters[2]
        for i in range(self.bias_peaks_number):
            y = self.generate_peak(y, widths[i], intensities[i], times[i])
        return y

    def generate_bias_parameters(self):
        widths = np.random.uniform(self.bias_min_peak_width, self.bias_max_peak_width, self.bias_peaks_number)
        intensities = np.random.uniform(self.bias_min_intensity, self.bias_max_intensity, self.bias_peaks_number)
        times = np.random.uniform(self.bias_left_border, self.bias_right_border, self.bias_peaks_number)
        result = []
        result.append(widths)
        result.append(intensities)
        result.append(times)
        return result

    def generate_dead_peak(self, y, dead_width, dead_intensity, dead_time):
        y = self.generate_peak(y, dead_width, dead_intensity, dead_time)
        return y

    def generate_n_chromatograms(self,
                                 number_chromatograms,
                                 bias_parameters,
                                 repeatability,
                                 dead_width,
                                 dead_intensity,
                                 dead_time,
                                 peaks_probe_number,
                                 widths_probe,
                                 intensities_probe_peaks,
                                 times_probe_peaks):
        result = []
        y = self.generate_baseline(self.noise_intensity, self.length_points)
        y = self.generate_dead_peak(y, dead_width, dead_intensity, dead_time)
        for i in range(number_chromatograms):
            repeatability_coef = np.random.uniform(1 - 0.5 * repeatability, 1 + 0.5 * repeatability)
            z = self.generate_peaks(y, peaks_probe_number, widths_probe * repeatability_coef,
                                        intensities_probe_peaks * repeatability_coef,
                                        times_probe_peaks * repeatability_coef)
            for parameter in bias_parameters:
                parameter = parameter * repeatability_coef
            z = self.generate_bias(z, bias_parameters)
            result.append(z)
        return result

    def get_exported_chromatograms(self):
        program_directory = path.dirname(path.realpath(__file__))
        export_path = path.join(program_directory, self.analysis_date)
        try:
            mkdir(export_path)
        except FileExistsError:
            pass
        export_path = path.join(export_path, self.start_time.replace(":", "_"))
        mkdir(export_path)
        stab_check = self.generate_chromatograms_stability_check()
        series = self.generate_series_with_given_concentrations()

        for i in range(len(stab_check)):
            self.export_result(values=stab_check[i], series_number=0, parallel_number=i, export_path=export_path)

        for k in range(len(series)):
            for j in range(self.number_chromatograms_in_series):
                self.export_result(values=series[k][j], series_number=k + 1, parallel_number=j, export_path=export_path)

    #значения ширины и времени удерживания берет как нулевые элементы в массивах ширин и времен для проб
    def generate_chromatograms_stability_check(self):
        result = []
        y = self.generate_baseline(self.noise_intensity, self.length_points)
        y = self.generate_dead_peak(y, self.dead_width, self.dead_intensity, self.dead_time)
        for i in range(self.number_chr_for_stability_check):
            repeatability_coef = np.random.uniform(1 - 0.5 * self.repeatability, 1 + 0.5 * self.repeatability)
            z = self.generate_peaks(y, self.peaks_probe_number, self.widths_probe[0] * repeatability_coef,
                                        self.intensities_stability_check[i] * repeatability_coef,
                                        self.times_probe_peaks[0] * repeatability_coef)
            result.append(z)

        return result

    def generate_series_with_given_concentrations(self):
        result = []
        for i in range(self.probes_count):
            bias_parameters = self.generate_bias_parameters()
            repeatability_coef = np.random.uniform(1 - 0.5 * self.repeatability, 1 + 0.5 * self.repeatability)
            one_series = self.generate_n_chromatograms(
                self.number_chromatograms_in_series,
                bias_parameters,
                self.repeatability,
                self.dead_width * repeatability_coef,
                self.dead_intensity * repeatability_coef,
                self.dead_time * repeatability_coef,
                self.peaks_probe_number,
                self.widths_probe[i],
                self.intensities_probe_peaks[i],
                self.times_probe_peaks[i])
            result.append(one_series)
        return result

    def export_result(self, values, series_number, parallel_number, export_path):
        name_out = '{:04d}-{}.txt'.format(series_number, parallel_number)
        f = open(export_path + "/" + name_out, mode='w')
        f.write('Число точек:  cycles=' + str(self.length_points) + '\r\n')
        f.write('Фактический интервал: cyctime=' + str(self.cyctime) + '\r\n')
        f.write('шаг АЦП: coef=' + str(self.coef) + '\r\n')
        f.write("Единицы измерений АЦП:  units='" + str(self.units) + "'\r\n")
        f.write("DATA:\r\n")
        for s in range(len(values)):
            f.write('{:.6f}\r\n'.format(values[s]))
        f.close()

    def generate_times(self):
        start_time_local = datetime.strptime(self.start_time, '%H:%M')
        times = [(start_time_local - timedelta(minutes=3 * self.interval_between_chromatograms)).strftime('%H:%M'),
                 (start_time_local - timedelta(minutes=2 * self.interval_between_chromatograms)).strftime('%H:%M'),
                 (start_time_local - timedelta(minutes=self.interval_between_chromatograms)).strftime('%H:%M'),
                 start_time_local.strftime('%H:%M')]
        current_time = start_time_local
        for i in range(self.probes_count * self.number_chromatograms_in_series - 1):
            current_time += timedelta(minutes=self.interval_between_chromatograms)
            times.append(current_time.strftime('%H:%M'))
        return times

    def generate_bats(self, current_date):
        times = self.generate_times()
        program_directory = path.dirname(path.realpath(__file__))
        export_path = path.join(program_directory, current_date, self.start_time.replace(":", "_"), "bats")
        mkdir(export_path)
        for n in range(len(times)):
            name_out = '{}.bat'.format(n)
            f = open(export_path + "/" + name_out, mode='w')
            f.write('@echo off\r\n')
            f.write('date ')
            f.write('{}\r\n'.format(current_date))
            f.write('@echo off\r\n')
            f.write('time ')
            f.write('{}\r\n'.format(times[n]))
            f.close()

    def generate_bats_mac(self, current_date, month, day, year):
        times = self.generate_times()
        program_directory = path.dirname(path.realpath(__file__))
        export_path = path.join(program_directory, current_date, self.start_time, "datetime_mac")
        mkdir(export_path)
        name_out = '{}.sh'.format('n')
        f = open(export_path + "/" + name_out, mode='w')
        for n in range(len(times)):
            f.write('\r\n')
            f.write("echo '555721qwertz' | sudo -S date {}\r\n".format(month + day + times[n].split(':')[0] + times[n].split(':')[1] + year))
        f.close()
