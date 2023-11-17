import numpy as np
from colorama import Fore, Style, init

# Initialize colorama
init()

# Colors for printing
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Style.RESET_ALL

# Step 1: Initialize Arrays
input_array = np.full((14, 14), " ", dtype=str)  # Use space for consistency with "X" and "O"
group_sizes = [3, 4, 5, 3, 4, 5]  # Example group sizes
orientations = ["horizontal", "vertical", "horizontal", "vertical", "horizontal", "vertical"]

# Step 2: Helper Functions
def visualize_group_mask(group_mask):
    """
    Visualizes a group mask as a string.

    Parameters:
    - group_mask (numpy.ndarray): The group mask to visualize.

    Returns:
    - str: The string representation of the group mask.
    """
    return "\n".join(["".join(row) for row in group_mask])

def create_group_mask(size, orientation):
    """
    Creates a group mask based on size and orientation.

    Parameters:
    - size (int): The size of the group mask.
    - orientation (str): The orientation of the group mask ("horizontal" or "vertical").

    Returns:
    - numpy.ndarray: The created group mask.
    """
    if orientation == "horizontal":
        return np.full((size, 1), " ", dtype=str)
    elif orientation == "vertical":
        return np.full((1, size), " ", dtype=str)

# Step 3: User Interaction (Command-line interface for simplicity)
def process_activation_sequence():
    """
    Handles the main interaction loop with the user, providing options to update the attack field,
    view probability boards, restart the program, or exit.
    """
    while True:
        print("\nMain Menu:")
        print("1. Update Attack Field")
        print("2. View Probability Boards")
        print("3. Restart Program")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            update_attack_field()
        elif choice == "2":
            view_probability_boards()
        elif choice == "3":
            print("Restarting program.")
            break  # Exit the inner loop to restart
        elif choice == "4":
            print("Exiting program. Goodbye!")
            exit()  # Exit the entire script
        else:
            print("Invalid choice. Please enter a valid option (1, 2, 3, or 4).")

        print("\nInitial Input Array:")
        print_board_with_color(input_array)

def update_attack_field():
    """
    Updates the attack field based on user input for coordinates and value ("X" or "O").
    """
    try:
        print("\nUpdate Attack Field (Input Array):")
        print_board_with_color(input_array)

        x_coordinate = int(input("Enter the X coordinate: "))
        y_coordinate = int(input("Enter the Y coordinate: "))
        value = input("Enter 'X' or 'O' for the selected coordinate: ").upper()  # Convert to uppercase

        if 0 <= x_coordinate < 14 and 0 <= y_coordinate < 14 and value in ["X", "O"]:
            input_array[y_coordinate, x_coordinate] = value
            print("\nAttack Field Updated:")
            print_board_with_color(input_array)
        else:
            print("Invalid coordinates or value. Please ensure valid input.")

    except ValueError as e:
        handle_input_error(e)

def handle_input_error(error):
    """
    Handles input-related errors by printing an error message.

    Parameters:
    - error (ValueError): The input-related error.
    """
    print(f"Error: {error}")
    print("Invalid input. Please enter valid coordinates and 'X' or 'O' for the value.")

def print_board_with_color(board):
    """
    Prints a 2D array (board) with color formatting and row/column indices.

    Parameters:
    - board (numpy.ndarray): The 2D array to print with color formatting.
    """
    # Find the maximum number of digits for row and column indices
    max_row_digits = len(str(len(board)))
    max_col_digits = len(str(len(board[0])))

    # Add column indices to the first row of the board
    board_with_col_indices = np.insert(board, 0, range(len(board[0])), axis=1)

    # Print column indices
    col_indices_format = f"{{:>{max_row_digits}}} " + " ".join([f"{{:>{max_col_digits}}}" for _ in range(len(board[0]))])
    print(col_indices_format.format("", *range(len(board[0]))))

    for i, row in enumerate(board_with_col_indices):
        # Print row index and row content
        row_index_format = f"{{:>{max_row_digits}}} "
        print(row_index_format.format(i), end="")
        
        for j, cell in enumerate(row):
            if j == 0:
                # Skip printing the first element (column index) in each row
                continue
            
            if cell == "X":
                print(f" {RED}{cell}{RESET}", end=" ")
            elif cell == "O":
                print(f" {GREEN}{cell}{RESET}", end=" ")
            else:
                print(f" {cell}", end=" ")
        print()

def view_probability_boards():
    """
    Provides options to view total probability array or sub-boards, and handles user input accordingly.
    """
    while True:
        print("\nView Probability Boards Menu:")
        print("1. View Total Probability Array")
        print("2. View Sub-boards")
        print("3. Back to Main Menu")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            print("\nTotal Probability Array:")
            print_board_with_color(sum([globals()[f"data_array_{i+1}"] for i in range(len(group_sizes))]))
        elif choice == "2":
            view_group_masks_menu()
        elif choice == "3":
            print("Returning to Main Menu.")
            break
        else:
            print("Invalid choice. Please enter a valid option (1, 2, or 3).")

def view_group_masks_menu():
    """
    Provides options to view sub-boards and handles user input accordingly.
    """
    while True:
        print("\nSelect Sub-board to View:")
        for i, size in enumerate(group_sizes):
            print(f"{i+1}. View Sub-board for {size}-cell Ship")

        print(f"{len(group_sizes) + 1}. Back to Previous Menu")

        mask_choice = input("Enter your choice: ")

        if mask_choice.isdigit():
            mask_choice = int(mask_choice)

            if 1 <= mask_choice <= len(group_sizes):
                print(f"\nVisualized Sub-board for {group_sizes[mask_choice-1]}-cell Ship:")
                print_board_with_color(create_group_mask(group_sizes[mask_choice-1], orientations[mask_choice-1]))
            elif mask_choice == len(group_sizes) + 1:
                print("Returning to Probability Boards Menu.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
        else:
            print("Invalid choice. Please enter a valid option (integer).")

# Initial Display
print("Initial Input Array:")
print_board_with_color(input_array)

# User Activation
process_activation_sequence()

# Iterative Update (you need to implement this part)
