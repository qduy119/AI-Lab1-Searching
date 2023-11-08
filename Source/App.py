import sys
import pygame.freetype
import random
import Pacman
import Food
import Ghost
import Wall
import Map
import GraphSearch
import HeuristicLocalSearch
from Constant import *
import time


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
        self.total_time = 0
        self.steps = 0
        self.cur_speed_index = 1
        self.speed_list = [
            ("SPEED: 0.5", 0.5),
            ("SPEED: 1.0", 1),
            ("SPEED: 2.0", 2),
            ("SPEED: 5.0", 5),
            ("SPEED: 10.0", 10),
        ]

        self.tile = pygame.image.load(APP_TILE)
        self.tile = pygame.transform.scale(self.tile, (CELL_SIZE, CELL_SIZE))
        self.home_background = pygame.image.load(HOME_BACKGROUND)
        self.home_background = pygame.transform.scale(
            self.home_background, (HOME_BG_WIDTH, HOME_BG_HEIGHT)
        )
        self.about_background = pygame.image.load(ABOUT_BACKGROUND)
        self.about_background = pygame.transform.scale(
            self.about_background, (APP_WIDTH, APP_HEIGHT)
        )
        self.level_background = self.home_background
        self.gameover_background = pygame.image.load(GAMEOVER_BACKGROUND)
        self.gameover_background = pygame.transform.scale(
            self.gameover_background,
            (GAMEOVER_BACKGROUND_WIDTH, GAMEOVER_BACKGROUND_HEIGHT),
        )
        self.victory_background = pygame.image.load(VICTORY_BACKGROUND)
        self.victory_background = pygame.transform.scale(
            self.victory_background, (VICTORY_WIDTH, VICTORY_HEIGHT)
        )

        self.state = STATE_HOME
        self.clock = pygame.time.Clock()
        self.mouse = None
        self.algorithm = SEARCH_A

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
        graph_map, pacman_pos, food_pos, wall_cell_list = Map.read_map_level_1(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index]
        )

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        food = Food.Food(self, food_pos)
        food.appear()
        start_time = time.time()
        path = self.get_path_search_algorithm(graph_map, pacman, food)
        end_time = time.time()
        self.total_time = end_time - start_time
        wall_list = [Wall.Wall(self, wall_pos) for wall_pos in wall_cell_list]
        for wall in wall_list:
            wall.appear()

        if self.ready():
            if path is not None:
                self.steps = len(path) - 1
                back_home = False
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    pacman.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(
                        int(SPEED // self.speed_list[self.cur_speed_index][1])
                    )

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
        (
            graph_map,
            pacman_pos,
            food_pos,
            ghost_pos_list,
            wall_cell_list,
        ) = Map.read_map_level_2(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index],
            ghost_as_wall=True,
        )

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        food = Food.Food(self, food_pos)
        food.appear()

        start_time = time.time()
        path = self.get_path_search_algorithm(graph_map, pacman, food_pos)
        end_time = time.time()
        self.total_time = end_time - start_time

        wall_list = [Wall.Wall(self, wall_pos) for wall_pos in wall_cell_list]
        for wall in wall_list:
            wall.appear()

        ghost_list = [Ghost.Ghost(self, ghost_pos) for ghost_pos in ghost_pos_list]
        for ghost in ghost_list:
            ghost.appear()

        if self.ready():
            back_home = False
            if path is None:
                graph_map, pacman_pos, food_pos, ghost_pos_list = Map.read_map_level_2(
                    MAP_INPUT_TXT[self.current_level - 1][self.current_map_index],
                    ghost_as_wall=False,
                )

                path = self.get_path_search_algorithm(graph_map, pacman, food_pos)

                if path is not None:
                    path = path[1:]

                    for cell in path:
                        pacman.move(cell)
                        self.update_score(SCORE_PENALTY)

                        if cell in ghost_pos_list:
                            break

                        pygame.time.delay(
                            int(SPEED // self.speed_list[self.cur_speed_index][1])
                        )

                        if self.launch_game_event():
                            back_home = True
                            break

                if not back_home:
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                self.steps = len(path) - 1
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    pacman.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(
                        int(SPEED // self.speed_list[self.cur_speed_index][1])
                    )

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
        (
            cells,
            graph_map,
            pacman_cell,
            food_cell_list,
            ghost_cell_list,
            wall_cell_list,
        ) = Map.read_map_level_3(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index]
        )

        # Initialize Pacman, Foods and Ghosts.
        food_list = [
            Food.Food(self, food_cell.pos, food_cell) for food_cell in food_cell_list
        ]
        for food in food_list:
            food.appear()

        ghost_list = [
            Ghost.Ghost(self, ghost_cell.pos, ghost_cell)
            for ghost_cell in ghost_cell_list
        ]
        for ghost in ghost_list:
            ghost.appear()

        pacman = Pacman.Pacman(self, pacman_cell.pos, pacman_cell)
        pacman.appear()

        wall_list = [Wall.Wall(self, wall_pos) for wall_pos in wall_cell_list]
        for wall in wall_list:
            wall.appear()

        # Game.
        if self.ready():
            back_home = False
            pacman_is_caught = False
            start_time = time.time()
            end_time = 0
            self.steps = 0
            while True:
                is_backtracking = False
                pacman_old_cell = pacman.cell

                # Pacman observes all of Cells in its sight then decide the direction to move.
                pacman.cell.pacman_leave()
                pacman.observe(graph_map, 3)

                if not pacman.empty_brain() and not pacman.have_food_in_cur_sight():
                    # Pacman tracks the peas which leads to one of Food that Pacman saw in the past.
                    pacman.cell = pacman.back_track(graph_map)
                    is_backtracking = True
                else:
                    # Pacman moves with heuristic.
                    pacman.cell = self.get_path_search_algorithm(
                        graph_map, pacman, [ghost.cell for ghost in ghost_list]
                    )

                pacman.cell.pacman_come()
                pacman.move(pacman.cell.pos)
                self.steps = self.steps + 1
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
                            pacman.food_cell_in_brain_list.remove(
                                pacman.food_cell_in_brain_list[i]
                            )
                            pacman.path_to_food_cell_in_brain_list.remove(
                                pacman.path_to_food_cell_in_brain_list[i]
                            )
                            break

                # Ghosts move around.
                for ghost in ghost_list:
                    ghost_old_cell = ghost.cell

                    ghost.cell.ghost_leave()

                    next_cell = ghost.initial_cell
                    if ghost.cell.pos == ghost.initial_cell.pos:
                        around_cell_list = ghost.get_around_cells_of_initial_cell(
                            graph_map
                        )
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
                    end_time = time.time()
                    self.total_time = end_time - start_time
                    self.state = STATE_VICTORY
                    break

                # Graphic: "while True" handling.
                pygame.time.delay(
                    int(SPEED // self.speed_list[self.cur_speed_index][1])
                )
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
        (
            cells,
            graph_cell,
            pacman_cell,
            graph_map,
            food_cell_list,
            ghost_cell_list,
            wall_cell_list,
        ) = Map.read_map_level_4(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index]
        )

        # Initialize Pacman, Foods and Ghosts.
        food_list = [
            Food.Food(self, food_cell.pos, food_cell) for food_cell in food_cell_list
        ]
        for food in food_list:
            food.appear()

        ghost_list = [
            Ghost.Ghost(self, ghost_cell.pos, ghost_cell)
            for ghost_cell in ghost_cell_list
        ]
        for ghost in ghost_list:
            ghost.appear()

        pacman = Pacman.Pacman(self, pacman_cell.pos, pacman_cell)
        pacman.appear()

        wall_list = [Wall.Wall(self, wall_pos) for wall_pos in wall_cell_list]
        for wall in wall_list:
            wall.appear()

        if self.ready():
            back_home = False
            pacman_is_caught = False
            start_time = time.time()
            end_time = 0
            self.steps = 0

            while True:
                is_backtracking = False
                pacman_old_cell = pacman.cell

                # Pacman observes all of Cells in its sight then decide the direction to move.
                pacman.cell.pacman_leave()
                pacman.observe(graph_cell, 3)

                if (
                    not pacman.empty_brain()
                    and not pacman.have_food_in_cur_sight()
                    and not pacman.have_ghost_in_cur_sight()
                ):
                    # Pacman tracks the peas which leads to one of Food that Pacman saw in the past.
                    pacman.cell = pacman.back_track(graph_cell)
                    is_backtracking = True
                else:
                    # Pacman moves with heuristic.
                    pacman.cell = self.get_path_search_algorithm(#HeuristicLocalSearch.local_search(                
                        graph_cell, pacman, [ghost.cell for ghost in ghost_list]
                    )
                    '''
                    pacman.cell = HeuristicLocalSearch.minimax(graph_cell, pacman.cell, [ghost.cell for ghost in ghost_list], pacman.food_cell_in_sight_list)
                     '''   
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
                self.steps = self.steps + 1
                self.update_score(SCORE_PENALTY)

                # Spread the peas.
                if not is_backtracking:
                    pacman.spread_peas(pacman_old_cell)

                # Pacman went through Monsters?
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

                # Ghosts try to seek and kill Pacman. have a ghost moved with A* search
                
                for ghost in ghost_list:
                    old_cell = ghost.cell
                    ghost.cell.ghost_leave()
                    next_cell = None 
                    distance = []  
                    for i in graph_cell[ghost.cell]:                 
                        distance.append(abs(i.pos[0]- pacman.cell.pos[0]) + abs(i.pos[1]- pacman.cell.pos[1]))
                    next_cell = graph_cell[ghost.cell][distance.index(min(distance))]
                    ghost.cell = next_cell
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
                    end_time = time.time()
                    self.total_time = end_time - start_time
                    self.state = STATE_VICTORY
                    break

                # Graphic: "while True" handling.
                pygame.time.delay(
                    int(SPEED // self.speed_list[self.cur_speed_index][1])
                )
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
            elif self.state == STATE_ALGORITHM:
                self.algorithm_draw()
                self.algorithm_event()
            elif self.state == STATE_LEVEL:
                self.level_draw()
                self.level_event()
            elif self.state == STATE_GAMEOVER:
                self.gameover_draw()
                self.gameover_event()
            elif self.state == STATE_VICTORY:
                self.victory_draw()
                self.victory_event()
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

        text_surf, text_rect = self.font.render(
            self.speed_list[self.cur_speed_index][0], WHITE
        )
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
                if (
                    HOME_RECT[0] <= self.mouse[0] <= HOME_RECT[0] + HOME_RECT[2]
                    and HOME_RECT[1] <= self.mouse[1] <= HOME_RECT[1] + HOME_RECT[3]
                ):
                    self.state = STATE_HOME
                    break
                if (
                    SPEED_RECT[0] <= self.mouse[0] <= SPEED_RECT[0] + SPEED_RECT[2]
                    and SPEED_RECT[1] <= self.mouse[1] <= SPEED_RECT[1] + SPEED_RECT[3]
                ):
                    self.cur_speed_index += 1
                    self.cur_speed_index %= len(self.speed_list)
                    break

        self.mouse = pygame.mouse.get_pos()
        if (
            HOME_RECT[0] <= self.mouse[0] <= HOME_RECT[0] + HOME_RECT[2]
            and HOME_RECT[1] <= self.mouse[1] <= HOME_RECT[1] + HOME_RECT[3]
        ):
            text_surf, text_rect = self.font.render("HOME", RED)
            self.screen.blit(text_surf, HOME_RECT)
            pygame.display.update(HOME_RECT)
        else:
            text_surf, text_rect = self.font.render("HOME", WHITE)
            self.screen.blit(text_surf, HOME_RECT)
            pygame.display.update(HOME_RECT)
        if (
            SPEED_RECT[0] <= self.mouse[0] <= SPEED_RECT[0] + SPEED_RECT[2]
            and SPEED_RECT[1] <= self.mouse[1] <= SPEED_RECT[1] + SPEED_RECT[3]
        ):
            pygame.draw.rect(self.screen, BLACK, SPEED_RECT)
            text_surf, text_rect = self.font.render(
                self.speed_list[self.cur_speed_index][0], RED
            )
            self.screen.blit(text_surf, SPEED_RECT)
            pygame.display.update(SPEED_RECT)
        else:
            pygame.draw.rect(self.screen, BLACK, SPEED_RECT)
            text_surf, text_rect = self.font.render(
                self.speed_list[self.cur_speed_index][0], WHITE
            )
            self.screen.blit(text_surf, SPEED_RECT)
            pygame.display.update(SPEED_RECT)

        if self.state == STATE_HOME:
            return True

        return False

    def ready(self):
        """
        Ready effect (3, 2, 1, GO).
        """
        text_list = [
            "3",
            "3",
            "3",
            "3",
            "2",
            "2",
            "2",
            "2",
            "1",
            "1",
            "1",
            "1",
            "GO",
            "GO",
            "GO",
            "GO",
        ]
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

        total_str = "TIME: " + "{:.7f}".format(self.total_time) + "s"
        text_surf, text_rect = self.font.render(total_str, WHITE)
        self.screen.blit(text_surf, (200, 360))
        steps_str = "STEPS: " + str(self.steps)
        text_surf, text_rect = self.font.render(steps_str, WHITE)
        self.screen.blit(text_surf, (200, 410))
        score_str = "SCORE: " + str(self.score)
        text_surf, text_rect = self.font.render(score_str, WHITE)
        self.screen.blit(text_surf, (200, 460))

    def gameover_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.gameover_background, (25, 10))
      
        steps_str = "STEPS: " + str(self.steps)
        text_surf, text_rect = self.font.render(steps_str, WHITE)
        self.screen.blit(text_surf, (150, 500)) 
        score_str = "SCORE: " + str(self.score)
        text_surf, text_rect = self.font.render(score_str, WHITE)
        self.screen.blit(text_surf, (350, 500))
    def update_score(self, achived_score):
        """
        Add 'achived_score' to the current score and display onto the screen.
        """
        text_surf, text_rect = self.font.render("SCORE: " + str(self.score), WHITE)
        text_rect[0] = SCORE_POS[0]
        text_rect[1] = SCORE_POS[1]
        pygame.draw.rect(self.screen, BLACK, text_rect)
        pygame.display.update(text_rect)

        self.score += achived_score

        text_surf, text_rect = self.font.render("SCORE: " + str(self.score), WHITE)
        text_rect[0] = SCORE_POS[0]
        text_rect[1] = SCORE_POS[1]
        pygame.draw.rect(self.screen, BLACK, text_rect)

        self.screen.blit(text_surf, SCORE_POS)
        pygame.display.update(text_rect)

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
        self.screen.fill(BLACK)
        y = MAP_POS_Y

        while True:
            x = MAP_POS_X
            while x < MAP_WIDTH + MAP_POS_X:
                self.screen.blit(self.tile, (x, y))
                x += CELL_SIZE

            y += CELL_SIZE
            if y >= MAP_HEIGHT + MAP_POS_Y:
                break

        pygame.display.update()

    def about_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.about_background, (0, 0))
        text_surf, text_rect = self.font.render("DEVELOPERS", BLUE_LIGHT, size=36)
        self.screen.blit(text_surf, (200, 60))
        text_surf, text_rect = self.font.render("21120184 - LE THI MINH THU", WHITE)
        self.screen.blit(text_surf, (150, 170))
        text_surf, text_rect = self.font.render("21120198 - NGUYEN THI LAN ANH", WHITE)
        self.screen.blit(text_surf, (150, 220))
        text_surf, text_rect = self.font.render("21120408 - DANG TUAN ANH", WHITE)
        self.screen.blit(text_surf, (150, 270))
        text_surf, text_rect = self.font.render("21120426 - HUYNH PHAT DAT", WHITE)
        self.screen.blit(text_surf, (150, 320))
        text_surf, text_rect = self.font.render("21120440 - CHU QUANG DUY", WHITE)
        self.screen.blit(text_surf, (150, 370))

    def map_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.level_background, (0, 0))

    def level_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.level_background, (0, 0))

    def algorithm_draw(self):
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
                if 450 <= self.mouse[0] <= 550 and 540 <= self.mouse[1] <= 580:
                    self.state = STATE_HOME

        self.mouse = pygame.mouse.get_pos()
        if 450 <= self.mouse[0] <= 550 and 540 <= self.mouse[1] <= 580:
            self.draw_button(self.screen, BACK_POS, BLUE_LIGHT, WHITE, "BACK")
        else:
            self.draw_button(self.screen, BACK_POS, BLUE, WHITE, "BACK")
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
            self.draw_button(self.screen, MAP_1_POS, BLUE_LIGHT, WHITE, "MAP 1")
        else:
            self.draw_button(self.screen, MAP_1_POS, BLUE, WHITE, "MAP 1")
        if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, MAP_2_POS, BLUE_LIGHT, WHITE, "MAP 2")
        else:
            self.draw_button(self.screen, MAP_2_POS, BLUE, WHITE, "MAP 2")
        if 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
            self.draw_button(self.screen, MAP_3_POS, BLUE_LIGHT, WHITE, "MAP 3")
        else:
            self.draw_button(self.screen, MAP_3_POS, BLUE, WHITE, "MAP 3")
        if 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
            self.draw_button(self.screen, MAP_4_POS, BLUE_LIGHT, WHITE, "MAP 4")
        else:
            self.draw_button(self.screen, MAP_4_POS, BLUE, WHITE, "MAP 4")
        if 150 <= self.mouse[0] <= 450 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, MAP_5_POS, BLUE_LIGHT, WHITE, "MAP 5")
        else:
            self.draw_button(self.screen, MAP_5_POS, BLUE, WHITE, "MAP 5")
        if 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, BACK_MAP_POS, BLUE_LIGHT, WHITE, "BACK")
        else:
            self.draw_button(self.screen, BACK_MAP_POS, BLUE, WHITE, "BACK")
        pygame.display.update()

    def level_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                    self.state = STATE_ALGORITHM
                    self.current_level = 1
                elif 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                    self.state = STATE_ALGORITHM
                    self.current_level = 2
                elif 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
                    self.state = STATE_PLAYING
                    self.current_level = 3
                elif 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
                    self.state = STATE_ALGORITHM
                    self.current_level = 4

                elif 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
                    self.state = STATE_MAP
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()
        if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
            self.draw_button(self.screen, LEVEL_1_POS, BLUE_LIGHT, WHITE, "LEVEL 1")
        else:
            self.draw_button(self.screen, LEVEL_1_POS, BLUE, WHITE, "LEVEL 1")
        if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, LEVEL_2_POS, BLUE_LIGHT, WHITE, "LEVEL 2")
        else:
            self.draw_button(self.screen, LEVEL_2_POS, BLUE, WHITE, "LEVEL 2")
        if 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
            self.draw_button(self.screen, LEVEL_3_POS, BLUE_LIGHT, WHITE, "LEVEL 3")
        else:
            self.draw_button(self.screen, LEVEL_3_POS, BLUE, WHITE, "LEVEL 3")
        if 150 <= self.mouse[0] <= 450 and 530 <= self.mouse[1] <= 580:
            self.draw_button(self.screen, LEVEL_4_POS, BLUE_LIGHT, WHITE, "LEVEL 4")
        else:
            self.draw_button(self.screen, LEVEL_4_POS, BLUE, WHITE, "LEVEL 4")
        if 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, BACK_LEVEL_POS, BLUE_LIGHT, WHITE, "BACK")
        else:
            self.draw_button(self.screen, BACK_LEVEL_POS, BLUE, WHITE, "BACK")
        pygame.display.update()   

    def algorithm_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_level < 3:
                    if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                        self.state = STATE_PLAYING
                        self.algorithm = SEARCH_A 
                    elif 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                        self.state = STATE_PLAYING
                        self.algorithm = SEARCH_BFS
                    elif 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
                        self.state = STATE_PLAYING
                        self.algorithm = SEARCH_DFS
                
                else:
                    if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                        self.state = STATE_PLAYING
                        self.algorithm = SEARCH_LOCAL
                    elif 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                        self.state = STATE_PLAYING
                        self.algorithm = SEARCH_MINIMAX
                if 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
                        self.state = STATE_LEVEL
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()
        if self.current_level< 3:
            if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                self.draw_button(self.screen, LEVEL_1_POS, BLUE_LIGHT, WHITE, "A* Search")
            else:
                self.draw_button(self.screen, LEVEL_1_POS, BLUE, WHITE, "A* Search")
            if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                self.draw_button(self.screen, LEVEL_2_POS, BLUE_LIGHT, WHITE, "BFS Search")
            else:
                self.draw_button(self.screen, LEVEL_2_POS, BLUE, WHITE, "BFS Search")
            if 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 510:
                self.draw_button(self.screen, LEVEL_3_POS, BLUE_LIGHT, WHITE, "DFS Search")
            else:
                self.draw_button(self.screen, LEVEL_3_POS, BLUE, WHITE, "DFS Search")
        else:
            if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 370:
                self.draw_button(self.screen, LEVEL_1_POS, BLUE_LIGHT, WHITE, "Local Search")
            else:
                self.draw_button(self.screen, LEVEL_1_POS, BLUE, WHITE, "Heuristic Local Search")
            if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
                self.draw_button(self.screen, LEVEL_2_POS, BLUE_LIGHT, WHITE, "Minimax Search")
            else:
                self.draw_button(self.screen, LEVEL_2_POS, BLUE, WHITE, "Minimax Search")
        if 500 <= self.mouse[0] <= 570 and 600 <= self.mouse[1] <= 650:
            self.draw_button(self.screen, BACK_LEVEL_POS, BLUE_LIGHT, WHITE, "BACK")
        else:
            self.draw_button(self.screen, BACK_LEVEL_POS, BLUE, WHITE, "BACK")
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
            self.draw_button(self.screen, START_POS, BLUE_LIGHT, WHITE, "PLAY")
        else:
            self.draw_button(self.screen, START_POS, BLUE, WHITE, "PLAY")
        if 150 <= self.mouse[0] <= 450 and 390 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, ABOUT_POS, BLUE_LIGHT, WHITE, "ABOUT")
        else:
            self.draw_button(self.screen, ABOUT_POS, BLUE, WHITE, "ABOUT")
        if 150 <= self.mouse[0] <= 450 and 470 <= self.mouse[1] <= 520:
            self.draw_button(self.screen, EXIT_POS, BLUE_LIGHT, WHITE, "EXIT")
        else:
            self.draw_button(self.screen, EXIT_POS, BLUE, WHITE, "EXIT")
        pygame.display.update()

    def gameover_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= self.mouse[0] <= 205 and 570 <= self.mouse[1] <= 620:
                    self.state = STATE_HOME
                if 405 <= self.mouse[0] <= 505 and 570 <= self.mouse[1] <= 620:
                    pygame.quit()
                    sys.exit()

        self.mouse = pygame.mouse.get_pos()
        HOME_POS = pygame.Rect(100, 570, 100, 50)
        EXIT_POS = pygame.Rect(400, 570, 100, 50)
        if 100 <= self.mouse[0] <= 155 and 570 <= self.mouse[1] <= 620:
            self.draw_button(self.screen, HOME_POS, BLUE_LIGHT, WHITE, "HOME")
        else:
            self.draw_button(self.screen, HOME_POS, BLUE, WHITE, "HOME")
        if 405 <= self.mouse[0] <= 505 and 570 <= self.mouse[1] <= 620:
            self.draw_button(self.screen, EXIT_POS, BLUE_LIGHT, WHITE, "EXIT")
        else:
            self.draw_button(self.screen, EXIT_POS, BLUE, WHITE, "EXIT")
        pygame.display.update()

    def victory_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 550 <= self.mouse[1] <= 600:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()

        if 255 <= self.mouse[0] <= 355 and 550 <= self.mouse[1] <= 600:
            self.draw_button(self.screen, OK_POS, BLUE_LIGHT, WHITE, "HOME")
        else:
            self.draw_button(self.screen, OK_POS, BLUE, WHITE, "HOME")

        pygame.display.update()

    def get_path_search_algorithm(self, graph_map, pacman, food_ghost):
        if self.algorithm == SEARCH_A:
            return GraphSearch.search_A(
                graph_map, pacman.cell.pos, food_ghost
            )
        elif self.algorithm == SEARCH_BFS:
            return GraphSearch.search_BFS(graph_map, pacman.cell.pos, food_ghost)
        elif self.algorithm == SEARCH_DFS:
            return GraphSearch.search_DFS(graph_map, pacman.cell.pos, food_ghost)
        elif self.algorithm == SEARCH_LOCAL:
            return HeuristicLocalSearch.local_search(graph_map, pacman.cell)
        else:
            return HeuristicLocalSearch.minimax(graph_map, pacman.cell, food_ghost, pacman.food_cell_in_sight_list)
