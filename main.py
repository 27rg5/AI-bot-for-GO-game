from copy import deepcopy
from read import readInput
from write import writeOutput
from host import GO

player_b=0
player_w=0

def neigh_al(i, j, board, player):
    neighbors = go.detect_neighbor(i, j) 
    group_allies = []
    for ne in neighbors:
        if board[ne[0]][ne[1]] == player:
            group_allies.append(ne)
    return group_allies


def al_pos(i, j, board, player):

    if not (i < 5 and j < 5 and i >= 0 and j >= 0):
        return []
    
    all_allies = []
    neighbors = neigh_al(i, j, board, player)
    all_allies.append((i, j))
    visited = {}
    visited[(i, j)] = True
    while True:
        temp_list = neighbors
        neighbors = []
        for x, y in temp_list:
            if (x, y) not in visited and board[x][y] == player:
                all_allies.append((x, y))
                visited[(x, y)] = True
                next_neighbor = neigh_al(x, y, board, player)
                for ne in next_neighbor:
                    neighbors.append(ne)
        if len(neighbors) == 0:
            return []
    return all_allies
    

def pos(i, j, board, player):
    stack = [(i, j)]  
    ally_members = []  
    while stack:
        piece = stack.pop()
        ally_members.append(piece)
        neighbor_allies = neigh_al(piece[0], piece[1], board, player)
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members


def lib_c(i, j, board, player):
    my_all_allies = pos(i, j, board, player)
    for ally in my_all_allies:
        neighbors = go.detect_neighbor(ally[0], ally[1])
        for piece in neighbors:
            if board[piece[0]][piece[1]] == 0:
                
                return True
    return False


def deadp(player, board):
    died_pieces = []

    for i in range(0, 5):
        for j in range(0, 5):

            if board[i][j] == player:

                if not lib_c(i, j, board, player):
                    died_pieces.append((i, j))
    return died_pieces


def rm_deadp(died_pieces, board):
    for piece in died_pieces:
        board[piece[0]][piece[1]] = 0
    return board


def lib_pos(i, j,board,player):
    liberties=set()
    allyMembers = pos(i, j,board,player)
    for member in allyMembers:
        neighbors = go.detect_neighbor(member[0], member[1])
        for piece in neighbors:
            if board[piece[0]][piece[1]] == 0:
                
                liberties=liberties|set([piece])

    return list(liberties)


def lib_pos_neigh(i,j,board,player):
    liberties = set()
    neighbors = go.detect_neighbor(i,j)
    for piece in neighbors:
        if board[piece[0]][piece[1]] == 0:
            liberties=liberties|set([piece])

    return list(liberties)
    
def practicem(i, j, board, player):
    new_board = board

    new_board[i][j] = player
    died_pieces = deadp(3 - player, new_board)

    if len(died_pieces) == 0:
        return new_board,len(died_pieces),new_board
    else:
        next_board = rm_deadp(died_pieces, new_board)

        return next_board,len(died_pieces),new_board



def options_in_moves(player, previous_board, new_board):
    moves = []
    imp_moves=[]
    
    all_liberties_vala_move=set()

    for i in range(0, 5):
        for j in range(0, 5):
            if new_board[i][j]==player:    
                self_end=lib_pos(i,j,new_board,player)
                if len(self_end)==1:
                    all_liberties_vala_move=all_liberties_vala_move|set(self_end)
                    if i==0 or i==4 or j==0 or j==4:
                        safe_positions=lib_pos_neigh(self_end[0][0],self_end[0][1],new_board,player)
                        if safe_positions:
                            all_liberties_vala_move=all_liberties_vala_move|set(safe_positions)

     
            elif new_board[i][j]==3-player:
                oppo_end=lib_pos(i,j,new_board,3-player)
                all_liberties_vala_move=all_liberties_vala_move|set(oppo_end)
   
   
    if len(list(all_liberties_vala_move)):
        for x in list(all_liberties_vala_move):
            tri_board = deepcopy(new_board)
            board_after_move,died_pieces,_ = practicem(x[0],x[1], tri_board, player)
            if lib_c(x[0], x[1], board_after_move, player)and board_after_move != new_board and board_after_move != previous_board:
                imp_moves.append((x[0], x[1],died_pieces)) 
        if len(imp_moves)!= 0:   
         
            return sorted(imp_moves, key=lambda x: x[2],reverse=True)
        
        
    
        
    for i in range(0, 5):
        for j in range(0, 5):
          
            if  new_board[i][j] == 0:
              
                trial_board = deepcopy(new_board)
                board_after_move,died_pieces,_ = practicem(i, j, trial_board, player)
                if lib_c(i, j, board_after_move, player) and board_after_move != new_board and board_after_move != previous_board:
                       
                    moves.append((i, j,died_pieces))
                            


    return sorted(moves, key=lambda x: x[2],reverse=True)
        
def joint_pieces(i, j, board, player):
    count = []
    visited = []
    count.append(go.detect_neighbor_ally(i, j))
    count_list = []
    for a in count:
        if (type(a) == list):
            for b in a:
                count_list.append(b)
        else:
            count_list.append(a)
    for ally in count_list:
        if ally not in visited:
            visited.append(ally)
            count.append(go.detect_neighbor_ally(ally[0], ally[1]))
            for a in count:
                if (type(a) == list):
                    for b in a:
                        count_list.append(b)
                else:
                    count_list.append(a)
    return len(visited)

def joint_pieces1(board, player):
    count = 0
    for i in range(5):
        for j in range(5):
            if (board[i][j] == player):
                neighbor_allies = go.detect_neighbor_ally(i, j)
                if (i == 0 or i == 4 or j == 0 or j == 4):
                    if(len(neighbor_allies) >= 2):
                        count = count + 0.2
                        
                else:
                    if(len(neighbor_allies) == 4):
                        count = count + 0.2
                    elif(len(neighbor_allies) == 3 or len(neighbor_allies) == 2):
                        count = count + 0.1
                    elif(len(neighbor_allies) == 0):
                        count = count - 0.1
    return count


def play_strategy(board, player):
    count = 0
    for i in range(5):
        for j in range(5):
            if (board[i][j] == player):
                if(i == 0 or i == 4 or j == 0 or j == 4):
                    count = count - 1
                elif(i == 2 and j == 2):
                    count = count + 1
    return count

def assess_funct(board, player,died_pieces_black,died_pieces_white):
    black_liberty = 0
    white_liberty = 0
    black_count = 0
    white_count = 0
    black_edge_moves = 0
    white_edge_moves = 0
    black_group_size = []
    white_group_size = []
    avg_black_group = 0
    avg_white_group = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == 1:
                #black_group_size.append(joint_pieces(i, j, board, 1))
                black_liberty = black_liberty + go.find_liberty(i, j)
                
                black_count += 1
                
            elif board[i][j] == 2:
                #white_group_size.append(joint_pieces(i, j, board, 2))
                white_liberty = white_liberty + go.find_liberty(i, j)
                                    
                white_count += 1
                
    komi = 2.5
        
    avg_black_group = joint_pieces1(board, 1)
    avg_white_group = joint_pieces1(board, 2)
    
    black_eyes = 0
    white_eyes = 0

    black_edge_moves = play_strategy(board, 1)
    white_edge_moves = play_strategy(board, 2)
    black_eyes = eyes(board, 1)
    white_eyes = eyes(board, 2)
        
    eval_value = abs(black_count - white_count) + abs(black_liberty - white_liberty) 

    return eval_value


def topm(board,previous_board,player,depth):
    score, actions = move_max(board,previous_board,player,depth, float("-inf"), float("inf"),board)
    if len(actions) > 0:
        return actions[0]  
    else:
        return "PASS"


def move_max(board,previous_board,player,depth, alpha, beta,new_board_without_died_pieces):
    global player_b
    global player_w
    if player==2:
        died_pieces_white=len(deadp(player,new_board_without_died_pieces))
        player_w=player_w+died_pieces_white
    if player==1:
        died_pieces_black=len(deadp(player,new_board_without_died_pieces))
        player_b=player_b+died_pieces_black
        
    
    
    
    if depth == 0:
        value = assess_funct(board,player,player_b,player_w)
        if player==1:
            player_b=player_b-len(deadp(1,new_board_without_died_pieces))
        if player==2:
            player_w=player_w-len(deadp(2,new_board_without_died_pieces))
        return value,[]
        

    max_score = float("-inf")
    max_score_actions = []
    my_moves = options_in_moves(player, previous_board, board)
    if len(my_moves)==25:
        return 100,[(2,2)]
    for move in my_moves:
        trial_board = deepcopy(board)
        next_board,died_pieces,new_board_without_died_pieces = practicem(move[0], move[1], trial_board, player)
        score, actions = move_min(next_board,board,3-player,depth-1, alpha, beta,new_board_without_died_pieces)
        
        
        if score > max_score:
            max_score = score
            max_score_actions = [move] + actions
            

        if max_score > beta:
            return max_score, max_score_actions

        if max_score > alpha:
            alpha = max_score

    return max_score, max_score_actions    
    
def move_min(board,previous_board,player,depth, alpha, beta,new_board_without_died_pieces):
    global player_b
    global player_w
    if player==2:
        died_pieces_white=len(deadp(player,new_board_without_died_pieces))
        player_w=player_w+died_pieces_white
    if player==1:
        died_pieces_black=len(deadp(player,new_board_without_died_pieces))
        player_b=player_b+died_pieces_black
        
    if depth == 0:
        value = assess_funct(board,player,player_b,player_w)
        if player==1:
            player_b=player_b-len(deadp(1,new_board_without_died_pieces))
        if player==2:
            player_w=player_w-len(deadp(2,new_board_without_died_pieces))
        return value,[]

    min_score = float("inf")
    min_score_actions = []
    my_moves = options_in_moves(player, previous_board, board)
    
    for move in my_moves:
        trial_board = deepcopy(board)
        next_board,died_pieces,new_board_without_died_pieces = practicem(move[0], move[1], trial_board, player)
        score, actions = move_max(next_board,board,3-player,depth-1, alpha, beta,new_board_without_died_pieces)
       
        if score < min_score:
            min_score = score
            min_score_actions = [move] + actions
            

        if min_score < alpha:
            return min_score, min_score_actions

        if min_score < beta:
            alpha = min_score

    return min_score, min_score_actions


player, previous_board, board = readInput(5)
go = GO(5)
go.set_board(player, previous_board, board)
depth=2
good_move = topm(board,previous_board,player,depth)
writeOutput(good_move)
