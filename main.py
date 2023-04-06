import random
import copy


class Board:
    def __init__(self):
        self.size = 5
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.player1_pos = (0, 0)
        self.player2_pos = 1, 1
        self.current_player = 1
        self.moves = 0

    def display(self):
        print()
        print()
        print("     ", end="")
        for j in range(self.size):
            print(j, end=" ")
        print()
        print("     ", end="")
        for j in range(self.size):
            print(end="==")
        print()

        for i in range(self.size):
            print(i, end=" || ")
            for j in range(self.size):
                if self.board[i][j] == 1:
                    print("1", end=" ")
                elif self.board[i][j] == 2:
                    print("2", end=" ")
                elif self.board[i][j] == -1:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print()


    def get_legal_moves(self):
        legal_moves = []
        if self.current_player == 1:
            pos = self.player1_pos
            opp_pos = self.player2_pos
        elif self.current_player == 2:
            pos = self.player2_pos
            opp_pos = self.player1_pos
        else:
            return

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                new_pos = (pos[0]+dx, pos[1]+dy)
                if 0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size:
                    if self.board[new_pos[0]][new_pos[1]] == 0 and new_pos != opp_pos:
                        legal_moves.append(new_pos)
        return legal_moves

    def make_move(self, move):
        if self.current_player == 1:
            self.board[self.player1_pos[0]][self.player1_pos[1]] = -1
            self.player1_pos = move
            self.board[self.player1_pos[0]][self.player1_pos[1]] = 1
            self.current_player = 2

        elif self.current_player == 2:
            self.board[self.player2_pos[0]][self.player2_pos[1]] = -1
            self.player2_pos = move
            self.board[self.player2_pos[0]][self.player2_pos[1]] = 2
            self.current_player = 1

    def undo_move(self, move):
        if self.current_player == 1:
            self.board[self.player1_pos[0]][self.player1_pos[1]] = -1
            self.player1_pos = move
            self.board[self.player1_pos[0]][self.player1_pos[1]] = 0
            self.current_player = 2

        elif self.current_player == 2:
            self.board[self.player2_pos[0]][self.player2_pos[1]] = -1
            self.player2_pos = move
            self.board[self.player2_pos[0]][self.player2_pos[1]] = 0
            self.current_player = 1

    def is_game_over(self):
        if self.moves == self.size**2 or len(self.get_legal_moves()) == 0:
            return True
        return False

    def evaluate(self):
        if len(self.get_legal_moves()) == 0:
            if self.current_player == 1:
                return float('inf')

            if self.current_player == 2:
                return float('-inf')
        return 0

    def get_winner(self):
        if self.is_game_over():
            if self.player1_pos == self.player2_pos:
                return 0
            elif len(self.get_legal_moves()) == 0:
                return 3 - self.current_player
        return None


def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():

        return board.evaluate(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in board.get_legal_moves():

            child = copy.deepcopy(board)
            child.make_move(move)

            eval, _ = minimax(child, depth - 1, False)
            child.undo_move(move)
            if eval==max_eval:
                if (move is not None) and (best_move is not None):
                    best_move = random.choice([move, best_move])
            if eval > max_eval:
                max_eval = eval
                best_move = move

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for move in board.get_legal_moves():

            child = copy.deepcopy(board)
            child.make_move(move)

            eval, _ = minimax(child, depth - 1, True)
            child.undo_move(move)
            if eval==min_eval:
                if (move is not None) and (best_move is not None):
                    best_move = random.choice([move, best_move])
            if eval < min_eval:
                min_eval = eval
                best_move = move

        return min_eval, best_move


def play_game(player1,player2):
    win=0
    kw=0            #buffor
    board = Board()
    mvsm=False       # True = minimax vs minimax | False = random vs minimax
    los =False       # random point or not
    depth = int(input("podaj głępokość= "))
    #depth =3
    N = int(input("Podaj wartość N: "))
    #N=4


    if los:
        board.player1_pos = (random.randint(0, N - 1), random.randint(0, N - 1))
        board.player2_pos = (random.randint(0, N - 1), random.randint(0, N - 1))

    else:
        while (True):
            print("Enter coordinates for the first point:")
            x1 = int(input("Enter x coordinate: "))
            y1 = int(input("Enter y coordinate: "))

            print("Enter coordinates for the second point:")
            x2 = int(input("Enter x coordinate: "))
            y2 = int(input("Enter y coordinate: "))

            if 0 <= x1 < N and 0 <= y1 < N and 0 <= x2 < N and 0 <= y2 < N and x1 !=x2:
                print("The entered coordinates are within range.")
                board.player1_pos = (x1, y1)
                board.player2_pos = (x2, y2)
                break
            else:
                print("At least one of the entered coordinates is out of range. Please try again.")

    #####################################################################################################

    board.board = [[0 for _ in range(N)] for _ in range(N)]  # tablica
    board.size=N
    board.board[board.player1_pos[0]][board.player1_pos[1]] = 1
    board.board[board.player2_pos[0]][board.player2_pos[1]] = 2

    while (not board.is_game_over()):

        child = copy.deepcopy(board)

        board.display()

        if mvsm:
            if board.current_player == 1:
                _, move = minimax(child, depth, False)
            else:
                _, move = minimax(child, depth, True)

                if move is not None:
                    gw=0
                else:
                    gw=1
        else:
            if board.current_player == 1:

                legal_moves = board.get_legal_moves()
                move = random.choice(legal_moves)

            else:
                _, move = minimax(child, depth, True)

                if move is not None:
                    gw=0
                else:
                    gw=1

        if move is not None:
            board.make_move(move)
        else:

            if len(child.get_legal_moves()) ==0:
                win=1
                break
            else:
                move = random.choice(child.get_legal_moves())
                board.make_move(move)

    winner = board.get_winner()
    #######################################################################

    board.display()

    board.current_player = 1
    if board.current_player == 1:
        legal_moves = board.get_legal_moves()
        board.current_player=2
        if len(legal_moves)==0:
            kw=1

    if board.current_player == 2:
        legal_moves = board.get_legal_moves()
        if len(legal_moves) == 0:
            gw = 1

    if move is not None:
        board.make_move(move)

####################    winner
    if gw == 1 and kw==1:
        print("Game over, draw!")
        return player1 , player2
    else:
        if win ==0:
            print("Game over, player", winner, "wins!")
            if winner ==1:
                return player1+1,player2
            if winner ==2:
                return player1,player2+1

        else:
            print("Game over, komputer give up player", winner, "wins!")

#########################
player1=0
player2=0
test=False
if test:

    for i in range(0,100):
        player1,player2=play_game(player1,player2)

    print("Wins of player 1= ",player1)
    print("Wins of player 2= ",player2)
    print("remis= ",100-player2-player1)
else:
    player1, player2 = play_game(player1, player2)