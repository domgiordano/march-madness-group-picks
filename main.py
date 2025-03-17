import PySimpleGUI as sg
import random
import json

# Function to prompt for a number of users and gather their names
def get_user_names():
    layout = [
        [sg.Text('How many users are participating?', font='Helvetica 14')],
        [sg.InputText(key='num_users', font='Helvetica 12')],
        [sg.Button('SUBMIT', font='Helvetica 12', button_color=('white', '#4CAF50'))]
    ]
    window = sg.Window('Number of Players', layout, element_justification='center')

    event, values = window.read()
    num_users = int(values['num_users']) if values['num_users'].isdigit() else 1
    window.close()

    user_names = []
    for i in range(num_users):
        layout = [
            [sg.Text(f'Enter name for User {i + 1}', font='Helvetica 14')],
            [sg.InputText(key=f'user_{i}', font='Helvetica 12')],
            [sg.Button('SUBMIT', font='Helvetica 12', button_color=('white', '#4CAF50'))]
        ]
        window = sg.Window('Enter Name', layout, element_justification='center')
        event, values = window.read()

        user_names.append(values[f'user_{i}'])
        window.close()

    return user_names

# Function to simulate matchups and get user predictions using radio buttons
def get_user_vote(team1, team2, user_name, round_name, region):
    layout = [
        [sg.Text(f"{user_name}'s Vote:", font='Helvetica 14')],
        [sg.Radio(team1, 'winner', key=team1), sg.Radio(team2, 'winner', key=team2)],
        [sg.Button('SUBMIT', font='Helvetica 12', button_color=('white', '#4CAF50'))]
    ]
    window = sg.Window(f"{region}: {round_name}", layout, element_justification='center')

    event, values = window.read()
    window.close()
    if event == 'SUBMIT':
        if values[team1]:
            return team1
        elif values[team2]:
            return team2
    return None  # In case no selection is made

# Function to simulate matchups and get votes from all users
def get_matchup_winner(team1, team2, user_names, round_name, region):
    user_votes = {}

    for user in user_names:
        winner = get_user_vote(team1, team2, user, round_name, region)
        if winner:
            user_votes[user] = winner

    return user_votes

# Function to simulate the rounds and get the winners
def round_matchups(matchups, user_names, round_name):
    match_results = {}
    for reg in matchups:
        match_results[reg] = []
    for reg in matchups:
        region = matchups[reg]
        for i in range(0, len(region), 2):
            team1, team2 = region[i], region[i + 1]
            user_votes = get_matchup_winner(team1, team2, user_names, round_name, reg)

            # Count the votes
            vote_counts = {team1: 0, team2: 0}
            for vote in user_votes.values():
                if vote == team1:
                    vote_counts[team1] += 1
                elif vote == team2:
                    vote_counts[team2] += 1

            # Determine the winner
            if vote_counts[team1] > vote_counts[team2]:
                winner = team1
            elif vote_counts[team2] > vote_counts[team1]:
                winner = team2
            else:
                # Tie: Randomly decide winner
                winner = handle_tie(team1, team2, round_name, region)

            match_results[reg].append(winner)
        sg.popup(f"{reg} {round_name} Results", '\n'.join(match_results[reg]), font='Helvetica 12', background_color='#000000', button_color=('white', '#4CAF50'))

    # Return winners
    return match_results

def handle_tie(team1, team2, round_name, region):
    options = ["GRANT", "LUKE", "MR. FOLK", "HUNTER BURY",
               "MEAT SHIELD", "REEZE","MONEY MITCH", "MIKE",
               "SMUT", "LELAND", "REDHEAD", "SOMI", "TROJAN"
            ]
    selection = random.choice(options)
    sg.popup(f"Tie! Pls call {selection} to decide.", font='Helvetica 12', background_color='#000000', button_color=('white', '#4CAF50'))
    return get_user_vote(team1, team2, "TIEBREAKER", round_name, region)
def process_bracket(user_names):
    matchups = load_matchups()

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

def load_matchups():
    with open('data/teams-2025.json', 'r') as file:
        data = json.load(file)
    return data

def main():
    user_names = get_user_names()  # Get user names
    process_bracket(user_names)  # Start the bracket processing

if __name__ == "__main__":
    print("STARTING...")
    main()
    print("DONE.")
