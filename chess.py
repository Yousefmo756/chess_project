
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
  if(move.is_black(move.unparse_move(pos_r,pos_c)) and move.is_black(move.unparse_move(target_r,target_c))):
   return True
  elif(move.is_white(move.unparse_move(pos_r,pos_c)) and move.is_white(move.unparse_move(target_r,target_c))):
      return True
  else:
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
        print('cant attack friend!')
        return False
      if(not move.is_empty2(newpos_r,newpos_c)):
       print('path blocked')
       return False
      pos_r=newpos_r
      pos_c=newpos_c
  
    return False
 

 def knight_legal(pos_r,pos_c,target_r,target_c):
  KNIGHT_DELTAS = {(-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(1,2),(-1,-2),(1,-2)}
  if (target_r-pos_r, target_c-pos_c) not in KNIGHT_DELTAS:
        print('illegal move for knight')
        return False
  if move.is_empty2(target_r,target_c) or not move.is_friend(pos_r,pos_c,target_r,target_c):
        board[target_r][target_c]=board[pos_r][pos_c]
        board[pos_r][pos_c]='.'
        return True
  else:
        print("can't attack friend!")
        return False
   
 def bishop_legal(pos_r,pos_c,target_r,target_c):
  bish_silding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1)]  
  (dx,dy)=(0,0)
  if(abs(pos_r-target_r)==abs(target_c-pos_c) and (pos_r,pos_c)!=(target_r,target_c)):
   if(target_c<pos_c and target_r<pos_r):
    dx,dy=bish_silding_dirs[3]
   elif(target_c<pos_c  and target_r>pos_r):
    dx,dy=bish_silding_dirs[2]
   elif(target_c>pos_c  and target_r>pos_r):
    dx,dy=bish_silding_dirs[0]
   elif(target_c>pos_c  and target_r<pos_r):
      dx,dy=bish_silding_dirs[1]
  else:
    print("wrong move for bishop ") 
    return False

  for_limit=abs(pos_c-target_c)
  for i in range(for_limit):
    newpos_r=pos_r+dx
    newpos_c=pos_c+dy
    if((newpos_r,newpos_c)==(target_r,target_c)):
     if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
      pos_r=newpos_r
      pos_c=newpos_c
      return True
     else:
      print('cant attack friend!')
      return False
    if(not move.is_empty2(newpos_r,newpos_c)):
     print('path blocked')
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
     dx,dy=queen_sliding_dirs[2]
    elif(target_c>pos_c  and target_r>pos_r):
     dx,dy=queen_sliding_dirs[0]
    elif(target_c>pos_c  and target_r<pos_r):
       dx,dy=queen_sliding_dirs[1]
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
      print('cant attack friend!')
      return False
    if(not move.is_empty2(newpos_r,newpos_c)):
     print('path blocked')
     return False
    pos_r=newpos_r
    pos_c=newpos_c
  return False
 king_moved=False

  
 def king_legal(pos_r,pos_c,target_r,target_c):
      king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
      (dx,dy)=(0,0)
      if(not move.can_be_checked(pos_r,pos_c,target_r,target_c)):
       if(abs(pos_r-target_r)==abs(target_c-pos_c)):
        if(target_c<pos_c and target_r<pos_r):
         dx,dy=king_dirs[3]
        elif(target_c<pos_c  and target_r>pos_r):
         dx,dy=king_dirs[2]
        elif(target_c>pos_c  and target_r>pos_r):
         dx,dy=king_dirs[0]
        elif(target_c>pos_c  and target_r<pos_r):
         dx,dy=king_dirs[1]
        else:
         return
       elif (target_r == pos_r and target_c > pos_c and move.is_rook(move.unparse_move(target_r,target_c)) and move.is_empty2(pos_r,pos_c+1) and  move.is_empty2(pos_r,pos_c+2) and not move.is_checked(pos_r,pos_c) and not move.can_be_checked(pos_r,pos_c,target_r,target_c) and not move.rook_or_king_moved(target_r,target_c)):
        dx,dy=(0,2)
       elif (target_r == pos_r and target_c < pos_c and move.is_rook(move.unparse_move(target_r,target_c)) and move.is_empty2(pos_r,pos_c-1) and  move.is_empty2(pos_r,pos_c-2) and not move.is_checked(pos_r,pos_c) and not move.can_be_checked(pos_r,pos_c,target_r,target_c) and not move.rook_or_king_moved(target_r,target_c)):
        dx,dy=(0,-2)
       elif (target_c == pos_c and target_r > pos_r):
        dx,dy=king_dirs[-4]
       elif (target_c == pos_c and target_r < pos_r):
        dx,dy=king_dirs[-3]
       elif (target_r == pos_r and target_c > pos_c):
        dx,dy=king_dirs[-2]
       elif (target_r == pos_r and target_c < pos_c):
        dx,dy=king_dirs[-1]
       else:
        return
       newpos_r=pos_r+dx
       newpos_c=pos_c+dy
       if((move.is_empty2(newpos_r,newpos_c) or not move.is_friend(newpos_r,newpos_c,pos_r,pos_c) ) and not move.is_king(move.unparse_move(pos_r+dx,pos_c+dy))):  
          pos_r=newpos_r
          pos_c=newpos_c 
          return True  
       else:
          print('cant attack here!')
          return False

 def rook_or_king_moved(r_r,r_c):
   r_moved=None
   k_moved=None
   (kr,kc)=move.index_my_king(r_r,r_c)
   color='black' if(move.is_black(move.unparse_move(r_r,r_c))) else'white'
   if(color=='black'):
    idx= move.positions[color]['rooks'].index(r_r,r_c)
    if(idx==0):
     r_moved=False if(r_r,r_c)==(0,0) else True
    if(idx==1):
     r_moved=False if(r_r,r_c)==(0,7) else True
     k_moved=False if(kr,kc)==(0,4) else True
   if(color=='white'):
      idx= move.positions[color]['rooks'].index(r_r,r_c)
      if(idx==0):
       r_moved=False if(r_r,r_c)==(7,0) else True
      if(idx==1):
       r_moved=False if(r_r,r_c)==(7,7) else True
       k_moved=False if(kr,kc)==(7,4) else True
   return r_moved or k_moved

 def pawn_legal(pos_r,pos_c,target_r,target_c):
  newpos_r=0
  newpos_c=0
  pawn_dirs=[(-1,0),(-1,1),(-1,-1),(-2,0)]
  pawn_dirs_negated=[(-dx, -dy) for dx, dy in pawn_dirs]
  
  (dx,dy)=(0,0)
  is_black=move.is_black(move.unparse_move(pos_r,pos_c))
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
  else:
     print("cant go there")
     return False
  pos_r=target_r
  pos_c=target_c
  
  return True
    

    
 def index_my_king(my_r,my_c):
  
  pos_sq=move.unparse_move(my_r,my_c)
  letter_config="black"if move.is_black(pos_sq) else "white"
  return move.positions[letter_config]['king']
 king_checkers={'white':[],'black':[]}
 def is_checked(k_r,k_c):
  
  pos_sq=move.unparse_move(k_r,k_c)
  color="black"if move.is_black(pos_sq) else "white"
  enemy_color="white"if move.is_black(pos_sq) else "black"
  move.king_checkers[color]=[]

  for piece,position in move.positions[enemy_color].items():
    if piece=='king':
     r,c=position
    if(move.king_legal(r,c,k_r,k_c)): 
        move.king_checkers[color].append((piece,r,c))
       
    else:
      for r,c in position:
        if(piece=='queen'):
           if(move.queen_legal(r,c,k_r,k_c)):
               move.king_checkers[color].append((piece,r,c))
        if(piece=='pawns'):
          if(move.pawn_legal(r,c,k_r,k_c)):
           move.king_checkers[color].append((piece,r,c))
        elif(piece=='rooks'):
          if(move.rook_legal(r,c,k_r,k_c)):
           move.king_checkers[color].append((piece,r,c))
        elif(piece=='knight'):
          if(move.knight_legal(r,c,k_r,k_c)):
           move.king_checkers[color].append((piece,r,c))
        else:
          if(move.bishop_legal(r,c,k_r,k_c)):
           move.king_checkers[color].append((piece,r,c))

  if(len(move.king_checkers[color])>0):
    return True
  else:
    return False
       
 # we need to identify 1.whether a king is under attack 2. if the king can be saved through a friends move(capture the threat , or block the threat) 3. king has no way to move
 # to make friend block we have to identify which r,c is the checker on relative to kings place
 """ def is_bishop_attack(piece):
       if(piece=='bishop'):
        return True
       return False
 def is_rook_attack(piece):
        if(piece=='rook'):
         return True
        return False
 def is_knight_attack(piece):
   if(piece=='knight'):
     return True
   return False
 def is_queen_attack(piece):
   if(piece=='queen'):
    return True
   return False"""
 

 def bishop_blocks(k_r,k_c):
    block_sqrs=[]
    king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
    for e_piece,er,ec in move.king_checkers[king_color]:
       if(e_piece=='bishop'):
        bish_sliding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1)]  
        if(ec<k_c and er<k_r):
            dx,dy=bish_sliding_dirs[3]
        elif(ec<k_c  and er>k_r):
            dx,dy=bish_sliding_dirs[2]
        elif(ec>k_c  and er>k_r):
            dx,dy=bish_sliding_dirs[0]
        elif(ec>k_c  and er<k_r):
              dx,dy=bish_sliding_dirs[1]
        else:
          continue      
        b_r,b_c=k_r,k_c
        for i in range(abs(k_c-ec)):
          b_r=b_r+dx
          b_c=b_c+dy
          block_sqrs.append((b_r,b_c))
    return block_sqrs
 def queen_blocks(k_r,k_c):
      block_sqrs=[]
      king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
      for e_piece,er,ec in move.king_checkers[king_color]:
       if(e_piece=='queen'):
          queen_sliding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
          (dx,dy)=(0,0)

          if(abs(k_r-er)==abs(k_c-ec)):
           if(ec<k_c and er<k_r):
            dx,dy=queen_sliding_dirs[3]
           elif(ec<k_c  and er>k_r):
            dx,dy=queen_sliding_dirs[2]
           elif(ec>k_c  and er>k_r):
            dx,dy=queen_sliding_dirs[0]
           elif(ec>k_c  and er<k_r):
              dx,dy=queen_sliding_dirs[1]
           else:
             continue
           b_r,b_c=k_r,k_c
           for i in range(abs(k_c-ec)):  
             b_r+=dx
             b_c+=dy    
             block_sqrs.append((b_r,b_c))

          elif (ec == k_c and er > k_r):
            dx,dy=queen_sliding_dirs[-4]
          elif (ec == k_c and er < k_r):
           dx,dy=queen_sliding_dirs[-3]
          elif (er == k_r and ec > k_c):
           dx,dy=queen_sliding_dirs[-2]    
          elif (er == k_r and ec < k_c):
           dx,dy=queen_sliding_dirs[-1]
          else:
            continue

          if not (abs(k_r-er)==abs(k_c-ec)):
              for_limit = abs(er-k_r) if ec==k_c else abs(k_c-ec)
              b_r,b_c=k_r,k_c
              for i in range(for_limit):
                  b_r+=dx
                  b_c+=dy  
                  block_sqrs.append((b_r,b_c))
      return block_sqrs
 def rook_blocks(k_r,k_c):
  block_sqrs=[]
  king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
  for e_piece,er,ec in move.king_checkers[king_color]:
   if(e_piece=='rook'):
             rook_dir=[(1,0),(-1,0),(0,1),(0,-1)] 
             dx,dy=(0,0)
             if (ec == k_c and er > k_r):
              dx,dy=rook_dir[-4]
             elif (ec == k_c and er < k_r):
               dx,dy=rook_dir[-3]
             elif (er == k_r and ec > k_c):
               dx,dy=rook_dir[-2]    
             elif (er == k_r and ec < k_c):
               dx,dy=rook_dir[-1]
             else:
               continue 
           
             for_limit=0
           
           
             if(er == k_r):
               for_limit=abs(k_c-ec)
             else:
               for_limit=abs(k_r-er)
             b_r,b_c=k_r,k_c
             for i in range(for_limit):
               b_r+=dx
               b_c+=dy
               block_sqrs.append((b_r,b_c))
  return block_sqrs
 king_escape=[]
 def can_king_escape(k_r,k_c):
  king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
  move.king_escape=[]
  rook_blocks_coor=move.rook_blocks(k_r,k_c)
  queen_blocks_coor=move.queen_blocks(k_r,k_c)
  bishop_blocks_coor=move.bishop_blocks(k_r,k_c)
  block_sqrs=[*queen_blocks_coor,*bishop_blocks_coor,*rook_blocks_coor]
  unacceptable=[*block_sqrs,(k_r,k_c)]
  friendly_occupied = [sq for positions in move.positions[king_color].values() for sq in positions]
  count=0
  for r in range(8):
    for c in range(8): 
       if(not (r,c)  in friendly_occupied and (not (r,c) in unacceptable) and move.king_legal(k_r,k_c,r,c) ):
         move.king_escape.append((r,c))
         count+=1
  if(count>0) :      
   return True 
  return False   
 attack_or_blocking_pieces=[] 
 def can_friend_block(k_r,k_c):
  king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
  move.attack_or_blocking_pieces=[]

  if(len(move.king_checkers[king_color])>1):
    return False
  rook_blocks_coor=move.rook_blocks(k_r,k_c)
  queen_blocks_coor=move.queen_blocks(k_r,k_c)
  bishop_blocks_coor=move.bishop_blocks(k_r,k_c)
  block_sqrs=[*queen_blocks_coor,*bishop_blocks_coor,*rook_blocks_coor]
  for piece,position in move.positions[king_color].items():
      if piece=='king':
        continue
      for r,c in block_sqrs:
            for fr,fc in position:
              if(piece=='queen'):
               if(move.queen_legal(fr,fc,r,c)):
                move.attack_or_blocking_pieces.append((fr,fc))
                return True 
              if(piece=='pawns'):
                if(move.pawn_legal(fr,fc,r,c)):
                  move.attack_or_blocking_pieces.append((fr,fc))
                  return True
              elif(piece=='rooks'):
                if(move.rook_legal(fr,fc,r,c)):
                  move.attack_or_blocking_pieces.append((fr,fc))
                  return True

              elif(piece=='knights'):
                if(move.knight_legal(fr,fc,r,c)):
                      move.attack_or_blocking_pieces.append((fr,fc))
                      return True

              elif(piece=='bishops'):
                if(move.bishop_legal(fr,fc,r,c)):
                        move.attack_or_blocking_pieces.append((fr,fc))
                        return True
  return False
 def friend_attack(k_r,k_c):
  king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
  move.attack_or_blocking_pieces=[]

  for piece,position in move.positions[king_color].items():
    for e_piece,r,c in move.king_checkers[king_color]:
     if  piece=='king':
      fr,fc=position
      
      if(piece=='king'):
       if(move.king_legal(fr,fc,r,c)): 
        move.attack_or_blocking_pieces.append((fr,fc))  
        return True 
     else:
      for fr,fc in position:
       if(piece=='pawns'):
        if(move.pawn_legal(fr,fc,r,c)):
         move.attack_or_blocking_pieces.append((fr,fc))
         return True
       elif(piece=='rooks'):
        if(move.rook_legal(fr,fc,r,c)):
           move.attack_or_blocking_pieces.append((fr,fc))
           return True
     
       elif(piece=='knights'):
        if(move.knight_legal(fr,fc,r,c)):
          move.attack_or_blocking_pieces.append((fr,fc))
          return True
     
       elif(piece=='bishops'):
        if(move.bishop_legal(fr,fc,r,c)):
         move.attack_or_blocking_pieces.append((fr,fc))
         return True
  return False
 
 moves_log= {
     "from":[]
     ,"to":[]
     }
 dead_pieces={"white":[],"black":[]}
 
 def enpassent_corr(turn):
  fr=move.moves_log['from'][-1][0]
  fc=move.moves_log['from'][-1][1]
  check=move.is_pawn(move.unparse_move(fr,fc)) and move.is_black(move.unparse_move(fr,fc)) if(turn=='white') else move.is_pawn(move.unparse_move(fr,fc)) and move.is_white(move.unparse_move(fr,fc))
  if(check):
    if(abs(move.moves_log['from'][-1][0]-move.moves_log['to'][0])==2):
     return move.is_pawn['to'][-1][0],move.is_pawn['to'][-1][1]
    else:
     return None  
  else:
    return None  
  
 def castling_rights(turn):
   r_q,c_q=move.positions[turn]['rooks'][0]
   r_k,c_k=move.positions[turn]['rooks'][1]
   check_q= " f{turn}queen side "if move.rook_or_king_moved(r_q,c_q) else None
   check_k=" f{turn}king side " if move.rook_or_king_moved(r_k,c_k) else None  
   return check_k+check_q
  
 
 def update_place(old_r,old_c,r,c):
   old_sq=move.unparse_move(old_r,old_c)
   color='white'if(move.is_white(old_sq)) else 'black'
   e_color='black'if(move.is_white(old_sq)) else 'white'

   is_pieces={"king":move.is_king(old_sq),"bishops":move.is_bishop(old_sq),"knights":move.is_knight(old_sq),"queen":move.is_queen(old_sq),"pawns":move.is_pawn(old_sq),"rooks":move.is_rook(old_sq)}
   piece=None
   for key,value in is_pieces.items():
    if(value):
     piece=key
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
 def is_stalemate(kr,kc):
   color='black' if move.is_black(move.unparse_move(kr,kc)) else 'white'
   friends=[(kr,kc)]

   for piece,position in move.positions[color].items():
     if(piece=='king'):
       continue
     else:
      for r,c in position:
       friends.append((r,c))
   for r,c in friends:
    for row in range(8):
     for col in range (8):
      if((move.is_pawn(move.unparse_move(r,c)) and move.pawn_legal(r,c,row,col)) or (move.is_rook(move.unparse_move(r,c)) and move.rook_legal(r,c,row,col)) or  (move.is_king(move.unparse_move(r,c)) and move.king_legal(r,c,row,col)) or (move.is_bishop(move.unparse_move(r,c)) and move.bishop_legal(r,c,row,col)) or move.is_knight(move.unparse_move(r,c)) and move.knight_legal(r,c,row,col) or (move.is_queen(move.unparse_move(r,c)) and move.queen_legal(r,c,row,col))):

       return False
   return True   
       

 def is_checkmated(k_r,k_c):
  king_color="white"if(move.is_white(move.unparse_move(k_r,k_c))) else "black"
  if(len(move.king_checkers[king_color])>1):
    return not move.can_king_escape(k_r,k_c)
  if(not (move.friend_attack(k_r,k_c) or move.can_friend_block(k_r,k_c) or move.can_king_escape(k_r,k_c))):
    return True
# castling/enpassent
 def is_board_end(r,c):
  row= 0 if move.is_white(move.unparse_move(r,c)) else 7
  return row==0 or row==7
 # for enpassent ,we need to have list of moves that works like a log , and we need to have an if condition that checks if moving pawn two pieces forward is right through invoking the log list and see if column of target square has a pawn move that moved two steps forward and capture if found  
  #return True
 king_moved=True
 pawn_choices=['b','k','q','r']
 def move_piece(pos_sq,target_sq,to_promote=None):
  pos=move.parse_move(pos_sq)
  r,c=pos
  if(not move.is_empty2(r,c) and pos_sq!=target_sq and not move.is_king(target_sq)):
   target=move.parse_move(target_sq)
   tr,tc=target
   legal_move=[move.is_pawn(pos_sq) and move.pawn_legal(r,c, tr,tc),move.is_bishop(pos_sq) and move.bishop_legal(r,c, tr,tc), move.rook_legal(r,c, tr,tc) and move.is_rook(pos_sq), move.knight_legal(r,c, tr,tc) and move.is_knight(pos_sq),move.queen_legal(r,c, tr,tc) and move.is_queen(pos_sq),move.king_legal(r,c, tr,tc) and move.is_king(pos_sq)]

   for x in legal_move:
    if(x):
     k_r,k_c=move.index_my_king(r,c)

     if(not move.is_checkmated(k_r,k_c) or not move.is_stalemate(k_r,k_c)):
      if((move.is_checked(k_r,k_c) and (tr,tc) in move.attack_or_blocking_pieces) or (move.is_checked(k_r,k_c) and (tr,tc) in move.king_escape ) or not move.is_checked(k_r,k_c)):
       if(move.is_king(r,c) and move.is_rook(move.unparse_move(tr,tc)) and not move.is_checked(k_r,k_c) and not move.can_be_checked(r,c,tr,tc) ):
        k_dy,r_dy=(2,-1) if(tc>c) else(-2,1)
        real_board[r][c+k_dy]=real_board[r][c]
        real_board[r][c+k_dy+r_dy]=board[tr][tc]
        real_board[r][c]='.'
        real_board[tr][tc]='.'
        move.update_place(r,c,r,c+k_dy)
        move.update_place(tr,tc,r,c+k_dy+r_dy)
        return True
       elif(move.is_pawn(move.unparse_move(r,c)) and move.is_white(move.unparse_move(r,c)) and tr==r-1 and(move.is_pawn(move.unparse_move(tr+1,tc)) and not move.is_friend(r,c,tr+1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr+1,tc) and move.moves_log["from"][-1][0]==1 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc-1):
        real_board[tr][tc]=real_board[r][c]
        real_board[tr+1][tc]='.'
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)
        return True
       elif(move.is_pawn(move.unparse_move(r,c)) and move.is_white(move.unparse_move(r,c)) and tr==r-1 and(move.is_pawn(move.unparse_move(tr+1,tc)) and not move.is_friend(r,c,tr+1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr+1,tc) and move.moves_log["from"][-1][0]==1 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc+1):
        real_board[tr][tc]=real_board[r][c]
        real_board[tr+1][tc]='.'
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)
        return True
       elif(move.is_pawn(move.unparse_move(r,c)) and move.is_black(move.unparse_move(r,c)) and tr==r+1 and (move.is_pawn(move.unparse_move(tr-1,tc)) and not move.is_friend(r,c,tr-1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr-1,tc) and move.moves_log["from"][-1][0]==6 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc+1):
        real_board[tr][tc]=real_board[r][c]
        real_board[tr-1][tc]='.'
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)
        return True
       elif(move.is_pawn(move.unparse_move(r,c)) and move.is_black(move.unparse_move(r,c)) and tr==r+1 and(move.is_pawn(move.unparse_move(tr-1,tc)) and not move.is_friend(r,c,tr-1,tc)) and move.is_empty2(tr,tc) and move.moves_log["to"][-1]==(tr-1,tc) and move.moves_log["from"][-1][0]==6 and abs(move.moves_log["from"][-1][0]-move.moves_log["to"][-1][0])==2 and c==tc-1):
        real_board[tr][tc]=real_board[r][c]
        real_board[tr-1][tc]='.'
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)
        return True
       else:
        real_board[tr][tc]=real_board[r][c]
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)
        pivot=None
        # pawn_choices=['b','k','q','r']
        if(move.is_pawn(move.unparse_move(r,c)) and move.is_board_end(r,c)):
          if(to_promote in (1,2,3,4)):
            pivot=move.pawn_choices[to_promote-1]
            real_board[tr][tc]= pivot.lower() if(move.is_black) else pivot.upper()
            color= 'black' if(move.is_black) else'white'
            idx=move.positions[color]['pawns'].index(r,c)
            del move.positions[color][idx]
          else:
            return False
        return True
     else:
        print("can't move there")
        return False
   print('game ended')
   return False
     #designed for castling
 def reset_board(board):
  board=real_board.copy()
 def can_be_checked(k_r,k_c,r,c):
  saved_board = [row[:] for row in real_board]
  color = 'black' if move.is_black(move.unparse_move(k_r,k_c)) else 'white'

  if(move.is_rook(move.unparse_move(r,c))): 
      k_dy,r_dy=(2,-1) if(c>k_c) else(-2,1)
      saved_checkers = move.king_checkers[color][:]
      real_board[k_r][k_c+k_dy]=real_board[k_r][k_c]
      real_board[k_r][k_c+k_dy+r_dy]=real_board[r][c]
      real_board[k_r][k_c]='.'
      real_board[r][c]='.'
      checked = move.is_checked(k_r,k_c+k_dy)
  else:
   real_board[k_r][k_c]=real_board[r][c]
   real_board[r][c]='.'
   checked = move.is_checked(k_r,k_c)
  for i in range(8):
    real_board[i][:] = saved_board[i]
  move.king_checkers[color] = saved_checkers

  return checked
    
def print_board(board):
    for row in board:
        print(' '.join(row))

def game_loop():
  white_turn=True
  while(True):
   print_board(real_board)
   while(white_turn):
    print("White turn")
    while(True):
     pos=input("Enter position square")
     if(move.is_black(pos)):
      print("enter white position!")
      continue
     if(move.is_empty(pos)):
       print("empty")
       continue   
     target=input("Enter target square")
     if(move.is_friend(*move.parse_move(pos),*move.parse_move(target))):
       print("cant do that to friend!")
       continue
     
     if(move.is_pawn(pos) and move.is_board_end(move.parse_move(pos),move.parse_move(target))):
      promotion=input("enter your promotion:[1:'bishop','knight','queen','rook]")
     if move.move_piece(pos,target,promotion):
       break
     else:
       print("enter legal moves!")
       continue 
    print_board(real_board)
    white_turn=False
   while(not white_turn):
    print("Black turn")
    while True:    
      pos=input("Enter position square")
      if(move.is_white(pos)):
           print("enter black pos!")
           continue
      if(move.is_empty(pos)):
              print("empty")
              continue
      target=input("Enter target square")
      if(move.is_black(target)):
           print("cant do that to friend!")
           continue
     
      if(move.move_piece(pos,target)):
        break
      else:
        print("enter legal move")
        continue
    print_board(real_board)
    white_turn=True


# testing here
game_loop()
