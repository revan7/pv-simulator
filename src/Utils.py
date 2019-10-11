import csv
import os


def write_output(time_stamp, measured_power, output_power, total_power):
    with open(get_file_path(time_stamp), 'a+') as f:
        writer = csv.writer(f)
        writer.writerow([time_stamp.time().strftime("%H:%M:%S"), round(measured_power, 2), round(output_power, 2), round(total_power, 2)])


def get_file_path(time_stamp):
    year = time_stamp.year
    month = time_stamp.month
    day = time_stamp.day
    folder_subdirectory = os.path.join('output', str(year), str(month))
    if not os.path.exists(folder_subdirectory):
        os.makedirs(folder_subdirectory)
    file_path = os.path.join(folder_subdirectory, '{}.csv'.format(day))
    if not os.path.exists(file_path):
        with open(file_path, 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Measured Power', 'Output Power', 'Total Power'])
    return file_path
