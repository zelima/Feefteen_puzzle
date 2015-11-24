"""
Loyd's Fifteen puzzle - solver and visualizer
Project written by Irakli Mchedlishvili for Python learning course "Principals of Computing" by Rice university (Online Course)

Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

"""
import FifteenGUI

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """
    
    def __init__(self, puzzle_height, puzzle_width, initial_grid = None ):
        """
        Initializes puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row                     # fils Empty grid with numbers from 0 to width*height-1
                       for col in range(self._width)]               # for e.g. test = Puzzle(2, 2)
                      for row in range(self._height)]               #          print  (test._grid) >>> ([0, 1], [2, 3])

        if initial_grid != None:
            for row in range(puzzle_height):                        # initialaises already exsiting grid, if it is passed
                for col in range(puzzle_width):                     # for e.g. test = Puzzle(2, 2, ([3, 1], [2, 0]))
                    self._grid[row][col] = initial_grid[row][col]   #          print  (test._grid) >>> ([3, 1], [2, 0])

    def __str__(self):
        """
        Generates string representaion for puzzle
        Returns a string
        """

        ans = ""
        for row in range(self._height):                             # 2D string representatin of grid 
            ans += str(self._grid[row])                             # for e.g. test = puzzle(2, 3)
            ans += "\n"                                             #          print (test) >>> [0, 1, 2]
        return ans                                                  #                           [3, 4, 5]

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Makes a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    # End of firs part
    ###############################################################

    def current_position(self, solved_row, solved_col):
        """
        Locates the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)          # velue of tile that should be at this position
                                                                        # e.g. in 4x4 puzzle at position (3, 2) should be 14 (2 + 3 * 4)
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)                                   # the actual position of that tile
        assert False, "Value " + str(solved_value) + " not found"       # throws error if apropriate value should not be on the grid

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)                # identifies where 0 tile is

        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction                      # notifies if left move is invalid (0 tile  goes outside grid)
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]     # switches places for 0 tile and the tile that is on the left of it
                self._grid[zero_row][zero_col - 1] = 0                                  # set the tiles value as zero
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction        #
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]     # everything same but on right side now
                self._grid[zero_row][zero_col + 1] = 0                                  # 
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction                         # asserts if invalid move is given (none of "l";"r";"u" or "d")

    # End of second part
    ################################################################

    def lower_row_invariant(self, target_row, target_col):
        """
        Checks whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)

        * At the targeted position should be 0 tile.
        * Every tile should be solved in the lower raws. e.g. if targeted tile position is (2,2) in 5x5 puzzle.
          every tile in bottom 2 rows should be solved.
        * Every tile that is on the right in the same row should be solved. 

        Returns a boolean

        """
        answer = True
        column = self.get_width()-1                                                 # variable to chek all tiles from most right tile till most left
        row = self.get_height()-1 

        if self.get_number(target_row, target_col) != 0:                            # returns false if velue of the targeted tile is not 0
            return  False
        while row > target_row or column > target_col:                              # one by one cheks values of all the tiles from
            if self.get_number(row, column) !=  row*self.get_width() + column:      # rigtmost bottom tile till targeted position if
                return False                                                        # they are on their apropriate places 
            row = (row * self.get_width() + column -1) // self.get_height()         # changes row number after every heightlength move
            column = (row * self.get_width() + column -1) % self.get_width()        # changes col number from widthlength to zero and back to widthlength
        return answer

    def solve_interior_tile(self, target_row, target_col):
        """
        Places correct tile that is not from fist column 
        or first two rows at target position
        Updates puzzle and returns a move string recursively      
        """
        zero = self.current_position(0, 0)                                          
        target = self.current_position(target_row, target_col)                      # position where targeted tile is
        
        if target[0] > 0:                       
            # if targeted tile is not in first row (top row),  
            # to make it go on the right we shoul go on sircles traveling
            # around from top of targeted tile, so we did not 
            # mass up alreade solved tiles that are in lower rows
            right = 'urrdl'                     #string that makes targeted tile go right      
            go_left = ['', 'ld', 'ulld']        # three options for zero tile to stand on the left of targeted tile (so that it goes on another circle)
        else:
        # case when zero tile cant go up, because targeted tile is on top row. it should circle from down
            right = 'drrul'                     
            go_left = ['', 'ld', 'dllu']        # three options for zero tile to go on left
        
        left = 'r'      #sting that makes targeted tile go left
        down = 'dru'    # and down

        # base case for recursion when targeted tile is on it's position
        # returns last string that takes zero tile to the left side of solved tile
        if target == (target_row, target_col): 
            # cheks wich of three posible options take zero tile to the left of solved
            for string in go_left: 
                # creates and updetes clone puzzle to chek                     
                clone = self.clone()                    
                clone.update_puzzle(string)             
                if clone.current_position(0,0) == (target[0], target[1] - 1):
                    self.update_puzzle(string)
                    return string                       # last part of string that solves targeted tile
        elif zero == (target_row, target_col):
            # Generates string for zero tile to go
            # at the position of targeted tile
            string = (zero[0] - target[0]) * 'u' + (zero[1] - min(zero[1], target[1])) * 'l' + (target[1] - min(zero[1], target[1])) * 'r'
            self.update_puzzle(string)
            return string + self.solve_interior_tile(target_row, target_col)  #returns the first parto of string that solves targeted tile in recursive way
        else:
            # body of recursion to take tile at targete row and column
            # first left or right. and than down.
            for left_string in go_left:
                clone = self.clone()
                clone.update_puzzle(left_string)
                if clone.current_position(0, 0) == (target[0], target[1] - 1):
                    # when zero tile is on the left sid of targeted tile
                    self.update_puzzle(left_string)
                    if target[1] > target_col:
                        # take tile to the left
                        string = left
                        self.update_puzzle(string)
                        return left_string + string + self.solve_interior_tile(target_row, target_col)
                    elif target[1] < target_col:
                        # take tile to the right
                        string = right
                        self.update_puzzle(string)
                        return left_string + string + self.solve_interior_tile(target_row, target_col)
                    else:
                        # take tile down
                        string = down
                        self.update_puzzle(string)
                        return left_string + string + self.solve_interior_tile(target_row, target_col)
            
    def solve_col0_tile(self, target_row):
        """
        Solves tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string recursevely
        """
        zero = self.current_position(0, 0)
        target = self.current_position(target_row, 0)

        # ufter taking zero tile to the position of
        # tageted tile it is either already on the right side of targeted 
        # tile or if tageted tile was at upper leftmost  corner, above it 
        go_right = ['', 'rd']

        if target[0] > 0:
            left = "ulldr"        
        else:
            left = "dllur"
        down = 'dlu' 
                              
        # base case fo recursion.
        # returns string tu take zero tail to the rightmost column of next (uper) row 
        if target == (target_row, 0):
            string = "r" * (self.get_width()-1)
            self.update_puzzle(string)
            return string
        # Ganerates string to take zero tile to the position of tageted tile.
        elif zero == (target_row, 0):
            string = (zero[0] - target[0]) * 'u' + (zero[1] - min(zero[1], target[1])) * 'l' + (target[1] - min(zero[1], target[1])) * 'r'
            self.update_puzzle(string)
            return string + self.solve_col0_tile(target_row)
        else:
            for direction in go_right:
                clone = self.clone()
                clone.update_puzzle(direction)
                if clone.current_position(0, 0) == (target[0], target[1] + 1):
                    self.update_puzzle(direction)
                    if target[1] > 0:
                        # takes tile to the left
                        string = left
                        self.update_puzzle(string)
                        return direction + string + self.solve_col0_tile(target_row)
                    elif target[0] < target_row - 1:
                        #takes tile down
                        string = down
                        self.update_puzzle(string)
                        return direction + string + self.solve_col0_tile(target_row)
                    else:
                        string = 'ulddrulurddlu'   # last combination of string that makes targeted tile to fit in it's position
                        self.update_puzzle(string)
                        return direction + string + self.solve_col0_tile(target_row)                        

    def row0_invariant(self, target_col):
        """
        Checks whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)

        * At the targeted tile position should be zero tile
        * Eeverything to the right or under targeted tile should be solved except leftmost upper 2x2 corner

        Returns a boolean
        """
        answer = True
        if self.current_position(0, 0) != (0, target_col):
            answer = False
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if col >= target_col or row >= 2:
                    if self.current_position(row, col) != (row, col) and self.current_position(0, 0) != (row, col):
                        return False
        return answer    

    def row1_invariant(self, target_col):
        """
        Checks whether the puzzle satisfies the row one invariant
        at the given column (col > 1)

        * At the targeted tile position should be zero tile
        * Eeverything to the right or under targeted tile should be solved.

        Returns a boolean
        """
        answer = True
        if self.current_position(0,0) != (1, target_col):
            answer = False
        for row in range(1, self.get_height()):
            for col in range(self.get_width()):
                if col >= target_col+1 or row >= 2:
                    if self.current_position(row, col) != (row, col):
                        answer = False
        return answer 
    
    def solve_row0_tile(self, target_col):
        """
        Solves the tile in row zero at the specified column
        Updates puzzle and returns a move string recursively
        """
        # idea of sloving this part is same as earlyer 
        # just with different tile mooving logic (as needed)
        
        go_down = ['', 'dr']
        zero = self.current_position(0, 0)
        target = self.current_position(0, target_col)

        left = 'lurdl'
        right = 'ruldr'

        if target == (0, target_col):
            self.update_puzzle('d')
            return 'd'
        elif zero == (0, target_col):
            string = 'l' * (target_col - target[1]) + 'd'* target[0]
            self.update_puzzle(string)
            return string + self.solve_row0_tile(target_col)
        elif target == (0, target_col - 1):
            for direction in go_down:
                clone = self.clone()
                clone.update_puzzle(direction)
                if clone.current_position(0, 0) == (target[0] +1, target[1]):
                    self.update_puzzle(direction)
                    string = 'lurrdluldrruld'
                    self.update_puzzle(string)                    
                    return direction + string                
        else:
            for direction in go_down:
                clone = self.clone()
                clone.update_puzzle(direction)
                if clone.current_position(0, 0) == (target[0] + 1, target[1]):
                    self.update_puzzle(direction)
                    if target[1] > target_col - 1:
                        string = left
                        self.update_puzzle(string)
                        return direction + string + self.solve_row0_tile(target_col)
                    else:
                        string = right
                        self.update_puzzle(string)
                        return direction + string + self.solve_row0_tile(target_col)       

    def solve_row1_tile(self, target_col):
        """
        Solves the tile in row one at the specified column
        Updates puzzle and returns a move string recursively
        """
        # idea of sloving this part is same as earlyer 
        # just with different tile mooving logic (as needed)

        go_up = ['', 'ur']
        zero = self.current_position(0, 0)
        target = self.current_position(1, target_col)
        right = 'rdlur'

        if target == (1, target_col):
            for direction in go_up:
                clone = self.clone()
                clone.update_puzzle(direction)
                if clone.current_position(0, 0) == (target[0] - 1, target[1]):
                    self.update_puzzle(direction)
                    return direction
        elif zero == (1, target_col):
            string = 'l' * (zero[1] - target[1]) + (1 - target[0]) * 'u'
            self.update_puzzle(string)
            return string + self.solve_row1_tile(target_col)
        else:
            for direction in go_up:
                clone = self.clone()
                clone.update_puzzle(direction)
                if clone.current_position(0, 0) == (target[0] - 1, target[1]):
                    self.update_puzzle(direction)
                    string = right
                    self.update_puzzle(string)
                    return direction + string + self.solve_row1_tile(target_col)

    def solve_2x2(self):
        """
        Solves the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string recursively
        """
        zero = self.current_position(0, 0)
        if self.current_position(0, 0) == (0, 0) and self.current_position(0, 1) == (0, 1):
            return ''
        else:
            to_corner = 'u' * zero[0] + 'l' * zero[1]
            string = 'drul'
            self.update_puzzle(to_corner + string)
            return to_corner + string + self.solve_2x2()
               
    def solve_puzzle(self):
        """
        Generates a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        height, width = self.get_height() - 1, self.get_width() - 1
        zero = self.current_position(0, 0)
        go_to_corner = (height - zero[0]) * 'd' + (width - zero[1]) * 'r'
        self.update_puzzle(go_to_corner)
        row_cont = 0
        col_cont = 0
        answer = go_to_corner

        while self.current_position(0, 0)[0] > 1:
            if self.current_position(0, 0)[1] > 0:
                answer += self.solve_interior_tile(height - row_cont, width - col_cont)
                col_cont += 1
                assert self.lower_row_invariant(height - row_cont, width - col_cont)
            else:
                answer += self.solve_col0_tile(height - row_cont)
                row_cont += 1
                col_cont = 0
                assert self.lower_row_invariant(height - row_cont, width - col_cont)
        while self.current_position(0, 0)[1] > 1:
            if self.current_position(0, 0)[0] == 1:
                answer += self.solve_row1_tile(width - col_cont)
                row_cont += 1
                assert self.row0_invariant(width - col_cont)
            else:
                answer += self.solve_row0_tile(width - col_cont)
                row_cont -= 1
                col_cont += 1
                assert self.row1_invariant(width - col_cont)
        answer += self.solve_2x2()
        return answer 
 


FifteenGUI.FifteenGUI(Puzzle(4, 4)).intro_loop()
