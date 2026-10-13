"""A small, beginner-friendly adventure in a mysterious forest."""

import random

import streamlit as st


# These image URLs are displayed only on the story stage where they belong.
GAME_VERSION = 4
FOREST_EVENTS = [
    "A talking mushroom offers you directions, then admits it is facing the wrong way.",
    "A confused owl asks if you have seen its glasses. They are on its head.",
    "A suspicious squirrel searches your pockets for acorns. It finds lint and looks offended.",
    "A pinecone drops nearby. The forest claims it was a warning; the pinecone declines to comment.",
]
FOREST_IMAGE = (
    "https://images.unsplash.com/photo-1448375240586-882707db888b"
    "?auto=format&fit=crop&w=1400&h=560&q=85"
)
FOX_IMAGE = (
    "https://images.unsplash.com/photo-1474511320723-9a56873867b5"
    "?auto=format&fit=crop&w=900&h=520&q=85"
)
GATE_IMAGE = (
    "https://images.unsplash.com/photo-1511497584788-876760111969"
    "?auto=format&fit=crop&w=1400&h=560&q=85"
)


def start_game():
    """Set up a fresh game in Streamlit's session state."""
    st.session_state.game_version = GAME_VERSION
    st.session_state.stage = 0
    st.session_state.has_key = False
    st.session_state.helped_fox = False
    st.session_state.gate_choice = None
    st.session_state.energy = 2
    st.session_state.stars = 0
    st.session_state.inventory = []
    st.session_state.feedback = "Your quest: find a way through the forest before nightfall."
    st.session_state.ending = None
    st.session_state.forest_event = random.choice(FOREST_EVENTS)
    st.session_state.gate_reaction = ""


def show_choice_buttons(options, keys, callback):
    """Show icon-led actions that move the story forward one stage."""
    icons = {
        "take_key": "🗝️",
        "leave_key": "🏮",
        "free_fox": "🦊",
        "leave_fox": "🥾",
        "use_key": "🔓",
        "ask_fox": "🤝",
        "follow_lantern": "✨",
    }
    columns = st.columns(len(options))
    for column, option, key in zip(columns, options, keys):
        with column:
            st.button(
                f"{icons[key]}  {option}",
                key=f"choice_{key}",
                on_click=callback,
                args=(key,),
                width="stretch",
            )


def choose_key(choice):
    st.session_state.has_key = choice == "take_key"
    if st.session_state.has_key:
        st.session_state.inventory.append("Silver key")
        st.session_state.stars += 1
        st.session_state.feedback = (
            "You pocket the silver key. The forest gasps, “Hey, I was using that "
            "to open my snack cupboard!”"
        )
    else:
        st.session_state.inventory.append("Lantern trail")
        st.session_state.feedback = (
            "You follow the lantern. It bobs proudly, then bumps into a tree. "
            "The tree says it happens every Thursday."
        )
    st.session_state.forest_event = random.choice(FOREST_EVENTS)
    st.session_state.stage = 1


def choose_fox(choice):
    st.session_state.helped_fox = choice == "free_fox"
    if st.session_state.helped_fox:
        st.session_state.energy = min(3, st.session_state.energy + 1)
        st.session_state.stars += 2
        st.session_state.inventory.append("Fox friend")
        st.session_state.inventory.append("Moonstone")
        st.session_state.feedback = (
            "The fox is free! “Finally, someone competent,” it says, then gives "
            "you a moonstone and offers gate advice."
        )
    else:
        st.session_state.energy = max(0, st.session_state.energy - 1)
        st.session_state.feedback = (
            "You hurry on. The fox calls, “I hope you enjoy making your own "
            "terrible decisions!” The brambles steal a little energy."
        )
    st.session_state.forest_event = random.choice(FOREST_EVENTS)
    st.session_state.stage = 2


def choose_gate(choice):
    st.session_state.gate_choice = choice
    if choice == "use_key" and st.session_state.has_key:
        st.session_state.stars += 2
        st.session_state.gate_reaction = (
            "The key fits! The gate compliments your excellent key-management skills."
        )
        st.session_state.ending = (
            "A new beginning",
            "The key turns with a click. Beyond the gate, dawn waits in a quiet village. "
            "The gate asks you to leave a five-star review.",
            "success",
        )
    elif choice == "ask_fox" and st.session_state.helped_fox:
        st.session_state.stars += 2
        st.session_state.gate_reaction = (
            "The fox squeezes through and says, “Try not to look surprised. I do this professionally.”"
        )
        st.session_state.ending = (
            "Friend of the forest",
            "The grateful fox slips through a gap and leads you to a hidden way out. "
            "It insists this was all part of its very affordable consulting package.",
            "success",
        )
    elif choice == "follow_lantern":
        st.session_state.stars += 1
        st.session_state.gate_reaction = (
            "You choose the lantern trail. It gives a tiny salute and immediately gets lost."
        )
        st.session_state.ending = (
            "The forest lets you go",
            "The lantern guides you safely back to the forest's edge, though its whispers follow. "
            "It is mostly asking whether you know the way back.",
            "success",
        )
    else:
        st.session_state.gate_reaction = (
            "The gate stays shut. Somewhere, the fox says, “I did mention the key thing.”"
        )
        st.session_state.ending = (
            "Lost among the trees",
            "The gate will not open. As the trees close around you, the lantern glows brighter. "
            "A nearby mushroom offers directions, but it is still facing the wrong way.",
            "failure",
        )
    st.session_state.forest_event = random.choice(FOREST_EVENTS)
    st.session_state.stage = 3


def show_hud():
    """Show the player's energy, collected stars, inventory, and quest."""
    with st.container(border=True):
        st.markdown("#### ✨ Quest: Find a way through the forest")
        energy_column, stars_column, inventory_column = st.columns([1, 1, 2])
        with energy_column:
            st.metric("💚 Energy", f"{st.session_state.energy}/3")
        with stars_column:
            st.metric("⭐ Stars", st.session_state.stars)
        with inventory_column:
            items = st.session_state.inventory
            st.markdown("**🎒 Inventory**")
            st.write(", ".join(items) if items else "No items yet")

        quest_done = (
            st.session_state.stage == 3 and st.session_state.ending[2] == "success"
        )
        if quest_done:
            quest_text = "Quest complete!"
        elif st.session_state.stage == 3:
            quest_text = "Quest ended — try another path"
        else:
            quest_text = "Journey progress"
        st.progress(
            1.0 if quest_done else st.session_state.stage / 3,
            text=quest_text,
        )


def show_ending():
    """Show the ending, collected rewards, and a button to play again."""
    title, description, result = st.session_state.ending
    achievements = {
        "A new beginning": "Keeper of the Extremely Convenient Key",
        "Friend of the forest": "Fox's Favorite (it denies having favorites)",
        "The forest lets you go": "Lantern's Unpaid Intern",
        "Lost among the trees": "Bravely Confused Pathfinder",
    }
    with st.container(border=True):
        result_icon = "🌟" if result == "success" else "🌲"
        st.markdown(f"## {result_icon} Adventure complete")
        if result == "success":
            st.success(f"### {title}\n\n{description}")
        else:
            st.error(f"### {title}\n\n{description}")

        if st.session_state.gate_reaction:
            st.info(f"🗯️ {st.session_state.gate_reaction}")

        st.markdown(
            f"### 🏅 Achievement unlocked: {achievements[title]}"
        )
        st.markdown(
            "**Plot twist:** The lantern is the forest's night-shift manager. "
            "This whole adventure was a very dramatic exit interview. The fox is its union representative."
        )

        reward_column, inventory_column = st.columns([1, 2])
        with reward_column:
            st.metric("✨ Stars earned", st.session_state.stars)
        with inventory_column:
            items = st.session_state.inventory
            st.markdown("**🎒 Your keepsakes**")
            st.write(", ".join(items) if items else "No items collected")

    if st.button("🌟 Play Again", type="primary", width="stretch"):
        start_game()
        st.rerun()


st.set_page_config(page_title="The Mysterious Forest", page_icon="🌲", layout="centered")

# A centered, responsive content area and woodland colors keep the story easy to follow.
st.markdown(
    """
    <style>
    .block-container {
        width: min(100%, 1080px);
        max-width: 1080px;
        box-sizing: border-box;
        margin: 0 auto;
        padding: 3.5rem clamp(0.75rem, 3vw, 1.5rem) 1.25rem;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 50% 0%, rgba(77, 119, 72, 0.25), transparent 48%),
            linear-gradient(180deg, #10251f 0%, #18372c 55%, #10251f 100%);
        color: #f5f0df;
    }
    h1, h2, h3, p, label { color: #f5f0df !important; }
    h1, h2, h3 { letter-spacing: 0.015em; }
    .hero { padding: 0.4rem 0.25rem; }
    .hero h1 {
        color: #ffe6a3 !important;
        margin: 0;
        font-size: clamp(1.6rem, 4vw, 2.45rem);
        text-shadow: 0 0 18px rgba(245, 200, 96, 0.32);
    }
    .hero p { color: #e4e8d4 !important; margin: 0.3rem 0 0; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(232, 202, 133, 0.4);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(28, 58, 43, 0.92), rgba(16, 37, 30, 0.96));
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
    }
    [data-testid="stButton"] button {
        min-height: 3.5rem;
        border: 1px solid #dbbd72;
        border-radius: 14px;
        background: linear-gradient(145deg, #f1d995, #d6b965);
        color: #183128;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
        white-space: normal;
        transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }
    [data-testid="stButton"] button:hover {
        border-color: #fff0bd;
        background: linear-gradient(145deg, #fff0bd, #ead080);
        color: #10251f;
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(229, 190, 92, 0.24);
    }
    [data-testid="stAlert"] {
        border-radius: 16px;
    }
    [data-testid="stMetric"] {
        padding: 0.65rem 0.75rem;
        border: 1px solid rgba(232, 202, 133, 0.34);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(43, 78, 56, 0.82), rgba(27, 53, 40, 0.82));
    }
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #b7d18b, #f1d27b);
    }
    [data-testid="stImage"] img {
        display: block;
        width: 100%;
        height: auto;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.26);
    }
    @media (max-width: 640px) {
        .block-container { padding-top: 3rem; }
        .hero h1 { font-size: 1.55rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Reset once for a new player or a session made by the previous game version.
needs_new_game = (
    st.session_state.get("game_version") != GAME_VERSION
    or st.session_state.get("stage") not in (0, 1, 2, 3)
)
if not needs_new_game and st.session_state.stage == 3:
    needs_new_game = st.session_state.get("gate_choice") not in (
        "use_key",
        "ask_fox",
        "follow_lantern",
    )
if needs_new_game:
    start_game()

with st.container(border=True):
    heading, restart_column = st.columns([5, 1], vertical_alignment="center")
    with heading:
        st.markdown(
            """
            <div class="hero">
                <h1>🌲 The Mysterious Forest 🌙</h1>
                <p>Warning: the trees have opinions, and none of them are botanists.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with restart_column:
        if st.button("↻ Restart", help="Start a new adventure", width="stretch"):
            start_game()
            st.rerun()

stage = st.session_state.stage
stage_names = ["The silver key", "The fox in the brambles", "The iron gate", "Adventure complete"]
stage_label = "Adventure complete" if stage == 3 else f"Choice {stage + 1} of 3 · {stage_names[stage]}"
st.markdown(f"### 🧭 {stage_label}")
show_hud()

if st.session_state.feedback and stage < 3:
    st.info(f"🧚 **Forest whisper:** {st.session_state.feedback}")

if stage < 3:
    st.caption(f"🍄 Forest encounter: {st.session_state.forest_event}")

if stage == 0:
    with st.container(border=True):
        image_column, story_column = st.columns([1.35, 1], gap="large", vertical_alignment="center")
        with image_column:
            st.image(FOREST_IMAGE, caption="The forest is full of secrets.", width="stretch")
        with story_column:
            st.markdown(
                """
                ### 🌙 The trees are whispering...
                At dusk, you find yourself beneath trees that whisper your name.
                A pale lantern bobs between the branches, and a cold wind rises.
                One tree whispers, “Could you keep it down? Some of us are photosynthesizing.”

                Near your feet lies a **silver key**. What do you do?

                *The lantern flickers: “Choose wisely, traveler. I forgot where I put my map.”*
                """
            )
        show_choice_buttons(
            ["Pick it up and keep it.", "Leave it and follow the lantern."],
            ["take_key", "leave_key"],
            choose_key,
        )

elif stage == 1:
    with st.container(border=True):
        image_column, story_column = st.columns([1.15, 1], gap="large", vertical_alignment="center")
        with image_column:
            st.image(FOX_IMAGE, caption="A fox waits for your help.", width="stretch")
        with story_column:
            st.markdown(
                """
                ### 🦊 A cry in the brambles
                A small fox is caught in a tangle of thorny vines.
                Its bright eyes meet yours. How do you respond?
                """
            )
            st.info(
                "“Well, this is awkward,” the fox says. “I was trying to look mysterious, "
                "not get tangled in decorative shrubbery.”"
            )
        show_choice_buttons(
            ["Carefully free the fox.", "Keep walking toward a distant gate."],
            ["free_fox", "leave_fox"],
            choose_fox,
        )

elif stage == 2:
    with st.container(border=True):
        image_column, story_column = st.columns([1.35, 1], gap="large", vertical_alignment="center")
        with image_column:
            st.image(
                GATE_IMAGE,
                caption="An old gate stands between you and the forest's edge.",
                width="stretch",
            )
        with story_column:
            st.markdown(
                """
                ### 🗝️ The old iron gate
                The path ends at an old iron gate. How will you get through?

                *A carved message glows faintly: “Key, kindness, or the lantern's way.”*
                The gate adds, “Please do not kick me. I am load-bearing.”
                """
            )
        show_choice_buttons(
            ["Try the silver key.", "Ask the fox for help.", "Turn back toward the lantern."],
            ["use_key", "ask_fox", "follow_lantern"],
            choose_gate,
        )

elif stage == 3 and st.session_state.gate_choice is not None:
    with st.container(border=True):
        show_ending()
