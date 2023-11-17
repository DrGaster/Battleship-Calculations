from itertools import permutations
from typing import List, Tuple
import json

class GameObject:
    """
    Represents a game object with height, width, and position.
    """
    def __init__(self, name: str, height: int, width: int, position: Tuple[int, int]):
        """
        Initialize a GameObject.

        Parameters:
        - name (str): The name of the object.
        - height (int): The height of the object.
        - width (int): The width of the object.
        - position (Tuple[int, int]): The position of the object as (x, y).
        """
        self.name = name
        self.height = height
        self.width = width
        self.position = position

def calculate_permutations(objects: List[GameObject], board_size: Tuple[int, int]) -> List[List[GameObject]]:
    """
    Calculate valid permutations for each game object separately.

    Parameters:
    - objects (List[GameObject]): List of game objects.
    - board_size (Tuple[int, int]): Size of the board.

    Returns:
    - List[List[GameObject]]: List of valid permutations for each game object.
    """
    all_permutations = []

    for obj in objects:
        obj_permutations = []
        print(f"Calculating permutations for Object: {obj.name}")
        for perm_indices in permutations(range(len(objects))):
            perm = [objects[i] for i in perm_indices]
            if is_valid_permutation(perm, board_size):
                obj_permutations.append(perm)
        all_permutations.append(obj_permutations)

    return all_permutations

def is_valid_permutation(perm: List[GameObject], board_size: Tuple[int, int]) -> bool:
    """
    Check if a permutation of game objects is valid.

    Parameters:
    - perm (List[GameObject]): Permutation of game objects.
    - board_size (Tuple[int, int]): Size of the board.

    Returns:
    - bool: True if the permutation is valid, False otherwise.
    """
    print(f"Checking validity for permutation: {[obj.name for obj in perm]}")
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            obj1 = perm[i]
            obj2 = perm[j]

            if overlap(obj1, obj2):
                print(f"Overlap detected: {obj1.name}, {obj2.name}")
                return False

    for obj in perm:
        if not within_board(obj, board_size):
            print(f"Object not within board: {obj.name}")
            return False

    return True

def overlap(obj1: GameObject, obj2: GameObject) -> bool:
    """
    Check if two game objects overlap completely.

    Parameters:
    - obj1 (GameObject): First game object.
    - obj2 (GameObject): Second game object.

    Returns:
    - bool: True if objects overlap completely, False otherwise.
    """
    x1, y1 = obj1.position
    x2, y2 = obj2.position

    if (
        x1 >= x2 and y1 >= y2 and
        x1 + obj1.height <= x2 + obj2.height and y1 + obj1.width <= y2 + obj2.width
    ) or (
        x2 >= x1 and y2 >= y1 and
        x2 + obj2.height <= x1 + obj1.height and y2 + obj2.width <= y1 + obj1.width
    ):
        return True

    return False

def within_board(obj: GameObject, board_size: Tuple[int, int]) -> bool:
    """
    Check if a game object is within the board boundaries.

    Parameters:
    - obj (GameObject): The game object to check.
    - board_size (Tuple[int, int]): Size of the board.

    Returns:
    - bool: True if the object is within the board, False otherwise.
    """
    x, y = obj.position
    height, width = obj.height, obj.width
    board_height, board_width = board_size

    return 0 <= x < board_height and 0 <= y < board_width and x + height <= board_height and y + width <= board_width

def write_permutations_to_file(filename: str, permutations_list: List[List[GameObject]]):
    """
    Write permutations to separate files for each object.

    Parameters:
    - filename (str): The base filename for output files.
    - permutations_list (List[List[GameObject]]): List of permutations for each object.
    """
    for i, obj_permutations in enumerate(permutations_list):
        with open(f'{filename}_object_{chr(97 + i)}.txt', 'w') as file:
            file.write(f"\nPermutations for Object {chr(97 + i)}:\n")
            for perm in obj_permutations:
                file.write(f"X, Y Coordinates: {[obj.position for obj in perm]}\n")

def save_objects_to_file(objects: List[GameObject], filename: str):
    """
    Save a list of GameObjects to a JSON file.

    Parameters:
    - objects (List[GameObject]): List of GameObjects.
    - filename (str): The name of the file to save to.
    """
    with open(filename, 'w') as file:
        data = [
            {"name": obj.name, "height": obj.height, "width": obj.width, "position": obj.position}
            for obj in objects
        ]
        json.dump(data, file, indent=2)

def load_objects_from_file(filename: str) -> List[GameObject]:
    """
    Load a list of GameObjects from a JSON file.

    Parameters:
    - filename (str): The name of the file to load from.

    Returns:
    - List[GameObject]: List of loaded GameObjects.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            objects = [
                GameObject(obj["name"], obj["height"], obj["width"], tuple(obj["position"]))
                for obj in data
            ]
            return objects
    except FileNotFoundError:
        return []

def display_objects_file(filename: str):
    """
    Display the contents of the objects file.

    Parameters:
    - filename (str): The name of the objects file.
    """
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print("Objects file not found.")

def main():
    """
    Main function to interact with the program.
    """
    # Load objects from file at the beginning
    objects = load_objects_from_file('objects.json')

    while True:
        print("\nMenu:")
        print("1. Add Object")
        print("2. Edit Objects")
        print("3. Generate Permutations")
        print("4. Display Objects File")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            objects.append(get_object_dimensions())  # Assuming you have a function get_object_dimensions
            save_objects_to_file(objects, 'objects.json')
        elif choice == "2":
            edit_objects_menu(objects)
            save_objects_to_file(objects, 'objects.json')
        elif choice == "3":
            if not objects:
                print("Please add at least one object first.")
                continue
            board_size = (14, 14)
            all_permutations = calculate_permutations(objects, board_size)
            for i, obj_permutations in enumerate(all_permutations):
                print(f"\nPermutations for Object {chr(97 + i)}:")
                for perm in obj_permutations:
                    print(f"X, Y Coordinates: {[obj.position for obj in perm]}")
            write_permutations_to_file('permutations_output', all_permutations)
        elif choice == "4":
            display_objects_file('objects.json')
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def edit_objects_menu(objects: List[GameObject]):
    """
    Display a menu for editing objects and perform the selected action.

    Parameters:
    - objects (List[GameObject]): List of game objects to edit.
    """
    while True:
        print("\nEdit Objects Menu:")
        print("1. Delete Object")
        print("2. Modify Object")
        print("3. Back")

        edit_choice = input("Enter your choice: ")

        if edit_choice == "1":
            delete_object(objects)
        elif edit_choice == "2":
            modify_object(objects)
        elif edit_choice == "3":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def delete_object(objects: List[GameObject]):
    """
    Delete a selected object from the list.

    Parameters:
    - objects (List[GameObject]): List of game objects.
    """
    print("Current Objects:")
    for i, obj in enumerate(objects):
        print(f"{i + 1}. {obj.name} at ({obj.position[0]}, {obj.position[1]})")

    index_to_delete = int(input("Enter the number of the object to delete: ")) - 1

    if 0 <= index_to_delete < len(objects):
        deleted_object = objects.pop(index_to_delete)
        print(f"Deleted object: {deleted_object.name} at ({deleted_object.position[0]}, {deleted_object.position[1]})")
    else:
        print("Invalid index. No object deleted.")

def modify_object(objects: List[GameObject]):
    """
    Modify the dimensions and position of a selected object.

    Parameters:
    - objects (List[GameObject]): List of game objects.
    """
    print("Current Objects:")
    for i, obj in enumerate(objects):
        print(f"{i + 1}. {obj.name} at ({obj.position[0]}, {obj.position[1]})")

    index_to_modify = int(input("Enter the number of the object to modify: ")) - 1

    if 0 <= index_to_modify < len(objects):
        modified_object = objects[index_to_modify]
        modified_object.height = int(input("Enter the new height: "))
        modified_object.width = int(input("Enter the new width: "))
        modified_object.position = tuple(map(int, input("Enter the new position (x y): ").split()))
        print(f"Modified object: {modified_object.name} at ({modified_object.position[0]}, {modified_object.position[1]})")
    else:
        print("Invalid index. No object modified.")

if __name__ == "__main__":
    main()
