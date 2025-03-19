import PySimpleGUI as sg
from matchups import load_matchups, round_matchups
from users import get_user_names

def process_bracket(user_names):
    matchups = load_matchups('data/teams-2025.json')

    # Round of 64
    r64_results = round_matchups(matchups, user_names, "Round of 64")
    # Round of 32
    r32_results = round_matchups(r64_results, user_names, "Round of 32")
    # Sweet 16
    s16_results = round_matchups(r32_results, user_names, "Sweeeeeeet 16")
    # Elite 8
    e8_results = round_matchups(s16_results, user_names, "Elite 8")
    # Final 4
    f4_matchups = {
        "FINAL 4": [
            e8_results["SOUTH"][0],
            e8_results["WEST"][0],
            e8_results["EAST"][0],
            e8_results["MIDWEST"][0]
        ]
    }
    f4_results = round_matchups(f4_matchups, user_names, "")
    # Championship
    champion_result = round_matchups(f4_results, user_names, "")
    sg.popup("CHAMPION", champion_result["FINAL 4"][0], font='Helvetica 14', background_color='#ffd700', button_color=('white', '#4CAF50'))

def main():
    user_names = get_user_names()  # Get user names
    process_bracket(user_names)  # Start the bracket processing

if __name__ == "__main__":
    print("STARTING...")
    main()
    print("DONE.")
