### Original code by [Mohammad Tomaraei] (2019)
### Modified by [@cemre10] for [FleetBattle-Bot] (2024)

from PIL import Image, ImageGrab
import random
from time import sleep
import win32api, win32con
from os import system
import traceback

### THESE COORDINATES ARE VALID FOR MY COMPUTER SCREEN (1920x1080). YOU COULD CHANGE IT! ###

# Constants for screen and game board coordinates
imageX1, imageY1, imageX2, imageY2 = 1023, 332, 1742, 1050 # These are the locations that you are going to capture
squareSize = 720 # Size of the Game Board. (720x720)
main_square_coordinates = (15, 15, 15 + imageX1 + squareSize, 15 + imageY1 + squareSize) # coordinates of Game Board
smallerSquareSize = 72 # Size of 1 entity of Game Board. (72x72)
game_finished = False # Boolean Variable that shows game finished or not

# To add logic on hit_around function define the ships
old_board = {}
board = {}
last_hit = ()

battleship = False # 5 square long
aircraft_carrier = False # 6 square size
cruiser = False # 4 square long
submarine = False # 4 square size 
destroyer = False # 3 square size
petrol_boat = False # 2 square size

# Function to capture screen
def capture_screen():
    return ImageGrab.grab(bbox=(imageX1, imageY1, imageX2, imageY2))

# Check if its our turn or not
def is_player_turn():
    global game_finished

    # Get the color of the indicator pixel
    indicator_pixel = (9,1071)  # Left bottom corner of screen. It can be any corner. When player turns change also corner colors change too
    finished_pixel = (100,100)  # If color becomes Dark Grey at this location than game finished
    img = ImageGrab.grab(bbox=(1, 1, 1920, 1080)) 
    indicator_color = img.getpixel(indicator_pixel)
    finished_color = img.getpixel(finished_pixel) 

    # Red : Enemies Turn , Blue : Our Turn , Dark Grey : Game Finised
    # print(f"Indicator Color: {indicator_color}") # if it is our turn, output must be [<20, >30, >90] 
    # EX: Our turn (11, 43, 106), Enemies turn (137, 19, 47), Game Finished (32, 32, 32)

    if all(value < 40 for value in finished_color):
        # Game Finished
        game_finished = True
        return False

    return (indicator_color[0]<20 and indicator_color[1]>30 and indicator_color[2]>90) # if its blue it ll return True, if its red it ll return False
 
# Function to analyze missed or succesful hits
def analyze_board(img):
    global old_board
    global board

    old_board = dict(board)

    # Crop the image to focus on the main square
    square_img = img.crop(main_square_coordinates)

    # Initialize an empty dictionary to represent the game board
    board = {}

    # Iterate through each square on the board
    for y in range(0, 10):
        for x in range(0, 10):
            # Calculate the pixel coordinates of the current square
            x_pix = main_square_coordinates[0] + x * smallerSquareSize
            y_pix = main_square_coordinates[1] + y * smallerSquareSize

            # Check if the pixel coordinates are within the bounds of the cropped image
            if 0 <= x_pix < square_img.width and 0 <= y_pix < square_img.height:
                # Convert the square image to RGB format
                rgb_im = square_img.convert('RGB')

                # Get the color of the current square
                coordinate_color = rgb_im.getpixel((x_pix, y_pix))
                #print(coordinate_color,end="")

                # Initialize the square status as 0 (empty)
                square_status = 0


                # Update the square status based on color conditions
                if all(value < 20 for value in coordinate_color):
                    square_status = 3 # If the color is black, Ship is down
                elif coordinate_color[2] < 50:
                    square_status = 2  # If the color is red, Ship shot
                elif all(value > 70 for value in coordinate_color):
                    square_status = 1  # If the color is white/gray, Missed shot

                # Store square information in the board dictionary
                board[x + 1, y + 1] = [square_status, x_pix, y_pix]

            else:
                print("Warning: Pixel coordinates out of bounds")

    return board

# Function to draw the board
def draw_board(board):
    system('cls') # Clear Output
    count = 0
    final_board = " " + "_"*21 + "\n"
    for square in board:
        if square[0] == 1:
            final_board += "| "
        final_board += str(board[square][0]).replace("0", "•").replace("1", "✖").replace("2", "✷").replace("3", "⚑") + " "

        if count == 9 and square[0] == 10:
            final_board += "|"
            break
        if square[0] == 10:
            count += 1
            final_board += "|\n"
    final_board += "\n " + "‾"*21
    return final_board

# Function to perform a click at a given screen position
def click(x, y):
    global last_hit

    smallSquareSize_win32api = 58
    startPoint_X_win32api = 814
    startPoint_Y_win32api = 263
    distance_win32api = 30
    z1 = x // smallerSquareSize
    z2 = y // smallerSquareSize

    last_hit = (z1 + 1, z2 + 1)

    x = int(startPoint_X_win32api + distance_win32api + smallSquareSize_win32api*z1)
    y = int(startPoint_Y_win32api + distance_win32api + smallSquareSize_win32api*z2)

    win32api.SetCursorPos((x, y)) # move the cursor to the position of (x, y)
    sleep(0.1) # To decrease Error ratio
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
    sleep(0.1) # To decrease Error ratio
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released

# Function to hit
def make_move(board):
    find_hits(board)

# Function to hit a random empty square
def hit_random(board):
    while True:
        random_y = random.randint(1, 10)
        if random_y % 2 == 0: # We dont need to shoot every square, half of it is enough.
            random_x = random.randrange(1, 11, 2) # If y is even x will be odd
        else:
            random_x = random.randrange(2, 11, 2) # If y is odd x will be even

        # Hit attempt possibilities: (-) : We ll not hit, (X) : we can hit
            # - X - X - X - X - X
            # X - X - X - X - X -
            # - X - X - X - X - X
            # X - X - X - X - X -
            # - X - X - X - X - X
            # X - X - X - X - X -
            # - X - X - X - X - X
            # X - X - X - X - X -
            # - X - X - X - X - X
            # X - X - X - X - X -
        # With this hits all ships can be found so we dont need to hit half of the squares

        if board[(random_x, random_y)][0] == 0:
            click(board[(random_x, random_y)][1], board[(random_x, random_y)][2])
            break       

# Function to find hit squares and hit the squares around it
def find_hits(board):
    hits = [] # Location of all Hits (Down ships are not included)
    for square in board:
        if board[square][0] == 2:
            hits.append(square)

    find_sunk_ships(board)

    if not hits:
        # If no hit square is found, hit a random empty square
        hit_random(board)

    hit_around(board, hits)

# Function to find down ships
def find_sunk_ships(board):
    global old_board
    global last_hit

    # If one of those ships sunk our program will not calculate that possibility
    global battleship
    global aircraft_carrier 
    global cruiser 
    global submarine 
    global destroyer 
    global petrol_boat 

    sunk_ships = []
    for square in board:
        if board[square][0] == 3:
            sunk_ships.append(square)

    old_hits = []
    for square in old_board:
        if old_board[square][0] == 2:
            old_hits.append(square)

    new_sunk = []
    for i in old_hits:
        if i in sunk_ships:
            new_sunk.append(i)
    
    if not new_sunk == []:
        new_sunk.append(last_hit)

    if len(new_sunk) == 6:
        aircraft_carrier = True
    
    elif len(new_sunk) == 5:
        battleship = True
    
    elif len(new_sunk) == 4:
        x, y = new_sunk[0]
        x1, y1 = new_sunk[1]
        x2, y2 = new_sunk[2]
        x3, y3 = new_sunk[3]

        if x == x1 and x1 == x2 and x2 == x3:
            cruiser = True
        
        elif y == y1 and y1 == y2 and y2 == y3:
            cruiser = True
        
        else:
            submarine = True
    
    elif len(new_sunk) == 3:
        destroyer = True
    
    elif len(new_sunk) == 2:
        petrol_boat = True

def click_caller(board, x, y):
    if (1 <= x <= 10) and (1 <= y <= 10) and board[(x, y)][0] == 0:
            click(board[(x, y)][1], board[(x, y)][2])
            return True           

def smart_hit(board, hit, count, bool1, bool2):
    if count == 1:
        x, y = hit[0]

        # Check and hit the square above, below, left, and right of the last hit square
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            return click_caller(board, new_x, new_y)

    elif count == 2:
        x1, y1 = hit[0]
        x2, y2 = hit[1]

        if x1 == x2:
            new_x, new_y = x1, y1 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1, y2 + 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2 - 1, y2
            if click_caller(board, new_x, new_y):
                return True

        if y1 == y2:
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2 + 1, y2
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1, y1 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2, y2 - 1
            if click_caller(board, new_x, new_y):
                return True

    elif count == 3 and bool1:
        x1, y1 = hit[0]
        x2, y2= hit[2]

        if x1 == x2:
            new_x, new_y = x1, y1 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2, y2 + 1
            if click_caller(board, new_x, new_y):
                return True
        
        if y1 == y2:     
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2 + 1, y2
            if click_caller(board, new_x, new_y):
                return True

    elif count == 3:
        x, y = hit[1]
        x1, y1 = hit[0]
        x2, y2= hit[2]

        if x1 == x2:
            new_x, new_y = x - 1, y
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x + 1, y
            if click_caller(board, new_x, new_y):
                return True
        
        if y1 == y2:
            new_x, new_y = x, y - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x, y + 1
            if click_caller(board, new_x, new_y):
                return True

        if x1 - 1 == x and y1 + 1 == y:
            new_x, new_y = x2 + 1, y2
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2, y2 + 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1 - 1, y1
            if (1 <= new_x <= 10) and (1 <= new_y <= 10) and board[(new_x, new_y)][0] == 0:
                if click_caller(board, new_x, new_y):
                    return True

        if x1 + 1 == x2 and y1 + 1 == y2:
            new_x, new_y = x - 1, y
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x, y + 1
            if click_caller(board, new_x, new_y):
                return True

            new_x, new_y = x + 1, y
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x, y - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1 + 1, y1
            if click_caller(board, new_x, new_y):
                return True

            new_x, new_y = x1, y1 + 1
            if click_caller(board, new_x, new_y):
                return True
            
        if x - 1 == x2 and y + 1 == y2:
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1, y1 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x, y + 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1, y1 - 1
            if click_caller(board, new_x, new_y):
                return True

    elif count == 4 and bool2:
        x1, y1 = hit[0]
        x2, y2 = hit[1]
        x3, y3 = hit[2]
        x4, y4 = hit[3]

        if (x1 == x3 and y1 == y3 - 1) and (x1 == x2 - 1 and y1 == y2) and (x2 == x3 + 1 and y2 == y3 - 1) and (x2 == x4 and y2 == y4 - 1):
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2, y2 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2 + 1, y2
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x4, y4 + 1
            if click_caller(board, new_x, new_y):
                return True            
        
        if (x1 == x4 and x1 == x3 - 1) and (y1 == y4 - 2 and y1 == y3 - 1):
            new_x, new_y = x3, y3 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x3, y3 + 1
            if click_caller(board, new_x, new_y):
                return True
        
        if (x1 == x3 - 2 and x1 == x4 - 1) and (y1 == y3 and y1 == y4 - 1):
            new_x, new_y = x4 - 1, y4
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x4 + 1, y4
            if click_caller(board, new_x, new_y):
                return True
        
        if (x1 == x2 + 1 and x1 == x4 - 1) and (y1 == y2 - 1 and y1 == y4 - 1):
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x1 + 1, y1
            if click_caller(board, new_x, new_y):
                return True

        if (x1 == x2 + 1 and x1 == x4) and (y1 == y2 - 1 and y1 == y4 - 2):
            new_x, new_y = x2, y2 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2, y2 + 1
            if click_caller(board, new_x, new_y):
                return True
    
    elif count == 4:
        x1, y1 = hit[0]
        x2, y2 = hit[3]

        if y2 == y1:
            new_x, new_y = x1 - 1, y1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2 + 1, y2
            if click_caller(board, new_x, new_y):
                return True
        
        if x2 == x1:
            new_x, new_y = x1, y1 - 1
            if click_caller(board, new_x, new_y):
                return True
            
            new_x, new_y = x2, y2 + 1
            if click_caller(board, new_x, new_y):
                return True

    elif count == 5:
        x1, y1 = hit[0]
        x2, y2 = hit[1]
        x3, y3 = hit[2]
        x4, y4 = hit[3]
        x5, y5 = hit[4]

        if (x1 == x4 and x1 == x3 - 1) and (y1 == y4 - 2 and y1 == y3 - 1):
            if x1 == x5 - 1 and y1 == y5 - 2:
                new_x, new_y = x5, y5 + 1
                if click_caller(board, new_x, new_y):
                    return True
            if x1 == x2 - 1 and y1 == y2:
                new_x, new_y = x2, y2 - 1
                if click_caller(board, new_x, new_y):
                    return True
        
        if (x1 == x3 - 2 and x1 == x4 - 1) and (y1 == y3 and y1 == y4 - 1):
            if x1 == x4 and y1 == y4 - 1:
                new_x, new_y = x4 - 1, y4
                if click_caller(board, new_x, new_y):
                    return True
            
            if x1 == x5 - 2 and y1 == y5 - 1:
                new_x, new_y = x5 + 1, 54
                if click_caller(board, new_x, new_y):
                    return True
            
        if (x1 == x2 + 1 and x1 == x4 - 1) and (y1 == y2 - 1 and y1 == y4 - 1):
            if x1 == x5 - 2 and y1 == y5 - 1:
                new_x, new_y = x1 - 1, y1
                if click_caller(board, new_x, new_y):
                    return True
            
            if x2 == x3 + 2 and y2 == y3 - 1:
                new_x, new_y = x2 + 1, y2
                if click_caller(board, new_x, new_y):
                    return True

        if (x1 == x2 + 1 and x1 == x4) and (y1 == y2 - 1 and y1 == y4 - 2):
            if x1 == x5 - 1 and y1 == y5 - 2:
                new_x, new_y = x1, y1 - 1
                if click_caller(board, new_x, new_y):
                    return True

            if x1 == x4 + 1 and y1 == y4 - 2:    
                new_x, new_y = x4, y4 + 1
                if click_caller(board, new_x, new_y):
                    return True
        
        if (x1 == x4 and x1 == x5 - 1) and (y1 == y4 - 1 and y1 == y5 - 1):
            new_x, new_y = x4 - 1, y4
            if click_caller(board, new_x, new_y):
                    return True

    else:
        return False

# Function to hit the squares around the last hit square
def hit_around(board, hits):
    # If one of those ships sunk our program will not calculate that possibility
    global battleship
    global aircraft_carrier 
    global cruiser 
    global submarine 
    global destroyer 
    global petrol_boat 

    hit_counts = len(hits)

    if not petrol_boat and hit_counts == 1:
        if smart_hit(board, hits, hit_counts, False, False):
            return True

    if not destroyer and (hit_counts == 1 or hit_counts == 2):
        if smart_hit(board, hits, hit_counts, False, False):
            return True
  
    if not submarine and (1 <= hit_counts <= 3):
        if smart_hit(board, hits, hit_counts, False, False):
            return True

    if not cruiser and (1 <= hit_counts <= 3):
        if smart_hit(board, hits, hit_counts, True, False):
            return True

    if not aircraft_carrier and (1 <= hit_counts <= 5):
        if smart_hit(board, hits, hit_counts, False, True):
            return True
            
    if not battleship and (1 <= hit_counts <= 4):
        if smart_hit(board, hits, hit_counts, True, False):
            return True

    # If there is any logical error
    for square in hits:
        x, y = square
        # Check and hit the square above, below, left, and right of the last hit square
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if (1 <= new_x <= 10) and (1 <= new_y <= 10) and board[(new_x, new_y)][0] == 0:
                click(board[(new_x, new_y)][1], board[(new_x, new_y)][2])
                return True

# Function to start new game
def start_game(x, y, z):
    sleep(z) # Delay to wait ads, simulations, finding a game
    win32api.SetCursorPos((x, y))
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
    sleep(0.1) # To decrease Error ratio
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released

# Main loop
while True:
    try:
        # Check if it's the player's turn
        if is_player_turn(): # Our Turn

            screen_img = capture_screen()

            game_board = analyze_board(screen_img)

            print(draw_board(game_board))
   
            make_move(game_board)
            sleep(2.8) # A delay to get exact colour. (Ship Explosion duration : (2.2-2.5)s)

        elif not game_finished: # Enemies Turn

            screen_img = capture_screen()

            game_board = analyze_board(screen_img)

            print(draw_board(game_board))

            print("Enemies Turn")

            sleep(3) # Delay to slow down program

        else: # Game Finished
            print(" Game Finished ")

            x = 1280
            y = 135
            start_game(x, y, 10) # Close daily play window

            x = 1143
            y = 160
            start_game(x, y, 2) # Close Possible Award Window

            x = 1280
            y = 135
            start_game(x, y, 4) # One more time to be sure for some possible cases

            x = 1143
            y = 160
            start_game(x, y, 4) # One more time to be sure for some possible cases

            x = 1300 # Click Continue Button
            y = 780
            start_game(x, y, 2) 
            
            x = 1480 # Close Ad
            y = 50
            start_game(x, y, 60) # Waiting the Ad ( All ads have different close button so we must wait )
            start_game(x, y, 10) # Waiting the Ad ( possible 2. ad )
            start_game(x, y, 10) # Waiting the Ad ( possible 3. ad )

            x = 865
            y = 580
            start_game(x, y, 5) # Click Start Button

            x = 1420
            y = 480
            start_game(x, y, 35) # Waiting to find game

            sleep(5)

            game_finished = False

            battleship = False # 5 square long
            aircraft_carrier = False # 6 square size
            cruiser = False # 4 square long
            submarine = False # 4 square size 
            destroyer = False # 3 square size
            petrol_boat = False # 2 square size
          
    except Exception as e:
        # Handle any exceptions 
        print(f"An error occurred: {e}")
        traceback.print_exc()

    # Add a delay to control the loop frequency
    sleep(0.1)
