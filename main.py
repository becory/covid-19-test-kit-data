import pandas


def request_all_data():
    csv_data = pandas.read_csv("https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv").drop(["廠牌項目", "快篩試劑截至目前結餘存貨數量", "來源資料時間"], axis=1)
    csv_data.to_json("all.json", orient='records', force_ascii=False)


if __name__ == '__main__':
    request_all_data()
