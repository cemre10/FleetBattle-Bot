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
main_square_coordinates = (15, 15, 15 + imageX1 + squareSize, 15 + imageY1 + squareSize) 
smallerSquareSize = 72 # Size of 1 entity of Game Board. (72x72)

# Function to capture screen
def capture_screen():
    return ImageGrab.grab(bbox=(imageX1, imageY1, imageX2, imageY2))

# Function to perform a click at a given screen position
def click(x, y):
    smallSquareSize_win32api = 58
    z1 = x // smallerSquareSize
    z2 = y // smallerSquareSize
    x = int(814 + 30 + smallSquareSize_win32api*z1)
    y = int(263 + 30 + smallSquareSize_win32api*z2)

    win32api.SetCursorPos((x, y)) # move the cursor to the position of (x, y)
    sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
    sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
   #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released

# Check if its our turn or not
def is_player_turn():
    # Get the color of the indicator pixel
    indicator_pixel = (9,1071)  # Left bottom corner of screen. It can be any corner. When player turns change also corner colors change too
    img = ImageGrab.grab(bbox=(1, 1, 1920, 1080)) # 
    indicator_color = img.getpixel(indicator_pixel)

    # Red : Enemies Turn , Blue : Our Turn 
    # print(f"Indicator Color: {indicator_color}") # if it is our turn, output must be [<20, >30, >90] 
    # EX: Our turn (11, 43, 106), Enemies turn (137, 19, 47)

    return (indicator_color[0]<20 and indicator_color[1]>30 and indicator_color[2]>90) # if its blue it ll return True, if its red it ll return False


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


# Function to draw a 2D representation of the board
def draw_board(board):
    system('cls') # Clear Output
    count = 0
    final_board = " " + "_"*22 + "\n"
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
    final_board += "\n " + "‾"*22
    return final_board

# Function to find and hit the last hit square or hit a random empty square
def make_move(board):
    # Implement the logic to decide the next move
    
    # Example: Call the hit_random function for simplicity
    hit_random(board)
# Function to hit a random empty square
def hit_random(board):
    while True:
        random_x = random.randint(1, 10)
        random_y = random.randint(1, 10)
        if board[(random_x, random_y)][0] == 0:
            # print("[RH] Clicking on:", random_x, random_y)
            #print(board[(random_x, random_y)][1], board[(random_x, random_y)][2])
            click(board[(random_x, random_y)][1], board[(random_x, random_y)][2])
            break
# Function to find the last hit square and hit the squares around it
def find_last_hit(board):
    for square in board:
        if board[square][0] == 2:
            # We have found a hit square, now check and hit the squares around it
            hit_around_last(board, square)
            break
    else:
        # If no hit square is found, hit a random empty square
        hit_random(board)
# Function to hit the squares around the last hit square
def hit_around_last(board, last_hit_square):
    x, y = last_hit_square

    # Check and hit the square above, below, left, and right of the last hit square
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if (1 <= new_x <= 10) and (1 <= new_y <= 10) and board[(new_x, new_y)][0] == 0:
            print("[FLH] Clicking on:", new_x, new_y)
            click(board[(new_x, new_y)][1], board[(new_x, new_y)][2])
            break
    else:
        # If no valid square around the last hit square is found, hit a random empty square
        hit_random(board)

# Main loop
while True:
    try:

        # Check if it's the player's turn
        if is_player_turn():

            screen_img = capture_screen()

            game_board = analyze_board(screen_img)

            # Print or visualize the game board
            print(draw_board(game_board))

            # Make a move (random hit)      
            make_move(game_board)

            sleep(2.5) # A delay to get exact colour. (Ship Explosion duration : (2.2-2.4)s)

        else:

            screen_img = capture_screen()

            game_board = analyze_board(screen_img)

            # Print or visualize the game board
            print(draw_board(game_board))

            print("His turn")
            sleep(3)
            

            

    except Exception as e:
        # Handle any exceptions 
        print(f"An error occurred: {e}")

    # Add a delay to control the loop frequency
    sleep(0.1)