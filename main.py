import pandas
import os
import pathlib


def request_all_data():
    csv_data = pandas.read_csv("https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv").drop(
        ["廠牌項目", "快篩試劑截至目前結餘存貨數量", "來源資料時間"], axis=1)
    path = pathlib.Path()
    if not os.path.isdir(str(path) + '/dist'):
        os.mkdir(str(path) + '/dist')
    csv_data.to_json("dist/all.json", orient='records', force_ascii=False)


if __name__ == '__main__':
    request_all_data()
