# Main.py

from PIL import Image, ImageGrab
import random
from time import sleep
import win32api, win32con

# Constants for screen and game board coordinates
phone_x_1, phone_y_1, phone_x_2, phone_y_2 = 479, 24, 823, 768
square_x, square_y, square_length = 15, 397, 313

# Function to capture the phone screen
def capture_screen():
    #return ImageGrab.grab(bbox=(phone_x_1, phone_y_1, phone_x_2, phone_y_2))

    # Modify the capture_screen function
    # Load the solid color image for testing (replace 'red.png' with your file's name)
    solid_color_img = Image.open('red.png')

    # Convert the image to RGB mode
    solid_color_img = solid_color_img.convert("RGB")

    return solid_color_img


# Function to perform a click at a given screen position
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

# Modify the is_player_turn function
def is_player_turn(img):
    try:
        # Print the image size for debugging
        print(f"Image Size: {img.size}")

        # Display the captured image for visual inspection
        img.show()

        # Get the color of the indicator pixel
        indicator_pixel = (112, 112)  # Or any other coordinates within the image size
        indicator_color = img.getpixel(indicator_pixel)
        print(f"Indicator Color: {indicator_color}")

        # It's our turn when indicator_color = [>100, >100, >100]
        #return all(value > 100 for value in indicator_color)
        return indicator_color[0]>100
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



# Function to analyze the game board from the captured image

def analyze_board(img):
    # Initialize an empty dictionary to represent the game board
    board = {}

    # Iterate through each pixel in the image
    for y in range(img.height):
        for x in range(img.width):
            # Get the color of the current pixel
            coordinate_color = img.getpixel((x, y))

            # Initialize the square status as 0 (empty)
            square_status = 0

            # Update the square status based on color conditions
            if coordinate_color[0] == 254 and coordinate_color[1] == 0 and coordinate_color[2] == 0:
                square_status = 2  # If the color is red, it's been hit

            # Store square information in the board dictionary
            board[x + 1, y + 1] = [square_status, x, y]

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
    # Find the first empty square and hit it
    for square in board:
        if board[square][0] == 0:
            x, y = square
            print(f"[Make Move] Clicking on: {x}, {y}")
            click(board[square][1], board[square][2])
            break


# Function to hit a random empty square

# Main AI loop
while True:
    try:
        # Capture the phone screen
        screen_img = capture_screen()

        # Check if it's the player's turn
        if is_player_turn(screen_img):
            print("True")
            # Analyze the game board
            game_board = analyze_board(screen_img)
            print("True")

            # Make a move (random hit)
            make_move(game_board)
            print("True")

            # Print or visualize the game board
            print(draw_board(game_board))
            print("True")

    except Exception as e:
        # Handle any exceptions gracefully
        print(f"An error occurred: {e}")

    # Add a delay to control the loop frequency
    sleep(30)