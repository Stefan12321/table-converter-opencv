import os

import cv2
import numpy as np
import pytesseract
import csv
import re
import platform
import pandas as pd

from pdf2image import convert_from_path
from openpyxl import load_workbook

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def open_image(src):
    if src.endswith(".pdf"):
        print('convert')
        src = pdf_to_png(src)
    raw = cv2.imread(src)
    # cv2.imshow("1", raw)
    # cv2.waitKey(2)
    return raw


def pdf_to_png(path: str) -> str:
    ext_img = convert_from_path(path)[0]
    ext_img.save("data/target.png", "PNG")
    return "./data/target.png"


def parse_pic_to_excel_data(raw, path: str):

    # print("SRC:", src)
    #
    # if src.endswith(".pdf"):
    #     src = pdf_to_png(src)
    # raw = cv2.imread(src, 1)
    # Изображение в оттенках серого
    gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
     # Показать картинки
    rows, cols = binary.shape
    scale = 40
     # Получите основную ценность адаптивно
     # Определите горизонтальные линии:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated_col = cv2.dilate(eroded, kernel, iterations=1)
    # cv2.imshow("excel_horizontal_line", dilated_col)

     # Определите вертикальную линию:
    scale = 20
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated_row = cv2.dilate(eroded, kernel, iterations=1)
    # cv2.imshow("excel_vertical_line：", dilated_row)
    # Объедините идентифицированные горизонтальные и вертикальные линии
    bitwise_and = cv2.bitwise_and(dilated_col, dilated_row)
    # cv2.imshow("excel_bitwise_and", bitwise_and)
    # cv2.waitKey(0)

     # Определить схему таблицы
    merge = cv2.add(dilated_col, dilated_row)

     # Вычитаются два изображения и удаляются границы таблицы
    merge2 = cv2.subtract(binary, merge)

    new_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    erode_image = cv2.morphologyEx(merge2, cv2.MORPH_OPEN, new_kernel)
    # cv2.imshow('erode_image2', erode_image)
    merge3 = cv2.add(erode_image, bitwise_and)
    # cv2.imshow('merge3', merge3)
    # cv2.waitKey(0)
     # Выньте логотип focus
    ys, xs = np.where(bitwise_and > 0)
    # cv2.waitKey(0)
    # Массив горизонтальных и вертикальных координат
    y_point_arr = []
    x_point_arr = []
     # При сортировке похожие пиксели исключаются, и берется только последняя точка с похожими значениями
     # Это 10 - это расстояние между двумя пикселями. Оно не фиксировано. Оно будет регулироваться в соответствии с разными изображениями. Это в основном высота (переходы по координате y) и длина (переходы по координате x) таблицы ячеек
    i = 0
    sort_x_point = np.sort(xs)
    for i in range(len(sort_x_point) - 1):
        if sort_x_point[i + 1] - sort_x_point[i] > 10:
            x_point_arr.append(sort_x_point[i])
        i = i + 1
     # Чтобы добавить последнюю точку
    x_point_arr.append(sort_x_point[i])

    i = 0
    sort_y_point = np.sort(ys)
    # print(np.sort(ys))
    for i in range(len(sort_y_point) - 1):
        if (sort_y_point[i + 1] - sort_y_point[i] > 10):
            y_point_arr.append(sort_y_point[i])
        i = i + 1
    y_point_arr.append(sort_y_point[i])

    # Цикл координаты y, таблица разделения координат x
    data = [[] for i in range(len(y_point_arr))]
    data_fr_pd = []
    for i in range(len(y_point_arr) - 1):
        data_fr_pd.append([])
        for j in range(len(x_point_arr) - 1):
            # При делении первый параметр - это координата y, а второй параметр - координата x
            cell = raw[y_point_arr[i]:y_point_arr[i + 1], x_point_arr[j]:x_point_arr[j + 1]]
            # print(y_point_arr[i]:y_point_arr[i + 1], x_point_arr[j]:x_point_arr[j + 1])
            cv2.rectangle(raw, (x_point_arr[j], y_point_arr[i]), (x_point_arr[j+1],y_point_arr[i+1]), (255, 0, 0), 5, 8, 0)
            # cv2.imshow("sub_pic" + str(i) + str(j), cell)

                     # Прочтите текст, это английский по умолчанию
            # pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract.exe'
            text1 = pytesseract.image_to_string(cell, lang="ukr")

                     # Удалить специальные символы
            # text1 = re.findall(r'[^\*"/:?\\|<>″′‖ 〈\n]', text1, re.S)
            text1 = "".join(text1)
            data_fr_pd[i].append(text1)
            # print(f'Информация об изображении ячейки x: {j} y: {i} :' + text1)
            data[i].append(text1)
            j = j + 1
        i = i + 1
    # cv2.imshow("test",raw)
    # cv2.waitKey(0)
    df = pd.DataFrame(data_fr_pd)
    df.to_excel(f"{path.split('.')[0]}.xlsx")
    print(df)
    return data, raw, x_point_arr, y_point_arr


def write_to_excel(data):
    wb = load_workbook('./test.xlsx')
    sheet = wb.get_sheet_by_name(wb.get_sheet_names()[0])


def write_csv(path, data):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for index, item in enumerate(data):
            print(item)
            if index != 0 and index != len(data) - 1:
                try:
                    writer.writerows([[item[0], item[1], item[2], item[3], item[4], item[5]]])
                except:
                    pass


def save(path, data):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for index, item in enumerate(data):
            writer.writerows([item])


def test():
    with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})


if __name__ == '__main__':
    cv_image = cv2.imread('./img.png')
    data = parse_pic_to_excel_data(cv_image)
    # write_to_excel(1)
