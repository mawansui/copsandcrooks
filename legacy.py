def generate_four(occupied):
	"""
	Генерирует одну случайную координату, а от неё строит остальные 3 
	(влево или вправо).
	"""
	random_x = randint(0, 9)
	random_y = randint(0, 9)
	start_coords = [random_x, random_y]

	# Если сгенерировались не занятые координаты
	if start_coords not in occupied:
		# и на три вправо по иксу можно ставить (не будет достигнут конец игрового поля)
		if start_coords[0] + 3 <= 9:
			add_coords_1 = [random_x+1, random_y]
			add_coords_2 = [random_x+2, random_y]
			add_coords_3 = [random_x+3, random_y]
			if add_coords_1 not in occupied and add_coords_2 not in occupied and add_coords_3 not in occupied:
				return [start_coords, add_coords_1, add_coords_2, add_coords_3]
			else:
				return generate_four(occupied)
		# на три вправо нельзя, значит пойдем ставить на три влево
		else:
			sub_coords_1 = [random_x-1, random_y]
			sub_coords_2 = [random_x-2, random_y]
			sub_coords_3 = [random_x-3, random_y]
			if sub_coords_1 not in occupied and sub_coords_2 not in occupied and sub_coords_3 not in occupied:
				return [start_coords, sub_coords_1, sub_coords_2, sub_coords_3]
			else:
				return generate_four(occupied)
	else:
		# надо как-то заново сгенерить координаты
		return generate_four(occupied)


# print(generate_four(occupied = [[0, 5], [9, 0], [9, 9]]))
# example output: [[5, 9], [6, 9], [7, 9], [8, 9]]

def generate_three(occupied):
	"""
	Принимает список занятых координат
	Возвращает координаты двух домов из трёх тайлов
	"""
	random_x = randint(0, 9)
	random_y = randint(0, 9)
	start_coords = [random_x, random_y]

	if start_coords not in occupied:
		if start_coords[0] + 2 <= 9:
			add_coords_1 = [random_x + 1, random_y]
			add_coords_2 = [random_x + 2, random_y]
			if add_coords_1 not in occupied and add_coords_2 not in occupied:
				return [start_coords, add_coords_1, add_coords_2]
			else:
				return generate_three(occupied)
		else:
			sub_coords_1 = [random_x - 1, random_y]
			sub_coords_2 = [random_x - 2, random_y]
			if sub_coords_1 not in occupied and sub_coords_2 not in occupied:
				return [start_coords, sub_coords_1, sub_coords_2]
			else:
				return generate_three(occupied)
	else:
		return generate_three(occupied)

# print(generate_three([[0, 5], [9, 0], [9, 9], [4, 8], [4, 9], [4, 10], [5, 8], [5, 9], [5, 10], [6, 8], [6, 9], [6, 10], [7, 8], [7, 9], [7, 10], [8, 8], [8, 9], [8, 10], [9, 8], [9, 10]]))
# example output: [[5, 3], [6, 3], [7, 3]]