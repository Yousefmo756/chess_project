from copy import deepcopy


board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
]
real_board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
]

#legal_dir={["p","P"]:(1,0),["r","R"]:[ (1,0),(-1,0),(0,1),(0,-1)],["b","B"]:[(1,1),(1,-1),(-1,1),(-1,-1)],["n","N"]:(()) }

class move:
 board_snapshots=[]
 def __init__(self):
  pass
 def parse_move(square):
  file='abcdefgh'
  col_letter=square[0]
  row_no=8-int(square[1])
  col=file.index(col_letter)
  return row_no,col
 def unparse_move(pos_r,pos_c):
 # file=['a','b','c','d','e','f','g','h']
  file='abcdefgh'

  col_letter=file[pos_c]
  row_no_str=(-pos_r+8)
  square=col_letter+str(row_no_str)
  return square
 def is_pawn2(r,c):
    return real_board[r][c] in ('P','p')
 def is_knight2(r,c):
     return real_board[r][c] in ('N','n')
 def is_bishop2(r,c):
     return real_board[r][c] in ('B','b')
 def is_rook2(r,c):
     return real_board[r][c] in ('R','r')
 def is_queen2(r,c):
     return real_board[r][c] in ('Q','q')
 def is_king2(r,c):
     return real_board[r][c] in ('K','k')
 def is_white2(r,c):
     if real_board[r][c]=='.':
         return False
     return real_board[r][c].isupper()
 def is_black2(r,c):
     if real_board[r][c]=='.':
         return False
     return real_board[r][c].islower()
 def is_friend2(pos_r,pos_c,target_r,target_c):
    if move.is_black2(pos_r,pos_c) and move.is_black2(target_r,target_c):
        return True
    elif move.is_white2(pos_r,pos_c) and move.is_white2(target_r,target_c):
        return True
    return False
 def is_pawn(square):
  r,c=move.parse_move(square)
  return  real_board[r][c]in('P','p')
 def is_knight(square):
  r,c=move.parse_move(square)
  return  real_board[r][c] in ('N','n')
 def is_bishop(square):
  r,c=move.parse_move(square)
  return  real_board[r][c] in ('B','b')
 def is_rook(square):
  r,c=move.parse_move(square)
  return  real_board[r][c] in ('R','r')
 def is_queen(square):
  r,c=move.parse_move(square)
  return  real_board[r][c]in('Q','q')
 def is_king(square):
  r,c=move.parse_move(square)
  return  real_board[r][c]in('K','k')
 def is_empty(square):
  r,c=move.parse_move(square)
  return real_board[r][c]=="."
 def is_empty2(r,c):
    square=move.unparse_move(r,c)
    return move.is_empty(square)
 def is_white(square):
  r,c=move.parse_move(square)
  if(move.is_empty(square)):
   return False
  return real_board[r][c].isupper()
 def is_black(square):
  r,c=move.parse_move(square)
  if(move.is_empty(square)):
   return False
  return real_board[r][c].islower()
 # need to define a generic function that takes the square and define the type of square if the movement is legal
 def is_friend(pos_r,pos_c,target_r,target_c):
  if move.is_black2(pos_r,pos_c) and move.is_black2(target_r,target_c):
        return True
  elif move.is_white2(pos_r,pos_c) and move.is_white2(target_r,target_c):
        return True
  return False
 positions = {
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


 def rook_legal(pos_r,pos_c,target_r,target_c):
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
       if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
        pos_r=newpos_r
        pos_c=newpos_c
        return True
       else:
        return False
      if(not move.is_empty2(newpos_r,newpos_c)):
       return False
      pos_r=newpos_r
      pos_c=newpos_c
  
    return False
 

 def knight_legal(pos_r,pos_c,target_r,target_c):
  KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
  if (target_r-pos_r, target_c-pos_c) not in KNIGHT_DELTAS:
        return False
  if move.is_empty2(target_r,target_c) or not move.is_friend(pos_r,pos_c,target_r,target_c):
        board[target_r][target_c]=board[pos_r][pos_c]
        board[pos_r][pos_c]='.'
        return True
  else:
        return False
   
 def bishop_legal(pos_r,pos_c,target_r,target_c):
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
     if(not move.is_friend( orig_r, orig_c,newpos_r,newpos_c)):
      pos_r=newpos_r
      pos_c=newpos_c
      return True
     else:
      return False
    if(not move.is_empty2(newpos_r,newpos_c)):
     return False
    pos_r=newpos_r
    pos_c=newpos_c

  return False
    
 def queen_legal(pos_r,pos_c,target_r,target_c):
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
     if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
      pos_r=newpos_r
      pos_c=newpos_c
      return True
     else:
      return False
    if(not move.is_empty2(newpos_r,newpos_c)):
     return False
    pos_r=newpos_r
    pos_c=newpos_c
  return False
 king_moved=False

  
 def king_legal(pos_r,pos_c,target_r,target_c):
       color= 'black' if move.is_black2(pos_r,pos_c) else 'white'
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
       elif (target_r == pos_r and target_c > pos_c and move.is_rook2(target_r,target_c) and move.is_empty2(pos_r,pos_c+1) and  move.is_empty2(pos_r,pos_c+2) and not move.is_checked(pos_r,pos_c) and not move.can_be_checked(pos_r,pos_c,target_r,target_c,castlingflag=True) and not move.rook_or_king_moved(target_r,target_c,color)):
        dx,dy=(0,2)
       elif (target_r == pos_r and target_c < pos_c and move.is_rook2(target_r,target_c) and move.is_empty2(pos_r,pos_c-1) and  move.is_empty2(pos_r,pos_c-2) and not move.is_checked(pos_r,pos_c) and not move.can_be_checked(pos_r,pos_c,target_r,target_c,castlingflag=True) and not move.rook_or_king_moved(target_r,target_c,color)):
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
       if(move.can_be_checked(pos_r,pos_c,newpos_r,newpos_c)):
        return False

      # --- 3. enemy-king adjacency rule, computed directly (no recursion) ---
       enemy_color = 'black' if move.is_white2(pos_r,pos_c) else 'white'
       enemy_kr, enemy_kc = move.positions[enemy_color]['king']
       not_next_to_enemy_king = max(abs(newpos_r-enemy_kr), abs(newpos_c-enemy_kc)) > 1

       if((move.is_empty2(newpos_r,newpos_c) or not move.is_friend(newpos_r,newpos_c,pos_r,pos_c))
         and not move.is_king2(newpos_r,newpos_c)
         and not_next_to_enemy_king):
          pos_r=newpos_r
          pos_c=newpos_c
          return True
       else:
          return False
      
 def rook_or_king_moved(r_r,r_c,color):
   r_moved=None
   k_moved=None
   (kr,kc)=move.positions[color]['king']
   if(color=='black'):
    idx= move.positions[color]['rooks'].index((r_r,r_c))
    k_moved=False if(kr,kc)==(0,4) else True
    if(idx==0):
     r_moved=False if(r_r,r_c)==(0,0) else True
    if(idx==1):
     r_moved=False if(r_r,r_c)==(0,7) else True
   if(color=='white'):
      idx= move.positions[color]['rooks'].index((r_r,r_c))
      k_moved=False if(kr,kc)==(7,4) else True
      if(idx==0):
       r_moved=False if(r_r,r_c)==(7,0) else True
      if(idx==1):
       r_moved=False if(r_r,r_c)==(7,7) else True
   return r_moved or k_moved
 
 def pawn_legal(pos_r,pos_c,target_r,target_c):
  r,c=pos_r,pos_c
  tr,tc=target_r,target_c
  newpos_r=0
  newpos_c=0
  pawn_dirs=[(-1,0),(-1,1),(-1,-1),(-2,0)]
  pawn_dirs_negated=[(-dx, -dy) for dx, dy in pawn_dirs]
  
  (dx,dy)=(0,0)
  is_black=move.is_black2(pos_r,pos_c) 
  is_white=not is_black
  if(pos_c==target_c and pos_r==target_r+1 and move.is_empty2(target_r,target_c) and is_white):
    dx,dy=pawn_dirs[0]
  elif(pos_c==target_c and pos_r==target_r-1 and move.is_empty2(target_r,target_c) and is_black):
    dx,dy=pawn_dirs_negated[0]
  elif(pos_c==target_c and pos_r==target_r+2 and move.is_empty2(target_r,target_c) and  move.is_empty2(pos_r-1,pos_c) and pos_r==6 and is_white):
     dx,dy=pawn_dirs[-1]
  elif(pos_c==target_c and pos_r==target_r-2 and move.is_empty2(target_r,target_c) and  move.is_empty2(pos_r+1,pos_c) and pos_r==1 and is_black):
     dx,dy=pawn_dirs_negated[-1]
  elif(pos_c==target_c-1 and pos_r==target_r+1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_white):
        dx,dy=pawn_dirs[1]

  elif(pos_c==target_c+1 and pos_r==target_r-1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_black):
        dx,dy=pawn_dirs_negated[1] 
  elif(pos_c==target_c+1 and pos_r==target_r+1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_white):
          dx,dy=pawn_dirs[2]
  
  elif(pos_c==target_c-1 and pos_r==target_r-1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_black):
          dx,dy=pawn_dirs_negated[2]       
  
 # for enpassent ,we need to have list of moves that works like a log , and we need to have an if condition that checks if moving pawn two pieces forward is right through invoking the log list and see if column of target square has a pawn move that moved two steps forward and capture if found  
  elif(move.is_pawn2(r,c) and move.is_white2(r,c) and tr==r-1 and(move.is_pawn2(tr+1,tc) and not move.is_friend(r,c,tr+1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr+1,tc) and move.moves_log["from"][-1][0]==1 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc-1):
     
          return True
  elif(move.is_pawn2(r,c)  and move.is_white2(r,c) and tr==r-1 and(move.is_pawn2(tr+1,tc) and not move.is_friend(r,c,tr+1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr+1,tc) and move.moves_log["from"][-1][0]==1 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc+1):

   return True
  elif(move.is_pawn2(r,c) and move.is_black2(r,c) and tr==r+1 and (move.is_pawn2(tr-1,tc) and not move.is_friend(r,c,tr-1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr-1,tc) and move.moves_log["from"][-1][0]==6 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc+1):
   
   return True
  elif(move.is_pawn2(r,c)  and move.is_black2(r,c) and tr==r+1 and(move.is_pawn2(tr-1,tc) and not move.is_friend(r,c,tr-1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr-1,tc) and move.moves_log["from"][-1][0]==6 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc-1):
  
   return True
  else:
     return False
  pos_r=target_r
  pos_c=target_c
  
  return True
    

    
 def index_my_king(my_r,my_c):
  
  letter_config="black"if move.is_black2(my_r,my_c) else "white"
  return move.positions[letter_config]['king']
 
 king_checkers={'white':[],'black':[]}

 def is_checked(kr,kc):
    king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
    KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
    pawn_dirs=[(-1,0),(-1,1),(-1,-1),(-2,0)]
    
    if(move.is_black2(kr,kc)):
      pawn_dirs=[(-dx,-dy) for dx,dy in pawn_dirs]
    enemy=[]
    color='black' if move.is_black2(kr,kc) else 'white'
    move.king_checkers[color]=[]
    for dx,dy in king_dirs:
          new_r,new_c=(kr,kc)
          while((0<=new_r+dx<=7 and 0<=new_c+dy<=7) ):
            next_r, next_c = new_r+dx, new_c+dy
            if(move.is_empty2(next_r,next_c)):
              new_r, new_c = next_r, next_c
            elif(move.is_friend(kr,kc,next_r,next_c)):
              break
            else:
              piece=get_piece(next_r,next_c)
              enemy.append((piece,(next_r,next_c)))
              break
            
    for dx,dy in KNIGHT_DELTAS:
          new_r,new_c=(kr,kc)
          if((0<=new_r+dx<=7 and 0<=new_c+dy<=7) ):
            new_r,new_c=(new_r+dx,new_c+dy)
            if(not move.is_empty2(new_r,new_c) and not move.is_friend(kr,kc,new_r,new_c) and move.is_knight2(new_r,new_c)):
              
              move.king_checkers[color].append(('knights',(new_r,new_c)))
              break  
    for dx,dy in pawn_dirs:
              new_r,new_c=(kr,kc)
              if((0<=new_r+dx<=7 and 0<=new_c+dy<=7) ):
                new_r,new_c=(new_r+dx,new_c+dy)
                if(not move.is_empty2(new_r,new_c) and not move.is_friend(kr,kc,new_r,new_c) and move.is_pawn2(new_r,new_c)):
                  
                  move.king_checkers[color].append(('pawns',(new_r,new_c)))  
                  break        
    for piece,(r,c) in enemy:
      if(piece=='rooks'):
       if  kr==r or kc==c:
        move.king_checkers[color].append((piece,(r,c)))
      if(piece=='bishops'): 
        if abs(kr-r)==abs(kc-c):
         move.king_checkers[color].append((piece,(r,c)))
      if(piece=='queen'):
        if (kr==r or kc==c) or abs(kr-r)==abs(kc-c):
          move.king_checkers[color].append((piece,(r,c)))
      else:
        continue

    return len(move.king_checkers[color] )>0

       
 

 moves_log= {
     "from":[]
     ,"to":[],
     "pawn":[],
     "capture":[],
     'pawn/capture':[],
     'castling':[]
     }
 dead_pieces={"white":[],"black":[]}
 
 def enpassent_corr(waspawn):
  fr=move.moves_log['from'][-1][0]
  tr=move.moves_log['to'][-1][0]
  tc=move.moves_log['to'][-1][1]
  if(waspawn):
    if(abs(fr-tr)==2):
     return (fr+tr)//2, tc
    else:
     return None  
  else:
    return None
 """  
 def castling_rights(turn):
   r_q,c_q=move.positions[turn]['rooks'][0]
   r_k,c_k=move.positions[turn]['rooks'][1]
   check_q= f"{turn}queen side "if not move.rook_or_king_moved(r_q,c_q,turn) else None
   check_k=f"{turn}king side " if not move.rook_or_king_moved(r_k,c_k,turn) else None  
   rights = [r for r in (check_q, check_k) if r is not None]
   return " ".join(rights)
  """
 def castling_rights(turn):
   rooks = move.positions[turn]['rooks']
   rights = []
   if len(rooks) > 0:
       r_q, c_q = rooks[0]
       if not move.rook_or_king_moved(r_q, c_q, turn):
           rights.append(f"{turn}queen side ")
   if len(rooks) > 1:
       r_k, c_k = rooks[1]
       if not move.rook_or_king_moved(r_k, c_k, turn):
           rights.append(f"{turn}king side ")
   return " ".join(rights)
 def update_place(old_r,old_c,r,c,castlingflag=False):
     
   old_sq=move.unparse_move(old_r,old_c)
   color='white'if(move.is_white2(old_r,old_c)) else 'black'
   e_color='black'if(move.is_white2(old_r,old_c)) else 'white'
   ispawnmove=True if(move.is_pawn2(old_r,old_c)) else False
   iscapture=True if  not move.is_empty2(r,c) else False
   iscapture_or_pawnmove=iscapture or ispawnmove
   if(castlingflag):
     k_dy,r_dy=(2,-1) if(old_c<c) else(-2,1)
     move.positions[color]['king']=(old_r,old_c+k_dy)
     idx=move.positions[color]['rooks'].index((old_r,c))
     move.positions[color]['rooks'][idx]=(r,old_c+k_dy+r_dy)
     move.moves_log["from"].append((old_r,old_c))
     move.moves_log["to"].append((r,c))
     move.moves_log['castling'].append('true')
     move.moves_log['pawn/capture'].append(iscapture_or_pawnmove)
     move.moves_log['pawn'].append(ispawnmove)
   
     move.board_snapshots.append({"board":deepcopy(move.positions),"turn":color,"enpassent":move.enpassent_corr(ispawnmove),"castling": {
        "white": move.castling_rights("white"),   
        "black": move.castling_rights("black"),
    },"checkers":deepcopy(move.king_checkers)})
   else:

 
    is_pieces={"king":move.is_king2(old_r,old_c),"bishops":move.is_bishop2(old_r,old_c),"knights":move.is_knight2(old_r,old_c),"queen":move.is_queen2(old_r,old_c),"pawns":move.is_pawn2(old_r,old_c),"rooks":move.is_rook2(old_r,old_c)}
    piece=None
    for key,value in is_pieces.items():
     if(value):
      piece=key
      break
    if(piece=='rooks' or piece=='bishops' or piece=='knights' or piece=='pawns' or piece=='queen'):
       idx=move.positions[color][piece].index((old_r,old_c))
       for e_piece,e_pos in move.positions[e_color].items():
         if e_piece=='king':
          continue
         for e_r,e_c in e_pos:
           if(e_r,e_c)==(r,c):
             e_pos.remove((r,c))
             
             move.dead_pieces[e_color].append(e_piece)
             break
       move.positions[color][piece][idx]=(r,c)
       
    else:
       for e_piece,e_pos in move.positions[e_color].items():
        if e_piece=='king':
          continue
        for e_r,e_c in e_pos:
         if(e_r,e_c)==(r,c):
           e_pos.remove((r,c))
           move.dead_pieces[e_color].append(e_piece)
           break
       move.positions[color][piece]=(r,c)
 
    move.moves_log["from"].append((old_r,old_c))
    move.moves_log["to"].append((r,c))
    move.moves_log['pawn/capture'].append(iscapture_or_pawnmove)
    move.moves_log['pawn'].append(ispawnmove)
    move.moves_log['castling'].append('false')
    
    move.board_snapshots.append({"board":deepcopy(move.positions),"turn":color,"enpassent":move.enpassent_corr(ispawnmove),"castling": {
         "white": move.castling_rights("white"),   
         "black": move.castling_rights("black"),
     },"checkers":deepcopy(move.king_checkers)})

 nextindex=None
 def is_three_fold():
   global nextindex
   if(nextindex==None):
     nextindex=0

   for i in range(nextindex,len(move.board_snapshots)):
    count=0
    for j in range(i+1,len(move.board_snapshots)):
      if(move.board_snapshots[i]==move.board_snapshots[j]):
        count+=1
      if(count==2):
        nextindex=j
        return True
   return False  
  
 index_leftoff=None
 def isfifty_moves_draw():
   global index_leftoff
   if(index_leftoff==None):
    index_leftoff=0
   movecount=0
   iscap_orpawn_count=0
   for i in range(index_leftoff,len(move.moves_log['pawn/capture'])):
     movecount+=1
     if(move.moves_log['pawn/capture'][i]):
       iscap_orpawn_count+=1
     if(movecount==50):
       break
   return iscap_orpawn_count==0

       

 def stalemate(kr,kc):
  color='white'if(move.is_white2(kr,kc)) else 'black'
  legal_moves=generate_legal_moves(color)
  if(len(legal_moves)==0) and not (move.is_checked(kr,kc)):
    return True
       

 def is_checkmated(kr,kc):
    color='white'if(move.is_white2(kr,kc)) else 'black'
    legal_moves=generate_legal_moves(color)
    if(len(legal_moves)==0) and (move.is_checked(kr,kc)):
      return True
    else:
      return False
# castling/enpassent
 def is_board_end(r,c):
  return r==0 or r==7
 king_moved=True
 pawn_choices=['b','n','q','r']

 def move_piece(pos_sq,target_sq,to_promote=None,verified=False):
  pos=move.parse_move(pos_sq)
  r,c=pos
  (old_r,old_c)=(r,c)
  target=move.parse_move(target_sq)
  tr,tc=target
  color=None
  if(not move.is_empty2(r,c) and pos_sq!=target_sq and not move.is_king2(tr,tc)):
         color='white'if(move.is_white2(r,c)) else 'black'

  
   
         k_r,k_c=move.index_my_king(r,c)
         legal_moves=[]
         is_pieces={"king":move.is_king2(old_r,old_c),"bishops":move.is_bishop2(old_r,old_c),"knights":move.is_knight2(old_r,old_c),"queen":move.is_queen2(old_r,old_c),"pawns":move.is_pawn2(old_r,old_c),"rooks":move.is_rook2(old_r,old_c)}
         piece=None
         for key,value in is_pieces.items():
             if(value):
              piece=key
              break
         if not verified:
           legal_moves = generate_legal_moves(color)
           if not ((piece,(r,c),(tr,tc)) in legal_moves):
             return False
         if(move.is_king2(r,c) and move.is_friend(tr,tc) and move.is_rook2(tr,tc)):
          k_dy,r_dy=(2,-1) if(tc>c) else(-2,1)
          move.update_place(r,c,tr,tc,castlingflag=True)
          real_board[r][c+k_dy]=real_board[r][c]
          real_board[r][c+k_dy+r_dy]=real_board[tr][tc]
          real_board[r][c]='.'
          real_board[tr][tc]='.'
        
          return True
         elif(move.is_pawn2(r,c) and move.is_white2(r,c) and tr==r-1 and(move.is_pawn2(tr+1,tc) and not move.is_friend(r,c,tr+1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr+1,tc) and move.moves_log["from"][-1][0]==1 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc-1):
          move.update_place(r,c,tr,tc)
          real_board[tr][tc]=real_board[r][c]
          real_board[tr+1][tc]='.'
          real_board[r][c]='.'
          return True
         elif(move.is_pawn2(r,c) and move.is_white2(r,c) and tr==r-1 and(move.is_pawn2(tr+1,tc) and not move.is_friend(r,c,tr+1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr+1,tc) and move.moves_log["from"][-1][0]==1 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc+1):
          move.update_place(r,c,tr,tc)
          real_board[tr][tc]=real_board[r][c]
          real_board[tr+1][tc]='.'
          real_board[r][c]='.'
          return True
         elif(move.is_pawn2(r,c) and move.is_black2(r,c) and tr==r+1 and (move.is_pawn2(tr-1,tc) and not move.is_friend(r,c,tr-1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr-1,tc) and move.moves_log["from"][-1][0]==6 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc+1):
          move.update_place(r,c,tr,tc)
          real_board[tr][tc]=real_board[r][c]
          real_board[tr-1][tc]='.'
          real_board[r][c]='.'
          return True
         elif(move.is_pawn2(r,c) and move.is_black2(r,c) and tr==r+1 and(move.is_pawn2(tr-1,tc) and not move.is_friend(r,c,tr-1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr-1,tc) and move.moves_log["from"][-1][0]==6 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc-1):
          move.update_place(r,c,tr,tc)
          real_board[tr][tc]=real_board[r][c]
          real_board[tr-1][tc]='.'
          real_board[r][c]='.'
          return True
         else:
          if(move.is_pawn2(r,c) and move.is_board_end(tr,tc) and to_promote not in (1,2,3,4)):
           return False
          move.update_place(r,c,tr,tc)
          real_board[tr][tc]=real_board[r][c]
          real_board[r][c]='.'
          pivot=None
         if(move.is_pawn2(tr,tc) and move.is_board_end(tr,tc)):
           if(to_promote in (1,2,3,4)):
             pivot=move.pawn_choices[to_promote-1]
             is_black_pawn = move.is_black2(tr,tc)
             real_board[tr][tc] = pivot.lower() if is_black_pawn else pivot.upper()
             color = 'black' if is_black_pawn else 'white'
             idx = move.positions[color]['pawns'].index((tr,tc))
             del move.positions[color]['pawns'][idx]
             promo_key={'b':'bishops','n':'knights','q':'queen','r':'rooks'}[pivot]
             move.positions[color][promo_key].append((tr,tc))
           else:
             return False
         return True
       
  


 def reset_board(board):
  board=real_board.copy()
 def can_be_checked(k_r,k_c,r,c,iscastling=False):
  if not (0<=r<=7 and 0<=c<=7 and 0<=k_r<=7 and 0<=k_c<=7):
      return False
  saved_board = [row[:] for row in real_board]
  color = 'black' if move.is_black2(k_r,k_c) else 'white'
  saved_checkers = move.king_checkers[color][:]

  if(iscastling): 
      k_dy,r_dy=(2,-1) if(c>k_c) else(-2,1)
      real_board[k_r][k_c+k_dy]=real_board[k_r][k_c]
      real_board[k_r][k_c+k_dy+r_dy]=real_board[r][c]
      real_board[k_r][k_c]='.'
      real_board[r][c]='.'
      checked = move.is_checked(k_r,k_c+k_dy)
  else:
   real_board[r][c]=real_board[k_r][k_c]
   real_board[k_r][k_c]='.'
   checked = move.is_checked(r,c)
  for i in range(8):
    real_board[i][:] = saved_board[i]
  move.king_checkers[color] = saved_checkers

  return checked
board_snapshots=[{"board":deepcopy(move.positions),"turn":"white","enpassent":None,"castling": {
        "white": move.castling_rights("white"),   
         "black": move.castling_rights("black")},"checkers":deepcopy(move.king_checkers)
}]   
def can_be_checked2(r,c,tr,tc):
 checked = False
 if(not move.is_king2(r,c)):
  (k_r,k_c)=move.index_my_king(r,c)
  saved_board = [row[:] for row in real_board]
  color = 'black' if move.is_black2(k_r,k_c) else 'white'
  saved_checkers = move.king_checkers[color][:]
  real_board[tr][tc]=real_board[r][c]
  real_board[r][c]='.'
  checked=move.is_checked(k_r,k_c)
  for i in range(8):
     real_board[i][:] = saved_board[i]
  move.king_checkers[color] = saved_checkers
 return checked

def get_piece(old_r,old_c):
  is_pieces={"king":move.is_king2(old_r,old_c),"bishops":move.is_bishop2(old_r,old_c),"knights":move.is_knight2(old_r,old_c),"queen":move.is_queen2(old_r,old_c),"pawns":move.is_pawn2(old_r,old_c),"rooks":move.is_rook2(old_r,old_c)}
  for key,value in is_pieces.items():
    if(value):
      return key
    
def diagonal_check(piece,r,c):
  bish_silding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1)]
  legal=[] 
  
  for dx,dy in bish_silding_dirs:
    new_r,new_c=(r,c) 
    while(0<=new_r+dx<=7 and 0<=new_c+dy<=7 ):
      check= not move.is_friend(r,c,new_r+dx,new_c+dy) and (move.bishop_legal(r,c,new_r+dx,new_c+dy) if(piece=='rooks') else move.queen_legal(r,c,new_r+dx,new_c+dy) )
      if(check and not can_be_checked2(r,c,new_r+dx,new_c+dy)):

        new_r+=dx
        new_c+=dy
        if(piece=='bishops'):
         legal.append(('bishops',(r,c),(new_r,new_c)))
        else:
          legal.append(('queen',(r,c),(new_r,new_c)))




      else:
        break
  return legal        
    
def row_col_check(piece,r,c):
  rook_dir=[(1,0),(-1,0),(0,1),(0,-1)] 
  legal=[] 
    
  for dx,dy in rook_dir:
      new_r,new_c=(r,c) 
      while(0<=new_r+dx<=7 and 0<=new_c+dy<=7 ):
        check= not move.is_friend(r,c,new_r+dx,new_c+dy) and (move.rook_legal(r,c,new_r+dx,new_c+dy) if(piece=='rooks') else move.queen_legal(r,c,new_r+dx,new_c+dy) )
        if(check and not can_be_checked2(r,c,new_r+dx,new_c+dy)):
  
          new_r+=dx
          new_c+=dy
          if(piece=='rooks'):
           legal.append(('rooks',(r,c),(new_r,new_c)))
          else:
            legal.append(('queen',(r,c),(new_r,new_c)))
            
        else:
          break 
  return legal         

def knight_check(r,c):
  KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
  legal=[]
  for dx,dy in KNIGHT_DELTAS:
      new_r,new_c=(r,c)
      if((0<=new_r+dx<=7 and 0<=new_c+dy<=7)  and move.knight_legal(r,c,new_r+dx,new_c+dy) and not can_be_checked2(r,c,new_r+dx,new_c+dy) ):
       new_r,new_c=(new_r+dx,new_c+dy)
       legal.append(('knights',(r,c),(new_r,new_c)))
      else:
        continue
  return legal
def king_check(r,c):
  king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 

  legal=[]
  for dx,dy in king_dirs:
        new_r,new_c=(r,c)
        if((0<=new_r+dx<=7 and 0<=new_c+dy<=7)  and move.king_legal(r,c,new_r+dx,new_c+dy)):
         new_r,new_c=(new_r+dx,new_c+dy)
         legal.append(('king',(r,c),(new_r,new_c)))
        else:
          continue
  return legal
def pawn_check(r,c):
    pawn_dirs=[(-1,0),(-1,1),(-1,-1),(-2,0)]
    legal=[]
    if(move.is_black2(r,c)):
      pawn_dirs=[(-dx,-dy) for dx,dy in pawn_dirs]
    for dx,dy in pawn_dirs:
            new_r,new_c=(r,c)
            if((0<=new_r+dx<=7 and 0<=new_c+dy<=7)  and move.pawn_legal(r,c,new_r+dx,new_c+dy) and not can_be_checked2(r,c,new_r+dx,new_c+dy) ):
             new_r,new_c=(new_r+dx,new_c+dy)
             legal.append(('pawns',(r,c),(new_r,new_c)))
            else:
              continue  
    return legal  

def generate_legal_moves(color):
   legal_moves=[]
   legal_moves_ordered=[]
   value={'pawns':1,'knights':3,'bishops': 3,'rooks':5,'queen':9,'king':1000}

   for piece,position in move.positions[color].items():
     if(piece=='king'):
       (r,c)=position
       legal_moves.extend(king_check(r,c))
     else:
      for r,c in position:
       if(piece=='rooks' ):
          legal_moves.extend(row_col_check(piece,r,c))
       elif(  piece=='bishops'):
         legal_moves.extend(diagonal_check(piece,r,c))
       elif(piece=='queen'):
        legal_moves.extend(diagonal_check(piece,r,c))
        legal_moves.extend(row_col_check(piece,r,c))
       elif(piece=='knights'):
        legal_moves.extend(knight_check(r,c))
       elif(piece=='pawns'):
         legal_moves.extend(pawn_check(r,c))
   captures = []
   quiet = []
   for piece,(r,c),(tr,tc) in legal_moves:
     if not move.is_empty2(tr,tc):
        captures.append((piece,(r,c),(tr,tc)))
     else:
        quiet.append((piece,(r,c),(tr,tc)))
     captures.sort(key=lambda m: value[get_piece(*m[2])] - value[m[0]], reverse=True)
   return captures + quiet
def material_count(color,positions):
  material=0
  value={'pawns':1,'knights':3,'bishops': 3,'rooks':5,'queen':9}
  for piece,position in positions[color].items():
   if(piece=='king'):
     continue
   else:
     for r,c in position:
       material+=value.get(piece)
  return material
def evaluate( positions):
    white_material = material_count('white', positions)
    black_material = material_count('black', positions)

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

    for piece,pos in positions['white'].items():
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

    for piece,pos in positions['black'].items():
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
def unmove():
 if(len(move.board_snapshots)>1):
  for i in range(8):
    for j in range(8):
      real_board[i][j]='.'
  move.king_checkers=deepcopy(move.board_snapshots[-2]['checkers'])
  move.positions=deepcopy(move.board_snapshots[-2]['board'])
  b_mapping={'knights':'n','king':'k','queen':'q','bishops':'b'  ,'rooks':'r','pawns':'p'}
  mapping={'knights':'N','king':'K','queen':'Q','bishops':'B'  ,'rooks':'R','pawns':'P'}
  for piece,position in move.positions['white'].items():
   letter=mapping.get(piece)
   if(piece=='king'):
     r,c=position
     real_board[r][c]=letter
   else:
     for r,c in position:
       real_board[r][c]=letter

  for piece,position in move.positions['black'].items():
     letter=b_mapping.get(piece)
     if(piece=='king'):
      r,c=position
      real_board[r][c]=letter
     else:
       for r,c in position:
         real_board[r][c]=letter     
  move.moves_log["from"].pop() 
  move.moves_log["to"].pop() 
  move.moves_log['castling'].pop() 
  move.moves_log['pawn/capture'].pop() 
  move.moves_log['pawn'].pop() 
  move.board_snapshots.pop()    
   
 else:
   return

import math
pos_inf = math.inf          # Positive infinity
neg_inf = -math.inf         # Negative infinity 
"""def minimax(color,depth):
  moves=generate_legal_moves(color)
  kr,kc=move.positions[color]['king']
  if len(moves) == 0:
    if move.is_checked(kr, kc):
        if(color=='white'):
         return -1000
        else:
          return 1000   # checkmate — return immediately
    else:
        return 0                                   # stalemate — return

  
  if(depth==0):
    return evaluate(move.positions)
  if color=='black' and depth==2:   # first-level black call from best_move(depth=3)
      print(f"    [minimax entry] black king at ({kr},{kc})={move.unparse_move(kr,kc)}, depth={depth}, {len(moves)} moves")
  if(color=='white'):
   maxeval=neg_inf
   for piece,(r,c),(tr,tc) in moves:
    move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
    eval=minimax('black',depth-1)
    maxeval=max(eval,maxeval)
    unmove()
    
   return maxeval
   
  else:
    mineval=pos_inf
    for piece,(r,c),(tr,tc) in moves:
       move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
       eval=minimax('white',depth-1)
       mineval=min(eval,mineval)
       unmove() 
    return mineval"""
    

  
     
     
          
def print_board(board):
    files = '  a b c d e f g h'
    print(files)
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank} {' '.join(row)} {rank}")
    print(files)
###testinnggg
def minimax(color,depth,alpha,beta):
  moves=generate_legal_moves(color)
  kr,kc=move.positions[color]['king']
  if len(moves) == 0:
    if move.is_checked(kr, kc):
        return -1000 if color=='white' else 1000
    else:
        return 0
  if(depth==0):
    return evaluate(move.positions)

  if(color=='white'):
   maxeval=neg_inf
   for piece,(r,c),(tr,tc) in moves:
    move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
    eval=minimax('black',depth-1,alpha,beta)
    unmove()
    alpha=max(alpha,eval) 

    maxeval=max(eval,maxeval)
    if(beta<=alpha):
      break
   return maxeval
  else:
    mineval=pos_inf
    for piece,(r,c),(tr,tc) in moves:
       move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
       eval=minimax('white',depth-1,alpha,beta)
       unmove()
       beta=min(beta,eval) 

       mineval=min(eval,mineval)
       if(beta<=alpha):
         break
    return mineval

"""def minimax(color,depth):
  moves=generate_legal_moves(color)
  kr,kc=move.positions[color]['king']
  if len(moves) == 0:
    if move.is_checked(kr, kc):
        return -1000 if color=='white' else 1000
    else:
        return 0
  if(depth==0):
    return evaluate(move.positions)

  if(color=='white'):
   maxeval=neg_inf
   for piece,(r,c),(tr,tc) in moves:
    move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
    if piece=='queen' and (r,c)==(5,5) and (tr,tc)==(1,5):
        print(f"  >>> About to recurse into minimax('black', {depth-1}) after Qxf7")
        k2r,k2c = move.positions['black']['king']
        m2 = generate_legal_moves('black')
        print(f"  >>> black king at ({k2r},{k2c}), {len(m2)} legal moves: {m2}")
    eval=minimax('black',depth-1)
    unmove()
    maxeval=max(eval,maxeval)
   return maxeval
  else:
    mineval=pos_inf
    for piece,(r,c),(tr,tc) in moves:
       move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
       eval=minimax('white',depth-1)
       unmove()
       mineval=min(eval,mineval)
    return mineval"""


def best_move(color,depth):
  moves=generate_legal_moves(color)
  bestmove=None

  if(color=='white'):
   maxeval=neg_inf
   for piece,(r,c),(tr,tc) in moves:
    move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
    eval = minimax('black', depth-1,neg_inf,pos_inf)
    unmove()

    if eval> maxeval:
     maxeval=eval
     bestmove=[piece,(r,c),(tr,tc),maxeval]
   return bestmove
   
  else:
    mineval=pos_inf
    for piece,(r,c),(tr,tc) in moves:
        move.move_piece(move.unparse_move(r,c),move.unparse_move(tr,tc),verified=True)
        eval = minimax('white', depth-1,neg_inf,pos_inf)
        unmove()
      
        if eval< mineval:
         mineval=eval
         bestmove=[piece,(r,c),(tr,tc),mineval]
    return bestmove

def game_loop(player_color='white', engine_depth=3):
    engine_color = 'black' if player_color == 'white' else 'white'

    while True:
        print_board(real_board)

        turn_color = player_color if len(move.moves_log['from']) % 2 == 0 else engine_color
        # Note: assumes white always moves first and colors alternate strictly.
        # If player_color == 'black', engine moves first below instead.

        # --- Game-over check for whoever is about to move ---
        current_color = player_color if (len(move.moves_log['from']) % 2 == 0) == (player_color == 'white') else engine_color
        kr, kc = move.positions[current_color]['king']
        legal = generate_legal_moves(current_color)
        if len(legal) == 0:
            if move.is_checked(kr, kc):
                winner = engine_color if current_color == player_color else player_color
                print(f"Checkmate — {winner} wins.")
            else:
                print("Stalemate — draw.")
            break

        if current_color == player_color:
            pos = input(f'Your move ({player_color}), from square: ').strip()
            target = input('to square: ').strip()

            if pos.lower() in ('quit', 'resign'):
                print("You resigned.")
                break

            try:
                fr, fc = move.parse_move(pos)
                tr, tc = move.parse_move(target)
            except (IndexError, ValueError):
                print("Invalid square format, try again (e.g. e2).")
                continue

            promo = None
            if move.is_pawn2(fr, fc) and move.is_board_end(tr, tc):
                raw = input('Promote to (1=bishop 2=knight 3=queen 4=rook): ').strip()
                if raw not in ('1', '2', '3', '4'):
                    print("Invalid promotion choice, try again.")
                    continue
                promo = int(raw)

            success = move.move_piece(pos, target, to_promote=promo, verified=False)
            if not success:
                print('Illegal move, try again.')
                continue

        else:
            print("Engine is thinking...")
            result = best_move(engine_color, engine_depth)
            if result is None:
                print("Engine has no legal moves.")
                break
            piece, (r, c), (tr, tc), score = result
            from_sq, to_sq = move.unparse_move(r, c), move.unparse_move(tr, tc)
            print(f"Engine plays {piece} {from_sq} -> {to_sq} (eval={score})")
            move.move_piece(from_sq, to_sq, verified=True)

game_loop(player_color='white', engine_depth=3)









"""move.move_piece('a2','a4')
move.move_piece('b7','b5')
x=minimax('black',depth=2)
y=minimax('white',depth=2)
print(x)
print(y)"""
########################################
"""def check_consistency():
    seen = {}
    for color in ('white','black'):
        for piece, pos in move.positions[color].items():
            squares = [pos] if piece=='king' else pos
            for r,c in squares:
                if (r,c) in seen:
                    print(f"DUPLICATE: ({r},{c}) claimed by both {seen[(r,c)]} and {color} {piece}")
                seen[(r,c)] = (color,piece)"""
"""move.move_piece('e2','e4')
move.move_piece('b8','c6')
move.move_piece('f1','c4')
move.move_piece('g8','f6')
move.move_piece('d1','f3')
move.move_piece('f6','e4')

import time
start = time.time()
result = best_move('white', 3)
print(result, time.time() - start)"""
"""import cProfile
cProfile.run("best_move('white', 3)", sort='cumulative')"""
"""def gameloop():
  while(True):
    print_board(real_board)
    pos=input('white pos:')

    target=input('black target:')

  
    try :move.move_piece(pos,target,to_promote=None,verified=False)
    except:print('illegal move')

    (r,c)=best_move('black',2)[1]
    (r1,c1)=best_move('black',2)[2]
    ai_pos=move.unparse_move(r,c)
    ai_tr=move.unparse_move(r1,c1)
    try :move.move_piece(ai_pos,ai_tr)
    except:print('illegal move')"""





