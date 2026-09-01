from copy import deepcopy
import math


class Game:
  
 
 #legal_dir={["p","P"]:(1,0),["r","R"]:[ (1,0),(-1,0),(0,1),(0,-1)],["b","B"]:[(1,1),(1,-1),(-1,1),(-1,-1)],["n","N"]:(()) }
 
  def __init__(self):
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
          "black": self.castling_rights("black")},"checkers":deepcopy(self.king_checkers)
 }]

   
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
     square=self.unparse_move(r,c)
     return self.is_empty(square)
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
       
  def rook_or_king_moved(self,r_r,r_c,color):
    r_moved=None
    k_moved=None
    (kr,kc)=self.positions[color]['king']
    if(color=='black'):
     idx= self.positions[color]['rooks'].index((r_r,r_c))
     k_moved=False if(kr,kc)==(0,4) else True
     if(idx==0):
      r_moved=False if(r_r,r_c)==(0,0) else True
     if(idx==1):
      r_moved=False if(r_r,r_c)==(0,7) else True
    if(color=='white'):
       idx= self.positions[color]['rooks'].index((r_r,r_c))
       k_moved=False if(kr,kc)==(7,4) else True
       if(idx==0):
        r_moved=False if(r_r,r_c)==(7,0) else True
       if(idx==1):
        r_moved=False if(r_r,r_c)==(7,7) else True
    return r_moved or k_moved
  
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
      self.moves_log["from"].append((old_r,old_c))
      self.moves_log["to"].append((r,c))
      self.moves_log['castling'].append('true')
      self.moves_log['pawn/capture'].append(iscapture_or_pawnmove)
      self.moves_log['pawn'].append(ispawnmove)
    
      self.board_snapshots.append({"board":deepcopy(self.positions),"turn":color,"enpassent":self.enpassent_corr(ispawnmove),"castling": {
         "white": self.castling_rights("white"),   
         "black": self.castling_rights("black"),
     },"checkers":deepcopy(self.king_checkers)})
    else:
 
  
     is_pieces={"king":self.is_king2(old_r,old_c),"bishops":self.is_bishop2(old_r,old_c),"knights":self.is_knight2(old_r,old_c),"queen":self.is_queen2(old_r,old_c),"pawns":self.is_pawn2(old_r,old_c),"rooks":self.is_rook2(old_r,old_c)}
     piece=None
     for key,value in is_pieces.items():
      if(value):
       piece=key
       break
     if(piece=='rooks' or piece=='bishops' or piece=='knights' or piece=='pawns' or piece=='queen'):
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
  
     self.moves_log["from"].append((old_r,old_c))
     self.moves_log["to"].append((r,c))
     self.moves_log['pawn/capture'].append(iscapture_or_pawnmove)
     self.moves_log['pawn'].append(ispawnmove)
     self.moves_log['castling'].append('false')
     
     self.board_snapshots.append({"board":deepcopy(self.positions),"turn":color,"enpassent":self.enpassent_corr(ispawnmove),"castling": {
          "white": self.castling_rights("white"),   
          "black": self.castling_rights("black"),
      },"checkers":deepcopy(self.king_checkers)})
 
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
          if(self.is_king2(r,c) and self.is_friend(r,c,tr,tc) and self.is_rook2(tr,tc)):
           k_dy,r_dy=(2,-1) if(tc>c) else(-2,1)
           self.update_place(r,c,tr,tc,castlingflag=True)
           self.real_board[r][c+k_dy]=self.real_board[r][c]
           self.real_board[r][c+k_dy+r_dy]=self.real_board[tr][tc]
           self.real_board[r][c]='.'
           self.real_board[tr][tc]='.'
         
           return True
          elif(self.is_pawn2(r,c) and self.is_white2(r,c) and tr==r-1 and(self.is_pawn2(tr+1,tc) and not self.is_friend(r,c,tr+1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr+1,tc) and self.moves_log["from"][-1][0]==1 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc-1):
           self.update_place(r,c,tr,tc)
           self.real_board[tr][tc]=self.real_board[r][c]
           self.real_board[tr+1][tc]='.'
           self.real_board[r][c]='.'
           return True
          elif(self.is_pawn2(r,c) and self.is_white2(r,c) and tr==r-1 and(self.is_pawn2(tr+1,tc) and not self.is_friend(r,c,tr+1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr+1,tc) and self.moves_log["from"][-1][0]==1 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc+1):
           self.update_place(r,c,tr,tc)
           self.real_board[tr][tc]=self.real_board[r][c]
           self.real_board[tr+1][tc]='.'
           self.real_board[r][c]='.'
           return True
          elif(self.is_pawn2(r,c) and self.is_black2(r,c) and tr==r+1 and (self.is_pawn2(tr-1,tc) and not self.is_friend(r,c,tr-1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr-1,tc) and self.moves_log["from"][-1][0]==6 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc+1):
           self.update_place(r,c,tr,tc)
           self.real_board[tr][tc]=self.real_board[r][c]
           self.real_board[tr-1][tc]='.'
           self.real_board[r][c]='.'
           return True
          elif(self.is_pawn2(r,c) and self.is_black2(r,c) and tr==r+1 and (self.is_pawn2(tr-1,tc) and not self.is_friend(r,c,tr-1,tc)) and self.is_empty2(tr,tc) and self.moves_log["to"][-1]==(tr-1,tc) and self.moves_log["from"][-1][0]==6 and abs(self.moves_log["from"][-1][0]-self.moves_log["to"][-1][0])==2 and c==tc-1):
           self.update_place(r,c,tr,tc)
           self.real_board[tr][tc]=self.real_board[r][c]
           self.real_board[tr-1][tc]='.'
           self.real_board[r][c]='.'
           return True
          else:
           if(self.is_pawn2(r,c) and self.is_board_end(tr,tc) and to_promote not in (1,2,3,4)):
            return False
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
            else:
              return False
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
       check= not self.is_friend(r,c,new_r+dx,new_c+dy) and (self.bishop_legal(r,c,new_r+dx,new_c+dy) if(piece=='rooks') else self.queen_legal(r,c,new_r+dx,new_c+dy) )
       if(check and not self.can_be_checked2(r,c,new_r+dx,new_c+dy)):
 
         new_r+=dx
         new_c+=dy
         if(piece=='bishops'):
          legal.append(('bishops',(r,c),(new_r,new_c)))
         else:
           legal.append(('queen',(r,c),(new_r,new_c)))
 
 
 
 
       else:
         break
   return legal        
     
  def row_col_check(self,piece,r,c):
   rook_dir=[(1,0),(-1,0),(0,1),(0,-1)] 
   legal=[] 
     
   for dx,dy in rook_dir:
       new_r,new_c=(r,c) 
       while(0<=new_r+dx<=7 and 0<=new_c+dy<=7 ):
         check= not self.is_friend(r,c,new_r+dx,new_c+dy) and (self.rook_legal(r,c,new_r+dx,new_c+dy) if(piece=='rooks') else self.queen_legal(r,c,new_r+dx,new_c+dy) )
         if(check and not self.can_be_checked2(r,c,new_r+dx,new_c+dy)):
   
           new_r+=dx
           new_c+=dy
           if(piece=='rooks'):
            legal.append(('rooks',(r,c),(new_r,new_c)))
           else:
             legal.append(('queen',(r,c),(new_r,new_c)))
             
         else:
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
 
  def generate_legal_moves(self,color):
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
  def evaluate(self,positions):
     white_material = self.material_count('white', positions)
     black_material = self.material_count('black', positions)
 
     score = white_material - black_material
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
     
     king = [
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-20,-30,-30,-40,-40,-30,-30,-20],
         [-10,-20,-20,-20,-20,-20,-20,-10],
         [20, 20,  0,  0,  0,  0, 20, 20],
         [20, 30, 10,  0,  0, 10, 30, 20]
     ]
 
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
 
     pos_eval=white_pos-black_pos
     score+=pos_eval       
 
 
 
 
 
     return score 
  def unmove(self):
   if(len(self.board_snapshots)>1):
    for i in range(8):
      for j in range(8):
        self.real_board[i][j]='.'
    self.king_checkers=deepcopy(self.board_snapshots[-2]['checkers'])
    self.positions=deepcopy(self.board_snapshots[-2]['board'])
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
  def minimax(self,color,depth,alpha,beta):
   moves=self.generate_legal_moves(color)
   kr,kc=self.positions[color]['king']
   if len(moves) == 0:
     if self.is_checked(kr, kc):
         return -1000 if color=='white' else 1000
     else:
         return 0
   if(depth==0):
     return self.evaluate(self.positions)
 
   if(color=='white'):
    maxeval=self.neg_inf
    for piece,(r,c),(tr,tc) in moves:
     self.move_piece(self.unparse_move(r,c),self.unparse_move(tr,tc),verified=True)
     eval=self.minimax('black',depth-1,alpha,beta)
     self.unmove()
     alpha=max(alpha,eval) 
 
     maxeval=max(eval,maxeval)
     if(beta<=alpha):
       break
    return maxeval
   else:
     mineval=self.pos_inf
     for piece,(r,c),(tr,tc) in moves:
        self.move_piece(self.unparse_move(r,c),self.unparse_move(tr,tc),verified=True)
        eval=self.minimax('white',depth-1,alpha,beta)
        self.unmove()
        beta=min(beta,eval) 
 
        mineval=min(eval,mineval)
        if(beta<=alpha):
          break
     return mineval
 
 
 
  def best_move(self,color,depth):
   moves=self.generate_legal_moves(color)
   bestmove=None
 
   if(color=='white'):
    maxeval=self.neg_inf
    for piece,(r,c),(tr,tc) in moves:
     self.move_piece(self.unparse_move(r,c),self.unparse_move(tr,tc),verified=True)
     eval = self.minimax('black', depth-1,self.neg_inf,self.pos_inf)
     self.unmove()
 
     if eval> maxeval:
      maxeval=eval
      bestmove=[piece,(r,c),(tr,tc),maxeval]
    return bestmove
    
   else:
     mineval=self.pos_inf
     for piece,(r,c),(tr,tc) in moves:
         self.move_piece(self.unparse_move(r,c),self.unparse_move(tr,tc),verified=True)
         eval = self.minimax('white', depth-1,self.neg_inf,self.pos_inf)
         self.unmove()
       
         if eval< mineval:
          mineval=eval
          bestmove=[piece,(r,c),(tr,tc),mineval]
     return bestmove

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
             self.moves_log
       
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

    game.positions = restore_positions(state["positions"])

    game.moves_log["from"] = [tuple(p) for p in state["moves_log"]["from"]]
    game.moves_log["to"] = [tuple(p) for p in state["moves_log"]["to"]]
    game.moves_log["pawn"] = state["moves_log"]["pawn"]
    game.moves_log["capture"] = state["moves_log"]["capture"]
    game.moves_log["pawn/capture"] = state["moves_log"]["pawn/capture"]
    game.moves_log["castling"] = state["moves_log"]["castling"]

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
     

