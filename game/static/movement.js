let game_id=null
async function create_game(){
 response= await fetch("/game/new/",{method:'POST'})
 data= await response.json()
 game_id=data['id']
 board=data['board']
 render_board(board)

}
function unparse_move(pos_r,pos_c){
   file=['a','b','c','d','e','f','g','h']
   file='abcdefgh'
   col_letter=file[pos_c]
   row_no_str=(-pos_r+8)
   square=col_letter+String(row_no_str)
   return square}
pos_r=null
pos_c=null
t_r=null
t_c=null


async function makemove(pos_sq,t_sq){
    response=await fetch (`/game/${game_id}/move/`,{method:'POST',
         headers: { 'Content-Type': 'application/json' },
body:JSON.stringify({from:pos_sq,to:t_sq})

})
data= await response.json()
board=data['board']
render_board(board)
}



function render_board(board){
outer_div=document.querySelector('.chessboard') 
outer_div.innerHTML = ''; // clear old squares first

for(let i=0;i<8;i++){
 for(let j=0;j<8;j++){
 cl_name=((i+j)%2==0)?'square light':'square dark' 
 div=document.createElement('div')
 div.setAttribute('data-row',i)
 div.setAttribute('data-col',j)
 div.setAttribute('draggable','true')

 div.innerText=board[i][j]??''
 div.className=cl_name
 
 outer_div.appendChild(div)
}
}
const squares=document.querySelectorAll('.square')
squares.forEach(square=>{

square.addEventListener('dragstart', (event) => {
  pos_r = Number(event.target.dataset.row);
  pos_c = Number(event.target.dataset.col);
});

square.addEventListener('dragover', (event) => {
  event.preventDefault(); // required, or 'drop' will never fire
});

square.addEventListener('drop', (event) => {
  t_r = Number(event.target.dataset.row);
  t_c = Number(event.target.dataset.col);
  const pos_sq = unparse_move(pos_r, pos_c);
  const t_sq = unparse_move(t_r, t_c);
  makemove(pos_sq, t_sq);
});
});
}

create_game();