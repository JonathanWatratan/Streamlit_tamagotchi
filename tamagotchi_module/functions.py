from tamagotchi_module.tamagotchi import Tamagotchi
import streamlit as st


def load_pet():

    if "pet" not in st.session_state:
        diff_level = st.slider("Select the difficulty level", 1, 5, 1)
        name = st.text_input("Name your Tamagotchi:")

        if name:
            st.session_state.pet = Tamagotchi(name)
            st.session_state.diff_level = diff_level  # Guardamos en sesión
            st.success(f"Created Tamagotchi named {name}!")
            return st.session_state.pet, diff_level
        else:
            return None, None

    else:
        # Ya están guardados en sesión
        return st.session_state.pet, st.session_state.get("diff_level", 1)


# We need a key for every button since they're going to be executed several times during the game
# so every time we click on a button, it won't get in conflict with previous clicks
def show_menu(tamagotchi: Tamagotchi):
    st.markdown("## Choose an action:")
    action = None

    if not tamagotchi.sleep:

        cols = st.columns(5)

        if cols[0].button("🍽️ Eat", key=f"btn_eat_{tamagotchi.name}"):
            action = "eat"
        if cols[1].button("🎮 Play", key=f"btn_play_{tamagotchi.name}"):
            action = "play"
        if cols[2].button("😴 Sleep", key=f"btn_sleep_{tamagotchi.name}"):
            action = "sleep"
        if cols[3].button("🛁 Bath", key=f"btn_bath_{tamagotchi.name}"):
            action = "bath"
        if cols[4].button("🍖 Go for food", key=f"btn_search_{tamagotchi.name}"):
            action = "search_food"
    else:
        if st.button("⏰ Awake", key=f"btn_awake_{tamagotchi.name}"):
            action = "awake"

    return action


def call_action(tamagotchi: Tamagotchi, action):

    if action == "eat":
        tamagotchi.eat()

    elif action == "play":
        st.session_state["playing"] = True
        st.session_state["message"] = (
            "info",
            "Choose scissors ✂️, paper 📄 or rock 🪨 to play!",
        )

    elif action == "sleep":
        tamagotchi.sleeping()

    elif action == "bath":
        tamagotchi.bath()

    elif action == "search_food":
        tamagotchi.search_food()

    elif action == "awake":
        tamagotchi.wake_up()
