import random
import json
import PySimpleGUI as sg

def load_matchups(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
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
            choice_popups(team1, team2)
            return team1

        elif values[team2]:
            choice_popups(team2, team1)
            return team2
    return None  # In case no selection is made

def choice_popups(winning_team, losing_team):
    if "11. UNC" in losing_team:
        sg.popup("Wtf u mean man...", "You sure about that???", font='Helvetica 14', background_color='#880808', button_color=('white', '#4CAF50'))
    elif "11. UNC" in winning_team:
        sg.popup("I C U", "Noice choice.", font='Helvetica 14', background_color='#008000', button_color=('white', '#4CAF50'))
    elif "DOOK" in winning_team:
        sg.popup("Gross", "Must be a flaggot or sum", font='Helvetica 14', background_color='#880808', button_color=('white', '#4CAF50'))
    elif "DOOK" in losing_team:
        sg.popup("I C U", "Noice choice.", font='Helvetica 14', background_color='#008000', button_color=('white', '#4CAF50'))
    elif "69 GAWD" in winning_team :
        sg.popup("Freaky Ahh..", "Wahp Wahp Wahp Wahp", font='Helvetica 14', background_color='#FFC0CB', button_color=('white', '#4CAF50'))
    elif "69 GAWD" in losing_team:
        sg.popup("Freaky Ahh..", "Dot fck em up", font='Helvetica 14', background_color='#FFC0CB', button_color=('white', '#4CAF50'))
    elif "MICHIGAN ST" in winning_team:
        sg.popup("SPARTY PARTY", "S/o Diesel", font='Helvetica 14', background_color='#008000', button_color=('white', '#4CAF50'))

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
                winner = handle_tie(user_names, team1, team2, round_name, region)

            match_results[reg].append(winner)
        sg.popup(f"{reg} {round_name} Results", '\n'.join(match_results[reg]), font='Helvetica 12', background_color='#000000', button_color=('white', '#4CAF50'))

    # Return winners
    return match_results

# Function for Tie Votes
def handle_tie(user_names, team1, team2, round_name, region):
    options = ["GRANT", "LUKE", "MR. FOLK", "HUNTER BURY",
               "MEAT SHIELD", "REEZE","MONEY MITCH", "MIKE",
               "SMUT", "LELAND", "REDHEAD", "SOMI", "TROJAN",
               "PRADIESEL"
            ]
    user = random.choice(user_names)
    while True:
        selection = random.choice(options)
        response = handle_tiebreaker_response(user, selection)
        if response:
            break
        #sg.popup("TIEBREAKER", f"{user} Pls call {selection} to decide.", font='Helvetica 12', background_color='#000000', button_color=('white', '#4CAF50'))
    return get_user_vote(team1, team2, selection, round_name, region)

def handle_tiebreaker_response(user, selection):
    layout = [
        [sg.Text(f"{user} Pls call {selection} to decide. Did they answer?", font='Helvetica 12', background_color='#000000')],
        [sg.Radio("Duh", 'random', key="duh"), sg.Radio("Nah :'(", 'random', key="nah")],
        [sg.Button('SUBMIT', font='Helvetica 12', button_color=('white', '#4CAF50'))]
    ]
    window = sg.Window("TIEBREAKER", layout, element_justification='center')

    event, values = window.read()
    window.close()
    if event == 'SUBMIT':
        if values["duh"]:
            return True

        elif values["nah"]:
            return False
    return False  # In case no selection is made
