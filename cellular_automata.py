import tkinter as tk


class Cell:
    def __init__(self, state, x=0, y=0):
        self.state = state
        self.x = x
        self.y = y
        self.up = ""
        self.right = ""
        self.down = ""
        self.left = ""
        self.loc_up = 0b0000
        self.loc_right = 0b0000
        self.loc_down = 0b0000
        self.loc_left = 0b0000
        self.wall_corner = False

    def data(self):
        print(self.state,
              self.x,
              self.y,
              self.up,
              self.right,
              self.down,
              self.left,
              bin(self.loc_up),
              bin(self.loc_right),
              bin(self.loc_down),
              bin(self.loc_left))


class CellAutoWall:
    def __init__(self, size):
        self.size = size
        self.step = 10
        self.grid = [[Cell('empty', j, i) for j in range(self.size)] for i in range(self.size)]

    def draw(self, root):
        def create_grid(event=None):
            w = c.winfo_width()  # Get current width of canvas
            h = c.winfo_height()  # Get current height of canvas
            step = min(h // self.size, w // self.size)
            self.step = step
            # c.delete('grid_line') # Will only remove the grid_line

            # Creates all vertical lines at intervals of 100
            for i in range(0, w, step):
                c.create_line([(i, 0), (i, h)], tag='grid_line')

            # Creates all horizontal lines at intervals of 100
            for i in range(0, h, step):
                c.create_line([(0, i), (w, i)], tag='grid_line')

        def show_cells(event=None):
            w = c.winfo_width()  # Get current width of canvas
            h = c.winfo_height()  # Get current height of canvas
            step = min(h // self.size, w // self.size)
            self.step = step
            # c.delete('wall') ##########
            for row in self.grid:
                for cell in row:
                    x = cell.x * step
                    y = cell.y * step
                    if cell.state == 'empty':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='white', tag='empty')
                    elif cell.state == 'clear':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='gray', tag='clear')
                    elif cell.state == 'init':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='red', tag='init')
                    elif cell.state == 'init_path':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='red4', tag='init_path')
                    elif cell.state in ['corner', 'corner_prepare']:
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='green', tag='corner_prepare')
                    elif cell.state == 'corner_active':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='lawn green', tag='corner_active')
                    elif cell.state == 'near_support':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='orange', tag='near_support')
                    elif cell.state == 'far_support':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='purple', tag='far_support')
                    elif cell.state == 'wall_prepare':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='deep sky blue', tag='wall_prepare')
                    elif cell.state == 'path':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='IndianRed2', tag='path')
                    elif (cell.state == 'up_wall_active') or (cell.state == 'down_wall_active') or \
                            (cell.state == 'right_wall_active') or (cell.state == 'left_wall_active'):
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='yellow', tag='wall_active')
                    elif cell.state == 'non_active':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='pink', tag='non_active')
                    elif cell.state.startswith('up_shorter') or cell.state.startswith('right_shorter'):
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='magenta', tag='ur_shorter')
                    elif cell.state.startswith('down_shorter') or cell.state.startswith('left_shorter'):
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='cyan', tag='dl_shorter')
                    elif cell.state == 'wall':
                        c.create_polygon(x + 1, y + 1, x + 1, y + step, x + step, y + step, x + step, y + 1,
                                         fill='black', tag='wall')
            self.signal_propagation()  # функция перехода

        c = tk.Canvas(root, height=600, width=600, bg='white')
        c.pack(fill=tk.BOTH, expand=False)
        c.bind('<Configure>', create_grid)
        c.bind('<Button-1>', show_cells)

    def signal_propagation(self):
        for row in self.grid:
            for cell in row:
                if cell.state == 'init':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (1 << 2)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (1 << 2)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (1 << 2)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (1 << 2)

                if (cell.state == 'near_support') | (cell.state == 'far_support'):
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (3 << 2)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (3 << 2)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (3 << 2)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (3 << 2)

                if cell.state == 'up_wall_active':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down ^= 1
                            self.grid[i][cell.x].loc_down |= (1 << 1)
                elif cell.state == 'right_wall_active':
                    for j in range(self.size):
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left ^= 1
                            self.grid[cell.y][j].loc_left |= (1 << 1)
                elif cell.state == 'down_wall_active':
                    for i in range(self.size):
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up ^= 1
                            self.grid[i][cell.x].loc_up |= (1 << 1)
                elif cell.state == 'left_wall_active':
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right ^= 1
                            self.grid[cell.y][j].loc_right |= (1 << 1)

                if cell.state == 'up_shorter_final':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (1 << 4)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (1 << 4)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (1 << 4)
                elif cell.state == 'right_shorter_final':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (1 << 4)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (1 << 4)
                    for j in range(self.size):
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (1 << 4)
                elif cell.state == 'down_shorter_final':
                    for i in range(self.size):
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (1 << 4)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (1 << 4)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (1 << 4)
                elif cell.state == 'left_shorter_final':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (1 << 4)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (1 << 4)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (1 << 4)

                if cell.state == 'corner_active':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (1 << 4)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (1 << 4)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (1 << 4)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (1 << 4)

                state_list = ['path', 'far_support', 'up_shorter_final', 'right_shorter_final',
                              'down_shorter_final', 'left_shorter_final']
                if cell.state == 'path' and cell.wall_corner and \
                        ((cell.up in state_list and cell.down not in state_list
                          and cell.right not in state_list and cell.left not in state_list) or
                         (cell.up not in state_list and cell.down in state_list
                          and cell.right not in state_list and cell.left not in state_list) or
                         (cell.up not in state_list and cell.down not in state_list
                          and cell.right in state_list and cell.left not in state_list) or
                         (cell.up not in state_list and cell.down not in state_list
                          and cell.right not in state_list and cell.left in state_list)):
                    if cell.up == 'path' or cell.down == 'path':
                        for j in range(self.size):
                            if cell.x > j:
                                self.grid[cell.y][j].loc_right |= (3 << 4)
                            if cell.x < j:
                                self.grid[cell.y][j].loc_left |= (3 << 4)
                    elif cell.right == 'path' or cell.left == 'path':
                        for i in range(self.size):
                            if cell.y > i:
                                self.grid[i][cell.x].loc_down |= (3 << 4)
                            if cell.y < i:
                                self.grid[i][cell.x].loc_up |= (3 << 4)

                elif (cell.state == 'path') and \
                        ((cell.up == 'empty') & (cell.right == 'empty') & (cell.down == 'empty') |
                         (cell.left == 'empty') & (cell.right == 'empty') & (cell.down == 'empty') |
                         (cell.left == 'empty') & (cell.up == 'empty') & (cell.down == 'empty') |
                         (cell.left == 'empty') & (cell.up == 'empty') & (cell.right == 'empty')):
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (3 << 4)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (3 << 4)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (3 << 4)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (3 << 4)

                if cell.state == 'init_path':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (3 << 4)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (3 << 4)

                if cell.state == 'clear':
                    for i in range(self.size):
                        if cell.y > i:
                            self.grid[i][cell.x].loc_down |= (1 << 5)
                        if cell.y < i:
                            self.grid[i][cell.x].loc_up |= (1 << 5)
                    for j in range(self.size):
                        if cell.x > j:
                            self.grid[cell.y][j].loc_right |= (1 << 5)
                        if cell.x < j:
                            self.grid[cell.y][j].loc_left |= (1 << 5)

        self.phi()

    def phi(self):
        for row in self.grid:
            for cell in row:
                if (cell.state == 'init') & ((cell.up == 'wall') | (cell.right == 'wall') |
                                             (cell.down == 'wall') | (cell.left == 'wall')):
                    cell.state = 'near_support'
                elif (cell.state == 'empty') & ((cell.loc_up >> 2 == 1) & (cell.loc_right >> 2 == 1) |
                                                (cell.loc_right >> 2 == 1) & (cell.loc_down >> 2 == 1) |
                                                (cell.loc_down >> 2 == 1) & (cell.loc_left >> 2 == 1) |
                                                (cell.loc_left >> 2 == 1) & (cell.loc_up >> 2 == 1)):
                    cell.state = 'corner'
                elif cell.state == 'corner':
                    cell.state = 'corner_prepare'
                elif (cell.state == 'corner_prepare') & ((cell.up == 'wall') | (cell.right == 'wall') |
                                                       (cell.down == 'wall') | (cell.left == 'wall')):
                    cell.state = 'far_support'
                elif (cell.state == 'corner_prepare') & ((cell.loc_up == 4) & (cell.loc_right == 4) |
                                                         (cell.loc_right == 4) & (cell.loc_down == 4) |
                                                         (cell.loc_down == 4) & (cell.loc_left == 4) |
                                                         (cell.loc_left == 4) & (cell.loc_up == 4)):
                    cell.state = 'corner_active'
                elif cell.state in ['corner_active', 'non_active'] and not cell.wall_corner \
                        and not (cell.loc_up | cell.loc_down | cell.loc_right | cell.loc_left):
                    cell.state = 'clear'
                elif (cell.state == 'empty') & (((cell.loc_down >> 2 == 1) & (cell.up == 'wall')) |
                                                ((cell.loc_left >> 2 == 1) & (cell.right == 'wall')) |
                                                ((cell.loc_up >> 2 == 1) & (cell.down == 'wall')) |
                                                ((cell.loc_right >> 2 == 1) & (cell.left == 'wall'))):
                    cell.state = 'near_support'
                elif (cell.state == 'empty') & (((cell.loc_up >> 2 == 1) & (cell.up == 'wall')) |
                                                ((cell.loc_right >> 2 == 1) & (cell.right == 'wall')) |
                                                ((cell.loc_down >> 2 == 1) & (cell.down == 'wall')) |
                                                ((cell.loc_left >> 2 == 1) & (cell.left == 'wall'))):
                    cell.state = 'far_support'
                elif (cell.state == 'empty') & ((cell.loc_up >> 2 == 3) & (cell.loc_down >> 2 == 3) |
                                                (cell.loc_right >> 2 == 3) & (cell.loc_left >> 2 == 3)):
                    cell.state = 'wall_prepare'
                elif (cell.state == 'empty') & (cell.loc_up >> 2 == 3) & \
                        (((cell.up == 'wall') | (cell.right == 'wall') |
                          (cell.down == 'wall') | (cell.left == 'wall')) | cell.wall_corner):
                    cell.state = 'up_wall_active'
                elif (cell.state == 'empty') & (cell.loc_down >> 2 == 3) & \
                        (((cell.up == 'wall') | (cell.right == 'wall') |
                          (cell.down == 'wall') | (cell.left == 'wall')) | cell.wall_corner):
                    cell.state = 'down_wall_active'
                elif (cell.state == 'empty') & (cell.loc_right >> 2 == 3) & \
                        (((cell.up == 'wall') | (cell.right == 'wall') |
                          (cell.down == 'wall') | (cell.left == 'wall')) | cell.wall_corner):
                    cell.state = 'right_wall_active'
                elif (cell.state == 'empty') & (cell.loc_left >> 2 == 3) & \
                        (((cell.up == 'wall') | (cell.right == 'wall') |
                          (cell.down == 'wall') | (cell.left == 'wall')) | cell.wall_corner):
                    cell.state = 'left_wall_active'
                elif (cell.state == 'up_wall_active') & ~(cell.loc_down & 1):
                    cell.state = 'non_active'
                elif (cell.state == 'down_wall_active') & ~(cell.loc_up & 1):
                    cell.state = 'non_active'
                elif (cell.state == 'right_wall_active') & ~(cell.loc_left & 1):
                    cell.state = 'non_active'
                elif (cell.state == 'left_wall_active') & ~(cell.loc_right & 1):
                    cell.state = 'non_active'
                elif cell.state.endswith('_shorter') and \
                        ((cell.loc_up >> 4 == 3) | (cell.loc_right >> 4 == 3) |
                         (cell.loc_down >> 4 == 3) | (cell.loc_left >> 4 == 3)):
                    cell.state = 'clear'
                elif (cell.state in ['near_support', 'up_shorter', 'down_shorter']) & \
                        ((cell.up in ['wall_prepare', 'up_wall_active', 'down_wall_active', 'non_active']) |
                         (cell.down in ['wall_prepare', 'up_wall_active', 'down_wall_active', 'non_active'])):
                    if not cell.loc_up >> 1 & 1:
                        cell.state = 'up_shorter_final'
                    elif not cell.loc_down >> 1 & 1:
                        cell.state = 'down_shorter_final'
                    elif (cell.loc_up >> 1 & 1) & (cell.loc_down >> 1 & 1):
                        cell.state = 'up_shorter' if (cell.loc_up & 1) < (cell.loc_down & 1) else 'down_shorter'
                elif (cell.state in ['near_support', 'right_shorter', 'left_shorter']) and \
                        ((cell.right in ['wall_prepare', 'right_wall_active', 'non_active']) |
                         (cell.left in ['wall_prepare', 'left_wall_active', 'non_active'])):
                    if not cell.loc_right >> 1 & 1:
                        cell.state = 'right_shorter_final'
                    elif not cell.loc_left >> 1 & 1:
                        cell.state = 'left_shorter_final'
                    elif (cell.loc_right >> 1 & 1) & (cell.loc_left >> 1 & 1):
                        cell.state = 'right_shorter' if (cell.loc_right & 1) < (cell.loc_left & 1) else 'left_shorter'
                elif cell.state == 'init' and \
                        ((cell.loc_up >> 4) & (cell.loc_right >> 4) | (cell.loc_right >> 4) & (cell.loc_down >> 4) |
                         (cell.loc_down >> 4) & (cell.loc_left >> 4) | (cell.loc_left >> 4) & (cell.loc_up >> 4)):
                    cell.state = 'init_path'
                elif cell.state == 'init_path':
                    cell.state = 'path'
                elif (cell.state in ['non_active', 'wall_prepare', 'init', 'corner_active']) & \
                        ((cell.loc_up >> 4) | (cell.loc_right >> 4) | (cell.loc_down >> 4) | (cell.loc_left >> 4)):
                    cell.state = 'path'
                elif (cell.state == 'empty') & ((cell.loc_up >> 4) & (cell.loc_down >> 4) |
                                                (cell.loc_right >> 4) & (cell.loc_left >> 4)):
                    cell.state = 'path'
                elif (cell.state == 'far_support') & (((cell.up == 'path') | cell.up.endswith('_final')) &
                                                      ((cell.down == 'path') | cell.down.endswith('_final')) |
                                                      ((cell.right == 'path') | cell.right.endswith('_final')) &
                                                      ((cell.left == 'path') | cell.left.endswith('_final'))):
                    cell.state = 'path'
                elif (cell.state.endswith('_final')) & \
                        ((cell.loc_up >> 5 == 1) | (cell.loc_right >> 5 == 1) |
                         (cell.loc_down >> 5 == 1) | (cell.loc_left >> 5 == 1)):
                    cell.state = 'path'
                elif (cell.state in ['non_active', 'wall_prepare', 'near_support', 'far_support', 'corner_prepare']) & \
                        ((cell.loc_up >> 5 == 1) | (cell.loc_right >> 5 == 1) |
                         (cell.loc_down >> 5 == 1) | (cell.loc_left >> 5 == 1)):
                    cell.state = 'clear'
                elif cell.state == 'clear':
                    cell.state = 'empty'

        self.update_neighbours()

    def update_neighbours(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].up = self.grid[i - 1][j].state if i > 0 else ""
                self.grid[i][j].right = self.grid[i][j + 1].state if j < self.size - 1 else ""
                self.grid[i][j].down = self.grid[i + 1][j].state if i < self.size - 1 else ""
                self.grid[i][j].left = self.grid[i][j - 1].state if j > 0 else ""

                self.grid[i][j].loc_up = 0b0
                self.grid[i][j].loc_right = 0b0
                self.grid[i][j].loc_down = 0b0
                self.grid[i][j].loc_left = 0b0


def test(cell_auto, y_s, x_s, y_e, x_e, y_u, y_d, x_u, x_d):
    for i in range(cell_auto.size):
        for j in range(cell_auto.size):
            if (i >= y_u) & (i <= y_d) & (j >= x_u) & (j <= x_d):
                cell_auto.grid[i][j].state = 'wall'
    cell_auto.grid[y_u - 1][x_u - 1].wall_corner = True  # up-left
    cell_auto.grid[y_u - 1][x_d + 1].wall_corner = True  # up-right
    cell_auto.grid[y_d + 1][x_u - 1].wall_corner = True  # down-left
    cell_auto.grid[y_d + 1][x_d + 1].wall_corner = True  # down-right

    # start - end
    cell_auto.grid[y_s][x_s].state = 'init'
    cell_auto.grid[y_e][x_e].state = 'init'

    return cell_auto


if __name__ == "__main__":
    CA = CellAutoWall(20)

    root = tk.Tk()

    CA = test(CA, y_s=7, x_s=1, y_e=5, x_e=12, y_u=2, y_d=17, x_u=5, x_d=9)  # vertical wall
    # CA = test(CA, y_s=7, x_s=1, y_e=7, x_e=12, y_u=2, y_d=17, x_u=5, x_d=9)  # vertical wall, same level init
    # CA = test(CA, y_s=7, x_s=1, y_e=7, x_e=12, y_u=2, y_d=12, x_u=5, x_d=9)  # vertical wall, same paths
    # CA = test(CA, y_s=12, x_s=5, y_e=1, x_e=7, y_u=5, y_d=9, x_u=2, x_d=17)  # horizontal wall
    # CA = test(CA, y_s=12, x_s=5, y_e=1, x_e=5, y_u=5, y_d=9, x_u=2, x_d=17)  # horizontal wall, same level init
    # CA = test(CA, y_s=12, x_s=4, y_e=1, x_e=5, y_u=5, y_d=9, x_u=2, x_d=17)  # horizontal wall, near_support close far_support
    # CA = test(CA, y_s=10, x_s=4, y_e=1, x_e=5, y_u=5, y_d=9, x_u=2, x_d=17)  # horizontal wall, init near wall
    # CA = test(CA, y_s=10, x_s=4, y_e=5, x_e=5, y_u=6, y_d=9, x_u=2, x_d=17)  # horizontal wall, both inits near wall
    # CA = test(CA, y_s=12, x_s=2, y_e=1, x_e=7, y_u=8, y_d=9, x_u=5, x_d=10)  # one-side obstacle
    # CA = test(CA, y_s=12, x_s=4, y_e=1, x_e=7, y_u=8, y_d=9, x_u=16, x_d=17)  # without obstacles
    # CA = test(CA, y_s=12, x_s=4, y_e=1, x_e=12, y_u=8, y_d=15, x_u=10, x_d=17)  # up and right init
    # CA = test(CA, y_s=7, x_s=1, y_e=6, x_e=12, y_u=6, y_d=9, x_u=5, x_d=9)  # init one shift near wall
    # CA = test(CA, y_s=7, x_s=1, y_e=5, x_e=12, y_u=6, y_d=9, x_u=5, x_d=9)  # init one shift from wall

    CA.draw(root)
    root.mainloop()
