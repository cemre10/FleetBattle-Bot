<p align="center">
  <img src="https://i.postimg.cc/cCNMr1LQ/Screenshot-2024-02-07-220957.png" alt="Fleet Battle Game Icon" width="200">
</p>
<h1 align="center" style="margin-left: 20px;">
  <font size="120">FleetBattle Bot</font>
</h1> 

## Description
FleetBattle Bot is an automated script designed for playing the Fleet Battle mobile game on desktop. Originally developed by [Mohammad Tomaraei](https://github.com/themreza) in 2019, I have modified the script by introducing new features, adding new functions, enhancing intelligence, and ensuring compatibility with recent updates. (New functions will be added in Future to enhance intelligence!)

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Features](#features)
4. [How to Use](#how-to-use)
5. [Troubleshooting](#troubleshooting)
6. [License](#license)
7. [Acknowledgements](#acknowledgements)



## Overview 🌐
<a name="overview"></a>

This script automates gameplay in Fleet Battle, allowing the bot to make moves during its turn. Additionally, the bot can analyze the game board, interpret various situations, and strategically make hits. With a win ratio of over 35% in Quick Games mode, the bot consistently performs well. The "start game" function enables the bot to start new games, ensuring a continuous and efficient gaming experience.

<a name="requirements"></a>

## Requirements ✨

- [PIL (Pillow)](https://python-pillow.org/): The Python Imaging Library, now maintained as Pillow.
- [pywin32](https://pypi.org/project/pywin32/): Extensions for Windows that provide access to Windows-specific functionalities.
- [random](https://docs.python.org/3/library/random.html): A core Python library for generating random numbers.
- [time](https://docs.python.org/3/library/time.html): A core Python library for time-related functions.
- [os](https://docs.python.org/3/library/os.html): A core Python library for interacting with the operating system.
- Fleet Battle on Desktop: Ensure that you have Fleet Battle installed and configured on your desktop.

You can install the necessary libraries using the following commands:

```bash
  pip install Pillow
  pip install pywin32
```

Make sure to have Python installed on your system before installing these libraries.



## Features 🚀
<a name="features"></a>

- **Automated Gameplay:** The bot autonomously makes moves during its turn.
- **Intelligent Board Analysis:** Utilizes pixel color changes for real-time detection and analysis of the game board status.
- **Visual Board Representation:** Provides a visual representation of the game board within the terminal for enhanced monitoring.
- **Strategic Hit Planning:** Employs a smart hit strategy to optimize gameplay and increase the chances of successful hits.
- **Turn Recognition:** Can identify whether it's the player's or the opponent's turn, enhancing decision-making capabilities.



## How to Use 🎯
<a name="how-to-use"></a>

1. Install required dependencies.

2. Modify screen constants according to your specific screen configuration.

   Adjust screen constants according to your specific screen configuration in the `main.py` file. The default values in the script are set for a screen size of 1920x1080. If your screen resolution is different, you may need to modify the following constants to match your setup:

   - `imageX1`, `imageY1`, `imageX2`, `imageY2`: Coordinates for capturing the game board.
   - `squareSize`: Size of the game board.
   - `main_square_coordinates`: Coordinates of the game board.
   - `smallerSquareSize`: Size of one entity on the game board.

   Example (for my screen configuration):

   ```python
   # My Screen Size: 1920x1080
   
   imageX1, imageY1, imageX2, imageY2 = 1023, 332, 1742, 1050 
   squareSize = 720  # 720x720
   main_square_coordinates = (15, 15, 15 + imageX1 + squareSize, 15 + imageY1 + squareSize)
   smallerSquareSize = 72  # 72x72
   ```
   
   If you encounter any problems while adjusting screen constants, refer to the [Troubleshooting section](#troubleshooting) for guidance, particularly in the subsection on [Adjusting Screen Constants](#adjusting-screen-constants).

3. Open Fleet Battle and start a game

4. Run the program:
   
   ```bash
   Main.py
   ```

   After running the program, the bot will analyze the game and make hits automatically. Once the game finishes, it is capable of opening a new match.

<div style="display: flex; justify-content: space-between;">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODI2aG9qdHhwMzR0aGh2Y2gxZnI5bGlqeHJyNGg0Yjlkc3o3NzMyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TLWlrQ47vt3K5AZCFy/giphy.gif" alt="gif1" width="43%">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWJib2RmODZ6MWk4N2I1dzNtNXh2dHBhd2IyZXJxbHgyZDd2aHR5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6Wg8yaARGecx7iKwLI/giphy-downsized.gif" alt="gif2" width="50%">
</div>

   If the bot does not accurately analyze the game screen or if mouse clicks occur at the wrong locations, please refer to [Screen Analysis Issues ](#screen-analysis-issues ) and [Win32 Location Issues](#win32-location-issues) in the [Troubleshooting section](#troubleshooting).


 
## Troubleshooting 🛠️
<a name="troubleshooting"></a>

### Adjusting Screen Constants
<a name="Adjusting Screen Constants"></a>

   Discovering accurate screen constants is crucial, and there is a lot of way to measure screen and one of them this is using the Windows ruler. Simply press the `Windows key + Shift + M` to open the ruler, and measure Game Board screen size and coordinates (x1, y1, x2, y2).

   <div style="display: flex; justify-content: space-between;">
  <img src="https://i.postimg.cc/wjn5yZLV/image3.png" alt="Windows Ruler Demo 3" width="30%">
  <img src="https://i.postimg.cc/vHqtMcmC/image1.png" alt="Windows Ruler Demo 1" width="30%">
  <img src="https://i.postimg.cc/P5CzqTpJ/image2.png" alt="Windows Ruler Demo 2" width="30%">
</div>

In this illustration, the Windows ruler provides a visual guide to identify precise screen constants for your configuration. 
In the first image, we identify the `squareSize`, while in the second and third images, we capture the coordinates (`imageX1`, `imageY1`, `imageX2`, `imageY2`) for precise configuration.
   
   If you're still experiencing difficulties in modifying screen constants, consider the following steps:
  
   1. **Check Screen Resolution:**
      Ensure that your screen resolution matches the configuration specified in the script. Any deviation might lead to incorrect screen captures.
  
   2. **Coordinate Precision:**
      Pay attention to the precision of the coordinates. Small adjustments can significantly impact the accuracy of screen captures.
  
   3. **Debugging Output:**
      Enable or review debugging output in the terminal. The script might provide information on why adjustments are not working as expected.

### Screen Analysis Issues 
<a name="Screen Analysis Issues"></a>

To resolve screen analysis issues, we first need to identify the source of the problem.
      
#### If the issue is within the analyze_board function:

  Try [Troubleshooting section](#troubleshooting). If you still encounter problems, the issue may be related to color pixels or the coordinates of the main square.

   1. Ensure that the image you captured is large enough to encompass the entire game board.
 
   2. Remember that the coordinates (0,0) for the main square are relative to the image you captured, not the entire screen.
 
   3. Check and adjust the main_square_coordinates parameter, where (15, 15) allows the bot to check the center of the entry. Note that these values may vary from screen to screen.
  
   4. Confirm that your Fleet Battle settings are correct, such as the colors for sunk (black), hit (red), missed (white), gray X, and empty entry (blue (ocean)).
 
   5. Verify if the RGB colors are appropriately configured.

#### If the issue is within the is_player_turn function:
  
  This function needs to capture a new screenshot to examine the corners. With updates, the color of the screen corners changes when the player's turn changes. Simply updating constants may not effect on this function.
 
  1. Confirm that the coordinates check the corners of the screen.
 
  2. Check if RGB colors are correctly configured (Red for enemy's turn, Blue for our turn, Black means game ended).

#### Otherwise:
  
  If the problem is in the capture_screen() function, refer to the [Adjusting Screen Constants](#Adjusting-Screen-Constants) must solve problem
 
  If the issue is within the click() function, consult [Win32 Location Issues](#win32-location-issues) must solve problem
  
  If the problem is in the game_start() function, check [else](#else)


  For issues in other functions, review the code structure, and ensure there are no syntax errors, as these functions are interconnected. If errors persist, the root cause may be within the mentioned functions.
     
### Win32 Location Issues 
<a name="Win32 Location Issues"></a>

   If mouse clicks are happening at incorrect locations, consider the following:
  
   1. **Adjust Win32API Coordinates:**
      Review and adjust the Win32API coordinates in the script (`Main.py`) to ensure that mouse clicks align with the intended game board positions.
  
   2. **Debugging Output:**
      Enable or review additional debugging output related to Win32API operations. This may provide insights into any inaccuracies in mouse click locations.

   The Win32API coordinates different from our constants, it's essential to perform iterative testing—alternating between fail and success—to identify the appropriate `smallSquareSize_win32api`, `startPoint_X_win32api`, `startPoint_Y_win32api`, `distance_win32api` constant in the `click` function within `Main.py`.
  
   Remember to run the program again after making adjustments to see if the issues are resolved.

   #### Example (for my case):  

   ```python
   def click(x, y):
      smallSquareSize_win32api = 58 # Each small square size
      startPoint_X_win32api = 814 # start point of the game board screen
      startPoint_Y_win32api = 263 # start point of the game board screen
      distance_win32api = 30 # Center of small square
      z1 = x // smallerSquareSize
      z2 = y // smallerSquareSize
      x = int(startPoint_X_win32api + distance_win32api + smallSquareSize_win32api*z1)
      y = int(startPoint_Y_win32api + distance_win32api + smallSquareSize_win32api*z2)
  
      win32api.SetCursorPos((x, y))
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
   ```

   If these constants do not work for your computer screen, continue the iterative process of testing and adjusting until you find the suitable constants.

### Else:
<a name="Else"></a>

   With the mentioned steps, problems should be resolved. If issues persist, consider the following:

   1. **Start Game Logic:** The `is_player_turn` function checks the screen corners for each loop. If it detects a black color pixel, it returns false, indicating that the game has finished and in the while loop it goes to the else condition and calls the `start_game` function multiple times, check the coordinates to click on (x, y) and delays within the else block. For instance, on your computer, the coordinates for closing an ad may differ.

   2. **Technical Issues:**  Ensure that all libraries are up-to-date and support the functions being called.
   
   3. **Check for Syntax Errors:** If you have tried all the suggested solutions and the problem persists, inspect the code structure for potential syntax errors. This is the second time you should review the code for any issues.   

By addressing these considerations, you should be able to troubleshoot and resolve any lingering problems.

## License 📄
<a name="license"></a>

This project is licensed under the [GNU General Public License (GPL) Version 3](LICENSE).

## Acknowledgements 🙏
<a name="acknowledgements"></a>

- Original code by [Mohammad Tomaraei](https://github.com/themreza) (2019).
- Modified and enhanced by [@cemre10](https://github.com/cemre10) (2024).


