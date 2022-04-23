import handle_selenium
from time import sleep
import handle_pandas

gc = handle_selenium.Currency()
hp = handle_pandas.HandleExcel()


class Main:
    def __init__(self):
        self.__main()


    def __main(self):
        download_or_not = input("Download data? (y/n) ")
        months_back = int(input("Months back: "))
        if download_or_not == "y":
            gc.get_currency_file(months_back)
            gc.get_prices_file(months_back)
            print('Done!')
        sleep(3)

        hp.get_average()


if __name__ == "__main__":
    Main()
