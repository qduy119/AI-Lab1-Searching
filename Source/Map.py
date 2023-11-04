from Constant import *
from HeuristicLocalSearch import *
import random

def input_raw(map_input_path):
    try:
        file = open(map_input_path, "r")
    except:
        print("Can not read file \'" + map_input_path + "\'. Please check again!")
        return None

    map_size = [int(num) for num in file.readline().split()]
    raw_map = [[int(num) for num in file.readline().strip()] for _ in range(map_size[0])]
    pacman_pos = [int(num) for num in file.readline().split()]

    return (map_size[0], map_size[1]), raw_map, (pacman_pos[0], pacman_pos[1])


def read_map_level_1(map_input_path):
    map_size, raw_map, pacman_pos = input_raw(map_input_path)
    food_pos = None

    graph_map = {}
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if raw_map[i][j] != 1:
                if raw_map[i][j] == 2:
                    food_pos = (j, i)

                cur = (j, i)
                graph_map[cur] = []

                if j - 1 >= 0 and raw_map[i][j - 1] != 1:
                    left = (j - 1, i)
                    graph_map[left] = graph_map[left] + [cur]
                    graph_map[cur] = graph_map[cur] + [left]

                if i - 1 >= 0 and raw_map[i - 1][j] != 1:
                    up = (j, i - 1)
                    graph_map[up] = graph_map[up] + [cur]
                    graph_map[cur] = graph_map[cur] + [up]
    
    return graph_map, pacman_pos, food_pos


def read_map_level_2(map_input_path, ghost_as_wall: bool):
    map_size, raw_map, pacman_pos = input_raw(map_input_path)
    food_pos = None
    ghost_pos_list = []

    graph_map = {}
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if raw_map[i][j] != 1:
                if raw_map[i][j] == 2:
                    food_pos = (j, i)
                elif raw_map[i][j] == 3:
                    ghost_pos_list.append((j, i))
                    if ghost_as_wall:
                        raw_map[i][j] = 1

                cur = (j, i)
                graph_map[cur] = []

                if j - 1 >= 0 and raw_map[i][j - 1] != 1:
                    left = (j - 1, i)
                    graph_map[left] = graph_map[left] + [cur]
                    graph_map[cur] = graph_map[cur] + [left]

                if i - 1 >= 0 and raw_map[i - 1][j] != 1:
                    up = (j, i - 1)
                    graph_map[up] = graph_map[up] + [cur]
                    graph_map[cur] = graph_map[cur] + [up]

    return graph_map, pacman_pos, food_pos, ghost_pos_list

def init_cells(map_size, raw_map, pacman_pos):
    cells = []

    for i in range(map_size[0]):
        row = []
        for j in range(map_size[1]):
            if raw_map[i][j] != 1:
                if raw_map[i][j] == 0:
                    row.append(Cell((j, i), []))
                else:
                    row.append(Cell((j, i), [CState(raw_map[i][j])]))

                if pacman_pos == (j, i):
                    row[j].state.append(CState(4))
                    pacman_cell = row[j]
            else:
                row.append(None)
        cells.append(row)

    return cells, pacman_cell

def read_map_level_3(map_input_path):
    map_size, raw_map, pacman_pos = input_raw(map_input_path)

    cells, pacman_cell = init_cells(map_size, raw_map, pacman_pos)

    food_cell_list = []
    ghost_cell_list = []
    graph_map = {}

    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if raw_map[i][j] != 1:
                cur = cells[i][j]

                if CState.GHOST in cur.state:
                    ghost_cell_list.append(cur)
                elif CState.FOOD in cur.state:
                    food_cell_list.append(cur)

                graph_map[cur] = []

                if j - 1 >= 0 and raw_map[i][j - 1] != 1:
                    left = cells[i][j - 1]
                    graph_map[left] = graph_map[left] + [cur]
                    graph_map[cur] = graph_map[cur] + [left]

                if i - 1 >= 0 and raw_map[i - 1][j] != 1:
                    up = cells[i - 1][j]
                    graph_map[up] = graph_map[up] + [cur]
                    graph_map[cur] = graph_map[cur] + [up]

    return cells, graph_map, pacman_cell, food_cell_list, ghost_cell_list


def read_map_level_4(map_input_path):
    map_size, raw_map, pacman_pos = input_raw(map_input_path)

    cells, pacman_cell = init_cells(map_size, raw_map, pacman_pos)

    food_cell_list = []
    ghost_cell_list = []
    graph_cell = {}
    graph_map = {}

    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if raw_map[i][j] != 1:
                c_cur = cells[i][j]
                cur = (j, i)

                if CState.GHOST in c_cur.state:
                    ghost_cell_list.append(c_cur)
                elif CState.FOOD in c_cur.state:
                    food_cell_list.append(c_cur)

                graph_cell[c_cur] = []
                graph_map[cur] = []

                if j - 1 >= 0 and raw_map[i][j - 1] != 1:
                    c_left = cells[i][j - 1]
                    graph_cell[c_left] = graph_cell[c_left] + [c_cur]
                    graph_cell[c_cur] = graph_cell[c_cur] + [c_left]

                    left = (j - 1, i)
                    graph_map[left] = graph_map[left] + [cur]
                    graph_map[cur] = graph_map[cur] + [left]

                if i - 1 >= 0 and raw_map[i - 1][j] != 1:
                    c_up = cells[i - 1][j]
                    graph_cell[c_up] = graph_cell[c_up] + [c_cur]
                    graph_cell[c_cur] = graph_cell[c_cur] + [c_up]

                    up = (j, i - 1)
                    graph_map[up] = graph_map[up] + [cur]
                    graph_map[cur] = graph_map[cur] + [up]

    return cells, graph_cell, pacman_cell, graph_map, food_cell_list, ghost_cell_list
