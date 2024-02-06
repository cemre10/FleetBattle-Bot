### Original code by [Mohammad Tomaraei] (2019)
### Modified by [@cemre10] for [FleetBattle-Bot] (2024)

from PIL import Image, ImageGrab
import random
from time import sleep
import win32api, win32con
from os import system

### THESE COORDINATES ARE VALID FOR MY COMPUTER SCREEN (1920x1080). YOU COULD CHANGE IT! ###

# Constants for screen and game board coordinates
imageX1, imageY1, imageX2, imageY2 = 1023, 332, 1742, 1050 # These are the locations that you are going to capture
squareSize = 720 # Size of the Game Board. (720x720)
main_square_coordinates = (15, 15, 15 + imageX1 + squareSize, 15 + imageY1 + squareSize) # coordinates of Game Board
smallerSquareSize = 72 # Size of 1 entity of Game Board. (72x72)
game_finished = False

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

            # Print the calculated coordinates for debugging
            #print(f"({x_pix}, {y_pix})",end="")

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

        #print("\n")

    return board

# Function to draw the board
def draw_board(board):
    system('cls') # Clear Output
    count = 0
    final_board = " " + "_"*21 + "\n"
    for square in board:
        if square[0] == 1:
            final_board += "| "
        final_board += str(board[square][0]).replace("0", "•").replace("1", "✖").replace("2", "✷").replace("3", "★") + " "

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
    smallSquareSize_win32api = 58
    z1 = x // smallerSquareSize
    z2 = y // smallerSquareSize
    x = int(814 + 30 + smallSquareSize_win32api*z1)
    y = int(263 + 30 + smallSquareSize_win32api*z2)

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

            # We have found a hit square, now check and hit the squares around it
            #hit_around_last(board, square)
            #break
    if not hits:
        # If no hit square is found, hit a random empty square
        hit_random(board)

    for square in hits:
        if hit_around_last(board, square, hits):
            break
    
# Function to hit the squares around the last hit square
def hit_around_last(board, hit_square, hits):
    x, y = hit_square

    # Check and hit the square above, below, left, and right of the last hit square
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if (1 <= new_x <= 10) and (1 <= new_y <= 10) and board[(new_x, new_y)][0] == 0:
            click(board[(new_x, new_y)][1], board[(new_x, new_y)][2])
            return True
    else:
        # If no valid square around hit square is found we ll try other hit square
        return False

def start_game(x, y, z):
    sleep(z)
    win32api.SetCursorPos((x, y))
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
    sleep(0.1) # To decrease Error ratio
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released


# Main loop
while True:
    try:
        # Check if it's the player's turn
        if is_player_turn():

            screen_img = capture_screen()

            game_board = analyze_board(screen_img)

            print(draw_board(game_board))
   
            make_move(game_board)
            sleep(2.8) # A delay to get exact colour. (Ship Explosion duration : (2.2-2.5)s)

        elif not game_finished:

            screen_img = capture_screen()

            game_board = analyze_board(screen_img)

            print(draw_board(game_board))

            print("His turn")

        else:
            print(" Game Finished ")

            x=1300 # Click Continue Button
            y=780
            start_game(x,y,10)
            
            x = 1480 # Close Ad
            y = 50
            start_game(x, y, 30) # Waiting the Ad
            start_game(x, y, 15) # Waiting the Ad
            start_game(x, y, 15) # Waiting the Ad

            x = 865
            y = 580
            start_game(x, y, 5) # Click Start Button

            x = 1420
            y = 480
            start_game(x,y,35) # Waiting to find game

            sleep(5)


            
    except Exception as e:
        # Handle any exceptions 
        print(f"An error occurred: {e}")

    # Add a delay to control the loop frequency
    sleep(0.1)