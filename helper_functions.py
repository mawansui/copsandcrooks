from random import randint, sample, shuffle
from itertools import product
import numpy as np

# ДОГОВАРИВАЕМСЯ О ТОМ, КАК ПИСАТЬ КООРДИНАТЫ
# ОТХОДИМ ОТ СТАНДАРТНЫХ x, y
# ПЕРВОЕ ЧИСЛО – ЭТО СТРОКА В PLAYFIELD
# ВТОРОЕ ЧИСЛО – ЭТО СТОЛБЕЦ В PLAYFIELD

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

# TODO: как-нибудь поумнее генерировать координаты домов в функции generate_house_coordinates

def generate_n_tiles(n, occupied):
	random_line = randint(0, 9)
	random_column = randint(0, 9)
	start_coords = [random_line, random_column]

	# Если координата первого сгенерированного тайла не занята,
	if start_coords not in occupied:
		# проверить, вправо от этого тайла делать или влево
		if start_coords[1] + n <= 9:
			# Заготовить нужное количество ячеек
			list_of_coordinates = [[]]*(n-1)
			for i in range((n-1)):
				list_of_coordinates[i] = [random_line, random_column + (i+1)]
			# Надо проверить, нет ли среди новых сгенеренных координат уэе занятых
			for c in list_of_coordinates:
				if c in occupied:
					return generate_n_tiles(n, occupied)
			list_of_coordinates.insert(0, start_coords)
			return list_of_coordinates
		else:
			# Заготовить нужное количество ячеек
			list_of_coordinates = [[]]*(n-1)
			substract_term = 1
			for i in range((n-1)):
				list_of_coordinates[i] = [random_line, random_column + (i-substract_term)]
				substract_term += 2
			# Надо проверить, нет ли среди новых сгенеренных координат уэе занятых
			for c in list_of_coordinates:
				if c in occupied:
					return generate_n_tiles(n, occupied)
			list_of_coordinates.insert(0, start_coords)
			return list_of_coordinates
	# А если занята, то заново сгененировать первый тайл и начать от него строить
	else:
		return generate_n_tiles(n, occupied)


# print(generate_n_tiles(1, [[0, 5], [9, 0], [9, 9]]))

def get_occupied_coords(currently_occupied, new_house_coords):
	"""
	Принимает список списков занятых на настоящий момент координат
	Возвращает дополненный список занятых коодинат
	"""
	for coords in new_house_coords:
		current_y = [coords[0]-1, coords[0], coords[0] + 1]
		current_x = [coords[1]-1, coords[1], coords[1] + 1]
		occupied_for_one_tile = list(product(current_y, current_x))
		for c_set in occupied_for_one_tile:
			if list(c_set) not in currently_occupied:
				currently_occupied.append(list(c_set))
	return currently_occupied

def get_lucky_coins_coords(unoccupied):
	"""
	Принимает список свободных координат
	Возвращает случайные координаты монеток
	"""
	random_coordinate_indices = sample(range(len(unoccupied)), 8)
	shuffle(random_coordinate_indices)
	return [unoccupied[i] for i in random_coordinate_indices]

def generate_house_coordinates(playfield):
	"""
	Принимает: np-массив игрового поля
	Возвращает: np-массив с расставленными домами
	"""
	# Что должно происходить:
	# 1. Поставить дом из 4-х тайлов, пока всё поле свободно
	# 	 - Мб этот дом вообще не нужен?
	# 2. Добавить в список недоступных координат все координаты всех 
	#  	 4 тайлов ± 1 по иксу и игреку
	# 3. Горизонтально ставить остальные дома, проверяя координаты
	# 
	# Либо можно пойти наоборот!
	# Сначала сгенерить только маленькие дома, потом сделать список всех 
	# доступных координат и по ним расставлять 2-е дома, потом 3-е и если 
	# останется место – 4ой.

	preoccupied_coordinates = [[0, 5], [9, 0], [9, 9]]

	tiles_4_hc = generate_n_tiles(4, preoccupied_coordinates)
	# print(f"tiles_4_hc: {tiles_4_hc}")
	for coords_set in tiles_4_hc:
		playfield[coords_set[0]][coords_set[1]] = 4

	occupied_coords = get_occupied_coords(preoccupied_coordinates, tiles_4_hc)

	tiles_3_hc_1 = generate_n_tiles(3, occupied_coords)
	# print(f"tiles_3_hc_1: {tiles_3_hc_1}")
	for coords_set in tiles_3_hc_1:
		playfield[coords_set[0]][coords_set[1]] = 4

	occupied_coords = get_occupied_coords(occupied_coords, tiles_3_hc_1)

	tiles_3_hc_2 = generate_n_tiles(3, occupied_coords)
	# print(f"tiles_3_hc_2: {tiles_3_hc_2}")
	for coords_set in tiles_3_hc_2:
		playfield[coords_set[0]][coords_set[1]] = 4

	occupied_coords = get_occupied_coords(occupied_coords, tiles_3_hc_2)

	for m in range(3):
		tiles_2_hc = generate_n_tiles(2, occupied_coords)
		# print(f"tiles_2_hc: {tiles_2_hc}")
		for coords_set in tiles_2_hc:
			playfield[coords_set[0]][coords_set[1]] = 4
		occupied_coords = get_occupied_coords(occupied_coords, tiles_2_hc)

	for m in range(4):
		tiles_1_hc = generate_n_tiles(1, occupied_coords)
		# print(f"tiles_1_hc: {tiles_1_hc}")
		playfield[tiles_1_hc[0][0]][tiles_1_hc[0][1]] = 4
		occupied_coords = get_occupied_coords(occupied_coords, tiles_1_hc)
	
	# print(playfield)

	inds = np.where(playfield == 0)
	print("\n")
	unoccupied_coordinates = []
	for one, two in zip(inds[0], inds[1]):
		unoccupied_coordinates.append([one, two])

	lucky_coins_coordinates = get_lucky_coins_coords(unoccupied_coordinates)
	for coin_coords in lucky_coins_coordinates:
		playfield[coin_coords[0]][coin_coords[1]] = 5

	return playfield, occupied_coords, lucky_coins_coordinates

# Сколько монет удачи есть у бандитов и копов (по нулям в начале игры)
crooks_coins = 0
cops_coins = 0

# Сколько блоков есть у бандитов и копов в начале игры
crooks_blocks = 1
cops_blocks = 3

def render_playfield(playfield):
	"""
	Принимает игровое поле в виде массива np-массивов
	Делает из них строки
	Заменяет цифры на эмодзи
	Выводит игровое поле в красивом виде
	"""
	# 0 – свободная клетка
	# 1 – выход
	# 2 – игрок 1 (убегающий)
	# 3 – игрок 2 (догоняющий)
	# 4 – один тайл здания
	# 5 – монета удачи
	# 6 – блок догоняющего
	# 7 – блок убегающего
	# 8 - путь игрока 1
	# 9 – путь игрока 2

	playfield = playfield.astype(str)
	playfield[playfield == "0"] = "_"
	playfield[playfield == "1"] = "🚁"
	playfield[playfield == "2"] = "🚘"
	playfield[playfield == "3"] = "🚔"
	playfield[playfield == "4"] = "🏠"
	playfield[playfield == "5"] = "✨"
	playfield[playfield == "6"] = "🚧"
	playfield[playfield == "7"] = "💣"
	playfield[playfield == "8"] = "♦️"
	playfield[playfield == "9"] = "🔹"

	string = ""
	for i in range(10):
		string += f" {i} |"
	print("  |"+ string + f"\tCops lucky coins: {cops_coins}, cops blocks: {cops_blocks}")
	print("  " + "_"*40 + f"\tCrooks lucky coins: {crooks_coins}, crooks_blocks: {crooks_blocks}")
	for index, row in enumerate(playfield.astype(str)):
		final = ""
		for item in row:
			if item == "_":
				final += f"_{item}_|"
			else:	
				final += f"_{item} |"
		print(f"{index} |" + final)
		# row_string = " | ".join(row)
		# print("| " + row_string + " |")
		# print("| " + "_"*len(row_string) + " |")

def cops_move(playfield, occupied, lucky):
	"""
	Принимает все координаты
	Обрабатывает ввод игрока
	Либо выдает ошибку с объяснением
	Либо делает то, что сказано, обновляя playfield 
	Возвращает новый playfield
	"""

	global cops_coins
	
	cops_raw_input = input("> ")
	cops_input = cops_raw_input.split()

	if len(cops_input) != 3:
		print("Координаты введены неправильно, проверьте правильность ввода.")
		return cops_move(playfield, occupied, lucky)

	# если игрок решил передвинуться
	if cops_input[0] == "move":
		# надо узнать, где игрок находится сейчас
		# первое вроде y, второе – x

		available_to_move = np.where(playfield == 0)

		available_to_move = [[row, col] for row, col in zip(available_to_move[0], available_to_move[1])]


		current_cops_coords = np.where(playfield == 3)
		cops_row = current_cops_coords[0][0]
		cops_column = current_cops_coords[1][0]

		# и куда он вообще в принципе может передвинуться
		# либо row ± 1, либо column ± 1
		cops_possible_coords = [[cops_row, cops_column-1], 
							   [cops_row, cops_column+1],
							   [cops_row-1, cops_column],
							   [cops_row+1, cops_column]]

		# URGENT TODO: нужна проверка на здания и монетки!
		# UPD: проверка на здания работает, а проверка на монетки не дает сходить наступив на монетку
		cops_move_allowed_coords = [i for i in cops_possible_coords if all(n in range(0, 10) for n in i) and i in available_to_move]
		print(cops_move_allowed_coords)
		# print(occupied)
		cops_move_allowed_coords = list(filter(lambda x: x in available_to_move, cops_move_allowed_coords))
		# добавляем координаты монеток удачи как разрешенные, потому что на них нужно ходить
		cops_move_allowed_coords.extend(lucky)
		print(cops_move_allowed_coords)
		
		# смотрим, что захотел игрок
		cops_input_row = int(cops_input[1])
		cops_input_column = int(cops_input[2])

		if [cops_input_row, cops_input_column] in cops_move_allowed_coords:
			# надо проверить, совпадает ли координата хода с координатой монетки удачи
			# если совпадает, надо добвить копам одну монетку
			if [cops_input_row, cops_input_column] in lucky:
				cops_coins += 1
				playfield[cops_row][cops_column] = 9
				occupied.append([cops_row, cops_column])
				playfield[cops_input_row][cops_input_column] = 3
				lucky.remove([cops_input_row, cops_input_column])
				return playfield, occupied, lucky
			else:
				playfield[cops_row][cops_column] = 9
				occupied.append([cops_row, cops_column])
				playfield[cops_input_row][cops_input_column] = 3
				return playfield, occupied, lucky
		else:
			print("Эти координаты недоступны для перемещения. Пожалуйста, уточните ввод")
			return cops_move(playfield, occupied, lucky)

		# если его координаты находятся в списке допустимых, то всё ок, 
		# передвинуть фигурку туда, а на прошлую координату 

		# а потом 
	# если игрок решил поставить блок
	elif cops_input[0] == "block":
		pass
	# если игрок ввел неправильную команду
	else:
		print("Команда не распознана, повторите, пожалуйста.")
		return cops_move(playfield, occupied, lucky)

























