from Constant import *


class Ghost:
    ################################################## CORE FUNCTIONS ##################################################
    def __init__(self, app, pos, cell=None):
        self.app = app
        self.width = CELL_SIZE - 2
        self.grid_pos = [pos[0], pos[1]]
        self.pixel_pos = self.get_current_pixel_pos()
        self.direction = 'up'

        self.ghost_left_image = pygame.image.load(GHOST_LEFT_IMAGE)
        self.ghost_left_image = pygame.transform.scale(self.ghost_left_image, (self.width, self.width))
        self.ghost_right_image = pygame.image.load(GHOST_RIGHT_IMAGE)
        self.ghost_right_image = pygame.transform.scale(self.ghost_right_image, (self.width, self.width))
        self.ghost_up_image = pygame.image.load(GHOST_UP_IMAGE)
        self.ghost_up_image = pygame.transform.scale(self.ghost_up_image, (self.width, self.width))
        self.ghost_down_image = pygame.image.load(GHOST_DOWN_IMAGE)
        self.ghost_down_image = pygame.transform.scale(self.ghost_down_image, (self.width, self.width))
        self.black_background = pygame.image.load(BLACK_BG)
        self.black_background = pygame.transform.scale(self.black_background, (CELL_SIZE, CELL_SIZE))
        self.cell = cell
        self.initial_cell = cell
    def appear(self):
        """
        Make the ghost appear on the screen.
        """
        self.draw()

    def get_around_cells_of_initial_cell(self, graph_map):
        return graph_map[self.initial_cell]

    def get_around_cells(self, graph_map):
        return graph_map[self.cell]

    def get_pos_move(self, next_direction):
        if next_direction == 'left':
            return self.grid_pos[0]-1, self.grid_pos[1]
        if next_direction == 'right':
            return self.grid_pos[0]+1, self.grid_pos[1]
        if next_direction == 'up':
            return self.grid_pos[0], self.grid_pos[1]-1
        elif next_direction == 'down':
            return self.grid_pos[0], self.grid_pos[1]+1

    def move(self, new_grid_pos):
        """
        Move the ghost to the new position (x, y) on the grid map.

        :param new_grid_pos: new position (x, y) on the grid map
        """
        self.update(new_grid_pos)
        self.draw()


    ####################################################################################################################

    def update_direction(self, new_grid_pos):
        """
        Update the ghost's direction based on the `new_grid_pos`.
        
        :param new_grid_pos: new position (x, y) on the grid map
        """
        if new_grid_pos[1] - self.grid_pos[1] == 1:
            self.direction = 'down'
        elif new_grid_pos[1] - self.grid_pos[1] == -1:
            self.direction = 'up'
        elif new_grid_pos[0] - self.grid_pos[0] == 1:
            self.direction = 'right'
        elif new_grid_pos[0] - self.grid_pos[0] == -1:
            self.direction = 'left'

    def get_available_moves(self, cells):
        avail_moves = []
        cells_row = len(cells)
        cells_col = len(cells[0])
        if self.grid_pos[0]+1 < cells_col and cells[self.grid_pos[1]][self.grid_pos[0]+1]:
            avail_moves.append('right')
        if self.grid_pos[0]>0 and cells[self.grid_pos[1]][self.grid_pos[0]-1]:
            avail_moves.append('left')
        if self.grid_pos[1]+1 < cells_row and cells[self.grid_pos[1]+1][self.grid_pos[0]]:
            avail_moves.append('down')
        if self.grid_pos[1]>0 and cells[self.grid_pos[1]-1][self.grid_pos[0]]:
            avail_moves.append('up')
        return avail_moves

    def update(self, new_grid_pos):
        """
        Update the ghost's grid position

        :param new_grid_pos: new position (x, y) on the grid map
        """
        pygame.display.update(self.app.screen.blit(self.black_background, (self.pixel_pos[0], self.pixel_pos[1])))
        self.update_direction(new_grid_pos)
        self.grid_pos = new_grid_pos
        self.pixel_pos = self.get_current_pixel_pos()


    def get_current_pixel_pos(self):
        """
        Get the current pixel position via the current grid position.

        :return: the pixel position [x, y]
        """
        return [self.grid_pos[0] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_X,
                self.grid_pos[1] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_Y]


    def draw(self):
        """
        Draw the ghost onto the screen.
        """
        if self.direction == 'up':
            pygame.display.update(self.app.screen.blit(self.ghost_up_image, (self.pixel_pos[0], self.pixel_pos[1])))
        elif self.direction == 'down':
            pygame.display.update(self.app.screen.blit(self.ghost_down_image, (self.pixel_pos[0], self.pixel_pos[1])))
        elif self.direction == 'left':
            pygame.display.update(self.app.screen.blit(self.ghost_left_image, (self.pixel_pos[0], self.pixel_pos[1])))
        elif self.direction == 'right':
            pygame.display.update(self.app.screen.blit(self.ghost_right_image, (self.pixel_pos[0], self.pixel_pos[1])))
