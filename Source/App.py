import sys
import pygame.freetype
import random
import Pacman
import Food
import Ghost
import Map
import GraphSearch
import HeuristicLocalSearch 
from Constant import *


class App:
    ################################################## CORE FUNCTIONS ##################################################
    def __init__(self):
        pygame.init()

        self.font = pygame.freetype.SysFont(FONT, 20, True)
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        self.caption = pygame.display.set_caption(APP_CAPTION)

        self.current_map_index = 0
        self.current_level = 1
        self.score = 0
        self.cur_speed_index = 1
        self.speed_list = [("SPEED: 0.5", 0.5), ("SPEED: 1.0", 1), ("SPEED: 2.0", 2), ("SPEED: 5.0", 5), ("SPEED: 10.0", 10)]

        self.map = pygame.image.load(MAP_IMG[self.current_map_index])
        self.map = pygame.transform.scale(self.map, (MAP_WIDTH, MAP_HEIGHT))
        self.home_background = pygame.image.load(HOME_BACKGROUND)
        self.home_background = pygame.transform.scale(self.home_background, (HOME_BG_WIDTH, HOME_BG_HEIGHT))
        self.about_background = pygame.image.load(ABOUT_BACKGROUND)
        self.about_background = pygame.transform.scale(self.about_background, (APP_WIDTH, APP_HEIGHT))
        self.level_background = self.home_background
        self.gameover_background = pygame.image.load(GAMEOVER_BACKGROUND)
        self.gameover_background = pygame.transform.scale(self.gameover_background,
                                                          (GAMEOVER_BACKGROUND_WIDTH, GAMEOVER_BACKGROUND_HEIGHT))
        self.coin = pygame.image.load(COIN_IMAGE)
        self.coin = pygame.transform.scale(self.coin, (COIN_WIDTH, COIN_HEIGHT))
        self.victory_background = pygame.image.load(VICTORY_BACKGROUND)
        self.victory_background = pygame.transform.scale(self.victory_background, (VICTORY_WIDTH, VICTORY_HEIGHT))
        self.pacmans = []
        self.pacmans.append(pygame.image.load(PACMAN1))
        self.pacmans[0] = pygame.transform.scale(self.pacmans[0], (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacmans.append(pygame.image.load(PACMAN2))
        self.pacmans[1] = pygame.transform.scale(self.pacmans[1], (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacmans.append(pygame.image.load(PACMAN3))
        self.pacmans[2] = pygame.transform.scale(self.pacmans[2], (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacmans.append(pygame.image.load(PACMAN4))
        self.pacmans[3] = pygame.transform.scale(self.pacmans[3], (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacmans.append(pygame.image.load(PACMAN5))
        self.pacmans[4] = pygame.transform.scale(self.pacmans[4], (PACMAN_WIDTH, PACMAN_HEIGHT))

        self.state = STATE_HOME
        self.clock = pygame.time.Clock()
        self.mouse = None

    def launch_pacman_game(self):
        """
        Launch the Pacman game with the corresponding level and map.
        """
        self.launch_game_draw()

        if self.current_level == 1:
            self.level_1()
        elif self.current_level == 2:
            self.level_2()
        elif self.current_level == 3:
            self.level_3()
        elif self.current_level == 4:
            self.level_4()

    def level_1(self):
        """
        Level 1: Pac-man know the food’s position in map and ghosts do not appear in map.
        There is only one food in the map.
        """
        graph_map, pacman_pos, food_pos = Map.read_map_level_1(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])
        path = GraphSearch.search_dijkstra_algorithm(graph_map, pacman_pos, food_pos)

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        food = Food.Food(self, food_pos)
        food.appear()

        if self.ready():
            if path is not None:
                back_home = False
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    pacman.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    pacman.move(goal)
                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_VICTORY
                    pygame.time.delay(2000)
            else:
                self.state = STATE_GAMEOVER
                pygame.time.delay(2000)

    def level_2(self):
        """
        Level 2: ghosts stand in the place ever (never move around).
        If Pac-man pass through the ghost or vice versa, game is over.
        There is still one food in the map and Pac-man know its position.
        """
        graph_map, pacman_pos, food_pos, ghost_pos_list = \
            Map.read_map_level_2(MAP_INPUT_TXT[self.current_level - 1][self.current_map_index], ghost_as_wall=True)

        path = GraphSearch.search_dijkstra_algorithm(graph_map, pacman_pos, food_pos)

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        food = Food.Food(self, food_pos)
        food.appear()

        ghost_list = [Ghost.Ghost(self, ghost_pos) for ghost_pos in ghost_pos_list]
        for ghost in ghost_list:
            ghost.appear()

        if self.ready():
            back_home = False
            if path is None:
                graph_map, pacman_pos, food_pos, ghost_pos_list = \
                    Map.read_map_level_2(MAP_INPUT_TXT[self.current_level - 1][self.current_map_index],
                                         ghost_as_wall=False)

                path = GraphSearch.search_dijkstra_algorithm(graph_map, pacman_pos, food_pos)

                if path is not None:
                    path = path[1:]

                    for cell in path:
                        pacman.move(cell)
                        self.update_score(SCORE_PENALTY)

                        if cell in ghost_pos_list:
                            break

                        pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                        if self.launch_game_event():
                            back_home = True
                            break

                if not back_home:
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    pacman.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    pacman.move(goal)
                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_VICTORY
                    pygame.time.delay(2000)

    def level_3(self):
        """
        Level 3: Pac-man cannot see the foods if they are outside Pacman’s nearest threestep.
        It means that Pac-man just only scan all the adjacent him (8 tiles x 3).
        There are many foods in the map.
        Monster just move one step in any valid direction (if any) around the initial location at the start of the game.
        Each step Pacman go, each step Monster move.
        """
        # Read map.
        cells, graph_map, pacman_cell, food_cell_list, ghost_cell_list = Map.read_map_level_3(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])

        # Initialize Pacman, Foods and Ghosts.
        food_list = [Food.Food(self, food_cell.pos, food_cell) for food_cell in food_cell_list]
        for food in food_list:
            food.appear()

        ghost_list = [Ghost.Ghost(self, ghost_cell.pos, ghost_cell) for ghost_cell in ghost_cell_list]
        for ghost in ghost_list:
            ghost.appear()

        pacman = Pacman.Pacman(self, pacman_cell.pos, pacman_cell)
        pacman.appear()

        # Game.
        if self.ready():
            back_home = False
            pacman_is_caught = False

            while True:
                is_backtracking = False
                pacman_old_cell = pacman.cell

                # Pacman observes all of Cells in its visitbility  then decide the direction to move.
                pacman.cell.pacman_leave()
                pacman.observe(graph_map, 3)

                if not pacman.empty_brain() and not pacman.have_food_in_cur_visible():
                    # Pacman tracks the peas which leads to one of Food that Pacman saw in the past.
                    pacman.cell = pacman.back_track(graph_map)
                    is_backtracking = True
                else:
                    # Pacman moves with heuristic.
                    pacman.cell = HeuristicLocalSearch.local_search(cells, graph_map, pacman.cell)

                pacman.cell.pacman_come()
                pacman.move(pacman.cell.pos)
                self.update_score(SCORE_PENALTY)

                # Spread the peas.
                if not is_backtracking:
                    pacman.spread_peas(pacman_old_cell)

                # Pacman went through Ghosts?
                for ghost in ghost_list:
                    if pacman.cell.pos == ghost.cell.pos:
                        self.state = STATE_GAMEOVER
                        pacman_is_caught = True
                        break
                if pacman_is_caught:
                    break

                # Pacman ate a Food?
                pre_food_list_len = len(food_list)
                for food in food_list:
                    if food.cell.pos == pacman.cell.pos:
                        food_list.remove(food)

                if pre_food_list_len != len(food_list):
                    self.update_score(SCORE_BONUS)

                    for i in range(len(pacman.food_cell_in_brain_list)):
                        if pacman.food_cell_in_brain_list[i] == pacman.cell:
                            pacman.food_cell_in_brain_list.remove(pacman.food_cell_in_brain_list[i])
                            pacman.path_to_food_cell_in_brain_list.remove(pacman.path_to_food_cell_in_brain_list[i])
                            break

                # Ghosts move around.
                for ghost in ghost_list:
                    ghost_old_cell = ghost.cell

                    ghost.cell.ghost_leave()

                    next_cell = ghost.initial_cell
                    if ghost.cell.pos == ghost.initial_cell.pos:
                        around_cell_list = ghost.get_around_cells_of_initial_cell(graph_map)
                        next_cell_index = random.randint(0, len(around_cell_list) - 1)
                        next_cell = around_cell_list[next_cell_index]
                    ghost.cell = next_cell

                    ghost.cell.ghost_come()

                    ghost.move(ghost.cell.pos)

                    if ghost_old_cell.exist_food():
                        temp_food = Food.Food(self, ghost_old_cell.pos, ghost_old_cell)
                        temp_food.appear()

                # Ghosts caught Pacman up?
                for ghost in ghost_list:
                    if pacman.cell.pos == ghost.cell.pos:
                        self.state = STATE_GAMEOVER
                        pacman_is_caught = True
                        break
                if pacman_is_caught:
                    break

                # Pacman ate all of Foods?
                if len(food_list) == 0:
                    self.state = STATE_VICTORY
                    break

                # Graphic: "while True" handling.
                pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))
                if self.launch_game_event():
                    back_home = True
                    break

            if not back_home:
                pygame.time.delay(2000)

    def level_4(self):
        """
        Level 4 (difficult): map is opened.
        Monster will seek and kill Pac-man.
        Pac-man want to get food as much as possible.
        Pacman will die if at least one ghost passes him.
        It is ok for ghosts go through each other.
        Each step Pacman go, each step Monster move.
        The food is so many.
        """
        # Read map.
        cells, graph_cell, pacman_cell, graph_map, food_cell_list, ghost_cell_list = Map.read_map_level_4(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])

        # Initialize Pacman, Foods and Ghosts.
        food_list = [Food.Food(self, food_cell.pos, food_cell) for food_cell in food_cell_list]
        for food in food_list:
            food.appear()

        ghost_list = [Ghost.Ghost(self, ghost_cell.pos, ghost_cell) for ghost_cell in ghost_cell_list]
        for ghost in ghost_list:
            ghost.appear()

        pacman = Pacman.Pacman(self, pacman_cell.pos, pacman_cell)
        pacman.appear()

        if self.ready():
            back_home = False
            pacman_is_caught = False

            while True:
                is_backtracking = False
                pacman_old_cell = pacman.cell

                # Pacman observes all of Cells in its visitbility then decide the direction to move.
                pacman.cell.pacman_leave()
                pacman.observe(graph_cell, 3)

                if not pacman.empty_brain() and not pacman.have_food_in_cur_visible() and not pacman.have_ghost_in_cur_visible():
                   # Pacman tracks the peas which leads to one of Food that Pacman saw in the past.
                    pacman.cell = pacman.back_track(graph_cell)
                    is_backtracking = True
                else:
                    #Pacman moves with heuristic.
                    pacman.cell = HeuristicLocalSearch.local_search(cells, graph_cell, pacman.cell)
                if pacman.cell == None:
                    self.state = STATE_GAMEOVER
                    break                
                # Pacman went through Ghosts?
                for ghost in ghost_list:
                    if pacman.cell.pos == ghost.cell.pos:
                        self.state = STATE_GAMEOVER
                        pacman_is_caught = True
                        break                
                if pacman_is_caught:
                    break      

                pacman.cell.pacman_come()
                pacman.move(pacman.cell.pos)
                self.update_score(SCORE_PENALTY)

                # Spread the peas.
                if not is_backtracking:
                    pacman.spread_peas(pacman_old_cell)

                # Pacman went through Ghost?
                for ghost in ghost_list:
                    if pacman.cell.pos == ghost.cell.pos:
                        self.state = STATE_GAMEOVER
                        pacman_is_caught = True
                        break
                if pacman_is_caught:
                    break

                # Pacman ate a Food?
                pre_food_list_len = len(food_list)
                for food in food_list:
                    if food.cell.pos == pacman.cell.pos:
                        food_list.remove(food)

                if pre_food_list_len != len(food_list):
                    self.update_score(SCORE_BONUS)

                # Ghosts try to seek and kill Pacman
                
                for ghost in ghost_list:
                    old_cell = ghost.cell
                    ghost.cell.ghost_leave()
                    dictance = []                
                    moves = graph_cell[ghost.cell]
                    for move in moves:
                        dictance.append(abs(move.pos[0]-pacman.cell.pos[0])+abs(move.pos[1]-pacman.cell.pos[1]))
                    
                    ghost.cell = moves[dictance.index(min(dictance))]
                    ghost.cell.ghost_come()
                    ghost.move(ghost.cell.pos)

                    if old_cell.exist_food():
                        temp_food = Food.Food(self, old_cell.pos, old_cell)
                        temp_food.appear()

                # Ghost caught Pacman up :( ?
                for ghost in ghost_list:
                    if pacman.cell.pos == ghost.cell.pos:
                        self.state = STATE_GAMEOVER
                        pacman_is_caught = True
                        break
                if pacman_is_caught:
                    break

                # Pacman ate all of Foods?
                if len(food_list) == 0:
                    self.state = STATE_VICTORY
                    break

                # Graphic: "while True" handling.
                pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))
                if self.launch_game_event():
                    back_home = True
                    break

            if not back_home:
                pygame.time.delay(2000)


    def run(self):
        """
        Run this program.
        """
        while True:
            if self.state == STATE_HOME:
                self.home_draw()
                self.home_event()
            elif self.state == STATE_PLAYING:
                self.play_draw()
                self.launch_pacman_game()
                self.play_event()
            elif self.state == STATE_ABOUT:
                self.about_draw()
                self.about_event()
            elif self.state == STATE_MAP:
                self.map_draw()
                self.map_event()
            elif self.state == STATE_LEVEL:
                self.level_draw()
                self.level_event()
            elif self.state == STATE_GAMEOVER:
                self.gameover_draw1()
                self.gameover_draw2()
                self.gameover_event()
            elif self.state == STATE_VICTORY:
                self.victory_draw()
            self.clock.tick(FPS)

    ####################################################################################################################

    def launch_game_draw(self):
        """
        Draw the initial Play Screen.
        """
        pygame.display.update()
        self.score = 0
        self.cur_speed_index = 1
        self.update_score(0)

        text_surf, text_rect = self.font.render("HOME", WHITE)
        self.screen.blit(text_surf, HOME_RECT)
        pygame.display.update(HOME_RECT)

        text_surf, text_rect = self.font.render(self.speed_list[self.cur_speed_index][0], WHITE)
        self.screen.blit(text_surf, SPEED_RECT)
        pygame.display.update(SPEED_RECT)

    def launch_game_event(self):
        """
        Get events while the Pacman is moving.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if HOME_RECT[0] <= self.mouse[0] <= HOME_RECT[0] + HOME_RECT[2] and \
                        HOME_RECT[1] <= self.mouse[1] <= HOME_RECT[1] + HOME_RECT[3]:
                    self.state = STATE_HOME
                    break
                if SPEED_RECT[0] <= self.mouse[0] <= SPEED_RECT[0] + SPEED_RECT[2] and \
                        SPEED_RECT[1] <= self.mouse[1] <= SPEED_RECT[1] + SPEED_RECT[3]:
                    self.cur_speed_index += 1
                    self.cur_speed_index %= len(self.speed_list)
                    break

        self.mouse = pygame.mouse.get_pos()
        if HOME_RECT[0] <= self.mouse[0] <= HOME_RECT[0] + HOME_RECT[2] and \
                HOME_RECT[1] <= self.mouse[1] <= HOME_RECT[1] + HOME_RECT[3]:
            text_surf, text_rect = self.font.render("HOME", WHITE)
            self.screen.blit(text_surf, HOME_RECT)
            pygame.display.update(HOME_RECT)
        else:
            text_surf, text_rect = self.font.render("HOME", WHITE)
            self.screen.blit(text_surf, HOME_RECT)
            pygame.display.update(HOME_RECT)
        if SPEED_RECT[0] <= self.mouse[0] <= SPEED_RECT[0] + SPEED_RECT[2] and \
                SPEED_RECT[1] <= self.mouse[1] <= SPEED_RECT[1] + SPEED_RECT[3]:
            pygame.draw.rect(self.screen, BLACK, SPEED_RECT)
            text_surf, text_rect = self.font.render(self.speed_list[self.cur_speed_index][0], WHITE)
            self.screen.blit(text_surf, SPEED_RECT)
            pygame.display.update(SPEED_RECT)
        else:
            pygame.draw.rect(self.screen, BLACK, SPEED_RECT)
            text_surf, text_rect = self.font.render(self.speed_list[self.cur_speed_index][0], WHITE)
            self.screen.blit(text_surf, SPEED_RECT)
            pygame.display.update(SPEED_RECT)

        if self.state == STATE_HOME:
            return True

        return False

    def ready(self):
        """
        Ready effect (3, 2, 1, GO).
        """
        text_list = ['3', '3', '3', '3', '2', '2', '2', '2', '1', '1', '1', '1', 'GO', 'GO', 'GO', 'GO']
        for text in text_list:
            text_surf, text_rect = self.font.render(text, WHITE)

            text_pos = (READY_POS[0] - len(text) * 5, READY_POS[1])
            text_rect[0] = text_pos[0]
            text_rect[1] = text_pos[1]

            self.screen.blit(text_surf, text_pos)
            pygame.display.update(text_rect)

            pygame.time.delay(250)
            pygame.display.update(pygame.draw.rect(self.screen, BLACK, text_rect))

            if self.launch_game_event():
                return False

        return True

    def victory_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.victory_background, (50, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, BLUE_LIGHT, WHITE, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        for i in range(5):
            self.screen.blit(self.pacmans[i], (50, 350))        
            pygame.time.delay(100)
            pygame.display.update()

    def gameover_draw1(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.gameover_background, (0, 0))
        self.screen.blit(self.coin, COIN_POS)
        pygame.time.delay(350)
        pygame.display.update()

    def gameover_draw2(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.gameover_background, (0, 0))
        pygame.time.delay(350)

    def gameover_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= self.mouse[0] <= 400 and 430 <= self.mouse[1] <= 630:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()

        pygame.display.update()

    def update_score(self, achived_score):
        """
        Add 'achived_score' to the current score and display onto the screen.
        """
        text_surf, text_rect = self.font.render("SCORES: " + str(self.score), WHITE)
        text_rect[0] = SCORE_POS[0]
        text_rect[1] = SCORE_POS[1]
        pygame.draw.rect(self.screen, BLACK, text_rect)
        pygame.display.update(text_rect)

        self.score += achived_score

        text_surf, text_rect = self.font.render("SCORES: " + str(self.score), WHITE)
        text_rect[0] = SCORE_POS[0]
        text_rect[1] = SCORE_POS[1]
        pygame.draw.rect(self.screen, BLACK, text_rect)

        self.screen.blit(text_surf, SCORE_POS)
        pygame.display.update(text_rect)

    def draw_grids(self):
        """
        Draw the grid onto the map for better designing.
        """
        for x in range(int(MAP_WIDTH / CELL_SIZE) + 1):
            self.screen.blit(self.font.render(str(x % 10), WHITE)[0],
                             (x * CELL_SIZE + MAP_POS_X + CELL_SIZE // 4, MAP_POS_Y - CELL_SIZE))

            pygame.draw.line(self.screen, (107, 107, 107),
                             (x * CELL_SIZE + MAP_POS_X, MAP_POS_Y),
                             (x * CELL_SIZE + MAP_POS_X, MAP_HEIGHT + MAP_POS_Y))

        for y in range(int(MAP_HEIGHT / CELL_SIZE) + 1):
            self.screen.blit(self.font.render(str(y % 10), WHITE)[0],
                             (MAP_POS_X - CELL_SIZE, y * CELL_SIZE + MAP_POS_Y))

            pygame.draw.line(self.screen, (107, 107, 107),
                             (MAP_POS_X, y * CELL_SIZE + MAP_POS_Y),
                             (MAP_WIDTH + MAP_POS_X, y * CELL_SIZE + MAP_POS_Y))

    def draw_button(self, surf, rect, button_color, text_color, text):
        pygame.draw.rect(surf, button_color, rect)
        text_surf, text_rect = self.font.render(text, text_color)
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    @staticmethod
    def draw_triangle_button(surf, rect, button_color):
        pygame.draw.polygon(surf, button_color, rect)

    def home_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.home_background, (0, 0))

    def play_draw(self):
        self.map = pygame.image.load(MAP_IMG[self.current_map_index])
        self.map = pygame.transform.scale(self.map, (MAP_WIDTH, MAP_HEIGHT))
       
        self.screen.fill(BLACK)
        self.screen.blit(self.map, (MAP_POS_X, MAP_POS_Y))

    def about_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.about_background, (0, 0))
        text_surf, text_rect = self.font.render("DEVELOPERS", WHITE)
        self.screen.blit(text_surf, (230, 50))
        text_surf, text_rect = self.font.render("21120184 - Le Minh Thu", WHITE)
        self.screen.blit(text_surf, (150, 170))
        text_surf, text_rect = self.font.render("21120198 - Nguyen Thi Lan Anh", WHITE)
        self.screen.blit(text_surf, (150, 220))
        text_surf, text_rect = self.font.render("21120408 - Dang Tuan Anh", WHITE)
        self.screen.blit(text_surf, (150, 270))
        text_surf, text_rect = self.font.render("21120426 - Huynh Phat Dat", WHITE)
        self.screen.blit(text_surf, (150, 320))
        text_surf, text_rect = self.font.render("21120440 - Chu Quang Duy", WHITE)
        self.screen.blit(text_surf, (150, 370))

    def map_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.level_background, (0, 0))
    def level_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.level_background, (0, 0))


    @staticmethod
    def play_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    def about_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 30 <= self.mouse[0] <= 130 and 50 <= self.mouse[1] <= 80:
                    self.state = STATE_HOME

        self.mouse = pygame.mouse.get_pos()
        if 30 <= self.mouse[0] <= 130 and 50 <= self.mouse[1] <= 80:
            self.draw_button(self.screen, BACK_POS, BLUE_LIGHT, WHITE, "Back")
        else:
            self.draw_button(self.screen, BACK_POS, BLUE, WHITE, "Back")
        pygame.display.update()

    def map_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                    self.state = STATE_LEVEL
                    self.current_map_index = 0
                elif 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                    self.state = STATE_LEVEL
                    self.current_map_index = 1
                elif 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
                    self.state = STATE_LEVEL
                    self.current_map_index = 2
                elif 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
                    self.state = STATE_LEVEL
                    self.current_map_index = 3
                elif 150 <= self.mouse[0] <= 450 and 600 <= self.mouse[1] <= 650:
                    self.state = STATE_LEVEL
                    self.current_map_index = 4

                elif 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
                    self.state = STATE_HOME
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()
        if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
            self.draw_button(self.screen, MAP_1_POS, DARK_GREY, RED, "Map 1")
        else:
            self.draw_button(self.screen, MAP_1_POS, BLUE, WHITE, "Map 1")
        if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, MAP_2_POS, DARK_GREY, RED, "Map 2")
        else:
            self.draw_button(self.screen, MAP_2_POS, BLUE, WHITE, "Map 2")
        if 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
            self.draw_button(self.screen, MAP_3_POS, DARK_GREY, RED, "Map 3")
        else:
            self.draw_button(self.screen, MAP_3_POS, BLUE, WHITE, "Map 3")
        if 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
            self.draw_button(self.screen, MAP_4_POS, DARK_GREY, RED, "Map 4")
        else:
            self.draw_button(self.screen, MAP_4_POS, BLUE, WHITE, "Map 4")
        if 150 <= self.mouse[0] <= 450 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, MAP_5_POS, DARK_GREY, RED, "Map 5")
        else:
            self.draw_button(self.screen, MAP_5_POS, BLUE, WHITE, "Map 5")
        if 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, BACK_MAP_POS, DARK_GREY, RED, "Back")
        else:
            self.draw_button(self.screen, BACK_MAP_POS, LIGHT_GREY, BLACK, "Back")
        pygame.display.update()

    def level_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                    self.state = STATE_PLAYING
                    self.current_level = 1
                elif 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                    self.state = STATE_PLAYING
                    self.current_level = 2
                elif 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
                    self.state = STATE_PLAYING
                    self.current_level = 3
                elif 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
                    self.state = STATE_PLAYING
                    self.current_level = 4

                elif 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
                    self.state = STATE_MAP
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()
        if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
            self.draw_button(self.screen, LEVEL_1_POS, BLUE_LIGHT, WHITE, "Level 1")
        else:
            self.draw_button(self.screen, LEVEL_1_POS, BLUE, WHITE, "Level 1")
        if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, LEVEL_2_POS, BLUE_LIGHT, WHITE, "Level 2")
        else:
            self.draw_button(self.screen, LEVEL_2_POS, BLUE, WHITE, "Level 2")
        if 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
            self.draw_button(self.screen, LEVEL_3_POS, BLUE_LIGHT, WHITE, "Level 3")
        else:
            self.draw_button(self.screen, LEVEL_3_POS, BLUE, WHITE, "Level 3")
        if 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
            self.draw_button(self.screen, LEVEL_4_POS, BLUE_LIGHT, WHITE, "Level 4")
        else:
            self.draw_button(self.screen, LEVEL_4_POS, BLUE, WHITE, "Level 4")
        if 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, BACK_LEVEL_POS, DARK_GREY, RED, "Back")
        else:
            self.draw_button(self.screen, BACK_LEVEL_POS, BLUE, WHITE, "Back")
        pygame.display.update()

    def home_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 395:
                    self.state = STATE_MAP
                elif 150 <= self.mouse[0] <= 450 and 400 <= self.mouse[1] <= 450:
                    self.state = STATE_ABOUT
                elif 150 <= self.mouse[0] <= 450 and 480 <= self.mouse[1] <= 530:                    
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()
        if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 375:
            self.draw_button(self.screen, START_POS, BLUE_LIGHT, WHITE, "Play")
        else:
            self.draw_button(self.screen, START_POS, BLUE, WHITE, "Play")
        if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, ABOUT_POS, BLUE_LIGHT, WHITE, "About")
        else:
            self.draw_button(self.screen, ABOUT_POS, BLUE, WHITE, "About")
        if 150 <= self.mouse[0] <= 450 and 470 <= self.mouse[1] <= 520:
            self.draw_button(self.screen, EXIT_POS, BLUE_LIGHT, WHITE, "Exit")
        else:
            self.draw_button(self.screen, EXIT_POS, BLUE, WHITE, "Exit")
        pygame.display.update()
