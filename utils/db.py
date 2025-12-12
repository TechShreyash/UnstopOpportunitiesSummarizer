FILE_NAME = "db.txt"


def save_competition_to_db(num):
    with open(FILE_NAME, "a") as f:
        f.write(f"{num}\n")


def is_competition_in_db(num):
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                if int(line.strip()) == num:
                    return True
        return False
    except FileNotFoundError:
        return False
