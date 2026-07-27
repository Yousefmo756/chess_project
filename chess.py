
board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','.','P','P','P','P','P','P'],
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
  return  board[r][c]in('P','p')
 def is_knight(square):
  r,c=move.parse_move(square)
  return  board[r][c] in ('N','n')
 def is_bishop(square):
  r,c=move.parse_move(square)
  return  board[r][c] in ('B','b')
 def is_rook(square):
  r,c=move.parse_move(square)
  return  board[r][c] in ('R','r')
 def is_queen(square):
  r,c=move.parse_move(square)
  return  board[r][c]in('Q','q')
 def is_king(square):
  r,c=move.parse_move(square)
  return  board[r][c]in('K','k')
 def is_empty(square):
  r,c=move.parse_move(square)
  return board[r][c]=="."
 def is_empty2(r,c):
    square=move.unparse_move(r,c)
    return move.is_empty(square)
 def is_white(square):
  r,c=move.parse_move(square)
  if(move.is_empty(square)):
   return False
  return board[r][c].isupper()
 def is_black(square):
  r,c=move.parse_move(square)
  if(move.is_empty(square)):
   return False
  return board[r][c].islower()
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
  color_mapping=move.is_black(move.unparse_move(pos_r,pos_c))

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
   print('wrong move for rook')
# 2 up (row-2)1 right(col+1) ,2 up(row-2) 1 left(col-1),2 down(row+2) 1right(col+1),2 down 1 left(col-1),2right(col+2) 1 down(row+1),2right(col+2) 1 up(row-1),2left(col-2) 1 down(row+1),2left (col-2) 1 up (row-1)
 def knight_legal(pos_r,pos_c,target_r,target_c): 
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
    print('cant attack friend!') 


   
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
  for i in range(abs(pos_r-target_c)+1):
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
      return
  board[pos_r][pos_c]="b"if(move.is_black(move.unparse_move(pos_r,pos_c))) else "B"   
  board[emptyr][emptyc]='.'

    
  


def move_piece(pos_sq,target_sq):
  
 # if(move.is_pawn(pos_sq) ):
  # pos_r,pos_c=move.parse_move(pos_sq)
 #  target_r,target_c=move.parse_move(target_sq)
 #  board[target_r][target_c]=board[pos_r][pos_c]
  # board[pos_r][pos_c]="."
  pos_r,pos_c=move.parse_move(pos_sq)
  target_r,target_c=move.parse_move(target_sq)  
  if(move.is_rook(pos_sq)):
   return move.rook_legal(pos_r,pos_c,target_r,target_c)
      
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
move.bishop_legal(6,1,6,0)

print_board(board)
