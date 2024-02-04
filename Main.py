# Original code by [Mohammad Tomaraei]
# Modified by [@cemre10] for [FleetBattle-Bot]

from PIL import Image, ImageGrab
import random
from time import sleep
import win32api, win32con

# Constants for screen and game board coordinates
#phone_x_1, phone_y_1, phone_x_2, phone_y_2 = 1000, 346, 1645, 984  # Update with the actual coordinates
phone_x_1, phone_y_1, phone_x_2, phone_y_2 = 1005, 312, 1645, 952 # 479, 24, 823, 768
#main_square_coordinates = (15 + 175, 397 - 100, 15 + 660 + 175, 397 + 660 - 100) # Update with the actual coordinates 982 334
main_square_coordinates = (15, 15,15 + 1005 + 640,15 + 312 + 640)
smaller_square_size = 64

# Function to capture the phone screen
def capture_screen():
    return ImageGrab.grab(bbox=(phone_x_1, phone_y_1, phone_x_2, phone_y_2))

# Function to perform a click at a given screen position
def click(x, y):
    smallSquareSize_win32api = 51
    z1 = x // smaller_square_size
    z2 = y // smaller_square_size
    x = int(813 + 15 + smallSquareSize_win32api*z1)
    y = int(263 + 15 + smallSquareSize_win32api*z2)

    win32api.SetCursorPos((x, y)) # move the cursor to the position of (x, y)
    sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
    sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # The left mouse button is pressed
   #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # The left mouse button is released

# Function to check if it's the player's turn
def is_player_turn(img):
    # Implement the logic to check if it's the player's turn

    # Define the coordinates of a pixel that indicates the player's turn
    indicator_pixel = (132, 274)

    # Get the color of the indicator pixel
     # It's our turn when enemy_fleet_color = [>100, >100, >100]
    indicator_color = img.getpixel(indicator_pixel) # indicator pixel = ( ? , ? , ?) if ? are greater than 100 it's our turn

    # Check if the color indicates the player's turn (example: RGB values greater than 100)
    return all(value > 100 for value in indicator_color)

def analyze_board(img):
    # Crop the image to focus on the main square
    square_img = img.crop(main_square_coordinates)

    # Initialize an empty dictionary to represent the game board
    board = {}

    # Iterate through each square on the board
    for y in range(0, 10):
        for x in range(0, 10):
            # Calculate the pixel coordinates of the current square
            x_pix = main_square_coordinates[0] + x * smaller_square_size
            y_pix = main_square_coordinates[1] + y * smaller_square_size

            # Print the calculated coordinates for debugging
            print(f"({x_pix}, {y_pix})",end="")

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
                if coordinate_color[2] < 50:
                    square_status = 2  # If the color is red, it's been hit
                elif all(value > 70 for value in coordinate_color):
                    square_status = 1  # If the color is white/gray, it's a missed square

                # Store square information in the board dictionary
                board[x + 1, y + 1] = [square_status, x_pix, y_pix]

            else:
                print("Warning: Pixel coordinates out of bounds")

        print("\n")

    return board


# Function to draw a 2D representation of the board
def draw_board(board):
    drawn_board = ""
    for square in board:
        drawn_board += str(board[square][0]).replace("0", "-").replace("1", "X").replace("2", "*") + " "
        if square[0] == 10:
            drawn_board += "\n"
    return drawn_board

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
            print("[RH] Clicking on:", random_x, random_y)
            print(board[(random_x, random_y)][1], board[(random_x, random_y)][2])
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

# Main AI loop
while True:
    try:
        # Capture the phone screen
        #print("True")
        screen_img = capture_screen()
        #print("True")

        # Check if it's the player's turn
        if True: # is_player_turn(screen_img) or 
            #print("True")
            # Analyze the game board
            game_board = analyze_board(screen_img)
            #print("True")

            # Print or visualize the game board
            print(draw_board(game_board))
            #print("True")

            # Make a move (random hit)
            make_move(game_board)
            #print("True")

            

    except Exception as e:
        # Handle any exceptions gracefully
        print(f"An error occurred: {e}")

    # Add a delay to control the loop frequency
    sleep(5)