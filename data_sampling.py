import csv
import datetime
import locale
import logging
import time
from decimal import Decimal
from math import fabs
from operator import le
from typing import Dict, List, Tuple

from tqdm import tqdm

from configure_logging import configure_logging
from constants import (DATETIME_FORMAT, FILENAME_BD, FILENAME_REQUEST,
                       MONCH_DICT, MONCH_DICT_FOR_STR)
from outputs import file_output


locale.setlocale(category=locale.LC_ALL, locale="ru")


def format_data(data_str: str) -> datetime.datetime:
    """Переводит дату и время из формата строки в формат datetime"""
    month_str = data_str.split()[1]
    datetime_str = data_str.replace(month_str, MONCH_DICT[month_str])
    date_time_obj = datetime.datetime.strptime(datetime_str, DATETIME_FORMAT)
    return date_time_obj


def format_data_in_str(date_time_obj:  datetime.datetime) -> str:
    """Переводит дату и время из формата datetime в формат строки"""
    date_str = date_time_obj.strftime(DATETIME_FORMAT)
    month_str = date_str.split()[1]
    datetime_str = date_str.replace(month_str, MONCH_DICT_FOR_STR[month_str])
    return datetime_str


def quicksort(
    data_list: List[Tuple[datetime.datetime, Tuple[float]]],
    start: int, end: int
) -> List[Tuple[datetime.datetime, Tuple[float]]]:
    """Быстрая сортировка списка"""
    if end - start > 1:
        pivot = partition(data_list, start, end)
        quicksort(data_list, start, pivot)
        quicksort(data_list, pivot + 1, end)
    return data_list


def partition(
    data_list: List[Tuple[datetime.datetime, Tuple[float]]],
    start: int, end: int
) -> int:
    """Определяет оптимальный pivot для быстрой сортировки"""
    pivot = data_list[start]
    left = start + 1
    right = end - 1
    while True:
        while left <= right and data_list[left] <= pivot:
            left = left + 1
        while left <= right and data_list[right] >= pivot:
            right = right - 1
        if left <= right:
            data_list[left], data_list[right] = (
                data_list[right],
                data_list[left]
            )
        else:
            data_list[start], data_list[right] = (
                data_list[right],
                data_list[start]
            )
            return right


def select_data(
    request_time_dict: Dict[str, datetime.datetime]
) -> Tuple[Tuple[str], List[Tuple[datetime.datetime, Tuple[float]]]]:
    """Считывает данные из файла базы для заданного диапазона времени"""
    packages_data = []
    try:
        with open(FILENAME_BD, encoding='utf-8') as file:
            title = tuple(file.readline().strip().split(';'))
            csv_reader = csv.reader(file, delimiter=';')
            for row in tqdm(
                csv_reader,
                desc='Загрузка данных для заданного диапазона времени'
            ):
                data_record = format_data(row[1])
                if (request_time_dict['start'] <=
                        data_record <= request_time_dict['end']):
                    data = []
                    for index, value in enumerate(row):
                        if index > 1:
                            data.append(float(value.replace(',', '.')))
                    packages_data.append((data_record, tuple(data)))
    except FileNotFoundError:
        print(f'Файл базы данных ({FILENAME_BD}) не найден')
    quicksort(packages_data, 0, len(packages_data))
    return title, packages_data


def comparison_parameters_with_aperture(
    parametr_1: List[float],
    parametr_2: List[float],
    aperture: List[float]
) -> bool:
    """Вычисляет разницу между значениями параметров
       и сравнивает ее с апертурой"""
    difference_parameter_values = (
        [(fabs(Decimal(x) - Decimal(y))
          for x, y in zip(parametr_2, parametr_1))]
    )
    comparison_parameters_with_aperture = map(
        le,
        difference_parameter_values,
        aperture
    )
    if False in comparison_parameters_with_aperture:
        return True


def data_sampling(aperture: List[float], packages_data: (Tuple[Tuple[str],
                  List[Tuple[datetime.datetime, List[float]]]])) -> None:
    """Выводит в файл csv данные, в которых хотя бы один параметр отличается
    от предыдущего на значение большее апертуры"""
    title, data_list = packages_data
    results = [title]
    count = 0
    for index in tqdm(
        range(1, len(data_list)),
        desc='Операция сравнения разницы значений параметра с апертурой'
    ):
        if comparison_parameters_with_aperture(
            data_list[index - 1][1], data_list[index][1], aperture
        ) is True:
            count += 1
            record_id = count
            list_index = data_list[index][:]
            data, list_parametrs = list_index
            date_time_str = format_data_in_str(data)
            list_resultat = list(list_parametrs)
            list_resultat.insert(0, record_id)
            list_resultat.insert(1, date_time_str)
            results.append(tuple(list_resultat))
    file_output(results)


def read_input() -> Tuple[Dict[str, datetime.datetime], List[float]]:
    """Считывает данные запроса"""
    try:
        with open(FILENAME_REQUEST, encoding='utf-8') as file:
            content = file.readline().strip().split(';')
            request_time_dict = {}
            request_time_dict['start'] = format_data(content[0])
            request_time_dict['end'] = format_data(content[1])
            aperture = []
            for index, value in tqdm(
                enumerate(content),
                desc='Загрузка данных запроса'
            ):
                if index > 1:
                    aperture.append(float(value.replace(',', '.')))
            return request_time_dict, aperture
    except FileNotFoundError:
        print(f'Файл данных запроса ({FILENAME_REQUEST}) не найден')


def main() -> None:
    start_time = time.time()
    configure_logging()
    logging.info('Программа запущена!')
    request_time_dict, aperture = read_input()
    packages_data = select_data(request_time_dict)
    data_sampling(aperture, packages_data)
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f'Программа завершила работу. '
                 f'Время выполнения: {total_time:0.3f}c')


if __name__ == '__main__':
    main()
