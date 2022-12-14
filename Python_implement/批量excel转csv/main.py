import pandas as pd
import os


def excel_to_csv_utf8():
    """ 批量转换文件夹中的excel文件为csv文件(UTF-8编码) """
    for k in list(os.walk('source_data/')):
        for v in k[2]:
            path = k[0] + '\\' + v
            filename = 'result_data' + os.sep + v.split('.')[0] + '.csv'
            print(filename)
            df = pd.read_excel(path)
            df.to_csv(filename, index=False)


if __name__ == '__main__':
    # 测试通过
    excel_to_csv_utf8()
