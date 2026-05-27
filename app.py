import streamlit as st
from tamagotchi_module.tamagotchi import Tamagotchi
from config import PAGE_CONFIG
from tamagotchi_module.functions import *
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components


def main():

    # page config
    st.set_page_config(**PAGE_CONFIG)
    st.title("🐾 Tamagotchi Game")

    # load pet and difficulty level
    my_pet, diff_level = load_pet()
    if my_pet is None:
        return

    # initialize history
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(
            columns=list(my_pet.get_parameters().keys())
        )

    # Set an anchor for every time the page reruns
    components.html("<div id='top'></div>", height=1)

    # select an action
    action = show_menu(my_pet)
    if action:
        call_action(my_pet, action)

        # go to the anchor
        components.html(
            """<script> document.getElementById("top").scrollIntoView({behavior: "smooth"}); </script>""",
            height=0,
        )

        # set difficulty and check if the pet is still alive
        my_pet.difficulty(diff_level)
        my_pet.death()

    # in case is Game Over
    if not my_pet.alive:
        st.markdown("## 💀 **GAME OVER**")
        st.error(f"{my_pet.name} has almost died. Social Services are on their way.")
        st.image("assets/almostdead.jpg", width=500)

        if st.button("🔁 To start a New Game, refresh the page."):
            for key in st.session_state.keys():
                del st.session_state[key]

        return

    # normal action when the pet is alive
    else:

        # get and store parameters
        parameters = my_pet.get_parameters()
        df_temp = pd.DataFrame([parameters])
        st.session_state.data = pd.concat(
            [st.session_state.data, df_temp], ignore_index=True
        )

        # df with life parameters
        df = pd.DataFrame(
            {
                "Parameter": ["Hunger", "Boredom", "Tiredness", "Dirtiness"],
                "Value": [
                    parameters["hunger"],
                    parameters["boredom"],
                    parameters["tiredness"],
                    parameters["dirtiness"],
                ],
            }
        )

        # columns
        col1, sep12, col2, sep23, col3 = st.columns([1, 0.2, 2, 0.2, 2])

        # Col 1: pic & general status and params
        with col1:

            st.write(f"### **Name**: {parameters['name']}")
            status_params = [
                parameters[k] for k in ["hunger", "boredom", "tiredness", "dirtiness"]
            ]

            if parameters["is_asleep"]:
                st.image("assets/sleeping.jpg", width=500)
            elif st.session_state.get("playing", False):
                st.image("assets/playing.jpg", width=500)
            elif max(status_params) > 6:
                st.image("assets/sad.jpg", width=500)
            else:
                st.image("assets/happy.jpg", width=500)

            # status, meals
            st.write(
                f"#####  {parameters['name']} is {'Sleeping 😴' if parameters['is_asleep'] else 'Awake 🐈'}"
            )
            st.write(f"##### **Available meals**: {parameters['meals']} 🍚")

        # Vertical divider
        with sep12:
            st.markdown(
                "<div style='border-left: 2px solid #bbb; height: 400px; margin: auto'></div>",
                unsafe_allow_html=True,
            )

        # Col 2: basic status
        with col2:
            st.markdown("### 📺 Message Screen")

            # Mostrar botones si estamos jugando
            if st.session_state.get("playing", False):
                st.info("Choose your move:")
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    if st.button("✂️", key="scissors_btn"):
                        my_pet.play("scissors")
                with col_b:
                    if st.button("📄", key="paper_btn"):
                        my_pet.play("paper")
                with col_c:
                    if st.button("🪨", key="rock_btn"):
                        my_pet.play("rock")

            # Mostrar mensaje final
            message = st.session_state.get("message", None)
            if message:
                msg_type, msg_text = message

                if msg_type == "success":
                    st.success(msg_text)
                elif msg_type == "warning":
                    st.warning(msg_text)
                elif msg_type == "error":
                    st.error(msg_text)
                elif msg_type == "info":
                    st.info(msg_text)
                else:
                    st.write(msg_text)

            if action == None:
                st.info("🚀 Choose an action to continue")
            else:
                if st.button("✅ Continue"):
                    st.session_state["message"] = None
                    st.session_state["playing"] = False  # in case we played

        # Vertical divider
        with sep23:
            st.markdown(
                "<div style='border-left: 2px solid #bbb; height: 400px; margin: auto'></div>",
                unsafe_allow_html=True,
            )

        # Col3: bar plot
        with col3:

            fig_bars = px.bar(
                df,
                x="Parameter",
                y="Value",
                color="Parameter",
                range_y=[0, 10],
                title="Pet Status",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_bars, use_container_width=True)

        st.empty()

        # History data
        st.markdown("### ⏱️ Parameter History")
        df_hist = st.session_state.data[["hunger", "boredom", "tiredness", "dirtiness"]]

        # avoid showing the plot if there's only one observation
        if len(df_hist) > 1:
            fig_line = px.line(
                df_hist,
                title="Parameters evolution",
                labels={"index": "rounds", "value": "times used"},
            )
            st.plotly_chart(fig_line, use_container_width=True)


if __name__ == "__main__":
    main()