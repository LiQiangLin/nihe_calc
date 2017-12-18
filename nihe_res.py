from cal_fun import *
import xlrd
import xlwt
from origin_data import *

def read_data(path,v_array,alfa_array):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    for i in range(2, 9):
        v_array.append(table.cell(i, 0).value)
    for i in range(1, 7):
        for j in range(2, 9):
            alfa_array.append(table.cell(j, i).value)
    return table

def write_datatitle(new_sheet):
    for i in range(len(datatitle)):
        new_sheet.write(0, i, datatitle[i])

    for i in range(len(np_array)):
        new_sheet.write_merge(i * 21 + 1, 21 * (i + 1), 0, 0, np_array[i])

    for i in range(len(sf_array) * len(np_array)):
        new_sheet.write_merge(7 * i + 1, 7 * (i + 1), 1, 1, sf_array[i % len(sf_array)])

def write_data_to_xls(gongkuang,v_array,alfa_array):
    new_workbook = xlwt.Workbook()
    new_sheet = new_workbook.add_sheet(gongkuang)
    write_datatitle(new_sheet)

    i = 1
    for alfa in alfa_array:
        new_sheet.write(i, 2, alfa)
        i += 1

    j = 1
    for v in v_array:
        for np in np_array:
            for sf in sf_array:
                Deq = deq(s1, sf, do, dertaf)
                Nambda = nambda_moistair(t, ts, B, v)
                Re = ref(t, ts, B, v, s1, sf, do, dertaf)
                Lp = lp(np,s2)
                new_sheet.write(j, 3, Nambda / Deq)
                new_sheet.write(j, 4, Re)
                new_sheet.write(j, 5, Lp / Deq)
                j += 1
    new_workbook.save(gongkuang + '_data.xls')

def main():
    for gongkuang in gongkuang_array:
        v_array = []
        alfa_array = []
        path = 'data_table/' + gongkuang + '_huanrexishu.xlsx'
        read_data(path,v_array,alfa_array)
        write_data_to_xls(gongkuang + '_data_table',v_array,alfa_array)


if __name__ == '__main__':
    main()