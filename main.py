import pandas
import os
import pathlib
import datetime


def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def request_all_data():
    csv_data = pandas.read_csv("https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv").drop(
        ["廠牌項目", "快篩試劑截至目前結餘存貨數量", "來源資料時間"], axis=1)
    get_datetime = datetime.datetime.now()+datetime.timedelta(hours=8)
    path = pathlib.Path()
    if not os.path.isdir(str(path) + '/dist'):
        os.mkdir(str(path) + '/dist')
    first = pandas.read_csv("https://raw.githubusercontent.com/becory/covid-19-test-kit-data/data/all.csv")
    merge_table = first.merge(csv_data, how='outer', on='醫事機構代碼')
    new_data = pandas.DataFrame(columns=first.columns)
    check_length = 0
    non_update = []
    for index, row in merge_table.iterrows():
        row_dict = {}
        is_check = False
        for key in first.columns:
            if key+"_x" in row and key+"_y" in row:
                if pandas.notnull(row[key+"_y"]):
                    row_dict[key] = row[key+"_y"]
                elif key == "醫事機構名稱":
                    row_dict[key] = row["醫事機構名稱_x"]
                    is_check = True
                    check_length += 1
                    non_update.append(row["醫事機構名稱_x"])
                else:
                    row_dict[key] = row[key+"_x"]
            else:
                if key == "開賣":
                    if time_in_range(datetime.time(23, 0, 0), datetime.time(6, 0, 0), get_datetime.time()):
                        row_dict["開賣"] = 0
                    elif row["開賣"] != 1:
                        row_dict["開賣"] = int(is_check is False)
                else:
                    row_dict[key] = row[key]
        new_data = pandas.concat([new_data, pandas.DataFrame([row_dict.values()], columns=first.columns)], ignore_index=True)
    new_data.to_csv('dist/all.csv', index=False)
    status = pandas.DataFrame([{"update_time": get_datetime.strftime('%Y/%m/%d %H:%M:%S')}])
    status.to_csv('dist/status.csv', index=False)
    print(str(check_length)+"間藥局沒有更新資料")


if __name__ == '__main__':
    request_all_data()
