# cleardcp.py
# This script removes all files from `decensor_input', `decensor_input_original' and `decensor_output' directories.
# Originally written by github.com/DioKyrie
#

import os
from typing import Union

def clear_folder(folder_path: Union[str, bytes]) -> None:
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                clear_folder(file_path)
        print(f"Content of '{folder_path}' cleared successfully.")
    except Exception as e:
        print(f"Error clearing content of '{folder_path}': {e}")


def main():
    folders_to_clear = ["decensor_input", "decensor_input_original", "decensor_output"]
    for folder in folders_to_clear:
        folder_path = os.path.join(os.path.dirname(__file__), folder)
        clear_folder(folder_path)


if __name__ == "__main__":
    main()
