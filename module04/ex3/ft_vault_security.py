def secure_archive(
    file_name: str, option: int = 0, new_text: str = ""
) -> tuple[bool, str]:
    mode: str = ""
    if option == 0:
        mode = 'r'
    elif option == 1:
        mode = 'w'
    else:
        return (False, "Invalid option")
    try:
        with open(file_name, mode) as file:
            if mode == 'r':
                msg = file.read()
            else:
                file.write(new_text)
                msg = "Content successfully written to file"
            return (True, msg)
    except OSError as err:
        return (False, str(err))


if __name__ == "__main__":
    pass
