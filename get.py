import os.path
import csv
import sys


def retry(func):
    def wrapper(*args):
        while func(*args):
            print("Error occurred, try one more time to write correct data.")

    return wrapper


# class Data:
#     file_path = ''
#     headers = []
#     data = []
#     region = ''
#     column_num = -1


class Get:
    def __init__(self):
        print("Computing statistical metrics")
        self.file_path = ''
        self.headers = []
        self.data = []
        self.region = ''
        self.regions = set()
        self.column_num = 0
        self.col_data = []

    def entry(self):
        self.__get_path()
        self.__get_region()
        self.__get_data()
        self.__get_column_num()
        self.__calc_metrics()

    def __get_path(self):
        print("FILE PATH")
        print('/Users/arinafedotova/PycharmProjects/lab1/russian_demography.csv')
        self.file_path = input("Enter file path: ")
        while not (os.path.exists(self.file_path)) or self.file_path.find('.csv') == -1:
            print("There is no file in this path")
            self.file_path = input("Enter file path: ")

    def __get_data(self):
        print("DATA")
        with open(self.file_path, newline='') as f:
            reader = csv.reader(f, delimiter=",")
            try:
                self.headers = next(reader)
                print(self.headers)
                for row in reader:
                    # if len(row) != 7:
                    #     self.__clear_data()
                    #     break
                    if row[1] == self.region:
                        self.data.append(row)
                        print(self.data[-1])
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(self.file_path, reader.line_num, e))

    def __get_headers(self):
        print("HEADERS")
        try:
            self.headers = self.data.pop(0)
            print(self.headers)
        except IndexError:
            print("This is an empty file")

    def __get_region(self):
        print("REGION NAME")
        self.__get_all_regions()
        self.region = input("Enter region name: ")
        while not (self.region in self.regions):
            print("There is no region with this name")
            self.region = input("Try again. Enter region name: ")

    def __get_all_regions(self):
        print("Avaliable options: ")
        with open(self.file_path, newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for row in reader:
                self.regions.add(row[1])
        self.regions = sorted(list(self.regions))
        for ind in range(1, len(self.regions) + 1):
            print(f'{ind}. {self.regions[ind-1]}')

    def __get_column_num(self):
        print('COLUMN NUM')
        print(self.headers[:1] + self.headers[2:])
        print('Choose a number from 1 to ', len(self.headers) - 1)
        column_num = input("Enter column number: ")
        while not(column_num.isdigit()) or not(0 < int(column_num) < len(self.headers)):
            print(f'You must enter integer number between 1 and {len(self.headers) - 1} !')
            column_num = input("Try again. Enter column number: ")

        self.column_num = 0 if column_num == 1 else int(column_num)
        self.__get_column_data()

    def __get_column_data(self):
        for row in self.data:
            if self.is_number(row[self.column_num]):
                self.col_data.append(float(row[self.column_num]))
    @staticmethod
    def is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __calc_metrics(self):
        print('CALCULATE METRICS')
        print(f'Maximum: {max(self.col_data)}')
        print(f'Minimum: {min(self.col_data)}')
        print(f'Median: {self.med(self.col_data)}')

    @staticmethod
    def med(data_list):
        data_list.sort()
        return data_list[len(data_list)//2] if len(data_list) % 2 else (data_list[len(data_list)//2]+data_list[len(data_list)//2-1])/2

    def __clear_data(self):
        self.file_path = ''
        self.headers = []
        self.data = []
        self.region = ''
        self.regions = set()
        self.column_num = 0
        self.col_data = []