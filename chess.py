
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
        "queen": (7, 3),
        "rooks": [(7, 0), (7, 7)],
        "bishops": [(7, 2), (7, 5)],
        "knights": [(7, 1), (7, 6)],
        "pawns": [(6, c) for c in range(8)]
    },

    # Black pieces
    "black": {
        "king": (0, 4),
        "queen": (0, 3),
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
     dy,dx=rook_dir[-4]
    elif (target_c == pos_c and target_r < pos_r):
      dy,dx=rook_dir[-3]
    elif (target_r == pos_r and target_c > pos_c):
      dy,dx=rook_dir[-2]    
    elif (target_r == pos_r and target_c < pos_c):
      dy,dx=rook_dir[-1]
    else:
      return False
  
    for_limit=0
  
  
    if(target_c == pos_c):
      for_limit=abs(target_c-pos_c)
    else:
      for_limit=abs(target_r-pos_r)
    for i in range(for_limit):
      newpos_r=pos_r+dx
      newpos_c=pos_c+dy
      if(move.is_empty2(newpos_r,newpos_c,)):  
       pos_r=newpos_r
       pos_c=newpos_c
       return True
      if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
       pos_r=newpos_r
       pos_c=newpos_c
       break
      else:
       print('cant attack friend!')
       return  False  
    board[newpos_r][newpos_c]="r"if(move.is_black(move.unparse_move(newpos_r,newpos_c))) else "R" 
    return True
   
  
 """def rook_legal(pos_r,pos_c,target_r,target_c):
  color_mapping=move.is_black(move.unparse_move(pos_r,pos_c))
  rook_dir=[(1,0)(-1,0),(0,1),(0,-1)] 
  if (target_c==pos_c and target_r>pos_r):
   for i in range (pos_r+1,target_r+1,1):
    if( move.is_empty2(i,target_c)):
     board[i][pos_c]= "r"if(color_mapping) else "R"
     board[i-1][pos_c]='.'
    elif (not move.is_friend(i-1,pos_c,i,pos_c)):
     board[i][pos_c]= "r"if(color_mapping) else "R"
     board[i-1][pos_c]='.'
     break
    else:
     break
  elif(target_c==pos_c and target_r<pos_r):
   for i in range(pos_r-1, target_r-1, -1):
    if( move.is_empty2(i,target_c) ):
     board[i][pos_c]= "r"if(color_mapping) else "R"
     board[i+1][pos_c]='.'
    elif (not move.is_friend(i+1,pos_c,i,pos_c)):
        board[i][pos_c]= "r"if(color_mapping) else "R"
        board[i+1][pos_c]='.'
        break
    else:
     break
  elif(target_r==pos_r and target_c>pos_c):
    for i in range (pos_c+1,target_c+1,1):
       if( move.is_empty2(target_r,i)):
        board[pos_r][i]= "r"if(color_mapping) else "R"
        board[pos_r][i-1]='.'
       elif (not move.is_friend(pos_r,i-1,pos_r,i)):
          board[pos_r][i]= "r"if(color_mapping) else "R"
          board[pos_r][i-1]='.'
          break
       else:
         break
  elif(target_r==pos_r and target_c<pos_c):
      for i in range (pos_c-1,target_c-1,-1):
       if( move.is_empty2(target_r,i) ):
         board[pos_r][i]= "r"if(color_mapping) else "R"
         board[pos_r][i+1]='.' 
       elif (not move.is_friend(pos_r,i+1,pos_r,i)):
        board[pos_r][i]= "r"if(color_mapping) else "R"
        board[pos_r][i+1]='.' 
        break
       else:
        break
  else:
   print('wrong move for rook')"""
# 2 up (row-2)1 right(col+1) ,2 up(row-2) 1 left(col-1),2 down(row+2) 1right(col+1),2 down 1 left(col-1),2right(col+2) 1 down(row+1),2right(col+2) 1 up(row-1),2left(col-2) 1 down(row+1),2left (col-2) 1 up (row-1)
 """def knight_legal(pos_r,pos_c,target_r,target_c): 
  #legal_movements=[istopright,istopleft,isdownright,isdownleft,isrightdown,isrightup,isleftdown,isleftup]
   if( move.is_empty2(target_r,target_c) or not move.is_friend(pos_r,pos_c,target_r,target_c)):
    if(target_r,target_c)==(pos_r-2,pos_c+1):
       board[target_r][target_c]=board[pos_r][pos_c] 
       board[pos_r][pos_c] ='.'
    elif (target_r,target_c)==(pos_r,pos_c):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    elif (target_r,target_c)==(pos_r+2,pos_c+1):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    elif (target_r,target_c)==(pos_r+2,pos_c-1):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    elif (target_r,target_c)==(pos_r,pos_c):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    elif (target_r,target_c)==(pos_r-1,pos_c+2):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    elif (target_r,target_c)==(pos_r+1,pos_c-2):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    elif (target_r,target_c)==(pos_r-1,pos_c-2):
       board[target_r][target_c]=board[pos_r][pos_c]
       board[pos_r][pos_c]='.'
    else:
        print('illegal move for knight')

   else:
    print('cant attack friend!') """


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
   
 def bishop_legal(pos_r,pos_c,target_r,target_c)  :
  bish_silding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1)]  
  (dx,dy)=(0,0)
  emptyr,emptyc=pos_r,pos_c
  #check diagonal
  if(abs(pos_r-target_r)==abs(target_c-pos_c)):
   if(target_c<pos_c and target_r<pos_r):
    dy,dx=bish_silding_dirs[3]
   elif(target_c<pos_c  and target_r>pos_r):
    dy,dx=bish_silding_dirs[2]
   elif(target_c>pos_c  and target_r>pos_r):
    dy,dx=bish_silding_dirs[0]
   elif(target_c>pos_c  and target_r>pos_r):
      dy,dx=bish_silding_dirs[1]
   else:
    print("wrong move for bishop ") 

    #must find number of tiles in digonal from a point to point =col-row
  for i in range(abs(pos_c-target_c)+1):
    newpos_r=pos_r+dx
    newpos_c=pos_c+dy
    if(move.is_empty2(newpos_r,newpos_c,)):  
        pos_r=newpos_r
        pos_c=newpos_c
    if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
      pos_r=newpos_r
      pos_c=newpos_c
      break
    else:
      print('cant attack friend!')
      return False
  board[pos_r][pos_c]="b"if(move.is_black(move.unparse_move(pos_r,pos_c))) else "B"   
  board[emptyr][emptyc]='.'
  return True
    
 def queen_legal(pos_r,pos_c,target_r,target_c):
  queen_sliding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
  (dx,dy)=(0,0)

  if(abs(pos_r-target_r)==abs(target_c-pos_c)):
    if(target_c<pos_c and target_r<pos_r):
     dy,dx=queen_sliding_dirs[3]
    elif(target_c<pos_c  and target_r>pos_r):
     dy,dx=queen_sliding_dirs[2]
    elif(target_c>pos_c  and target_r>pos_r):
     dy,dx=queen_sliding_dirs[0]
    elif(target_c>pos_c  and target_r<pos_r):
       dy,dx=queen_sliding_dirs[1]
    else:
      return False
    for i in range(abs(pos_c-target_c)+1):
        newpos_r=pos_r+dx
        newpos_c=pos_c+dy
        if(move.is_empty2(newpos_r,newpos_c,)):  
            pos_r=newpos_r
            pos_c=newpos_c
        if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
          pos_r=newpos_r
          pos_c=newpos_c
          break
        else:
          print('cant attack friend!')
          return False
      
  elif (target_c == pos_c and target_r > pos_r):
     dy,dx=queen_sliding_dirs[-4]
  elif (target_c == pos_c and target_r < pos_r):
    dy,dx=queen_sliding_dirs[-3]
  elif (target_r == pos_r and target_c > pos_c):
    dy,dx=queen_sliding_dirs[-2]    
  elif (target_r == pos_r and target_c < pos_c):
    dy,dx=queen_sliding_dirs[-1]
  else:
     return False

  for_limit=0


  if(target_r == pos_r):
    for_limit=abs(target_c-pos_c)
  else:
    for_limit=abs(target_r-pos_r)
  for i in range(for_limit):
    newpos_r=pos_r+dx
    newpos_c=pos_c+dy
    if(move.is_empty2(newpos_r,newpos_c,)):  
     pos_r=newpos_r
     pos_c=newpos_c
     return True
    if(not move.is_friend(pos_r,pos_c,newpos_r,newpos_c)):
     pos_r=newpos_r
     pos_c=newpos_c
     break
    else:
     print('cant attack friend!')
     return  False  
  board[newpos_r][newpos_c]="k"if(move.is_black(move.unparse_move(newpos_r,newpos_c))) else "K" 
  return True
 def king_legal(pos_r,pos_c,target_r,target_c):
    king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)] 
    (dx,dy)=(0,0)
    if(abs(pos_r-target_r)==abs(target_c-pos_c)):
      if(target_c<pos_c and target_r<pos_r):
       dx,dy=king_dirs[3]
      elif(target_c<pos_c  and target_r>pos_r):
       dx,dy=king_dirs[2]
      elif(target_c>pos_c  and target_r>pos_r):
       dx,dy=king_dirs[0]
      elif(target_c>pos_c  and target_r>pos_r):
       dx,dy=king_dirs[1]
      else:
        return
      if (target_c == pos_c and target_r > pos_r):
       dx,dy=king_dirs[-4]
      elif (target_c == pos_c and target_r < pos_r):
       dx,dy=king_dirs[-3]
      elif (target_r == pos_r and target_c > pos_c):
       dx,dy=king_dirs[-2]
      elif (target_r == pos_r and target_c < pos_c):
       dx,dy=king_dirs[-1]

       ###nigga rook here
      elif (target_r == pos_r and target_c >pos_c and move.is_rook(move.unparse_move(target_r,target_c)) and move.is_empty2(pos_r,pos_c+1) and  move.is_empty2(pos_r,pos_c+2) and not move.is_checked(pos_r,pos_c)):
       dx,dy=None
      elif (target_r == pos_r and target_c < pos_c and move.is_rook(move.unparse_move(target_r,target_c)) and move.is_empty2(pos_r,pos_c-1) and  move.is_empty2(pos_r,pos_c-2) and not move.is_checked(pos_r,pos_c)):
       dx,dy=None
      else:
       return
      newpos_r=pos_r+dx
      newpos_c=pos_c+dy
    if((move.is_empty2(newpos_r,newpos_c) or not move.is_friend(newpos_r,newpos_c,pos_r,pos_c) ) and not move.is_king(move.unparse_move(pos_r+dx,pos_c+dy))):  
       pos_r=newpos_r
       pos_c=newpos_c 
       board[newpos_r][newpos_c]="k"if(move.is_black(move.unparse_move(newpos_r,newpos_c))) else "K" 
       return True  
    else:
       print('cant attack friend!')
       return True
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
  
  board[newpos_r][newpos_c]= "p"if(move.is_black(move.unparse_move(pos_r,pos_c))) else"P"
  board[pos_r][pos_c]='.'
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
  for piece,position in move.positions[enemy_color].items():
    if piece=='queen' or piece=='king':
     r,c=position
     if(piece=='queen'):
      if(move.queen_legal(r,c,k_r,k_c)):
       move.king_checkers[color].append((piece,r,c))
     elif(piece=='king'):
       if(move.king_legal(r,c,k_r,k_c)): 
        move.king_checkers[color].append((piece,r,c))
       
    else:
      for r,c in position:
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
        if(len(move.king_checkers)>0):
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
             return False
           b_r,b_c=k_r,k_c
           for i in range(abs(k_c-ec)):  
             b_r+=dx
             b_c+=dy    
             block_sqrs.append((b_r,b_c))
           
          elif (ec == k_c and er > k_r):
            dy,dx=queen_sliding_dirs[-4]
          elif (ec == k_c and er < k_r):
           dy,dx=queen_sliding_dirs[-3]
          elif (er == k_r and ec > k_c):
           dy,dx=queen_sliding_dirs[-2]    
          elif (er == k_c and ec < k_c):
           dy,dx=queen_sliding_dirs[-1]
          else:
            return False
       
       for_limit=0
       
       
       if(ec == k_c):
           for_limit=abs(er-k_r)
       else:
           for_limit=abs(k_c-ec)
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
               return 
           
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
  if(len(move.king_checkers[king_color]>1)):
    return False
  rook_blocks_coor=move.rook_blocks(k_r,k_c)
  queen_blocks_coor=move.queen_blocks(k_r,k_c)
  bishop_blocks_coor=move.bishop_blocks(k_r,k_c)
  block_sqrs=[*queen_blocks_coor,*bishop_blocks_coor,*rook_blocks_coor]
  for piece,position in move.positions[king_color].items():
      for r,c in block_sqrs:
          if piece=='queen':
           fr,fc=position
           if(piece=='queen'):
            if(move.queen_legal(fr,fc,r,c)):
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

              elif(piece=='knight'):
                if(move.knight_legal(fr,fc,r,c)):
                      move.attack_or_blocking_pieces.append((fr,fc))
                      return True

              elif(piece=='bishop'):
                if(move.bishop_legal(fr,fc,r,c)):
                        move.attack_or_blocking_pieces.append((fr,fc))
                        return True
  return False
 def friend_attack(k_r,k_c):
  king_color='white' if move.is_white(move.unparse_move(k_r,k_c)) else 'black'
  
  for piece,position in move.positions[king_color]:
    for e_piece,r,c in move.king_checkers[king_color]:
     if piece=='queen' or piece=='king':
      fr,fc=position
      if(piece=='queen'):
       if(move.queen_legal(fr,fc,r,c)):
        move.attack_or_blocking_pieces.append((fr,fc)) 
        return True
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
     
       elif(piece=='knight'):
        if(move.knight_legal(fr,fc,r,c)):
          move.attack_or_blocking_pieces.append((fr,fc))
          return True
     
       elif(piece=='bishop'):
        if(move.bishop_legal(fr,fc,r,c)):
         move.attack_or_blocking_pieces.append((fr,fc))
         return True
  return False
  
 moves_log= {
     "from":[]
     ,"to":[]
     }
 def update_place(old_r,old_c,r,c):
   old_sq=move.unparse_move(old_r,old_c)
   color='white'if(move.is_white(old_sq)) else 'black'
   is_pieces={"king":move.is_king(old_sq),"bishops":move.is_bishop(old_sq),"knights":move.is_knight(old_sq),"queen":move.is_queen(old_sq),"pawns":move.is_pawn(old_sq)}
   piece=None
   for key,value in is_pieces.items():
    if(value):
     piece=key
     if(piece=='rooks' or piece=='bishops' or piece=='knights' or piece=='pawns'):
      idx=move.positions[color][piece].index((old_r,old_c))
      move.positions[color][piece][idx]=(r,c)
      
     else:
      move.positions[color][piece]=(r,c)
    move.moves_log["from"].append((old_r,old_c))
    move.moves_log["to"].append((r,c))
     
 def is_checkmated(k_r,k_c):
  king_color="white"if(move.is_white(move.unparse_move(k_r,k_c))) else "black"
  if(len(move.king_checkers[king_color])>1):
    return not move.can_king_escape(k_r,k_c)
  if(move.friend_attack(k_r,k_c) or move.can_friend_block(k_r,k_c) or move.can_king_escape(k_r,k_c)):
    return True
# castling/enpassent
 def is_board_end(row):
  return row==0 or row==7
 # for enpassent ,we need to have list of moves that works like a log , and we need to have an if condition that checks if moving pawn two pieces forward is right through invoking the log list and see if column of target square has a pawn move that moved two steps forward and capture if found  
 
 def move_piece(pos_sq,target_sq):
  pos=move.parse_move(pos_sq)
  r,c=pos
  if(not move.is_empty2(r,c) and pos_sq!=target_sq and not move.is_king(target_sq)):
   target=move.parse_move(target_sq)
   tr,tc=target
   legal_move=[move.is_pawn(pos_sq) and move.pawn_legal(r,c, tr,tc),move.is_bishop(pos_sq) and move.bishop_legal(r,c, tr,tc), move.rook_legal(r,c, tr,tc) and move.is_rook(pos_sq), move.knight_legal(r,c, tr,tc) and move.is_knight(pos_sq),move.queen_legal(r,c, tr,tc) and move.queen_legal(pos_sq),move.king_legal(r,c, tr,tc) and move.is_king(pos_sq)]

   for x in legal_move:
    if(x):
     k_r,k_c=move.index_my_king(r,c)
     
    if(not move.is_checkmated(k_r,k_c)):
     if((move.is_checked(k_r,k_c) and (tr,tc) in move.attack_or_blocking_pieces) or (move.is_checked(k_r,k_c) and (tr,tc) in move.king_escape ) or not move.is_checked(k_r,k_c)):
      if(move.is_queen(r,c) and move.is_rook(move.unparse_move(tr,tc))):
        k_dy,r_dy=(2,-1) if(tc>c) else(-2,1)
        real_board[r][c+k_dy]=real_board[r][c]
        real_board[r][c+k_dy+r_dy]=board[tr][tc]
        real_board[r][c]='.'
        real_board[tr][tc]='.' 
        move.update_place(r,c,r,c+k_dy)
        move.update_place(tr,tc,r,c+k_dy+r_dy)
      elif(move.is_pawn(move.unparse_move(r,c)) and move.is_white(move.unparse_move(r,c)) and(move.is_pawn(move.unparse_move(tr-1,tc-1)) and not move.is_friend(r,c,tr-1,tc-1)) and move.is_empty2(tr,tc) and abs(move.moves_log["from"][-1][1]-move.moves_log["to"][-1][1]== 2)):
       real_board[tr][tc]=real_board[r][c]
       real_board[tr-1][tc-1]='.'
       real_board[r][c]='.'
       move.update_place(r,c,tr,tc)

       move.update_place(r,c,tr,tc)
      elif(move.is_pawn(move.unparse_move(r,c)) and move.is_white(move.unparse_move(r,c)) and(move.is_pawn(move.unparse_move(tr-1,tc+1)) and not move.is_friend(r,c,tr-1,tc-1)) and move.is_empty2(tr,tc)  and abs(move.moves_log["from"][-1][1]-move.moves_log["to"][-1][1]== 2)):
        real_board[tr][tc]=real_board[r][c]
        real_board[tr-1][tc+1]='.'
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)

      elif(move.is_pawn(move.unparse_move(r,c)) and move.is_black(move.unparse_move(r,c)) and (move.is_pawn(move.unparse_move(tr+1,tc-1)) and not move.is_friend(r,c,tr-1,tc-1)) and move.is_empty2(tr,tc) and abs(move.moves_log["from"][-1][1]-move.moves_log["to"][-1][1]== 2)):
       real_board[tr][tc]=real_board[r][c]
       real_board[tr+1][tc-1]='.'
       real_board[r][c]='.'
       move.update_place(r,c,tr,tc)

      elif(move.is_pawn(move.unparse_move(r,c)) and move.is_black(move.unparse_move(r,c)) and(move.is_pawn(move.unparse_move(tr+1,tc+1)) and not move.is_friend(r,c,tr-1,tc-1)) and move.is_empty2(tr,tc) and abs(move.moves_log["from"][-1][1]-move.moves_log["to"][-1][1]== 2)):
        real_board[tr][tc]=real_board[r][c]
        real_board[tr+1][tc+1]='.'
        real_board[r][c]='.'
        move.update_place(r,c,tr,tc)
  
      else:
       real_board[tr][tc]=real_board[r][c]
       real_board[tr][tc]='.'
      move.update_place(r,c,tr,tc)
     else:
        return
    
    #designed for castling
def reset_board(board):
 board.copy(real_board)
def can_be_checked(k_r,k_c,R_r,R_c):
   k_dy,r_dy=(2,-1) if(R_c>c) else(-2,1)
   board[k_r][k_c+k_dy]=board[k_r][k_c]
   board[k_r][k_c+k_dy+r_dy]=board[R_r][R_c]
   board[k_r][k_c]='.'
   board[R_r][R_c]='.'
   checked=None
   if(move.is_checked(k_r,k_c+k_dy)):
     checked=True
   else :
     checked=False
   reset_board(board)
   return checked
    
def print_board(board):
    for row in board:
        print(' '.join(row))

def game_loop():
  white_turn=True
  while(True):
   print_board(real_board)
   while(white_turn):
    pos=input("Enter position square")
    if(move.is_black(pos)):
     print("enter white position!")
     continue
    
    print("enter target square")
    target=input("Enter position square")
    if(move.is_white(target)):
     print("enter black target!")
     continue
    move.move_piece(pos,target)
    print_board(real_board)
   while(not white_turn):
    print("Enter position square")
    
    pos=input("Enter position square")
    if(move.is_white(pos)):
         print("enter black pos!")
         continue
    print("enter target square")
    target=input("Enter position square")
    if(move.is_black(pos)):
         print("enter white position!")
         continue
    move.move_piece(pos,target)
    print_board(real_board)


# testing here
game_loop()
