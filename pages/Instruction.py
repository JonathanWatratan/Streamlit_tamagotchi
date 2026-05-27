import streamlit as st

st.set_page_config(page_title="Instructions", page_icon="📖")

st.title("📖 :rainbow[How to Play Tamagotchi]")

st.markdown(
    """
Welcome to **Tamagotchi for Streamlit**!

This is a virtual pet you must take care of. You can:

- 🍽️ Feed your pet (lowers hunger)
- 🎮 Play (lowers boredom)
- 🛁 Bathe it (cleans dirtiness)
- 😴 Put it to sleep (rest to reduce tiredness)
- 🍖 Search for food (find meals)

Be careful! If any parameter (hunger, boredom, dirtiness, tiredness) reaches **10**, your pet will **die**.

---

### 🎮 Game Mechanics

- You can interact by clicking buttons below the message screen.
- If your pet is asleep, only the **Wake Up** button will be available. It may take more than one click to wake your pet up!
- When you play, you'll face your pet in a game of **rock-paper-scissors**.

---

### 👨‍💻 About the Project

This game and webiste using streamlit was created mainly for summative project of a kid named Jonathan in his International Baccalaureate (IB) school. Due to joining the Coding Co-coriculerm, it has been his responsibility to learn as much as possible and so his best specifically at the final project, which is this project. So enjoy!!!

Inspiration from: [Álvaro Mejía](https://alvarodsci.wixsite.com/alvaro-mejia)

Author : [Jonathan Barack Watratan :heart_eyes: ](https://youtu.be/PXqcHi2fkXI?si=izGnDTLoUFaTqdLr)

---
"""
)
