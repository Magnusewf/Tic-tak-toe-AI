from tensorflow.keras.models import load_model
import random


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


def spiler_skal_plassere(spiler, all_mulig_posisjoner):
    while True:
        move = int(input('Hvilken posisjon vil du legge til? '))-1
        if move in all_mulig_posisjoner:
            spiler[move] = True
            break
        else:
            print('Posisjonen er tatte, prøv igjen.')

def spill_mot_computer():
    spiler1= [False]*9
    spiler2= [False]*9

    hvemsom_starter = input('Do you want to start? (y/n)')

    if hvemsom_starter == 'y':
        model = load_model('forste_model_tic_tak_toe_p2.h5')
    else:
        model = load_model('forste_model_tic_tak_toe.h5')
    for x in range(9):

        all_mulig_posisjoner = finner_mulige_trekk(spiler1, spiler2)

        if hvemsom_starter == 'y':
            if x % 2 == 0:
                spiler_skal_plassere(spiler1, all_mulig_posisjoner)
            else:
                best_move = None
                best_prediction = None

                for move in all_mulig_posisjoner:
                    combined = spiler1 + spiler2
                    combined[move+9] = True
                    prediction = model.predict([combined*1])
                    print(prediction, move)
                    if best_move is None or prediction > best_prediction:
                        best_move = move
                        best_prediction = prediction
                spiler2[best_move] = True
        else:
            if x % 2 == 0:
                best_move = None
                best_prediction = None

                for move in all_mulig_posisjoner:
                    combined = spiler1 + spiler2
                    combined[move] = True
                    prediction = model.predict([combined*1])
                    print(prediction, move)
                    if best_move is None or prediction > best_prediction:
                        best_move = move
                        best_prediction = prediction
                spiler1[best_move] = True
            else:
                spiler_skal_plassere(spiler2, all_mulig_posisjoner)

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

