import os
import csv


def get_file_list(v_dir):
    list = os.listdir(v_dir)
    return list


def extract_csv_rows_into_list(v_dir, v_file_nm):
    try:
        v_file_path = v_dir + "//" + v_file_nm
        with open(v_file_path , 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            in_lines_list = []

            for row in csv_reader:
                in_lines_list.append(row)
                out_lines_list = in_lines_list

            return out_lines_list

    except FileNotFoundError:
        print(v_file_path + " not exists")
