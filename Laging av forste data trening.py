import random
import numpy as np
import csv

def har_noen_vunnet(vector1):
    if vector1[0] and vector1[1] and vector1[2]:
        return True
    elif vector1[3] and vector1[4] and vector1[5]:
        return True
    elif vector1[6] and vector1[7] and vector1[8]:
        return True
    elif vector1[0] and vector1[3] and vector1[6]:
        return True
    elif vector1[1] and vector1[4] and vector1[7]:
        return True
    elif vector1[2] and vector1[5] and vector1[8]:
        return True
    elif vector1[0] and vector1[4] and vector1[8]:
        return True
    elif vector1[2] and vector1[4] and vector1[6]:
        return True
    else:
        return False
    
def print_board(spiler1, spiler2):
    board = [' ']*9
    for i in range(9):
        if spiler1[i]:
            board[i] = 'X'
        elif spiler2[i]:
            board[i] = 'O'
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print('---------')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print('---------')
    print(f'{board[6]} | {board[7]} | {board[8]}')
    print('\n')

def finner_mulige_trekk(spiler1, spiler2):
    all_mulig_posisjoner = []
    for z in range(9):
        if not spiler1[z] and not spiler2[z]:
            all_mulig_posisjoner.append(z)
    return all_mulig_posisjoner

def legger_til_vinner(runder, vinner, game_matrix):
    resulat = np.array([vinner]*runder)
    resulat = resulat.reshape(-1, 1)  # Reshape to 2D
    game_matrix = np.hstack([game_matrix, resulat])
    return game_matrix
def simulate_game():
    spiler1= [False]*9
    spiler2= [False]*9
    game_matrix = np.empty((0, 18), bool)  # Initialize the game matrix
    for x in range(9):
        all_mulig_posisjoner=finner_mulige_trekk(spiler1, spiler2)
        if not(x % 2 == 0):
            spiler2[random.choice(all_mulig_posisjoner)] = True
        else:
            spiler1[random.choice(all_mulig_posisjoner)] = True
        game_matrix = np.vstack([game_matrix, spiler1 + spiler2])  # Add the current state to the game matrix

        #print_board(spiler1, spiler2)
        if har_noen_vunnet(spiler1):
            game_matrix=legger_til_vinner(x+1, 1, game_matrix)
            return game_matrix
        elif har_noen_vunnet(spiler2):
            game_matrix=legger_til_vinner(x+1, 2, game_matrix)
            return game_matrix
        
    game_matrix=legger_til_vinner(9, 0, game_matrix)
    return game_matrix


def writing_to_csv(antall_ganger):
    for x in range(antall_ganger):
        print(x)
        result = simulate_game()
        with open("data_tic_tak_toe_v0.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)

def spiler_skal_plassere(spiler1, all_mulig_posisjoner):
    while True:
        move = int(input('Hvilken posisjon vil du legge til? '))-1
        if move in all_mulig_posisjoner:
            spiler1[move] = True
            break
        else:
            print('Posisjonen er tatte, prøv igjen.')

def spill_mot_computer():
    spiler1= [False]*9
    spiler2= [False]*9
    hvemsom_starter = input('Do you want to start? (y/n)')
    for x in range(9):

        all_mulig_posisjoner = finner_mulige_trekk(spiler1, spiler2)

        if hvemsom_starter == 'y':
            if x % 2 == 0:
                spiler_skal_plassere(spiler1, all_mulig_posisjoner)
            else:
                spiler2[random.choice(all_mulig_posisjoner)] = True
        else:
            if x % 2 == 0:
                spiler2[random.choice(all_mulig_posisjoner)] = True
            else:
                spiler_skal_plassere(spiler1, all_mulig_posisjoner)

        print_board(spiler1, spiler2)
        if har_noen_vunnet(spiler1):
            return "Spiller 1 har vunnet"
        elif har_noen_vunnet(spiler2):
            return "Spiller 2 har vunnet"
    return "Ingen har vant"

while True:
    print(spill_mot_computer())
    if input('Vil du spille igjen? (y/n)') == 'n':
        break







