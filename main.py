#!/usr/bin/env python3

from place import Place
from functions import error, procces, success, get_output_file, read_csv, remove_from_csv, check_if_empty
from scraper import Scraper
import settings

first_que = True
file_name = None
max_per_search = settings.max_per_search


def extract_data(scraper, url):
    scraper.download_webpage(url)
    scraper.extract_details()


def write_data():
    f_object = None
    global file_name
    global first_que
    if first_que:
        file_name = get_output_file()
        first_que = False
    procces(f'opening {file_name}')
    while True:
        try:
            f_object = open(file_name, 'a', encoding="utf-8", newline='')
        except PermissionError:
            error(f'write_data - permission error while openning the {file_name}')
        if f_object:
            break
    for place_ in Place.places:
        place_.save_data(f_object)
        del place_
    f_object.close()
    success(f'added data for sq - {scraper.search_query} to {file_name}')

def a_process()


def main():
    global max_per_search
    scraper = Scraper()
    scraper.setup_driver()
    while True:
        scraper.search_query = read_csv('input.csv')
        if scraper.search_query == '' or scraper.search_query is None:
            if check_if_empty('input.csv'):
                raise KeyboardInterrupt
        links_for_places = scraper.search()
        if len(links_for_places) > max_per_search != 0:
            links_for_places = links_for_places[:max_per_search]
        for url in links_for_places:
            extract_data(scraper, url)
        write_data()
        remove_from_csv('input.csv', scraper.search_query)
    scraper.shutdown()


if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('Leaving scrapper')
            break
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write('\n')
                f.write(e)
                f.write('********************************************************************************************************************')
                f.write('\n')


