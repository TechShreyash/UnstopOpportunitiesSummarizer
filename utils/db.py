import logging

FILE_NAME = "db.txt"


def save_competition_to_db(num):
    """
    Saves a competition ID to the database file.

    Args:
        num (int or str): Competition ID.
    """
    try:
        with open(FILE_NAME, "a") as f:
            f.write(f"{num}\n")
    except IOError as e:
        logging.error(f"Failed to save competition {num} to DB: {e}")


def is_competition_in_db(num):
    """
    Checks if a competition ID exists in the database file.

    Args:
        num (int or str): Competition ID.

    Returns:
        bool: True if found, False otherwise.
    """
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                if int(line.strip()) == int(num):
                    return True
        return False
    except FileNotFoundError:
        logging.warning(f"{FILE_NAME} not found. Assuming empty DB.")
        return False
    except ValueError:
        # Handle cases where line is not an integer
        return False
    except Exception as e:
        logging.error(f"Error checking DB for competition {num}: {e}")
        return False
