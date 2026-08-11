import sys


def main() -> None:
    i: int = 1
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) > 1:
        print(f"Arguments received: {len(sys.argv) - 1}")
        for arg in sys.argv[1:]:
            print(f"Argument {i}: {arg}")
            i += 1
    else:
        print("No arguments provided!")
    print(f"Total arguments: {len(sys.argv)}")
    return


if __name__ == "__main__":
    print("=== Command Quest ===")
    main()
