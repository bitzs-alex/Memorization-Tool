# write your code here
# importing necessary packages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


# declaring the class
class Question(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer, default=1)


# Declaring global variable
DB_UL = "sqlite:///flashcard.db?check_same_thread=False"
engine = create_engine(DB_UL)
Session = sessionmaker(bind=engine)
exec_session = Session()

# creating all the tables
Base.metadata.create_all(engine)


def get_user_choice(menu: dict, is_numeric: bool = False) -> str:
    # show the menu with options
    for key, option in menu.items():
        # present the options to the user
        print(f"{key}. {option}" if is_numeric else f"{option}:")

    # get user choice, and let upper and lower cases
    choice = input()

    # show error message if the choice isn't an option
    if choice.lower() not in menu.keys():
        print(" ")
        print(f"{choice} is not an option")

    return choice.lower()


def get_main_menu_choice() -> str:
    # defining main menu options
    main_menu = {"1": "Add flashcards", "2": "Practice flashcards", "3": "Exit"}

    # getting user's choice
    return get_user_choice(main_menu, is_numeric=True)


def get_sub_menu_choice() -> str:
    # defining sub menu options
    menu = {"1": "Add a new flashcard", "2": "Exit"}

    # getting user's choice
    return get_user_choice(menu, is_numeric=True)


def get_flashcard() -> dict:
    # declaring a flashcard
    flashcard = {"question": None, "answer": None}

    print(" ")
    # loop through keys and get the inputs
    for key in flashcard.keys():
        # loop until I get a valid string
        while True:
            print(f"{key.capitalize()}:")
            flashcard[key] = input().strip()

            if flashcard[key]:
                break

            if key == "answer":
                print(" ")

    # return the flashcard
    return Question(**flashcard)


def update_flashcard(card: Question) -> None:
    # create a dictionary to store the input values
    flashcard = {"question": "", "answer": ""}

    # loop through keys and get the inputs
    for key in flashcard.keys():
        print(f"current {key}: {card.__dict__.get(key)}")
        print(f"please write a new {key}:")
        flashcard[key] = input().strip()

    # filter only the keys with new value
    flashcard = {key: value for key, value in flashcard.items() if value}

    # save the change to the database
    if len(flashcard):
        # update using the primary id
        exec_session.query(Question.id == card.id).update(flashcard)
        exec_session.commit()


def delete_flashcard(flashcard: Question) -> None:
    # deleting the flashcard
    exec_session.delete(flashcard)
    # saving the change
    exec_session.commit()


def flashcard_updater(flashcard: Question) -> None:
    menu = {
        "d": "press \"d\" to delete the flashcard",
        "e": "press \"e\" to edit the flashcard"
    }
    choice = get_user_choice(menu)

    if choice == "d":
        delete_flashcard(flashcard)
    elif choice == "e":
        update_flashcard(flashcard)


def update_card_box(card: Question) -> None:
    menu = {
        "y": "press \"y\" if your answer is correct",
        "n": "press \"n\" if your answer is wrong"
    }
    choice = get_user_choice(menu)

    if choice == "y":
        if card.box_number == 3:
            # remove from the box
            exec_session.delete(card)
        else:
            # update the box_number
            card.box_number += 1

        # save the change
        exec_session.commit()
    elif choice == "n":
        # bring the card back to box 1
        card.box_number = 1
        # save the change
        exec_session.commit()


def play_flashcard(flashcard: Question) -> None:
    print(" ")
    print("Question:", flashcard.question)

    menu = {
        "y": "press \"y\" to see the answer",
        "n": "press \"n\" to skip",
        "u": "press \"u\" to update"
    }
    choice = get_user_choice(menu)

    # printing the answer
    if choice == "y":
        print(" ")
        print("Answer:", flashcard.answer)
        update_card_box(flashcard)
    elif choice == "u":
        flashcard_updater(flashcard)


def practice_flashcards(flashcards) -> None:
    # check if there is any flashcard
    if len(flashcards):
        # loop over each flashcard
        for flashcard in flashcards:
            play_flashcard(flashcard)
    else:
        print(" ")
        print("There is no flashcard to practice!")


def main() -> None:
    # loop through main menu until the user chose to exit
    while True:
        # get user choice
        main_choice = get_main_menu_choice()

        # check user options
        if main_choice == "3":
            print(" ")
            break
        elif main_choice == "2":
            cards = exec_session.query(Question).all()
            practice_flashcards(cards)
        elif main_choice == "1":
            # loop through sub menu until the user chose to exit
            while True:
                print(" ")
                # get user option
                sub_choice = get_sub_menu_choice()

                # check user options
                if sub_choice == "2":
                    break
                elif sub_choice == "1":
                    # adding the orm
                    exec_session.add(get_flashcard())

            # saving all to the database
            exec_session.commit()

        print(" ")

    # greeting Goodbye
    print("Bye!")


if __name__ == "__main__":
    main()
