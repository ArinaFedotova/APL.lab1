from csv_struct import CSV


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