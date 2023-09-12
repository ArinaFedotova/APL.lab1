import os.path
import csv
import sys
import math
from calculate import Calculate
from csv_struct import CSV
# ошибка при вводе года колонки    +
# разбить на считывание и подсчет  (струтуру данных выделить и передать ее в подсчет)
# размер файла до 1гб ограничить   +


class Parser:
    def __init__(self):
        print("Csv parser")
        self.file_max_size = 2**30

    def entry(self):
        self.__get_path()
        self.__get_region()
        self.__get_data()
        self.__get_column_num()
        calc = Calculate()
        calc.calc_metrics()
        self.__clear_data()

    def __get_path(self):
        print("FILE PATH")
        print("Path must have an extention .csv and less than 1gb")
        print('/Users/arinafedotova/PycharmProjects/lab1/russian_demography.csv')
        CSV.file_path = input("Enter file path: ")
        while not (os.path.exists(CSV.file_path)) or CSV.file_path.find('.csv') == -1 or os.stat(CSV.file_path).st_size >= self.file_max_size:
            print("This file does not exist or not csv or larger than 1gb")
            CSV.file_path = input("Enter file path: ")

    @staticmethod
    def __get_data():
        print("DATA")
        with open(CSV.file_path, newline='') as f:
            reader = csv.reader(f, delimiter=",")
            try:
                CSV.headers = next(reader)
                print(CSV.headers)
                for row in reader:
                    if row[1] == CSV.region:
                        CSV.data.append(row)
                        print(CSV.data[-1])
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(CSV.file_path, reader.line_num, e))

    @staticmethod
    def __get_headers():
        print("HEADERS")
        try:
            CSV.headers = CSV.data.pop(0)
            print(CSV.headers)
        except IndexError:
            print("This is an empty file")

    def __get_region(self):
        print("REGION NAME")
        self.__get_all_regions()
        CSV.region = input("Enter region name: ")
        while not (CSV.region in CSV.regions):
            print("There is no region with this name")
            CSV.region = input("Try again. Enter region name: ")

    def __get_all_regions(self):
        print("Avaliable options: ")
        with open(CSV.file_path, newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for row in reader:
                if not (self.is_number(row[1])) and len(row[1]) != 0:
                    CSV.regions.add(row[1])
        CSV.regions = sorted(list(CSV.regions))
        for ind in range(1, len(CSV.regions) + 1):
            print(f'{ind}. {CSV.regions[ind-1]}')

    def __get_column_num(self):
        print('COLUMN NUM')
        print(CSV.headers[:1] + CSV.headers[2:])
        print('Choose a number from 1 to ', len(CSV.headers) - 1)
        column_num = input("Enter column number: ")
        while not(column_num.isdigit()) or not(0 < int(column_num) < len(CSV.headers)):
            print(f'You must enter integer number between 1 and {len(CSV.headers) - 1} !')
            column_num = input("Try again. Enter column number: ")

        CSV.column_num = 0 if int(column_num) == 1 else int(column_num)
        self.__get_column_data()

    def __get_column_data(self):
        for row in CSV.data:
            if self.is_number(row[CSV.column_num]):
                CSV.col_data.append(float(row[CSV.column_num]))

    @staticmethod
    def is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __clear_data(self):
        CSV.file_path = ''
        CSV.headers = []
        CSV.data = []
        CSV.region = ''
        CSV.regions = set()
        CSV.column_num = 0
        CSV.col_data = []


class Calculate:
    def __init__(self):
        print("Computing statistical metrics")

    def calc_metrics(self):
        print('CALCULATE METRICS')
        if len(CSV.col_data):
            print(f'Maximum: {max(CSV.col_data)}')
            print(f'Minimum: {min(CSV.col_data)}')
            print(f'Median: {self.med(CSV.col_data)}')
            print(f'Average: {sum(CSV.col_data)/len(CSV.col_data)}')
            self.print_percentile_table()
        else:
            print("There is no data to calculate!")

    @staticmethod
    def med(data_list):
        data_list.sort()
        if len(data_list) % 2:
            return data_list[len(data_list)//2]
        else:
            return (data_list[len(data_list)//2]+data_list[len(data_list)//2-1])/2

    @staticmethod
    def percentile(list, percent):
        sorted_list = sorted(list)
        x = percent/100 * (len(sorted_list) - 1) + 1
        elem1 = sorted_list[int(x) - 1] #v(n)
        elem2 = sorted_list[math.ceil(x)-1] # v(n+1)
        _x = x % int(x)
        return round(elem1 + _x * (elem2 - elem1), 4)

    def print_percentile_table(self):
        print("+-------+-------------+")
        print("|   N%  |  Percentile |")
        print("+-------+-------------+")
        for i in range(0, 101, 5):
            digit = self.percentile(CSV.col_data, i)
            print(f"|{' ' * (4 - len(str(i)))}{i}%  |  {digit}{' ' * (10 - len(str(digit)) + 1)}|")
        print("+-------+-------------+")