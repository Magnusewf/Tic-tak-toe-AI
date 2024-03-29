from tensorflow.keras.models import load_model
import numpy as np
import csv
import threading



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


def simulate_game(model_p1, model_p2):
    spiler1= [False]*9
    spiler2= [False]*9
    game_matrix = np.empty((0, 18), bool)  # Initialize the game matrix
    for x in range(9):
        all_mulig_posisjoner=finner_mulige_trekk(spiler1, spiler2)
        if x % 2 == 0:
            combined_list = []
            for move in all_mulig_posisjoner:
                combined = spiler1 + spiler2
                combined[move] = True
                combined_list.append(combined*1)
            predictions = model_p1.predict(combined_list, verbose=0)
            sansynlighet_for_pos = predictions.flatten()**2
            
            probabilities = sansynlighet_for_pos / sansynlighet_for_pos.sum()
            pos_i_listen_til_trekk = np.random.choice(np.arange(len(sansynlighet_for_pos)), p=probabilities)
            spiler1[all_mulig_posisjoner[pos_i_listen_til_trekk]] = True
 
        else:
            combined_list = []
            for move in all_mulig_posisjoner:
                combined = spiler1 + spiler2
                combined[move+9] = True
                combined_list.append(combined*1)
            predictions = model_p2.predict(combined_list, verbose=0)
            sansynlighet_for_pos = predictions.flatten()**2
            
            probabilities = sansynlighet_for_pos / sansynlighet_for_pos.sum()
            pos_i_listen_til_trekk = np.random.choice(np.arange(len(sansynlighet_for_pos)), p=probabilities)
            spiler2[all_mulig_posisjoner[pos_i_listen_til_trekk]] = True
        game_matrix = np.vstack([game_matrix, spiler1 + spiler2]) 
        if har_noen_vunnet(spiler1):
            game_matrix=legger_til_vinner(x+1, 1, game_matrix)
            return game_matrix
        elif har_noen_vunnet(spiler2):
            game_matrix=legger_til_vinner(x+1, 2, game_matrix)
            return game_matrix
        
    game_matrix=legger_til_vinner(9, 0, game_matrix)
    return game_matrix


def writing_to_csv(antall_ganger, fillnavn):
    model_p1 = load_model('Modeler\\forste_model_tic_tak_toe.h5')
    model_p2 = load_model('Modeler\\forste_model_tic_tak_toe_p2.h5')
    if fillnavn == 'data_tic_tak_toe_v1.csv':
        hvem = 'p1'
    else:   
        hvem = 'p2'
    for x in range(antall_ganger):
        print(x, hvem)
        result = simulate_game(model_p1, model_p2)
        with open(fillnavn, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)


threading.Thread(target=writing_to_csv, args=(10000, 'Data set\data_tic_tak_toe_v1_eval.csv')).start()

