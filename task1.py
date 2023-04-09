# 1. Задание на закрепление знаний по модулю CSV.
# Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV.
# Для этого:
#
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
# их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений
# извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например,
# main_data — и поместить в него названия столбцов отчета в виде списка:
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
#
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(),
# а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().
from pathlib import Path
from typing import Sequence

import chardet
import re
import csv


class FileExtensionError(Exception):
    pass


BASE_DIR = Path(__file__).parent
FILE_DIR = BASE_DIR / 'var'

FILE_NAMES = (
    'info_1.txt',
    'info_2.txt',
    'info_3.txt',
)
REGEXPS = (
    r'Изготовитель ОС:\s+(.*)',
    r'Название ОС:\s+(.*)',
    r'Код продукта:\s+(.*)',
    r'Тип системы:\s+(.*)',
)


def get_encoding(file_name: str) -> str:
    with open(FILE_DIR / file_name, 'rb') as f:
        return chardet.detect(f.read(300))['encoding']


def get_data(file_names: Sequence[str]) -> list[list]:
    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]

    for file_name in file_names:
        parsed_data = list()
        encoding = get_encoding(file_name)
        with open(FILE_DIR / file_name, encoding=encoding) as file:
            text = file.read()
            for regexp in REGEXPS:
                try:
                    parsed_data.append(re.search(regexp, text).group(1))
                except IndexError:
                    print(f'The value of the regular expression: {regexp} was not found in the file {file_name}')

        main_data.append(parsed_data)

    return main_data


def write_to_csv(csv_file):
    file_ext = csv_file.split('.')[-1]

    if file_ext != 'csv':
        raise FileExtensionError('Incorrect file extension passed for writing (CSV required)')

    main_data = get_data(file_names=FILE_NAMES)

    with open(FILE_DIR / csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        for data in main_data:
            writer.writerow(data)


if __name__ == '__main__':
    csv_file_name = input('Enter the file name to save the report: ')
    write_to_csv(csv_file_name)
