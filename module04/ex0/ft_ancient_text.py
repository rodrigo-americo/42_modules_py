import sys
from typing import IO


def main() -> None:
    file_name: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{file_name}'")
    file: IO
    try:
        file = open(file_name, "r")
    except OSError as err:
        print(f"Error opening file '{file_name}': {str(err)}")
        return
    print("---")
    while True:
        line = file.readline()
        if line == "":
            break
        print(line, end="")
    print("---")
    file.close()
    print(f"File '{file_name}' closed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
    else:
        main()
