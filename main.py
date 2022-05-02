import pandas
import os
import pathlib

def request_all_data():
    csv_data = pandas.read_csv("https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv").drop(
        ["廠牌項目", "快篩試劑截至目前結餘存貨數量", "來源資料時間"], axis=1)
    path = pathlib.Path()
    if not os.path.isdir(str(path) + '/dist'):
        os.mkdir(str(path) + '/dist')
    first = pandas.read_csv("first.csv")
    merge_table = first.merge(csv_data, how='outer', on='醫事機構代碼')
    new_data = pandas.DataFrame(columns=csv_data.columns)
    for index, row in merge_table.iterrows():
        row_dict = {}
        is_check = False
        for key in csv_data.columns:
            if key+"_x" in row and key+"_y" in row:
                if pandas.notnull(row[key+"_y"]):
                    row_dict[key] = row[key+"_y"]
                elif key == "醫事機構名稱":
                    print(row)
                    row_dict[key] = row["醫事機構名稱_x"] + "（今日資料未更新）"
                    is_check = True
                else:
                    row_dict[key] = row[key+"_x"]
            else:
                if is_check is True and key == "備註":
                    row_dict[key] =  "（今日資料未更新）"
                else:
                    row_dict[key] = row[key]
        new_data = pandas.concat([new_data, pandas.DataFrame([row_dict.values()], columns=csv_data.columns)], ignore_index=True)
    new_data.to_csv('dist/all.csv', index=False)

if __name__ == '__main__':
    request_all_data()
