
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
 def is_legal(pos_square):
  if(move.is_pawn(pos_square)):
   pass

  """
 def rook_legal(parsed_square,target_pos):
 pos_r,pos_c=move.parse_move(pos_sq)
 target_r,target_c=move.parse_move(target_sq)
 for i in range (8):
  if(not move.board[i][pos_c]
"""
 def is_friend(pos_r,pos_c,target_r,target_c):
  if(move.is_black(move.unparse_move(pos_r,pos_c)) and move.is_black(move.unparse_move(target_r,target_c))):
   return True
  elif(move.is_white(move.unparse_move(pos_r,pos_c)) and move.is_white(move.unparse_move(target_r,target_c))):
      return True
  else:
   return False

 def rook_legal(pos_r,pos_c,target_r,target_c):
    rook_dir=[(1,0)(-1,0),(0,1),(0,-1)] 
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
  queen_sliding_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0)(-1,0),(0,1),(0,-1)] 
  (dx,dy)=(0,0)

  if(abs(pos_r-target_r)==abs(target_c-pos_c)):
    if(target_c<pos_c and target_r<pos_r):
     dy,dx=queen_sliding_dirs[3]
    elif(target_c<pos_c  and target_r>pos_r):
     dy,dx=queen_sliding_dirs[2]
    elif(target_c>pos_c  and target_r>pos_r):
     dy,dx=queen_sliding_dirs[0]
    elif(target_c>pos_c  and target_r>pos_r):
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
  board[newpos_r][newpos_c]="k"if(move.is_black(move.unparse_move(newpos_r,newpos_c))) else "K" 
  return True
 def king_legal(pos_r,pos_c,target_r,target_c):
    king_dirs=[(1,1),(1,-1),(-1,1),(-1,-1),(1,0)(-1,0),(0,1),(0,-1)] 
    (dx,dy)=(0,0)
    if(abs(pos_r-target_r)==abs(target_c-pos_c)):
      if(target_c<pos_c and target_r<pos_r):
       dy,dx=king_dirs[3]
      elif(target_c<pos_c  and target_r>pos_r):
       dy,dx=king_dirs[2]
      elif(target_c>pos_c  and target_r>pos_r):
       dy,dx=king_dirs[0]
      elif(target_c>pos_c  and target_r>pos_r):
         dy,dx=king_dirs[1]
      else:
        return
      if (target_c == pos_c and target_r > pos_r):
       dy,dx=king_dirs[-4]
      elif (target_c == pos_c and target_r < pos_r):
       dy,dx=king_dirs[-3]
      elif (target_r == pos_r and target_c > pos_c):
       dy,dx=king_dirs[-2]
      elif (target_r == pos_r and target_c < pos_c):
       dy,dx=king_dirs[-1]
      else:
       return
      newpos_r=pos_r+dx
      newpos_c=pos_c+dy
    if(move.is_empty2(newpos_r,newpos_c) or not move.is_friend(newpos_r,newpos_c,pos_r,pos_c)):  
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
  pawn_dirs=[(1,0),(1,1),(1,-1),(2,0)]
  pawn_dirs_negated=[(-dx, -dy) for dx, dy in pawn_dirs]
  (dx,dy)=(0,0)
  is_black=move.is_black(move.unparse_move(pos_r,pos_c))
  is_white=not is_black
  if(pos_c==target_c and pos_r==target_r+1 and move.is_empty2(target_r,target_c) and is_white):
    dx,dy=pawn_dirs[0]
  elif(pos_c==target_c and pos_r==target_r-1 and move.is_empty2(target_r,target_c) and is_black):
    dx,dy=pawn_dirs_negated[0]
  elif(pos_c==target_c and pos_r==target_r+2 and move.is_empty2(target_r,target_c) and  move.is_empty2(pos_r+1,pos_c) and pos_r==1 and is_white):
     dx,dy=pawn_dirs[-1]
  elif(pos_c==target_c and pos_r==target_r-2 and move.is_empty2(target_r,target_c) and  move.is_empty2(pos_r-1,pos_c) and pos_r==6 and is_black):
     dx,dy=pawn_dirs_negated[-1]
  elif(pos_c==target_c-1 and pos_r==target_r+1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_white):
        dx,dy=pawn_dirs[1]

  elif(pos_c==target_c+1 and pos_r==target_r+1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_black):
        dx,dy=pawn_dirs_negated[1] 
  elif(pos_c==target_c-1 and pos_r==target_r-1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_white):
          dx,dy=pawn_dirs[2]
  
  elif(pos_c==target_c+1 and pos_r==target_r-1 and not move.is_empty2(target_r,target_c) and not move.is_friend(pos_r,pos_c,target_r,target_c) and is_black):
          dx,dy=pawn_dirs_negated[2]       
  else:
     print("cant go there")
     return False
  pos_r=pos_r+dx
  pos_c=pos_c+dy
  
  board[newpos_r][newpos_c]= "p"if(move.is_black(move.unparse_move(pos_r,pos_c))) else"P"
  board[pos_r][pos_c]='.'
  return True
    
     
 def index_my_king(my_r,my_c):
  (k_r,k_c)=0,0
  pos_sq=move.unparse_move(my_r,my_c)
  letter_config="k"if move.is_black(pos_sq) else "K"
  for r in range (8):
   for c in range (8):
     if (real_board[r][c]==letter_config):
       (k_r,k_c)=(r,c)
       return k_r,k_c
    
 king_checked_by=(0,0)
 def is_checked(k_r,k_c):
  for r in range (8):
   for c in range(8):
    if(r,c)!=(k_r,k_c):
     if((move.bishop_legal(r,c,k_r,k_c) or move.pawn_legal(r,c,k_r,k_c) or move.rook_legal(r,c,k_r,k_c) or move.queen_legal(r,c,k_r,k_c) or move.king_legal(r,c,k_r,k_c) ) and not move.is_friend(k_r,k_c,r,c)):
      move.king_checked_by[0]=r
      move.king_checked_by[1]=c
      return True       
  return False
 # we need to identify 1.whether a king is under attack 2. if the king can be saved through a friends move(capture the threat , or block the threat) 3. king has no way to move
 # to make friend block we have to identify which r,c is the checker on relative to kings place
 def friend_block(k_r,k_c):
  (e_r,e_c)=(move.king_checked_by[0],move.king_checked_by[1])
 def friend_attack(k_r,k_c):
   (e_r,e_c)=(move.king_checked_by[0],move.king_checked_by[1])
   for r in range (8):
    for c in range(8):
     if(move.is_friend(r,c,k_r,k_c)):
      if((move.bishop_legal(r,c,e_r,e_c) or move.pawn_legal(r,c,e_r,e_c) or move.rook_legal(r,c,e_r,e_c) or move.queen_legal(r,c,e_r,e_c) or move.king_legal(r,c,e_r,e_c) )):
       return True
   return False  

 def generate_king_possible_moves(k_r,k_c):
   legal_move_count=0
   for r in range(8):
    for c in range(8):
     if(r,c)!=(k_r,k_c) :
      if(move.king_legal(k_r,k_c,r,c) and not move.is_checked(k_r,k_c)):
        legal_move_count+=1
   return legal_move_count
 def is_check_mate(k_r,k_c):
   if(move.is_checked(k_r,k_c) and (move.generate_king_possible_moves(k_r,k_c)==0)):
     return True
   else:
     return False
   
   if move.is_checked(k_r,k_c):
     

 def move_piece(real_board,pos_sq,target_sq):
  pos=move.parse_move(pos_sq)
  r,c=pos
  if(not move.is_empty2(r,c) and pos_sq!=target_sq):
   target=move.parse_move(target_sq)
   tr,tc=target
   legal_move=[move.is_pawn(pos_sq) and move.pawn_legal(r,c, tr,tc),move.is_bishop(pos_sq) and move.bishop_legal(r,c, tr,tc), move.rook_legal(r,c, tr,tc) and move.is_rook(pos_sq), move.knight_legal(r,c, tr,tc) and move.is_knight(pos_sq),move.queen_legal(r,c, tr,tc) and move.queen_legal(pos_sq),move.king_legal(r,c, tr,tc) and move.is_king(pos_sq)]

   for x in legal_move:
    if(x):
     k_r,k_c=move.index_my_king(real_board,r,c)
     if(move.is_checked(real_board,k_r,k_c)):
      real_board[tr][tc]=real_board[pos]
      real_board[tr][tc]='.'
 
  
      
def print_board(board):
    for row in board:
        print(' '.join(row))


# testing here
#print(move.is_white('a1'))
c=move.unparse_move(5,5)
print(move.is_black(move.unparse_move(5,5)))
print(move.is_friend(7,0,6,0))

print(move.is_empty2(6,0))
move.bishop_legal(7,2,6,1)


print_board(board)
