
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

#legal_dir={["p","P"]:(1,0),["r","R"]:[ (1,0),(-1,0),(0,1),(0,-1)],["b","B"]:[(1,1),(1,-1),(-1,1),(-1,-1)],["n","N"]:(()) }

class move:
 def parse_move(square):
  file='abcdefgh'
  col_letter=square[0]
  row_no=8-int(square[1])
  col=file.index(col_letter)
  return row_no,col
 def unparse_move(pos_r,pos_c):
  file=['a','b','c','d','e','f','g','h']
  
  col_letter=file[pos_c]
  col_letter
  row_no_str=(str(pos_r+8))
  square=col_letter+(row_no_str)
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
 """ def is_empty(r,c):
    square=board[r][c]
    return is_empty(square)"""
 def is_white(square):
  r,c=move.parse_move(square)
  if(move.is_empty(square)):
   return f'{square} is empty'
  return board[r][c].isupper()
 def is_black(square):
  r,c=move.parse_move(square)
  if(move.is_empty(square)):
   return f'{square} is empty'
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
  if(move.is_black(move.unparse_move(pos_r,pos_c)) and move.is_black(move.unparse_move(target_c,target_r))):
   return True
  elif(move.is_white(move.unparse_move(pos_r,pos_c)) and move.is_white(move.unparse_move(target_c,target_r))):
      return True
  else:
   return False
 def rook_legal(pos_r,pos_c,target_r,target_c):
  if (target_c==pos_c and target_r>pos_r):
   for i in range (pos_r+1,target_r+1,1):
    if( move.is_empty(i,target_c)and not move.is_friend(i-1,pos_c,i,pos_c)):
     board[i][pos_c]= "R"if(move.is_black(move.unparse_move(pos_r,pos_c,target_r,target_c))) else "r"
     board[i-1][pos_c]='.'
  elif(target_c==pos_c and target_r<pos_r):
   for i in range(pos_r-1, target_r, -1):
    if( move.is_empty(i,target_c)and (not move.is_friend(i+1,pos_c,i,pos_c))):
     board[i][pos_c]= "R"if(move.is_black(move.unparse_move(pos_r,pos_c,target_r,target_c))) else "r"
    board[i+1][pos_c]='.'
  elif(target_r==pos_r and target_c>pos_c):
    for i in range (pos_c+1,target_c+1,1):
       if( move.is_empty(target_r,i) and (not move.is_friend(pos_r,i-1,pos_r,i))):
        board[pos_r][i]= "R"if(move.is_black(move.unparse_move(pos_r,pos_c,target_r,target_c))) else "r"
        board[pos_r][i-1]='.'
  elif(target_r==pos_r and target_c<pos_c):
      for i in range (pos_c-1,target_c,-1):
       if( move.is_empty(target_r,i) and (not move.is_friend(pos_r,i+1,pos_r,i))):
        board[pos_r][i]= "R"if(move.is_black(move.unparse_move(pos_r,pos_c,target_r,target_c))) else "r"
        board[pos_r][i+1]='.'
  else:
   print('illegal move for rook')   

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
move.move_piece('a1', 'a2')
print(move.is_empty('a2'))
print(move.is_rook('a2'))
x=move.unparse_move(0,0)
print(type(x))
print_board(board)
