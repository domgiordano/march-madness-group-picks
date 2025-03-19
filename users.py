import PySimpleGUI as sg

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

        user_names.append(values[f'user_{i}'].upper())
        window.close()

    return user_names
