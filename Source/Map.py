from Constant import *
from HeuristicLocalSearch import *
import random

def input_raw(map_input_path):
    try:
        f = open(map_input_path, "r")
    except:
        print("Can not read file \'" + map_input_path + "\'. Please check again!")
        return None

    pacman_pos = [int(y) for y in next(f).split()]
    raw_map = [[int(num) for num in line if num != '\n'] for line in f]

    return (pacman_pos[0], pacman_pos[1]), raw_map

def update_graph_map(graph_map, raw_map, x, y):
    cur = (x, y)
    graph_map[cur] = []
    # update posittion of possible direction from (y,x) 
    if y + 1 >= 0 and raw_map[x][y - 1] != 1: 
        left = (x, y - 1)
        graph_map[left].append(cur)
        graph_map[cur].append(left)
    if x - 1 >= 0 and raw_map[x - 1][y] != 1:
        up = (x -1, y)
        graph_map[up].append(cur)
        graph_map[cur].append(up)

def read_map_level_1(map_input_path):
    pacman_pos, raw_map = input_raw(map_input_path)
    food_pos = None
    graph_map = {}

    for x in range(len(raw_map)):
        for y in range(len(raw_map[x])):
            if raw_map[x][y] != 1:
                if raw_map[x][y] == 2:
                    food_pos = (x, y)

                update_graph_map(graph_map, raw_map, x, y)
                
    return graph_map, pacman_pos, food_pos

def read_map_level_2(map_input_path, ghost_as_wall: bool):
    pacman_pos, raw_map = input_raw(map_input_path)
    food_pos = None
    ghost_pos_list = []
    graph_map = {}

    for x in range(len(raw_map)):
        for y in range(len(raw_map[x])):
            if raw_map[x][y] != 1:
                if raw_map[x][y] == 2:
                    food_pos = (x, y)
                elif raw_map[x][y] == 3:
                    ghost_pos_list.append((x, y))
                    if ghost_as_wall:
                        raw_map[x][y] = 1

                update_graph_map(graph_map, raw_map, x, y)              
                
    return graph_map, pacman_pos, food_pos, ghost_pos_list

def init_cells(raw_map, pacman_pos):
    cells = []
    for x in range(len(raw_map)):
        row = []
        for y in range(len(raw_map[x])):
            if raw_map[x][y] != 1:
                if raw_map[x][y] == 0:
                    row.append(Cell((x, y), []))
                else:
                    row.append(Cell((x, y), [CState(raw_map[x][y])]))
                if pacman_pos == (x, y):
                    row[y].state.append(CState(4))
                    pacman_cell = row[y]
            else:
                row.append(None)
        cells.append(row)

    return cells, pacman_cell

def update_graph_cell(graph_cell, raw_map, cells, x, y):
    cur = cells[x][y]    
    graph_cell[cur] = []
    if y - 1 >= 0 and raw_map[x][y - 1] != 1:
        up = cells[x][y - 1]
        graph_cell[up].append(cur)
        graph_cell[cur].append(up)
    if x - 1 >= 0 and raw_map[x - 1][y] != 1:
        left = cells[x - 1][y]
        graph_cell[left].append(cur)
        graph_cell[cur].append(left)

def read_map_level_3(map_input_path):
    pacman_pos, raw_map = input_raw(map_input_path)
    cells, pacman_cell = init_cells(raw_map, pacman_pos)
    food_cell_list = []
    ghost_cell_list = []
    graph_map = {}

    for x in range(len(raw_map)):
        for y in range(len(raw_map[x])):
            if raw_map[x][y] != 1:
                cur = cells[x][y]

                if CState.GHOST in cur.state:
                    ghost_cell_list.append(cur)
                elif CState.FOOD in cur.state:
                    food_cell_list.append(cur)

                update_graph_cell(graph_map, raw_map, cells, x, y)
    
    return cells, graph_map, pacman_cell, food_cell_list, ghost_cell_list

def read_map_level_4(map_input_path):
    pacman_pos, raw_map = input_raw(map_input_path)
    cells, pacman_cell = init_cells(raw_map, pacman_pos)
    food_cell_list = []
    ghost_cell_list = []
    graph_cell = {}
    graph_map = {}

    for x in range(len(raw_map)):
        for y in range(len(raw_map[x])):
            if raw_map[x][y] != 1:
                cur = cells[x][y]

                if CState.GHOST in cur.state:
                    ghost_cell_list.append(cur)
                elif CState.FOOD in cur.state:
                    food_cell_list.append(cur)

                update_graph_map(graph_map, raw_map, x, y)
                update_graph_cell(graph_cell, raw_map, cells, x, y)

    return cells, graph_cell, pacman_cell, graph_map, food_cell_list, ghost_cell_list
