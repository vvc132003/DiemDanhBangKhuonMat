import numpy as np

# Tạo mảng hai chiều 4x6
array_2d = np.array([[1, 2, 3, 4, 5, 6],
                    [7, 8, 9, 10, 11, 12],
                    [13, 14, 15, 16, 17, 18],
                    [19, 20, 21, 22, 23, 24]])

# Truy xuất phần tử nằm ở dòng thứ 3 và cột thứ 2
element_3_2 = array_2d[2, 1]
print("Truy xuất phần tử nằm ở dòng thứ 3 và cột thứ 2:", element_3_2)

# Truy xuất dòng thứ 3
row_3 = array_2d[2, :]
print("Truy xuất dòng thứ 3:", row_3)

# Truy xuất các dòng 1,2,3,4
rows_1_to_4 = array_2d[0:4, :]
print("Truy xuất các dòng 1,2,3,4:", rows_1_to_4)

# Truy xuất các dòng 1,3,5
rows_1_3_5 = array_2d[::2, :]
print("Truy xuất các dòng 1,3,5:", rows_1_3_5)

# Truy xuất cột 3
column_3 = array_2d[:, 2]
print("Truy xuất cột 3:", column_3)

# Truy xuất cột 2,3,4
columns_2_to_4 = array_2d[:, 1:4]
print("Truy xuất cột 2,3,4:", columns_2_to_4)

# Truy xuất các cột 1,3,4
columns_1_3_4 = array_2d[:, [0, 2, 3]]
print("Truy xuất các cột 1,3,4:", columns_1_3_4)

# Truy xuất các phần tử là số chẵn
even_elements = array_2d[array_2d % 2 == 0]
print("Truy xuất các phần tử là số chẵn:", even_elements)

# Truy xuất các phần tử là số lẻ
odd_elements = array_2d[array_2d % 2 != 0]
print("Truy xuất các phần tử là số lẻ:", odd_elements)

# Truy xuất các phần tử có giá trị lớn hơn hoặc bằng 4
elements_greater_than_4 = array_2d[array_2d >= 4]
print("Truy xuất các phần tử có giá trị lớn hơn hoặc bằng 4:", elements_greater_than_4)

# Truy xuất các phần tử lớn hơn hoặc bằng 4 và là số chẵn
even_elements_greater_than_4 = array_2d[(array_2d >= 4) & (array_2d % 2 == 0)]
print("Truy xuất các phần tử lớn hơn hoặc bằng 4 và là số chẵn:", even_elements_greater_than_4)