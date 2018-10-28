# Это для того, чтобы создать нулевую матрицу и заполнять её координатами
import numpy as np

# Эта функция будет расставлять дома по игровому полю
from helper_functions import generate_house_coordinates, render_playfield, cops_move

# Задачи:
# 1. (+) Создать игровое поле
# 2. (+) Заполнить стационарными первыми координатами (игроки + выход)
# 3. (+) Сделать функцию, которая выдаст рандомные координаты всех домов
# 4. (+) Расставить координаты домов
# 5. (+) Сделать функцию, которая выдаст рандомные координаты монет удачи
# 6. (+) Расставить координаты монет
# 7. Сделать игровой цикл, который будет учитывать, чей сейчас ход, что может 
#    сделать игрок (поставить блок или сходить), сколько у кого монет, 
#	 куда он может сходить, и ждать от него ввода команды/координат хода.

# Шаг 0. Условные обозначения:
# 1 – выход
# 2 – игрок 1 (убегающий)
# 3 – игрок 2 (догоняющий)
# 4 – один тайл здания
# 5 – монета удачи
# 6 – блок догоняющего
# 7 – блок убегающего
# 8 - путь игрока 1
# 9 – путь игрока 2

# Шаг 1. Создаём игровое поле. Это матрица целых чисел (в данный момент) – нулей
play_field = np.zeros((10, 10)).astype(int)

"""
	0| 1| 2| 3| 4| 5| 6| 7| 8| 9|
0 |__|__|__|__|__|__|__|__|__|__|
1 |__|__|__|__|__|__|__|__|__|__|
2 |__|__|__|__|__|__|__|__|__|__|
3 |__|__|__|__|__|__|__|__|__|__|
4 |__|__|__|__|__|__|__|__|__|__|
5 |__|__|__|__|__|__|__|__|__|__|
6 |__|__|__|__|__|__|__|__|__|__|
7 |__|__|__|__|__|__|__|__|__|__|
8 |__|__|__|__|__|__|__|__|__|__|
9 |__|__|__|__|__|__|__|__|__|__|
"""

# [[4, 4], [5, 4], [6, 4], [7, 4]]
# [4, 4] => [[3, 4, 5], [3, 4, 5]] => [[3,3], [3,4], [3,5], [4,3], [4,4], [4,5], [5,3], [5,4], [5,5]]

# Шаг 2. Расставляем стационарные координаты
# Выхода
play_field[0][5] = 1
# Игрока 1
play_field[9][0] = 2
# Игрока 2
play_field[9][9] = 3

# Шаг 3. Генерируем координаты домов и монет удачи (игровое поле короче)
playfield, occupied_coords, lucky_coins_coordinates = generate_house_coordinates(play_field)

# Шаг 4. Основной цикл игры

# Обозначения: 2 – убегающий, 3 – догоняющий (чтобы не путаться)
# По умолчанию игру начинает догоняющий
turn = 3

preturn_playfield = playfield

while True:
	# Отрендерить то, что есть сейчас
	render_playfield(preturn_playfield)
	print("\n\n")
	if turn == 3:
		preturn_playfield = cops_move(playfield, occupied_coords, lucky_coins_coordinates)
		turn -= 1
		continue
	else:
		print("Ход грабителей!")
		print("Доступные команды:\n- move y x : передвинуться на координату "
			  "(x,y)\n- block y x : поставить блок на координату (x,y)")
		crooks_move = input("> ")
		print(crooks_move)
		turn += 1
		continue
	break