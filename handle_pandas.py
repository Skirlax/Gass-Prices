import datetime
import os

import pandas as psd
import warnings
import numpy as np


class HandleExcel:

    def __init__(self):
        warnings.simplefilter("ignore")

        self.result_list = []

    def get_average(self):
        plyn_name = os.listdir('Downloads/')[0]
        curreny_name = os.listdir('Downloads/')[1]
        plyn = psd.read_excel(f'Downloads/{plyn_name}', 0, 0)
        currencies = psd.read_excel(f'Downloads/{curreny_name}', 0, 0)
        index = 5
        row_index = 2
        skip = 0

        for x in plyn.iloc[5:, 5]:
            index += 1
            if skip > 0:
                skip -= 1
                continue
            skip = self.fridays(index, row_index, plyn, currencies)
            self.result_list.append([currencies.iloc[row_index, 0], x * currencies.iloc[row_index, 1]])
            row_index += 1

        # self.result_list = np.array(self.result_list).reshape(len(self.result_list),1)
        result_list_average = np.average([x[1] for x in self.result_list])
        print('------------------------------------------------------')
        print('Prices from day one to the end of the month in CZK:')
        print('------------------------------------------------------')
        print(self.result_list)
        print('\n')
        print('Average price:')
        print('------------------------------------------------------')
        print(result_list_average)
        print('------------------------------------------------------')
        self.write_to_excel(currencies, result_list_average)
        # Write result_list to excel file, include average price and dates all in one sheet
        # result_file = psd.DataFrame(self.result_list)
        # # Add a new column with dates
        # result_file.insert(0, 'Datumy', plyn.iloc[5:, 0])
        # print(result_file)

    def fridays(self, index, row_index, plyn, currencies):
        # Check if the day is a Friday
        if row_index > 2:
            if int(str(currencies.iloc[row_index, 0][0:2])) > int(str(currencies.iloc[row_index - 1, 0][0:2])) + 1:
                self.result_list.append(['Sobota', plyn.iloc[index - 1, 5] * currencies.iloc[row_index - 1, 1]])
                self.result_list.append(['Nedele', plyn.iloc[index, 5] * currencies.iloc[row_index - 1, 1]])
                if index < 10:
                    return 2
                else:
                    return 2
            else:
                return 0
        else:
            return 0

    def write_to_excel(self, currencies, average):
        df = psd.DataFrame(self.result_list)
        # Create new column in the dataframe
        df.insert(2,'','')
        df.insert(3,'Average','')
        # df.insert(3,'','')
        # Insert average only in the first row
        # df.iloc[0, 3] = "Average"
        df.iloc[1, 3] = average
        df.to_excel('Output/result.xlsx', sheet_name='Vysledky')
