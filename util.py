import numpy as np
import random
from itertools import repeat

class Game():
    def __init__(self):
        self.board_stat = np.zeros((3,3))

    def ret_board(self):
        return self.board_stat
    
    def reset_board(self):
        self.board_stat = np.zeros((3,3))
        
    def check_victory(self,player):
        to_comp = np.full(3,player.symbol)
        board = self.board_stat
        fr = board[0,:]
        sr = board[1,:]
        tr = board[2,:]
        fc = board[:,0]
        sc = board[:,1]
        tc = board[:,2]
        fd = np.diagonal(board)
        sd = np.fliplr(board).diagonal()
        fn = np.array_equal
        if (fn(to_comp,fr) or fn(to_comp,sr) or fn(to_comp,tr) or fn(to_comp,fc) or fn(to_comp,sc) or fn(to_comp,tc) or fn(to_comp,fd) or fn(to_comp,sd)):
            print ("{} wins".format(player.agent))
            return player.symbol
        return 0
    
    def update_spot(self,row,col,player):
        self.board_stat[row][col] = player
        
    def get_play_spots(self):
        bfl = list(self.board_stat.flatten())
        free_spots=[]
        for count,ele in enumerate(bfl):
            if ele==0:
                row,col = int(count/3), count%3
                free_spots.append([row,col])
        return free_spots
    
class Player():
    state_record = {'index':[]}
    
    def __init__(self,symbol,agent ="AI",strategy = "learn"):
        self.strategy = strategy
        self.agent = agent
        self.symbol = symbol
        self.game_record = {'index':[]}
    
    def play_human(self,free_spots):
        print ("Available slots are")
        for count,ele in enumerate(free_spots):
            print ("{}.{}".format(count+1,ele))
        spot = input("select spot to play: ")
        print ("played {}".format(free_spots[int(spot)-1]))
        spot = free_spots[int(spot)-1]
        return spot[0],spot[1]
    
    def play_AI_random(self,free_spots):
        sel = list(range(0,len(free_spots)))
        spot = random.choice(sel)
        print ("AI play")
        print (free_spots[spot])
        return free_spots[spot][0],free_spots[spot][1]
    
    def lookup_state(self,board,free_spots=[]):
        found = False
        ind = 0
        count = 0
        for count,ele in enumerate(Player.state_record['index']):
            ind = count
            if (np.array_equal(board,ele)):
                print ("found state in record")
                found = True
                return ind
        if not found:
            print ("adding state to record")
            Player.state_record['index'].append(board)
            len_state = len(Player.state_record['index'])
            new_state_options = []
            for i in free_spots:
                new_state_options.extend(repeat(i,5))
            Player.state_record[len_state - 1] = new_state_options
            return len_state - 1

    def play_AI_learn(self,board,free_spots):
        ind = self.lookup_state(board,free_spots)
        print ("Printing State Record")
        print (Player.state_record)
        state_options = Player.state_record[ind]
        spot = random.choice(state_options)
        print ("appending game record with board {}".format(board))
        self.game_record['index'].append(board)
        ind2 = len(self.game_record['index'])
        self.game_record[ind2-1] = spot
        print ("AI play")
        print (spot)
        print ("printing game record")
        print (self.game_record)
        return spot[0],spot[1]
    
    def AI_update_state_record(self, result):
        print ("updating state record with the game record")
        print (self.game_record)
        for count,i in enumerate(self.game_record['index']):
            print ("Looking up Player record")
            ind = self.lookup_state(i)
            if result == 'win':
                Player.state_record[ind].append(self.game_record[count])
                Player.state_record[ind].append(self.game_record[count])
                print ("inside win appending; state record after appending {} on index {} of state record".format(self.game_record[count],ind))
                print (Player.state_record[ind])
            elif result == 'loss':
                Player.state_record[ind].remove(self.game_record[count])
                Player.state_record[ind].remove(self.game_record[count])
                print ("inside loss removing; state record after removing {} on index {} of state record".format(self.game_record[count],ind))
                print (Player.state_record[ind])
            elif result == 'draw':
                Player.state_record[ind].append(self.game_record[count])
                print ("inside draw appending; state record after appending {} on index {} of state record".format(self.game_record[count],ind))
                print (Player.state_record[ind])
        return

    def play(self,board,free_spots):
        if self.agent == "human":
            return self.play_human(free_spots)
        elif self.strategy == "random":
            return self.play_AI_random(free_spots)
        elif self.strategy == "learn":
            return self.play_AI_learn(board,free_spots)