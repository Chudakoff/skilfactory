def print_board(board):
    print(' ', 0, 1, 2)
    for i in range(3):
        print(i, *board[i])


def take_input(player_token):
    valid = False
    while not valid:
        print(f"Игрок, на какую позицию ходим '{player_token}'?")
        row = input('Введите номер строки для хода (0-2): ')
        col = input('Введите номер столбца для хода (0-2): ')
        move = (row, col)
        try:
            move = tuple(map(int, move))
        except:
            print("Введена некорректная информация! Вы уверены, что ввели числа?")
            continue
        if 0 <= move[0] <= 2 and 0 <= move[1] <= 2:
            if str(board[move[0]][move[1]]) not in "XO":
                board[move[0]][move[1]] = player_token
                valid = True
            else:
                print("Эта клетка уже занята!")
        else:
            print("Некорректный ввод. Введите число от 0 до 2.")


def check_win(board):
    board_lst = []
    for i in board:
        board_lst += i
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board_lst[each[0]] == board_lst[each[1]] == board_lst[each[2]] == 'O' or \
                board_lst[each[0]] == board_lst[each[1]] == board_lst[each[2]] == 'X':
            return board_lst[each[0]]
    return False


def main(board):
    counter = 0
    win = False
    while not win:
        print_board(board)
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1

        tmp = check_win(board)
        if tmp:
            print(f'Игрок "{tmp}" выиграл!')
            break
        if counter == 9:
            print("На этот раз ничья!")
            break
    print_board(board)


board = [["-" for _ in range(3)] for _ in range(3)]
main(board)
