from copy import deepcopy
import json
import math
from multiprocessing import Pool
import time
import random
import numpy as np
#from game.NN import neuralnet


random.seed(12345)
class time_out(Exception):
  pass
class Game:
  
 
 #legal_dir={["p","P"]:(1,0),["r","R"]:[ (1,0),(-1,0),(0,1),(0,-1)],["b","B"]:[(1,1),(1,-1),(-1,1),(-1,-1)],["n","N"]:(()) }
 
  def __init__(self):
   self.node_count = 0 

   self.piece_index = {'pawns': 0, 'knights': 1, 'bishops': 2, 'rooks': 3, 'queen': 4, 'king': 5}
   
   self.real_board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]
   self.positions= {
        "white": {
            "king": (7, 4),
            "queen": [(7, 3)],
            "rooks": [(7, 0), (7, 7)],
            "bishops": [(7, 2), (7, 5)],
            "knights": [(7, 1), (7, 6)],
            "pawns": [(6, c) for c in range(8)]
        },
    
        # Black pieces
        "black": {
            "king": (0, 4),
            "queen": [(0, 3)],
            "rooks": [(0, 0), (0, 7)],
            "bishops": [(0, 2), (0, 5)],
            "knights": [(0, 1), (0, 6)],
            "pawns": [(1, c) for c in range(8)]
        }
        }
   self.king_checkers={'white':[],'black':[]}
   self.castling_flags={
       'white': {'kingside': True, 'queenside': True},
       'black': {'kingside': True, 'queenside': True}
   }
   self.castle_order = [
    ('white', 'kingside'),
    ('white', 'queenside'),
    ('black', 'kingside'),
    ('black', 'queenside'),
]
   self.moves_log= {
      "from":[]
      ,"to":[],
      "pawn":[],
      "capture":[],
      'pawn/capture':[],
      'castling':[]
      }
   self.board_snapshots=[]
   self.nextindex=None
   self.index_leftoff=None
   self.board_snapshots=[{"board":deepcopy(self.positions),"turn":"white","enpassent":None,"castling": {
         "white": self.castling_rights("white"),   
          "black": self.castling_rights("black")},"checkers":deepcopy(self.king_checkers),"castle_flags":deepcopy(self.castling_flags)
 }]
   self.z_board = [[[0 for _ in range(2)] for _ in range(6)] for _ in range(64)]
   self.z_castle = [random.getrandbits(64) for _ in range(4)]
   self.z_turn = random.getrandbits(64)
   for i in range(64):
    for j in range(6):
      for k in range(2):
        self.z_board[i][j][k]=random.getrandbits(64)
   self.transpos_table={ }
   self.hash_key=self.get_zobrist_key(self.positions,'white')
   self.hash_stack = [] 
   self.quiescence_stack=[]
  def _clear_castle_right(self, color, side):
    if self.castling_flags[color][side]:
        idx = self.castle_order.index((color, side))
        self.hash_key ^= self.z_castle[idx]
        self.castling_flags[color][side] = False 
  def parse_move(self,square):
   file='abcdefgh'
   col_letter=square[0]
   row_no=8-int(square[1])
   col=file.index(col_letter)
   return row_no,col
  def unparse_move(self,pos_r,pos_c):
  # file=['a','b','c','d','e','f','g','h']
   file='abcdefgh'
 
   col_letter=file[pos_c]
   row_no_str=(-pos_r+8)
   square=col_letter+str(row_no_str)
   return square
  def is_pawn2(self,r,c):
     return  self.real_board[r][c] in ('P','p')
  def is_knight2(self,r,c):
      return self.real_board[r][c] in ('N','n')
  def is_bishop2(self,r,c):
      return self.real_board[r][c] in ('B','b')
  def is_rook2(self,r,c):
      return self.real_board[r][c] in ('R','r')
  def is_queen2(self,r,c):
      return self.real_board[r][c] in ('Q','q')
  def is_king2(self,r,c):
      return self.real_board[r][c] in ('K','k')
  def is_white2(self,r,c):
      if self.real_board[r][c]=='.':
          return False
      return self.real_board[r][c].isupper()
  def is_black2(self,r,c):
      if self.real_board[r][c]=='.':
          return False
      return self.real_board[r][c].islower()
  def is_friend2(self,pos_r,pos_c,target_r,target_c):
     if self.is_black2(pos_r,pos_c) and self.is_black2(target_r,target_c):
         return True
     elif self.is_white2(pos_r,pos_c) and self.is_white2(target_r,target_c):
         return True
     return False
  def is_pawn(self,square):
   r,c=self.parse_move(square)
   return  self.real_board[r][c]in('P','p')
  def is_knight(self,square):
   r,c=self.parse_move(square)
   return  self.real_board[r][c] in ('N','n')
  def is_bishop(self,square):
   r,c=self.parse_move(square)
   return  self.real_board[r][c] in ('B','b')
  def is_rook(self,square):
   r,c=self.parse_move(square)
   return  self.real_board[r][c] in ('R','r')
  def is_queen(self,square):
   r,c=self.parse_move(square)
   return  self.real_board[r][c]in('Q','q')
  def is_king(self,square):
   r,c=self.parse_move(square)
   return  self.real_board[r][c]in('K','k')
  def is_empty(self,square):
   r,c=self.parse_move(square)
   return self.real_board[r][c]=="."
  def is_empty2(self,r,c):
    return self.real_board[r][c]=='.'
  def is_white(self,square):
   r,c=self.parse_move(square)
   if(self.is_empty(square)):
    return False
   return self.real_board[r][c].isupper()
  def is_black(self,square):
   r,c=self.parse_move(square)
   if(self.is_empty(square)):
    return False
   return self.real_board[r][c].islower()
  # need to define a generic function that takes the square and define the type of square if the movement is legal
  def is_friend(self,pos_r,pos_c,target_r,target_c):
   if self.is_black2(pos_r,pos_c) and self.is_black2(target_r,target_c):
         return True
   elif self.is_white2(pos_r,pos_c) and self.is_white2(target_r,target_c):
         return True
   return False
  
 
 
  def rook_legal(self,pos_r,pos_c,target_r,target_c):
     rook_dir=[(1,0),(-1,0),(0,1),(0,-1)] 
     dx,dy=(0,0)
     if (target_c == pos_c and target_r > pos_r):
      dx,dy=rook_dir[-4]
     elif (target_c == pos_c and target_r < pos_r):
       dx,dy=rook_dir[-3]
     elif (target_r == pos_r and target_c > pos_c):
       dx,dy=rook_dir[-2]    
     elif (target_r == pos_r and target_c < pos_c):
       dx,dy=rook_dir[-1]
     else:
       return False
   
     for_limit=0
   
     if(target_c == pos_c):
       for_limit=abs(target_r-pos_r)
     else:
       for_limit=abs(target_c-pos_c)
 
     for i in range(for_limit):
       newpos_r=pos_r+dx
       newpos_c=pos_c+dy
       if((newpos_r,newpos_c)==(target_r,target_c)):
        if(not self.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
         pos_r=newpos_r
         pos_c=newpos_c
         return True
        else:
         return False
       if(not self.is_empty2(newpos_r,newpos_c)):
        return False
       pos_r=newpos_r
       pos_c=newpos_c
   
     return False
  
 
  def knight_legal(self,pos_r,pos_c,target_r,target_c):
   KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
   if (target_r-pos_r, target_c-pos_c) not in KNIGHT_DELTAS:
         return False
   if self.is_empty2(target_r,target_c) or not self.is_friend(pos_r,pos_c,target_r,target_c):
      
         return True
   else:
         return False
    
  def bishop_legal(self,pos_r,pos_c,target_r,target_c):
   orig_r, orig_c = pos_r, pos_c
   bish_silding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1)]  
   (dx,dy)=(0,0)
   if(abs(pos_r-target_r)==abs(target_c-pos_c) and (pos_r,pos_c)!=(target_r,target_c)):
    if(target_c<pos_c and target_r<pos_r):
     dx,dy=bish_silding_dirs[3]
    elif(target_c<pos_c  and target_r>pos_r):
     dx,dy=bish_silding_dirs[1]
    elif(target_c>pos_c  and target_r>pos_r):
     dx,dy=bish_silding_dirs[0]
    elif(target_c>pos_c  and target_r<pos_r):
       dx,dy=bish_silding_dirs[2]
   else:
     return False
 
   for_limit=abs(pos_c-target_c)
   for i in range(for_limit):
     newpos_r=pos_r+dx
     newpos_c=pos_c+dy
     if((newpos_r,newpos_c)==(target_r,target_c)):
      if(not self.is_friend( orig_r, orig_c,newpos_r,newpos_c)):
       pos_r=newpos_r
       pos_c=newpos_c
       return True
      else:
       return False
     if(not self.is_empty2(newpos_r,newpos_c)):
      return False
     pos_r=newpos_r
     pos_c=newpos_c
 
   return False
     
  def queen_legal(self,pos_r,pos_c,target_r,target_c):
   queen_sliding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
   (dx,dy)=(0,0)
 
   if((pos_r,pos_c)==(target_r,target_c)):
     return False
 
   if(abs(pos_r-target_r)==abs(target_c-pos_c)):
     if(target_c<pos_c and target_r<pos_r):
      dx,dy=queen_sliding_dirs[3]
     elif(target_c<pos_c  and target_r>pos_r):
      dx,dy=queen_sliding_dirs[1]
     elif(target_c>pos_c  and target_r>pos_r):
      dx,dy=queen_sliding_dirs[0]
     elif(target_c>pos_c  and target_r<pos_r):
        dx,dy=queen_sliding_dirs[2]
     for_limit=abs(pos_c-target_c)
 
   elif (target_c == pos_c and target_r > pos_r):
      dx,dy=queen_sliding_dirs[-4]
      for_limit=abs(target_r-pos_r)
   elif (target_c == pos_c and target_r < pos_r):
     dx,dy=queen_sliding_dirs[-3]
     for_limit=abs(target_r-pos_r)
   elif (target_r == pos_r and target_c > pos_c):
     dx,dy=queen_sliding_dirs[-2]    
     for_limit=abs(target_c-pos_c)
   elif (target_r == pos_r and target_c < pos_c):
     dx,dy=queen_sliding_dirs[-1]
     for_limit=abs(target_c-pos_c)
   else:
      return False
 
   for i in range(for_limit):
     newpos_r=pos_r+dx
     newpos_c=pos_c+dy
     if((newpos_r,newpos_c)==(target_r,target_c)):
      if(not self.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
       pos_r=newpos_r
       pos_c=newpos_c
       return True
      else:
       return False
     if(not self.is_empty2(newpos_r,newpos_c)):
      return False
     pos_r=newpos_r
     pos_c=newpos_c
   return False
  king_moved=False
 
   
  def king_legal(self,pos_r,pos_c,target_r,target_c):
        color= 'black' if self.is_black2(pos_r,pos_c) else 'white'
        king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
        (dx,dy)=(0,0)
        if(abs(pos_r-target_r)==1 and abs(target_c-pos_c)==1):
         if(target_c<pos_c and target_r<pos_r):
          dx,dy=king_dirs[3]
         elif(target_c<pos_c  and target_r>pos_r):
          dx,dy=king_dirs[1]
         elif(target_c>pos_c  and target_r>pos_r):
          dx,dy=king_dirs[0]
         elif(target_c>pos_c  and target_r<pos_r):
          dx,dy=king_dirs[2]
         else:
          return
        elif (target_r == pos_r and target_c > pos_c and self.is_rook2(target_r,target_c) and self.is_empty2(pos_r,pos_c+1) and  self.is_empty2(pos_r,pos_c+2) and not self.is_checked(pos_r,pos_c) and not self.can_be_checked(pos_r,pos_c,target_r,target_c,castlingflag=True) and not self.rook_or_king_moved(target_r,target_c,color)):
         dx,dy=(0,2)
        elif (target_r == pos_r and target_c < pos_c and self.is_rook2(target_r,target_c) and self.is_empty2(pos_r,pos_c-1) and  self.is_empty2(pos_r,pos_c-2) and self.is_empty2(pos_r,pos_c-3) and not self.is_checked(pos_r,pos_c) and not self.can_be_checked(pos_r,pos_c,target_r,target_c,castlingflag=True) and not self.rook_or_king_moved(target_r,target_c,color)):
         dx,dy=(0,-2)
        elif (target_c == pos_c and target_r > pos_r and target_r-pos_r==1):
         dx,dy=king_dirs[-4]
        elif (target_c == pos_c and target_r < pos_r and pos_r-target_r==1):
         dx,dy=king_dirs[-3]
        elif (target_r == pos_r and target_c > pos_c and target_c-pos_c==1):
         dx,dy=king_dirs[-2]
        elif (target_r == pos_r and target_c < pos_c and pos_c-target_c==1):
         dx,dy=king_dirs[-1]
        else:
         return False
        newpos_r=pos_r+dx
        newpos_c=pos_c+dy
        if(self.can_be_checked(pos_r,pos_c,newpos_r,newpos_c)):
         return False
 
       # --- 3. enemy-king adjacency rule, computed directly (no recursion) ---
        enemy_color = 'black' if self.is_white2(pos_r,pos_c) else 'white'
        enemy_kr, enemy_kc = self.positions[enemy_color]['king']
        not_next_to_enemy_king = max(abs(newpos_r-enemy_kr), abs(newpos_c-enemy_kc)) > 1
 
        if((self.is_empty2(newpos_r,newpos_c) or not self.is_friend(newpos_r,newpos_c,pos_r,pos_c))
          and not self.is_king2(newpos_r,newpos_c)
          and not_next_to_enemy_king):
           pos_r=newpos_r
           pos_c=newpos_c
           return True
        else:
           return False
       
  def rook_or_king_moved(self, r_r, r_c, color):
    side = 'queenside' if r_c == 0 else 'kingside'
    return not self.castling_flags[color][side]
  def pawn_legal(self,pos_r,pos_c,target_r,target_c):
   r,c=pos_r,pos_c
   tr,tc=target_r,target_c
   newpos_r=0
   newpos_c=0
   pawn_dirs=[(-1,0),(-1,1),(-1,-1),(-2,0)]
   pawn_dirs_negated=[(-dx, -dy) for dx, dy in pawn_dirs]
   
   (dx,dy)=(0,0)
   is_black=self.is_black2(pos_r,pos_c) 
   is_white=not is_black
   if(pos_c==target_c and pos_r==target_r+1 and self.is_empty2(target_r,target_c) and is_white):
     dx,dy=pawn_dirs[0]
   elif(pos_c==target_c and pos_r==target_r-1 and self.is_empty2(target_r,target_c) and is_black):
     dx,dy=pawn_dirs_negated[0]
   elif(pos_c==target_c and pos_r==target_r+2 and self.is_empty2(target_r,target_c) and  self.is_empty2(pos_r-1,pos_c) and pos_r==6 and is_white):
      dx,dy=pawn_dirs[-1]
   elif(pos_c==target_c and pos_r==target_r-2 and self.is_empty2(target_r,target_c) and  self.is_empty2(pos_r+1,pos_c) and pos_r==1 and is_black):
      dx,dy=pawn_dirs_negated[-1]
   elif(pos_c==target_c-1 and pos_r==target_r+1 and not self.is_empty2(target_r,target_c) and not self.is_friend(pos_r,pos_c,target_r,target_c) and is_white):
         dx,dy=pawn_dirs[1]
 
   elif(pos_c==target_c+1 and pos_r==target_r-1 and not self.is_empty2(target_r,target_c) and not self.is_friend(pos_r,pos_c,target_r,target_c) and is_black):
         dx,dy=pawn_dirs_negated[1] 
   elif(pos_c==target_c+1 and pos_r==target_r+1 and not self.is_empty2(target_r,target_c) and not self.is_friend(pos_r,pos_c,target_r,target_c) and is_white):
           dx,dy=pawn_dirs[2]
   
   elif(pos_c==target_c-1 and pos_r==target_r-1 and not self.is_empty2(target_r,target_c) and not self.is_friend(pos_r,pos_c,target_r,target_c) and is_black):
           dx,dy=pawn_dirs_negated[2]       
   
  # for enpassent ,we need to have list of moves that works like a log , and we need to have an if condition that checks if moving pawn two pieces forward is right through invoking the log list and see if column of target square has a pawn move that moved two steps forward and capture if found  
   elif(self.is_pawn2(r,c) and self.is_white2(r,c) and tr==r-1 and(self.is_pawn2(tr+1,tc) and not self.is_friend(r,c,tr+1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr+1,tc) and self.moves_log["from"][-1][0]==1 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc-1):
      
           return True
   elif(self.is_pawn2(r,c)  and self.is_white2(r,c) and tr==r-1 and(self.is_pawn2(tr+1,tc) and not self.is_friend(r,c,tr+1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr+1,tc) and self.moves_log["from"][-1][0]==1 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc+1):
 
    return True
   elif(self.is_pawn2(r,c) and self.is_black2(r,c) and tr==r+1 and (self.is_pawn2(tr-1,tc) and not self.is_friend(r,c,tr-1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr-1,tc) and self.moves_log["from"][-1][0]==6 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc+1):
    
    return True
   elif(self.is_pawn2(r,c)  and self.is_black2(r,c) and tr==r+1 and(self.is_pawn2(tr-1,tc) and not self.is_friend(r,c,tr-1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr-1,tc) and self.moves_log["from"][-1][0]==6 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc-1):
   
    return True
   else:
      return False
   pos_r=target_r
   pos_c=target_c
   
   return True
     
 
     
  def index_my_king(self,my_r,my_c):
   
   letter_config="black"if self.is_black2(my_r,my_c) else "white"
   return self.positions[letter_config]['king']
  
 
  def is_checked(self,kr,kc):
     king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
     KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
     pawn_dirs=[(-1,1),(-1,-1)]
     
     if(self.is_black2(kr,kc)):
       pawn_dirs=[(-dx,-dy) for dx,dy in pawn_dirs]
     enemy=[]
     color='black' if self.is_black2(kr,kc) else 'white'
     self.king_checkers[color]=[]
     for dx,dy in king_dirs:
           new_r,new_c=(kr,kc)
           while((0<=new_r+dx<=7 and 0<=new_c+dy<=7) ):
             next_r, next_c = new_r+dx, new_c+dy
             if(self.is_empty2(next_r,next_c)):
               new_r, new_c = next_r, next_c
             elif(self.is_friend(kr,kc,next_r,next_c)):
               break
             else:
               piece=self.get_piece(next_r,next_c)
               enemy.append((piece,(next_r,next_c)))
               break
             
     for dx,dy in KNIGHT_DELTAS:
           new_r,new_c=(kr,kc)
           if((0<=new_r+dx<=7 and 0<=new_c+dy<=7) ):
             new_r,new_c=(new_r+dx,new_c+dy)
             if(not self.is_empty2(new_r,new_c) and not self.is_friend(kr,kc,new_r,new_c) and self.is_knight2(new_r,new_c)):
               
               self.king_checkers[color].append(('knights',(new_r,new_c)))
               break  
     for dx,dy in pawn_dirs:
               new_r,new_c=(kr,kc)
               if((0<=new_r+dx<=7 and 0<=new_c+dy<=7) ):
                 new_r,new_c=(new_r+dx,new_c+dy)
                 if(not self.is_empty2(new_r,new_c) and not self.is_friend(kr,kc,new_r,new_c) and self.is_pawn2(new_r,new_c)):
                   
                   self.king_checkers[color].append(('pawns',(new_r,new_c)))  
                   break        
     for piece,(r,c) in enemy:
       if(piece=='rooks'):
        if  kr==r or kc==c:
         self.king_checkers[color].append((piece,(r,c)))
       if(piece=='bishops'): 
         if abs(kr-r)==abs(kc-c):
          self.king_checkers[color].append((piece,(r,c)))
       if(piece=='queen'):
         if (kr==r or kc==c) or abs(kr-r)==abs(kc-c):
           self.king_checkers[color].append((piece,(r,c)))
       else:
         continue
 
     return len(self.king_checkers[color] )>0
 
        
  
 
 
  dead_pieces={"white":[],"black":[]}
  
  def enpassent_corr(self,waspawn):
   fr=self.moves_log['from'][-1][0]
   tr=self.moves_log['to'][-1][0]
   tc=self.moves_log['to'][-1][1]
   if(waspawn):
     if(abs(fr-tr)==2):
      return (fr+tr)//2, tc
     else:
      return None  
   else:
     return None
 
  def castling_rights(self,turn):
    rooks = self.positions[turn]['rooks']
    rights = []
    if len(rooks) > 0:
        r_q, c_q = rooks[0]
        if not self.rook_or_king_moved(r_q, c_q, turn):
            rights.append(f"{turn}queen side ")
    if len(rooks) > 1:
        r_k, c_k = rooks[1]
        if not self.rook_or_king_moved(r_k, c_k, turn):
            rights.append(f"{turn}king side ")
    return " ".join(rights)
  def update_place(self,old_r,old_c,r,c,castlingflag=False):
      
    old_sq=self.unparse_move(old_r,old_c)
    color='white'if(self.is_white2(old_r,old_c)) else 'black'
    e_color='black'if(self.is_white2(old_r,old_c)) else 'white'
    ispawnmove=True if(self.is_pawn2(old_r,old_c)) else False
    iscapture=True if  not self.is_empty2(r,c) else False
    iscapture_or_pawnmove=iscapture or ispawnmove
    if(castlingflag):
      k_dy,r_dy=(2,-1) if(old_c<c) else(-2,1)
      self.positions[color]['king']=(old_r,old_c+k_dy)
      idx=self.positions[color]['rooks'].index((old_r,c))
      self.positions[color]['rooks'][idx]=(r,old_c+k_dy+r_dy)
      self._clear_castle_right(color, 'kingside')
      self._clear_castle_right(color, 'queenside')
      self.moves_log["from"].append((old_r,old_c))
      self.moves_log["to"].append((r,c))
      self.moves_log['castling'].append('true')
      self.moves_log['pawn/capture'].append(iscapture_or_pawnmove)
      self.moves_log['pawn'].append(ispawnmove)
    
      self.board_snapshots.append({"board":deepcopy(self.positions),"turn":color,"enpassent":self.enpassent_corr(ispawnmove),"castling": {
         "white": self.castling_rights("white"),   
         "black": self.castling_rights("black"),
     },"checkers":deepcopy(self.king_checkers),"castle_flags":deepcopy(self.castling_flags)})
    else:
 
  
     is_pieces={"king":self.is_king2(old_r,old_c),"bishops":self.is_bishop2(old_r,old_c),"knights":self.is_knight2(old_r,old_c),"queen":self.is_queen2(old_r,old_c),"pawns":self.is_pawn2(old_r,old_c),"rooks":self.is_rook2(old_r,old_c)}
     piece=None
     for key,value in is_pieces.items():
      if(value):
       piece=key
       break
     if(piece=='rooks' or piece=='bishops' or piece=='knights' or piece=='pawns' or piece=='queen'):
        if(piece=='rooks'):
          home_row=7 if color=='white' else 0
          if((old_r,old_c)==(home_row,0)):
            self._clear_castle_right(color, 'queenside')
          elif((old_r,old_c)==(home_row,7)):
           self._clear_castle_right(color, 'kingside')
        idx=self.positions[color][piece].index((old_r,old_c))
        for e_piece,e_pos in self.positions[e_color].items():
          if e_piece=='king':
           continue
          for e_r,e_c in e_pos:
            if(e_r,e_c)==(r,c):
              e_pos.remove((r,c))
              
              self.dead_pieces[e_color].append(e_piece)
              break
        self.positions[color][piece][idx]=(r,c)
        
     else:
        for e_piece,e_pos in self.positions[e_color].items():
         if e_piece=='king':
           continue
         for e_r,e_c in e_pos:
          if(e_r,e_c)==(r,c):
            e_pos.remove((r,c))
            self.dead_pieces[e_color].append(e_piece)
            break
        self.positions[color][piece]=(r,c)
        self._clear_castle_right(color, 'kingside')
        self._clear_castle_right(color, 'queenside')
  
     self.moves_log["from"].append((old_r,old_c))
     self.moves_log["to"].append((r,c))
     self.moves_log['pawn/capture'].append(iscapture_or_pawnmove)
     self.moves_log['pawn'].append(ispawnmove)
     self.moves_log['castling'].append('false')
     
     self.board_snapshots.append({"board":deepcopy(self.positions),"turn":color,"enpassent":self.enpassent_corr(ispawnmove),"castling": {
          "white": self.castling_rights("white"),   
          "black": self.castling_rights("black"),
      },"checkers":deepcopy(self.king_checkers),"castle_flags":deepcopy(self.castling_flags)})
  nextindex=None
  def is_three_fold(self):
    if(self.nextindex==None):
      self.nextindex=0
 
    for i in range(self.nextindex,len(self.board_snapshots)):
     count=0
     for j in range(i+1,len(self.board_snapshots)):
       if(self.board_snapshots[i]==self.board_snapshots[j]):
         count+=1
       if(count==2):
         self.nextindex=j
         return True
    return False  
   
  index_leftoff=None
  def isfifty_moves_draw(self):
    if(self.index_leftoff==None):
        self.index_leftoff=0
    
    total_since_leftoff = len(self.moves_log['pawn/capture']) - self.index_leftoff
    if total_since_leftoff < 50:
        return False

    movecount=0
    iscap_orpawn_count=0
    for i in range(self.index_leftoff,len(self.moves_log['pawn/capture'])):
      movecount+=1
      if(self.moves_log['pawn/capture'][i]):
        iscap_orpawn_count+=1
      if(movecount==50):
        break
    return iscap_orpawn_count==0
 
        
 
  def stalemate(self,kr,kc):
   color='white'if(self.is_white2(kr,kc)) else 'black'
   legal_moves=self.generate_legal_moves(color)
   if(len(legal_moves)==0) and not (self.is_checked(kr,kc)):
     return True
        
 
  def is_checkmated(self,kr,kc):
     color='white'if(self.is_white2(kr,kc)) else 'black'
     legal_moves=self.generate_legal_moves(color)
     if(len(legal_moves)==0) and (self.is_checked(kr,kc)):
       return True
     else:
       return False
 # castling/enpassent
  def is_board_end(self,r,c):
   return r==0 or r==7
  king_moved=True
  pawn_choices=['b','n','q','r']
 
  def move_piece(self,pos_sq,target_sq,to_promote=None,verified=False):
   pos=self.parse_move(pos_sq)
   r,c=pos
   (old_r,old_c)=(r,c)
   target=self.parse_move(target_sq)
   tr,tc=target
   color=None
   if(not self.is_empty2(r,c) and pos_sq!=target_sq and not self.is_king2(tr,tc)):
          #self.node_count+=1
          color='white'if(self.is_white2(r,c)) else 'black'
          k_r,k_c=self.index_my_king(r,c)
          legal_moves=[]
          is_pieces={"king":self.is_king2(old_r,old_c),"bishops":self.is_bishop2(old_r,old_c),"knights":self.is_knight2(old_r,old_c),"queen":self.is_queen2(old_r,old_c),"pawns":self.is_pawn2(old_r,old_c),"rooks":self.is_rook2(old_r,old_c)}
          piece=None
          for key,value in is_pieces.items():
              if(value):
               piece=key
               break
          if not verified:
            legal_moves = self.generate_legal_moves(color)
            if not ((piece,(r,c),(tr,tc)) in legal_moves):
              return False

          self.hash_stack.append(self.hash_key)   # NEW — save old hash before any mutation
          enemy_color = 'black' if color=='white' else 'white'  # NEW

          if(self.is_king2(r,c) and self.is_friend(r,c,tr,tc) and self.is_rook2(tr,tc)):
           k_dy,r_dy=(2,-1) if(tc>c) else(-2,1)
           self.hash_key ^= self._sq_hash(color,'king',r,c)          # NEW
           self.hash_key ^= self._sq_hash(color,'rooks',tr,tc)       # NEW
           self.update_place(r,c,tr,tc,castlingflag=True)
           self.real_board[r][c+k_dy]=self.real_board[r][c]
           self.real_board[r][c+k_dy+r_dy]=self.real_board[tr][tc]
           self.real_board[r][c]='.'
           self.real_board[tr][tc]='.'
           self.hash_key ^= self._sq_hash(color,'king', r, c+k_dy)          # NEW
           self.hash_key ^= self._sq_hash(color,'rooks', r, c+k_dy+r_dy)    # NEW
           self.hash_key ^= self.z_turn                                     # NEW
           return True

          elif(self.is_pawn2(r,c) and self.is_white2(r,c) and tr==r-1 and(self.is_pawn2(tr+1,tc) and not self.is_friend(r,c,tr+1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr+1,tc) and self.moves_log["from"][-1][0]==1 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc-1):
           self.hash_key ^= self._sq_hash(color,'pawns',r,c)                # NEW
           self.hash_key ^= self._sq_hash(enemy_color,'pawns',tr+1,tc)      # NEW
           self.update_place(r,c,tr,tc)
           self.real_board[tr][tc]=self.real_board[r][c]
           self.real_board[tr+1][tc]='.'
           self.real_board[r][c]='.'
           if (tr+1, tc) in self.positions['black']['pawns']:
               self.positions['black']['pawns'].remove((tr+1, tc))
               self.dead_pieces['black'].append('pawns')
           self.hash_key ^= self._sq_hash(color,'pawns',tr,tc)              # NEW
           self.hash_key ^= self.z_turn                                     # NEW
           return True

          elif(self.is_pawn2(r,c) and self.is_white2(r,c) and tr==r-1 and(self.is_pawn2(tr+1,tc) and not self.is_friend(r,c,tr+1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr+1,tc) and self.moves_log["from"][-1][0]==1 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc+1):
               self.hash_key ^= self._sq_hash(color,'pawns',r,c)            # NEW
               self.hash_key ^= self._sq_hash(enemy_color,'pawns',tr+1,tc)  # NEW
               self.update_place(r,c,tr,tc)
               self.real_board[tr][tc]=self.real_board[r][c]
               self.real_board[tr+1][tc]='.'
               self.real_board[r][c]='.'
               if (tr+1, tc) in self.positions['black']['pawns']:
                   self.positions['black']['pawns'].remove((tr+1, tc))
                   self.dead_pieces['black'].append('pawns')
               self.hash_key ^= self._sq_hash(color,'pawns',tr,tc)          # NEW
               self.hash_key ^= self.z_turn                                 # NEW
               return True

          elif(self.is_pawn2(r,c) and self.is_black2(r,c) and tr==r+1 and (self.is_pawn2(tr-1,tc) and not self.is_friend(r,c,tr-1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr-1,tc) and self.moves_log["from"][-1][0]==6 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc+1):
               self.hash_key ^= self._sq_hash(color,'pawns',r,c)            # NEW
               self.hash_key ^= self._sq_hash(enemy_color,'pawns',tr-1,tc)  # NEW
               self.update_place(r,c,tr,tc)
               self.real_board[tr][tc]=self.real_board[r][c]
               self.real_board[tr-1][tc]='.'
               self.real_board[r][c]='.'
               if (tr-1, tc) in self.positions['white']['pawns']:
                   self.positions['white']['pawns'].remove((tr-1, tc))
                   self.dead_pieces['white'].append('pawns')
               self.hash_key ^= self._sq_hash(color,'pawns',tr,tc)          # NEW
               self.hash_key ^= self.z_turn                                 # NEW
               return True

          elif(self.is_pawn2(r,c) and self.is_black2(r,c) and tr==r+1 and (self.is_pawn2(tr-1,tc) and not self.is_friend(r,c,tr-1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr-1,tc) and self.moves_log["from"][-1][0]==6 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc-1):
               self.hash_key ^= self._sq_hash(color,'pawns',r,c)            # NEW
               self.hash_key ^= self._sq_hash(enemy_color,'pawns',tr-1,tc)  # NEW
               self.update_place(r,c,tr,tc)
               self.real_board[tr][tc]=self.real_board[r][c]
               self.real_board[tr-1][tc]='.'
               self.real_board[r][c]='.'
               if (tr-1, tc) in self.positions['white']['pawns']:
                   self.positions['white']['pawns'].remove((tr-1, tc))
                   self.dead_pieces['white'].append('pawns')
               self.hash_key ^= self._sq_hash(color,'pawns',tr,tc)          # NEW
               self.hash_key ^= self.z_turn                                 # NEW
               return True

          else:
           if(self.is_pawn2(r,c) and self.is_board_end(tr,tc) and to_promote not in (1,2,3,4)):
            self.hash_stack.pop()   # NEW — undo the push above, since nothing actually moved
            return False
           captured_piece = self.get_piece(tr,tc) if not self.is_empty2(tr,tc) else None  # NEW
           self.hash_key ^= self._sq_hash(color,piece,r,c)                                # NEW
           if captured_piece:                                                             # NEW
               self.hash_key ^= self._sq_hash(enemy_color,captured_piece,tr,tc)           # NEW
           self.update_place(r,c,tr,tc)
           self.real_board[tr][tc]=self.real_board[r][c]
           self.real_board[r][c]='.'
           pivot=None
          if(self.is_pawn2(tr,tc) and self.is_board_end(tr,tc)):
            if(to_promote in (1,2,3,4)):
              pivot=self.pawn_choices[to_promote-1]
              is_black_pawn = self.is_black2(tr,tc)
              self.real_board[tr][tc] = pivot.lower() if is_black_pawn else pivot.upper()
              color = 'black' if is_black_pawn else 'white'
              idx = self.positions[color]['pawns'].index((tr,tc))
              del self.positions[color]['pawns'][idx]
              promo_key={'b':'bishops','n':'knights','q':'queen','r':'rooks'}[pivot]
              self.positions[color][promo_key].append((tr,tc))
              self.hash_key ^= self._sq_hash(color,promo_key,tr,tc)   # NEW — add promoted piece
            else:
              self.hash_stack.pop()   # NEW — undo push, nothing happened
              return False
          else:
              self.hash_key ^= self._sq_hash(color,piece,tr,tc)      # NEW — normal (non-promoting) arrival
          self.hash_key ^= self.z_turn   # NEW
          return True
        
   
 
 
 
  def can_be_checked(self,k_r,k_c,r,c,castlingflag=False):
   if not (0<=r<=7 and 0<=c<=7 and 0<=k_r<=7 and 0<=k_c<=7):
       return False
   saved_board = [row[:] for row in self.real_board]
   color = 'black' if self.is_black2(k_r,k_c) else 'white'
   saved_checkers = self.king_checkers[color][:]
 
   if(castlingflag): 
       k_dy,r_dy=(2,-1) if(c>k_c) else(-2,1)
       self.real_board[k_r][k_c+k_dy]=self.real_board[k_r][k_c]
       self.real_board[k_r][k_c+k_dy+r_dy]=self.real_board[r][c]
       self.real_board[k_r][k_c]='.'
       self.real_board[r][c]='.'
       checked = self.is_checked(k_r,k_c+k_dy)
   else:
    self.real_board[r][c]=self.real_board[k_r][k_c]
    self.real_board[k_r][k_c]='.'
    checked = self.is_checked(r,c)
   for i in range(8):
     self.real_board[i][:] = saved_board[i]
   self.king_checkers[color] = saved_checkers
 
   return checked
  def can_be_checked2(self,r,c,tr,tc):
   checked = False
   if(not self.is_king2(r,c)):
    (k_r,k_c)=self.index_my_king(r,c)
    saved_board = [row[:] for row in self.real_board]
    color = 'black' if self.is_black2(k_r,k_c) else 'white'
    saved_checkers = self.king_checkers[color][:]
    self.real_board[tr][tc]=self.real_board[r][c]
    self.real_board[r][c]='.'
    checked=self.is_checked(k_r,k_c)
    for i in range(8):
       self.real_board[i][:] = saved_board[i]
    self.king_checkers[color] = saved_checkers
   return checked
 
  def get_piece(self,old_r,old_c):
   is_pieces={"king":self.is_king2(old_r,old_c),"bishops":self.is_bishop2(old_r,old_c),"knights":self.is_knight2(old_r,old_c),"queen":self.is_queen2(old_r,old_c),"pawns":self.is_pawn2(old_r,old_c),"rooks":self.is_rook2(old_r,old_c)}
   for key,value in is_pieces.items():
     if(value):
       return key
     
  def diagonal_check(self,piece,r,c):

   bish_silding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1)]
   legal=[] 
   
   for dx,dy in bish_silding_dirs:
     new_r,new_c=(r,c) 
     while(0<=new_r+dx<=7 and 0<=new_c+dy<=7 ):
       target_r,target_c=new_r+dx,new_c+dy
       is_legal_shape = not self.is_friend(r,c,target_r,target_c) and (self.bishop_legal(r,c,target_r,target_c) if(piece=='rooks') else self.queen_legal(r,c,target_r,target_c))
       
       if not is_legal_shape:
         break

       if not self.can_be_checked2(r,c,target_r,target_c):
         if(piece=='bishops'):
           legal.append(('bishops',(r,c),(target_r,target_c)))
         else:
           legal.append(('queen',(r,c),(target_r,target_c)))

       was_capture = not self.is_empty2(target_r,target_c)
       new_r,new_c=target_r,target_c

       if was_capture:
         break
   return legal        
     
  def row_col_check(self,piece,r,c):
   rook_dir=[(1,0),(-1,0),(0,1),(0,-1)] 
   legal=[] 
     
   for dx,dy in rook_dir:
       new_r,new_c=(r,c) 
       while(0<=new_r+dx<=7 and 0<=new_c+dy<=7 ):
         target_r,target_c=new_r+dx,new_c+dy
         is_legal_shape = not self.is_friend(r,c,target_r,target_c) and (self.rook_legal(r,c,target_r,target_c) if(piece=='rooks') else self.queen_legal(r,c,target_r,target_c))

         if not is_legal_shape:
           break

         if not self.can_be_checked2(r,c,target_r,target_c):
           if(piece=='rooks'):
             legal.append(('rooks',(r,c),(target_r,target_c)))
           else:
             legal.append(('queen',(r,c),(target_r,target_c)))

         was_capture = not self.is_empty2(target_r,target_c)
         new_r,new_c=target_r,target_c

         if was_capture:
           break
   return legal
 
  def knight_check(self,r,c):
   KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
   legal=[]
   for dx,dy in KNIGHT_DELTAS:
       new_r,new_c=(r,c)
       if((0<=new_r+dx<=7 and 0<=new_c+dy<=7)  and self.knight_legal(r,c,new_r+dx,new_c+dy) and not self.can_be_checked2(r,c,new_r+dx,new_c+dy) ):
        new_r,new_c=(new_r+dx,new_c+dy)
        legal.append(('knights',(r,c),(new_r,new_c)))
       else:
         continue
   return legal
  def king_check(self,r,c):
   king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
 
   legal=[]
   for dx,dy in king_dirs:
         new_r,new_c=(r,c)
         if((0<=new_r+dx<=7 and 0<=new_c+dy<=7)  and self.king_legal(r,c,new_r+dx,new_c+dy)):
          new_r,new_c=(new_r+dx,new_c+dy)
          legal.append(('king',(r,c),(new_r,new_c)))
         else:
           continue
   color = 'black' if self.is_black2(r,c) else 'white'
   for rook_r,rook_c in self.positions[color]['rooks']:
       if self.king_legal(r,c,rook_r,rook_c):
           legal.append(('king',(r,c),(rook_r,rook_c)))
   return legal
  def pawn_check(self,r,c):
     pawn_dirs=[(-1,0),(-1,1),(-1,-1),(-2,0)]
     legal=[]
     if(self.is_black2(r,c)):
       pawn_dirs=[(-dx,-dy) for dx,dy in pawn_dirs]
     for dx,dy in pawn_dirs:
             new_r,new_c=(r,c)
             if((0<=new_r+dx<=7 and 0<=new_c+dy<=7)  and self.pawn_legal(r,c,new_r+dx,new_c+dy) and not self.can_be_checked2(r,c,new_r+dx,new_c+dy) ):
              new_r,new_c=(new_r+dx,new_c+dy)
              legal.append(('pawns',(r,c),(new_r,new_c)))
             else:
               continue  
     return legal  
 
  def generate_legal_moves(self,color,capture=False):
    legal_moves=[]
    legal_moves_ordered=[]
    value={'pawns':1,'knights':3,'bishops': 3,'rooks':5,'queen':9,'king':1000}
 
    for piece,position in self.positions[color].items():
      if(piece=='king'):
        (r,c)=position
        legal_moves.extend(self.king_check(r,c))
      else:
       for r,c in position:
        if(piece=='rooks' ):
           legal_moves.extend(self.row_col_check(piece,r,c))
        elif(  piece=='bishops'):
          legal_moves.extend(self.diagonal_check(piece,r,c))
        elif(piece=='queen'):
         legal_moves.extend(self.diagonal_check(piece,r,c))
         legal_moves.extend(self.row_col_check(piece,r,c))
        elif(piece=='knights'):
         legal_moves.extend(self.knight_check(r,c))
        elif(piece=='pawns'):
          legal_moves.extend(self.pawn_check(r,c))
    captures = []
    quiet = []
    for piece,(r,c),(tr,tc) in legal_moves:
      if not self.is_empty2(tr,tc):
         captures.append((piece,(r,c),(tr,tc)))
      else:
         quiet.append((piece,(r,c),(tr,tc)))
    captures.sort(key=lambda m: value[self.get_piece(*m[2])] - value[m[0]], reverse=True)
    if(capture==True):
      return captures
    return captures + quiet
  def material_count(self,color,positions):
   material=0
   value={'pawns':1,'knights':3,'bishops': 3,'rooks':5,'queen':9}
   for piece,position in self.positions[color].items():
    if(piece=='king'):
      continue
    else:
      for r,c in position:
        material+=value.get(piece)
   return material
  def pawn_penalty(self, pawns):
    files = [c for r, c in pawns]
    penalty = 0
    for f in set(files):
        count = files.count(f)
        if count > 1:
            penalty += 12 * (count - 1)
    return penalty
  def isendgame(self,white_material,black_material):
    return white_material+black_material <20
  def evaluate(self,positions):
     white_material = self.material_count('white', positions)
     black_material = self.material_count('black', positions)
 
     score = (white_material - black_material)*100
     black_pos=0
     white_pos=0
     pawn = [
     [0,  0,  0,  0,  0,  0,  0,  0],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [10, 10, 20, 30, 30, 20, 10, 10],
     [5,  5, 10, 25, 25, 10,  5,  5],
     [0,  0,  0, 20, 20,  0,  0,  0],
     [5, -5,-10,  0,  0,-10, -5,  5],
     [5, 10, 10,-20,-20, 10, 10,  5],
     [0,  0,  0,  0,  0,  0,  0,  0]
 ]
 
     knights = [
         [-50,-40,-30,-30,-30,-30,-40,-50],
         [-40,-20,  0,  0,  0,  0,-20,-40],
         [-30,  0, 10, 15, 15, 10,  0,-30],
         [-30,  5, 15, 20, 20, 15,  5,-30],
         [-30,  0, 15, 20, 20, 15,  0,-30],
         [-30,  5, 10, 15, 15, 10,  5,-30],
         [-40,-20,  0,  5,  5,  0,-20,-40],
         [-50,-40,-30,-30,-30,-30,-40,-50]
     ]
     
     bishops = [
         [-20,-10,-10,-10,-10,-10,-10,-20],
         [-10,  0,  0,  0,  0,  0,  0,-10],
         [-10,  0,  5, 10, 10,  5,  0,-10],
         [-10,  5,  5, 10, 10,  5,  5,-10],
         [-10,  0, 10, 10, 10, 10,  0,-10],
         [-10, 10, 10, 10, 10, 10, 10,-10],
         [-10,  5,  0,  0,  0,  0,  5,-10],
         [-20,-10,-10,-10,-10,-10,-10,-20]
     ]
     
     rooks = [
         [0,  0,  0,  0,  0,  0,  0,  0],
         [5, 10, 10, 10, 10, 10, 10,  5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [0,  0,  0,  5,  5,  0,  0,  0]
     ]
     
     queen = [
         [-20,-10,-10, -5, -5,-10,-10,-20],
         [-10,  0,  0,  0,  0,  0,  0,-10],
         [-10,  0,  5,  5,  5,  5,  0,-10],
         [-5,  0,  5,  5,  5,  5,  0, -5],
         [0,  0,  5,  5,  5,  5,  0, -5],
         [-10,  5,  5,  5,  5,  5,  0,-10],
         [-10,  0,  5,  0,  0,  0,  0,-10],
         [-20,-10,-10, -5, -5,-10,-10,-20]
     ]
     
     king_middle_game = [
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-20,-30,-30,-40,-40,-30,-30,-20],
         [-10,-20,-20,-20,-20,-20,-20,-10],
         [20, 20,  0,  0,  0,  0, 20, 20],
         [20, 30, 10,  0,  0, 10, 30, 20]
     ]
     king_end_game=[ [-50,-40,-30,-20,-20,-30,-40,-50],
         [-30,-20,-10,  0,  0,-10,-20,-30],
         [-30,-10, 20, 30, 30, 20,-10,-30],
         [-30,-10, 30, 40, 40, 30,-10,-30],
         [-30,-10, 30, 40, 40, 30,-10,-30],
         [-30,-10, 20, 30, 30, 20,-10,-30],
         [-30,-30,  0,  0,  0,  0,-30,-30],
         [-50,-30,-30,-30,-30,-30,-30,-50] ]
     king=king_end_game if(self.isendgame(white_material,black_material)) else king_middle_game
     for piece,pos in self.positions['white'].items():
       if(piece=='king'): 
         kr,kc=pos
         white_pos+=king[kr][kc]
       else:
        for r,c in pos:
          if(piece=='rooks'):
            white_pos+=rooks[r][c]
          elif (piece=='knights'):
            white_pos+=knights[r][c]
          elif (piece=='bishops'):
             white_pos+=bishops[r][c]
          elif (piece=='pawns'):
             white_pos+=pawn[r][c]
          else:
            white_pos+=queen[r][c]  
 
     for piece,pos in self.positions['black'].items():
           if(piece=='king'): 
             kr,kc=pos
             black_pos+=king[7-kr][kc]
           else:
            for r,c in pos:
              if(piece=='rooks'):
                black_pos+=rooks[7-r][c]
              elif (piece=='knights'):
                black_pos+=knights[7-r][c]
              elif (piece=='bishops'):
                 black_pos+=bishops[7-r][c]
              elif (piece=='pawns'):
               black_pos+=pawn[7-r][c]
              else:
                black_pos+=queen[7-r][c]  
     white_pos-=self.pawn_penalty(self.positions['white']['pawns'])           
     black_pos-=self.pawn_penalty(self.positions['black']['pawns'])           
     pos_eval=white_pos-black_pos
     score+=pos_eval
     if len(self.positions['white']['bishops']) == 2:
      score += 30
     if len(self.positions['black']['bishops']) == 2:
      score -= 30       
     
 
 
 
 
     return score 
  def unmove(self):
   if(len(self.board_snapshots)>1):
    for i in range(8):
      for j in range(8):
        self.real_board[i][j]='.'
    self.king_checkers=deepcopy(self.board_snapshots[-2]['checkers'])
    self.positions=deepcopy(self.board_snapshots[-2]['board'])
    self.castling_flags=deepcopy(self.board_snapshots[-2]['castle_flags'])
    b_mapping={'knights':'n','king':'k','queen':'q','bishops':'b'  ,'rooks':'r','pawns':'p'}
    mapping={'knights':'N','king':'K','queen':'Q','bishops':'B'  ,'rooks':'R','pawns':'P'}
    for piece,position in self.positions['white'].items():
     letter=mapping.get(piece)
     if(piece=='king'):
       r,c=position
       self.real_board[r][c]=letter
     else:
       for r,c in position:
         self.real_board[r][c]=letter
   
    for piece,position in self.positions['black'].items():
       letter=b_mapping.get(piece)
       if(piece=='king'):
        r,c=position
        self.real_board[r][c]=letter
       else:
         for r,c in position:
           self.real_board[r][c]=letter     
    self.moves_log["from"].pop() 
    self.moves_log["to"].pop() 
    self.moves_log['castling'].pop() 
    self.moves_log['pawn/capture'].pop() 
    self.moves_log['pawn'].pop() 
    self.board_snapshots.pop()    
    self.hash_key = self.hash_stack.pop()   # NEW
   else:
     return
   
  import math
  pos_inf = math.inf          # Positive infinity
  neg_inf = -math.inf         # Negative infinity 
 
     

   
      
      
           
  def print_board(self):
     files = '  a b c d e f g h'
     print(files)
     for i, row in enumerate(self.real_board):
         rank = 8 - i
         print(f"{rank} {' '.join(row)} {rank}")
     print(files)
 ###testinnggg
  def quiescence(self, color, alpha, beta, qdepth=0):
    stand_pat = self.evaluate(self.positions)

    if qdepth >= 6:
        return stand_pat

    captures = self.generate_legal_moves(color, capture=True)

    if color == 'white':
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
        for piece, (r, c), (tr, tc) in captures:
            promo = 3 if (self.is_pawn2(r, c) and self.is_board_end(tr, tc)) else None
            self.move_piece(self.unparse_move(r, c), self.unparse_move(tr, tc),
                             to_promote=promo, verified=True)
            score = self.quiescence('black', alpha, beta, qdepth + 1)
            self.unmove()
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        return alpha
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)
        for piece, (r, c), (tr, tc) in captures:
            promo = 3 if (self.is_pawn2(r, c) and self.is_board_end(tr, tc)) else None
            self.move_piece(self.unparse_move(r, c), self.unparse_move(tr, tc),
                             to_promote=promo, verified=True)
            score = self.quiescence('white', alpha, beta, qdepth + 1)
            self.unmove()
            if score <= alpha:
                return alpha
            beta = min(beta, score)
        return beta
   
  def _sq_hash(self, color, piece, r, c):
    k = 0 if color == 'white' else 1
    j = self.piece_index[piece]
    return self.z_board[r*8 + c][j][k]
  def get_zobrist_key(self,positions,turn):
  
    hash=0
    
    for color in ('white','black'):
     k = 0 if color == 'white' else 1
     for piece,pos in positions[color].items():
       j=self.piece_index[piece]

       if piece=='king':
            
           r,c=pos
           square_index = r * 8 + c

           hash^=self.z_board[square_index][j][k]
       else:    
        for r,c in pos:
         square_index = r * 8 + c
         hash^=self.z_board[square_index][j][k]
    for (color, side), z in zip(self.castle_order, self.z_castle):
        if self.castling_flags[color][side]:
            hash ^= z     
    if(turn=='black'):
      hash^=self.z_turn
    else:
     hash^=0     
      
    return hash
  
  def minimax(self,color,depth,alpha,beta,deadline):
    if(time.monotonic()>=deadline):
      raise time_out()
    key = self.hash_key   # replaces: key=self.get_zobrist_key(self.positions,color)
    if(key in self.transpos_table):
      if(self.transpos_table[key]['depth']>=depth): 
       if(self.transpos_table[key]['type']=='exact'):
         return self.transpos_table[key]['score']
       elif( self.transpos_table[key]['type']=='upperbound'):
        beta=min(beta,self.transpos_table[key]['score'])
       elif(self.transpos_table[key]['type']=='lowerbound'):
         alpha=max(alpha,self.transpos_table[key]['score'])
       if(alpha>=beta):
        return self.transpos_table[key]['score'] 
    moves=self.generate_legal_moves(color)
    kr,kc=self.positions[color]['king']
    if len(moves) == 0:
      if self.is_checked(kr, kc):
          return -10000 if color=='white' else 10000
      else:
          return 0
    if(depth==0):
     return self.quiescence(color, alpha, beta)   # was: return self.evaluate(self.positions) 
    prev_alpha=alpha
    prev_beta=beta
    if(color=='white'):
     maxeval=self.neg_inf
     for piece,(r,c),(tr,tc) in moves:
      promo = 3 if (self.is_pawn2(r,c) and self.is_board_end(tr,tc)) else None
      self.move_piece(self.unparse_move(r,c), self.unparse_move(tr,tc), to_promote=promo, verified=True)
      try:
       eval=self.minimax('black',depth-1,alpha,beta,deadline)
      finally:
       self.unmove()

      alpha=max(alpha,eval) 
  
      maxeval=max(eval,maxeval)
  
      if(beta<=alpha):
        break

      score=maxeval
         

     if(maxeval>=beta):
      entry_type='lowerbound'
     elif(maxeval<=prev_alpha):
        entry_type='upperbound'
     else:
       entry_type='exact'  
     self.transpos_table[key] = {'score': maxeval, 'depth': depth, 'type': entry_type}

     return maxeval
    else:
      mineval=self.pos_inf
      for piece,(r,c),(tr,tc) in moves:

         promo = 3 if (self.is_pawn2(r,c) and self.is_board_end(tr,tc)) else None
         self.move_piece(self.unparse_move(r,c), self.unparse_move(tr,tc), to_promote=promo, verified=True)
         try:
          eval=self.minimax('white',depth-1,alpha,beta,deadline)
         finally:
          self.unmove()
 
         beta=min(beta,eval) 

         mineval=min(eval,mineval)
         
         if(beta<=alpha):
           break
      score=mineval
      if(mineval>=prev_beta):
       entry_type='lowerbound'
      elif(mineval<=alpha):
       entry_type='upperbound'
      else:
       entry_type='exact'   
      self.transpos_table[key] = {'score': mineval, 'depth': depth, 'type': entry_type}

      return mineval
 

 
  import time   
  def best_move(self,color,depth,time_limit=2):
   dead_line=time.monotonic()+time_limit
   moves=self.generate_legal_moves(color)
   best_move=None
   best_move_tuples=None
   for i in range(1,depth+1):
    try:
         if best_move_tuples is not None and best_move_tuples in moves:
          moves.remove(best_move_tuples)
          moves.insert(0,best_move_tuples)
         if(color=='white'):
             maxeval=self.neg_inf
             for piece,(r,c),(tr,tc) in moves:
              promo = 3 if (self.is_pawn2(r,c) and self.is_board_end(tr,tc)) else None
              self.move_piece(self.unparse_move(r,c), self.unparse_move(tr,tc), to_promote=promo, verified=True)
              try:
               eval = self.minimax('black', i-1,self.neg_inf,self.pos_inf,dead_line)
              
              finally:
               self.unmove()
          
              if eval> maxeval:
               maxeval=eval
               best_move=[piece,(r,c),(tr,tc),maxeval]
               best_move_tuples=(piece,(r,c),(tr,tc))
         else:
              mineval=self.pos_inf
              for piece,(r,c),(tr,tc) in moves:
                  promo = 3 if (self.is_pawn2(r,c) and self.is_board_end(tr,tc)) else None
                  self.move_piece(self.unparse_move(r,c), self.unparse_move(tr,tc), to_promote=promo, verified=True)
                  try:
                   eval = self.minimax('white', i-1,self.neg_inf,self.pos_inf,dead_line)

                  finally:

                   self.unmove()
                
                  if eval< mineval:
                   mineval=eval
                   best_move=[piece,(r,c),(tr,tc),mineval]
                   best_move_tuples=(piece,(r,c),(tr,tc))
         #print('depth completed:',i)

    except (time_out):
     #print('depth uncompleted:',i)
     
     break
   return best_move               

  def translate_click(self,r,c):
    if(self.is_empty2(r,c)):
      return None
    color='black' if self.is_black2(r,c) else 'white'
    piece=self.get_piece(r,c)
    w_mapping={'king':'♔','queen'	:'♕','rooks':'♖','bishops':'♗','knights':	'♘','pawns':'♙'}
    b_mapping={'king':'♚','queen':'♛'	,'rooks':'♜','bishops':	'♝'	,'knights':'♞','pawns':'♟'}
    if(color=='black'):
      return b_mapping.get(piece)
    else:
      return w_mapping.get(piece)  
  def translate_board(self):
    board = [[None for j in range(8)] for i in range(8)]
    for i in range(8):
      for j in range(8):
        board[i][j]=self.translate_click(i,j)  
    return board    
  
  def is_game_end(self, color):
    kr, kc = self.positions[color]['king']

    if self.is_checkmated(kr, kc):
        return "checkmate"
    if self.stalemate(kr, kc):
        return "stalemate"
    if self.isfifty_moves_draw():
        return "draw"
    if self.is_three_fold():
        return "draw"
    return "ongoing"
  
  def to_state_dict(self):
     

     return {
        "positions": self.positions,
        "moves_log": 
             self.moves_log,
        "castling_flags": deepcopy(self.castling_flags), 
        "board_snapshots": self.board_snapshots,

    }
  @classmethod
  def from_state_dict(cls, state):
    game = cls()  # runs __init__, gives us a fresh Game with default board/positions

    def restore_positions(pos):
        out = {}
        for color, pieces in pos.items():
            out[color] = {}
            for piece, value in pieces.items():
                if piece == "king":
                    # king was stored as a list, e.g. [7, 4] -> tuple (7, 4)
                    out[color][piece] = tuple(value)
                else:
                    # everything else was a list of lists -> list of tuples
                    out[color][piece] = [tuple(p) for p in value]
        return out
    def restore_snapshot(snap):
        board = restore_positions(snap["board"])
        checkers = {
            color: [(piece, tuple(pos)) for piece, pos in lst]
            for color, lst in snap["checkers"].items()
        }
        castle_flags = {
            color: dict(sides) for color, sides in snap["castle_flags"].items()
        }
        ep = snap["enpassent"]
        enpassent = tuple(ep) if ep is not None else None
        return {
            "board": board,
            "turn": snap["turn"],
            "enpassent": enpassent,
            "castling": snap["castling"],
            "checkers": checkers,
            "castle_flags": castle_flags,
        }
    game.positions = restore_positions(state["positions"])

    game.moves_log["from"] = [tuple(p) for p in state["moves_log"]["from"]]
    game.moves_log["to"] = [tuple(p) for p in state["moves_log"]["to"]]
    game.moves_log["pawn"] = state["moves_log"]["pawn"]
    game.moves_log["capture"] = state["moves_log"]["capture"]
    game.moves_log["pawn/capture"] = state["moves_log"]["pawn/capture"]
    game.moves_log["castling"] = state["moves_log"]["castling"]

    if "castling_flags" in state:
        game.castling_flags = {
            color: dict(sides) for color, sides in state["castling_flags"].items()
        }
    if "board_snapshots" in state:
        game.board_snapshots = [restore_snapshot(s) for s in state["board_snapshots"]]    

    # rebuild real_board from the restored positions, since real_board itself
    # isn't stored — it's derived
    game.real_board = [['.' for _ in range(8)] for _ in range(8)]
    mapping = {'knights': 'N', 'king': 'K', 'queen': 'Q', 'bishops': 'B', 'rooks': 'R', 'pawns': 'P'}
    b_mapping = {k: v.lower() for k, v in mapping.items()}

    for piece, value in game.positions['white'].items():
        letter = mapping[piece]
        if piece == 'king':
            r, c = value
            game.real_board[r][c] = letter
        else:
            for r, c in value:
                game.real_board[r][c] = letter

    for piece, value in game.positions['black'].items():
        letter = b_mapping[piece]
        if piece == 'king':
            r, c = value
            game.real_board[r][c] = letter
        else:
            for r, c in value:
                game.real_board[r][c] = letter

    return game

  def encode_board(self, positions):
  
      # En passant
      ep = self.board_snapshots[-1]['enpassent']
      enpassent = [0] * 64
  
      if ep is not None:
          e_r, e_c = ep
          square_index = e_r * 8 + e_c
          enpassent[square_index] = 1
  
      # Castling rights
      castling = [
          int(self.castling_flags['white']['kingside']),
          int(self.castling_flags['white']['queenside']),
          int(self.castling_flags['black']['kingside']),
          int(self.castling_flags['black']['queenside'])
      ]
  
      # Turn
      turn = 1 if self.board_snapshots[-1]['turn'] == 'black' else 0
  
      # Board
      tensor = [
          [[0 for _ in range(2)] for _ in range(6)]
          for _ in range(64)
      ]
  
      for color in ('white', 'black'):
          k = 0 if color == 'white' else 1
  
          for piece, pos in positions[color].items():
  
              j = self.piece_index[piece]
  
              if piece == 'king':
  
                  r, c = pos
                  square_index = r * 8 + c
                  tensor[square_index][j][k] = 1
  
              else:
  
                  for r, c in pos:
                      square_index = r * 8 + c
                      tensor[square_index][j][k] = 1
  
      # Convert to numpy
      tensor = np.array(tensor, dtype=np.float32).flatten()
      castling = np.array(castling, dtype=np.float32)
      enpassent = np.array(enpassent, dtype=np.float32)
      turn = np.array([turn], dtype=np.float32)
  
      # Final NN input
      x = np.concatenate([
          tensor,
          castling,
          enpassent,
          turn
      ])
  
      return x

  def label_eval(self, color, depth, time_limit=10000):
    entry = self.transpos_table.get(self.hash_key)
    if entry is not None and entry['depth'] >= depth and entry['type'] == 'exact':
        return entry['score']
    try:
        return self.minimax(color, depth, self.neg_inf, self.pos_inf,
                             time.monotonic() + time_limit)
    except time_out:
        return self.evaluate(self.positions)
def simulate_game():
  g=Game()
  turn=['white','black']
  i=False
  examples={}
  count=0
  while(g.is_game_end(turn[int(i)])=='ongoing' and count<30):
   israndom=False

   count+=1
   color=turn[int(i)]
   RANDOM_OPENING_PLIES = 8
   if(count <= RANDOM_OPENING_PLIES):
     moves = g.generate_legal_moves(color)
     piece, (r, c), (tr, tc) = random.choice(moves)
     _score =None
     israndom=True   
   elif(color=='black'):
    piece, (r, c), (tr, tc), _score = g.best_move('black',6)
   else:
    piece, (r, c), (tr, tc), _score = g.best_move('white',2)

   from_sq = g.unparse_move(r, c)
   to_sq = g.unparse_move(tr, tc)
   promo = 3 if (piece == 'pawns' and g.is_board_end(tr, tc)) else None
   g.move_piece(from_sq, to_sq, to_promote=promo, verified=True)
   if(israndom):
     next_to_move = 'black' if color == 'white' else 'white'
     _score = g.quiescence(next_to_move, g.neg_inf, g.pos_inf) 
     israndom=False

   i = not i  # flip BEFORE checking, since it's now the other side's turn
   result = g.is_game_end(turn[int(i)])   # check the side that must move next

   examples[count] = {
       "evaluation": _score,
       "board": g.encode_board(g.positions),
       "result": result
   }
  """  with open("training_data.txt", "a") as f:
        for example in examples.values():
            example["board"] = example["board"].tolist()

            f.write(json.dumps(example) + "\n")"""
  return examples



"""def run_game(game_number):
    return simulate_game()

if __name__ == "__main__":

    with Pool(processes=10,maxtasksperchild=1) as pool:

        with open("training_data.txt", "a", encoding="utf-8") as f:

            for game_number, examples in enumerate(
                pool.imap_unordered(run_game, range(1000),chunksize=1),
                start=1
            ):

                for example in examples.values():
                    example["board"] = example["board"].tolist()
                    f.write(json.dumps(example) + "\n")

                f.flush()

                print("Finished:", game_number)"""
"""n_games=100
for game_idx in range(n_games):
    examples = simulate_game()
    
    print(f"game {game_idx+1}/{n_games} done, {len(examples)} plies")
"""
"""g=Game()
x=torch.from_numpy( g.encode_board(g.positions))
model=neuralnet(x)
print(model(x))

print(model(x).shape)"""
