import pygame, sys, time
import random

pygame.init()

# images for Tiles and Buttons
TILE = pygame.image.load("buttontemplete.png")
PUSHED_BUTTON = pygame.image.load("Pushed_button.png")
RELISED_BUTTON = pygame.image.load("Relised_button.png")
ICON = pygame.image.load("icon.png")
# Sound for sliding tiles
SOUND = pygame.mixer.Sound("slide.wav")

# Set the Constant for Tile width and height
BUTTONRECT = TILE.get_rect()
TILE_WIDTH = BUTTONRECT[2] - BUTTONRECT[0]
TILE_HEIGHT = BUTTONRECT[3] - BUTTONRECT[1]

class FifteenGUI:
    """
    Main GUI class
    """
    def __init__(self, puzzle):
        """
        Create screen timer and main loop. register event handlers
        """
        self._puzzle = puzzle
        self._puzzle_height = puzzle.get_height()
        self._puzzle_width = puzzle.get_width()
        self._solution = ""
        self._current_moves = ""
        self._shuffle_moves = ""
        self._title = pygame.display.set_caption('Feefteen Puzzle')
        self._screen = pygame.display.set_mode((self._puzzle_width * TILE_WIDTH * 2, 
                                                self._puzzle_height * TILE_HEIGHT + TILE_WIDTH * 3))
        pygame.display.set_icon(ICON)
        self._text_font = pygame.font.Font(None, 30)
        self._clock = pygame.time.Clock()                   
        self._fps = 5                                      # number of frames per secod
        self._finished = False
        self._game_finished = False


    def tick(self):
        """
        Timer for incrementally displaying computed solution.
        """
        if self._solution == "":
            return
        direction = self._solution[0]
        self._solution = self._solution[1:]
        try:
            self._puzzle.update_puzzle(direction)
        except:
            pass

    def shuffle_tick(self):
        """
        Timer for incrementally displaying computed random shuffle moves
        """
        
        if self._shuffle_moves == "":
            return
        direction = self._shuffle_moves[0]
        self._shuffle_moves = self._shuffle_moves[1:]
        try:
            self._puzzle.update_puzzle(direction)
            
        except:
            pass

    def shuffle(self):
        """
        Shufles the puzzle with random mooves
        """
        sensless_moves = {"l":"r", "r":"l", "d":"u", "u": "d"}      # To avoid zero tile to go back and forward 
        self._shuffle_moves = random.choice(["r", "d"])             # So to check whether next move will be sensless or not
                                                                    # the very first move must be something. 
        move_list = ['l', 'r', 'd','u']
        new_puzzle = self._puzzle.clone()

        while len(self._shuffle_moves) < 10 * max(self._puzzle_height, self._puzzle_width):
            move = random.choice(move_list)
            if sensless_moves[move] != self._shuffle_moves[-1]:
                try:
                    new_puzzle.update_puzzle(move)
                    self._shuffle_moves += move
                except:
                    pass

    def solve(self):
        """
        Event handler to generate solution string for given configuration
        """
        new_puzzle = self._puzzle.clone()
        self._solution = new_puzzle.solve_puzzle()

    def print_moves(self):
        """
        Event handler to print and reset current move string
        """
        print (self._current_moves)
        self._current_moves = ""

    def enter_moves(self, txt):
        """
        Event handler to enter move string
        """
        self._solution = txt

    def key(self, event): 
        """
        Event hendler for pushing kays
        """  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                try:
                    self._puzzle.update_puzzle("u")
                    self._current_moves += "u"
                    SOUND.play()
                except:
                    print ("Invalid moove: UP")
            elif event.key == pygame.K_DOWN:
                try:
                    self._puzzle.update_puzzle("d")
                    self._current_moves += "d"
                    SOUND.play()
                except:
                    print ("Invalid moove: DOWN")
            elif event.key == pygame.K_LEFT:
                try:
                    self._puzzle.update_puzzle("l")
                    self._current_moves += "l"
                    SOUND.play()
                except:
                    print ("Invalid moove: LEFT")
            elif event.key == pygame.K_RIGHT:
                try:
                    self._puzzle.update_puzzle("r")
                    self._current_moves += "r"
                    SOUND.play()
                except:
                    print ("Invalid moove: RIGHT")

    def button_handler(self, image, location, screen, pushable = False, text = None,
                       pushed_image = None, push_action = None):
        """
        handler for drawing button shape images and text on them.
        """
        mouse = pygame.mouse.get_pos()                  # x an y position of mouse
        click = pygame.mouse.get_pressed()              # returns tuple with 3 zeros if mouse is not clicked, 1 if it is.
                                                        # eg (0, 0, 0) if not clicked, (1, 0, 0) if clicked left button 
                                                        
        image_center = image.get_rect(center = (location))
        screen.blit(image, image_center)

        try:
            pushed_center = pushed_image.get_rect(center = (location))
        except:
            pass

        if pushable:
            screen.blit(image, image_center)
            if image_center[0] < mouse[0] < image_center[0] + image_center[2] and image_center[1] < mouse[1] < image_center[1] + image_center[3] and click[0] == 1:
                if push_action == pygame.quit:
                    push_action()
                    quit()
                else:
                    try:
                        push_action()
                        screen.blit(pushed_image, pushed_center)
                    except:
                        pass
                
            elif image_center[0] < mouse[0] < image_center[0] + image_center[2] and image_center[1] < mouse[1] < image_center[1] + image_center[3] :
                screen.blit(image, (image_center[0], image_center[1] - 1))
        try:
            # to display text if there are some
            text_image = self._text_font.render(text, True, (0,0,0))
            text_center = text_image.get_rect(center = (location))
            if text != '0':
                screen.blit(text_image, (text_center))
        except:
            pass


    def intro_loop(self):
        """
        Intro page of game
        """
        while not self._finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self._screen.fill((0,240,250))    
            self.button_handler(RELISED_BUTTON, (self._puzzle_width * TILE_WIDTH, 
                                         self._puzzle_height * TILE_HEIGHT ), self._screen, True, "Quit", PUSHED_BUTTON, pygame.quit)
            self.button_handler(RELISED_BUTTON, (self._puzzle_width * TILE_WIDTH, 
                                         self._puzzle_height * TILE_HEIGHT - TILE_HEIGHT), self._screen, True, "Start", PUSHED_BUTTON, self.game_loop)
            # after quit button is pushed in game loop display is updatet anyway. so it throws error.
            try:
                pygame.display.update()
            except:
                pass

    def game_loop(self):
        """
        Loop to start the GUI and clock
        """
        self._finished = True
        while not self._game_finished:
            self._clock.tick(self._fps)
            self.tick()
            self.shuffle_tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                self.key(event)
            self._screen.fill((0,250,250))
           
            for row in range(self._puzzle_height):
                for col in range(self._puzzle_width):
                    tile_num = self._puzzle.get_number(row, col)
                    self.button_handler(TILE, (TILE_WIDTH*self._puzzle_width / 2 + TILE_WIDTH / 2 + TILE_WIDTH * col, 
                                                              TILE_HEIGHT / 2 + TILE_HEIGHT * row + TILE_HEIGHT), self._screen, False, str(tile_num))
            self.button_handler(RELISED_BUTTON, (self._puzzle_width * TILE_WIDTH  -  TILE_WIDTH, 
                                         self._puzzle_height * TILE_HEIGHT + TILE_WIDTH * 2), self._screen, True, "Solve", PUSHED_BUTTON, self.solve)
            self.button_handler(RELISED_BUTTON, (self._puzzle_width * TILE_WIDTH  + TILE_WIDTH, 
                                         self._puzzle_height * TILE_HEIGHT + TILE_WIDTH * 2), self._screen, True, "Shuffle", PUSHED_BUTTON, self.shuffle)
            
            pygame.display.update()
