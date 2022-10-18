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


# Declaring global variable
DB_UL = "sqlite:///flashcard.db?check_same_thread=False"
engine = create_engine(DB_UL)
Session = sessionmaker(bind=engine)
exec_session = Session()

# creating all the tables
Base.metadata.create_all(engine)


def get_user_choice(menu: list) -> int:
    choice = None

    # show the menu with options
    for key, option in enumerate(menu):
        # add one when displaying the key
        print(f"{key + 1}.", option)

    # check for any parsing error
    try:
        choice = input()
        choice = int(choice)
    except ValueError:
        pass

    # break the loop if the condition is met
    if type(choice) != int or 0 > choice or choice > len(menu):
        print(" ")
        print(f"{choice} is not an option")

    return choice


def get_main_menu_choice() -> int:
    # defining main menu options
    main_menu = ["Add flashcards", "Practice flashcards", "Exit"]

    # getting user's choice
    return get_user_choice(main_menu)


def get_sub_menu_choice() -> int:
    # defining sub menu options
    sub_menu = ["Add a new flashcard", "Exit"]

    # getting user's choice
    return get_user_choice(sub_menu)


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


def play_flashcard(flashcard: dict) -> None:
    print(" ")
    print("Question:", flashcard.question)
    print("Please press \"y\" to see the answer or press \"n\" to skip:")

    choice = input()

    # accept capital or small letter options
    if choice not in "YyNn":
        print(" ")
        print(f"{choice} is not an option")

    # printing the answer
    if choice in "Yy":
        print(" ")
        print("Answer:", flashcard.answer)


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
        if main_choice == 3:
            print(" ")
            break
        elif main_choice == 2:
            cards = exec_session.query(Question).all()
            practice_flashcards(cards)
        elif main_choice == 1:
            # loop through sub menu until the user chose to exit
            while True:
                print(" ")
                # get user option
                sub_choice = get_sub_menu_choice()

                # check user options
                if sub_choice == 2:
                    break
                elif sub_choice == 1:
                    # adding the orm
                    exec_session.add(get_flashcard())

            # saving all to the database
            exec_session.commit()

        print(" ")

    # greeting Goodbye
    print("Bye!")


if __name__ == "__main__":
    main()
