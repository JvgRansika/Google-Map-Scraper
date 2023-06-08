import os, random
import csv
import pandas as pd
import settings

proxies = [p for p in settings.proxies if p['proxy'] != '']


# print error msg
def error(e):
    print(f'ERROR : {e}')


# print success msg
def success(s):
    print(f'SUCCESS : {s}')


# print proccessing msg
def procces(p):
    print(f'PROCCESS : {p}')


def get_output_file():
    file = 'output.csv'
    '''
    id = 0
    while True:
        if os.path.exists(file):
            file = 'output(' + str(id) + ").csv"
            id += 1
        else:
            break
    '''
    return file


def write_to_csv(file, data):
    writer = csv.writer(file)
    writer.writerow(data)


def remove_from_csv(file, line_to_remove):
    ok_line = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = ','.join(line)
            if line_to_remove != line:
                ok_line.append(line)
    with open(file, 'w', encoding="utf-8", newline='') as f:
        for li in ok_line:
            f.write(li + '\n')


def read_csv(file):  # return first line of the csv
    line = None
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = ','.join(line)
            return line


def get_a_proxy():
    global proxies
    if not proxies:
        return None

    while True:
        random_proxy = random.choice(proxies)
        if random_proxy['proxy'] != '':
            return random_proxy


def check_if_empty(file):
    with open(file, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            success(f'all search queries completed. {file} file is empty')
            return True
        else:
            return False
