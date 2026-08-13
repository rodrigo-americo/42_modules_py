import sys
from typing import IO


def save_fragment(text: str) -> None:
    file_name = input("Enter new file name (or empty): ")
    if file_name == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{file_name}'")
    file: IO
    try:
        file = open(file_name, "w")
    except OSError as err:
        print(f"Error opening file '{file_name}': {str(err)}")
        return
    file.write(text)
    file.close()
    print(f"Data saved in file '{file_name}'")


def main() -> None:
    file_name: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")
    file: IO
    try:
        file = open(file_name, "r")
    except OSError as err:
        print(f"Error opening file '{file_name}': {str(err)}")
        return
    print("---")
    new_text = ""
    while True:
        line = file.readline()
        if line == "":
            break
        print(line, end="")
        new_text = new_text + line.rstrip("\n") + "#\n"
    print("---")
    file.close()
    print(f"File '{file_name}' closed.")
    print("Transform data:")
    print("---")
    print(new_text)
    print("---")
    save_fragment(new_text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
    else:
        main()
