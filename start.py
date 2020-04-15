import numpy as np
from util import Game,Player


def start_game(g):
    P1sym = 1
    AIsym = 2
    P1 = Player(symbol = P1sym,agent="human")
    AI_1 = Player(symbol=AIsym,strategy="learn")
    while(1):
        free = g.get_play_spots()
        board = g.ret_board()
        print (board)
        row,col = P1.play(board,free)
        g.update_spot(row,col,P1sym)
        board = g.ret_board()
        print (board)
        if (g.check_victory(P1)==P1sym):
            AI_1.AI_update_state_record('loss')
            break
        free = g.get_play_spots()
        if len(free)==0:
            print ("Game Drawn")
            AI_1.AI_update_state_record('draw')
            break
        bcop = np.copy(board)
        row,col = AI_1.play(bcop,free)
        g.update_spot(row,col,AIsym)
        if (g.check_victory(AI_1)==AIsym):
            AI_1.AI_update_state_record('win')
            break

g = Game()
print ("game1")
start_game(g)
g.reset_board()
print ("game2")
start_game(g)
print ("printing State Record after 2 games")
print (Player.state_record)

