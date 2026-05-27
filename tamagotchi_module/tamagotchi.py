import random
import pandas as pd
import streamlit as st


# Create the class Tamagotchi
class Tamagotchi:

    def __init__(self, name):

        self.name = name

        # life & care parameters
        self.hunger = 0
        self.boredom = 0
        self.tiredness = 0
        self.dirtiness = 0

        self.food = 2
        self.sleep = False
        self.alive = True

    # Define the method eat, when the creature eats
    def eat(self):

        # Check if there is food available
        if self.food >= 1:

            self.food -= 1
            self.hunger -= random.randint(1, 4)
            st.session_state["message"] = ("success", f"{self.name} has eaten.")

        elif self.food == 0:
            st.session_state["message"] = ("warning", "No food available.")

        # make sure hunger won't take any negative value
        self.hunger = 0 if self.hunger < 0 else self.hunger

    # when the creature wants to play, this method governs the action
    def play(self, player_move: str):
        answers = ("scissors", "paper", "rock")

        pet_move = random.choice(answers)

        result_msg = (
            f"{self.name} chose **{pet_move}**. You chose **{player_move}**.\n\n"
        )

        if player_move == pet_move:
            result_msg += "It's a tie!"
            self.boredom -= 2
            msg_type = "warning"

        elif (
            (player_move == "scissors" and pet_move == "paper")
            or (player_move == "paper" and pet_move == "rock")
            or (player_move == "rock" and pet_move == "scissors")
        ):
            result_msg += "You WIN!"
            self.boredom -= 3
            msg_type = "success"

        else:
            result_msg += f"{self.name} WINS!"
            self.boredom -= 1
            msg_type = "info"

        self.boredom = max(0, self.boredom)  # ensure positive value

        st.session_state["message"] = (msg_type, result_msg)
        st.session_state["playing"] = False

    def sleeping(self):

        # sleeping mode
        self.sleep = True
        self.tiredness -= 3
        self.boredom -= 2

        st.session_state["message"] = ("info", f"{self.name} is sleeping... 😴")

        # return values to 0 when negative
        self.tiredness = 0 if self.tiredness < 0 else self.tiredness
        self.boredom = 0 if self.boredom < 0 else self.boredom

    # waking up
    def wake_up(self):

        num = random.randint(0, 2)

        # The creature wakes up if the generated random number is zero
        if num == 0:

            st.session_state["message"] = ("success", f"{self.name} is awake!")
            self.sleep = False
            self.boredom = 0

        else:

            st.session_state["message"] = ("info", f"{self.name} keeps on sleeping.")
            self.sleeping()

    # Bath function for cleaning the creature
    def bath(self):

        self.dirtiness = 0
        st.session_state["message"] = ("info", f"{self.name} has taken a bath 🧼🐈🫧")

    def search_food(self):

        found_food = random.randint(0, 4)

        self.food += found_food
        self.dirtiness += 2

        # print the meals found
        meals = "meals" if found_food != 1 else "meal"
        st.session_state["message"] = (
            "success",
            f"{self.name} has found {found_food} {meals} 🍚🍕",
        )

    # get values of the parameters
    def get_parameters(self):

        parameters = {
            "name": self.name,
            "hunger": self.hunger,
            "boredom": self.boredom,
            "tiredness": self.tiredness,
            "dirtiness": self.dirtiness,
            "meals": self.food,
            "is_asleep": self.sleep,
        }

        return parameters

    # Difficulty will vary the parameters depending on the difficulty level
    def difficulty(self, level):

        if not 1 <= level <= 5:
            raise ValueError("Difficulty level must be between 1 and 5!")

        else:

            # increase hunger and dirtiness
            self.hunger += random.randint(0, level)
            self.dirtiness += random.randint(0, level)

            # increase boredom and tiredness when awake
            if self.sleep != True:

                self.boredom += random.randint(0, level)
                self.tiredness += random.randint(0, level)

    # Death
    def death(self):

        if self.hunger >= 10:
            st.session_state["message"] = ("error", f"{self.name} is starving")
            self.alive = False

        elif self.dirtiness >= 10:
            st.session_state["message"] = (
                "error",
                f"{self.name} stinks so bad he almost die",
            )
            self.alive = False

        elif self.boredom >= 10:
            st.session_state["message"] = (
                "error",
                f"{self.name} is so bored he almost gave up on life",
            )
            self.alive = False

        elif self.tiredness >= 10:
            st.session_state["message"] = (
                "error",
                f"{self.name} collapsed from exahustion",
            )
            self.alive = False
