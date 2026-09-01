let game_id=null
async function create_game(vsAi) {
  const response = await fetch("/game/new/", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ vs_ai: vsAi })
  });
  const data = await response.json();
  game_id = data['id'];
  board = data['board'];
  localStorage.setItem('game_id', game_id);
  render_board(board);
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

  function parse_move(square){
   file='abcdefgh'
   
   col_letter=square[0]
   row_no=8-Number(square[1])
   col=file.index(col_letter)
   return [row_no,col]}
async function isPromotionMove(pos_r,pos_c, t_r,t_c) {
  // landing on rank 8 (row 0) or rank 1 (row 7)
   response=await fetch(`/game/${game_id}/board`)
   data=await response.json()
   board=data['board']
   if(board[pos_r][pos_c]=='♟'){return t_r === 7}
if(board[pos_r][pos_c]=='♙'){return t_r === 0;}
  else{return false;}
}

function askPromotionChoice() {
  // returns a Promise that resolves to 1/2/3/4, matching pawn_choices = ['b','n','q','r']
  return new Promise((resolve) => {
    const choice = prompt("Promote to: (1) Bishop, (2) Knight, (3) Queen, (4) Rook", "3");
    resolve(Number(choice) || 3); // default to queen if invalid input
  });
}

async function makemove(pos_sq, t_sq, promotion = null) {
    const response = await fetch(`/game/${game_id}/move/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from: pos_sq, to: t_sq, promotion: promotion })
    });
    const data = await response.json();

    if (!response.ok) {
        console.log("Illegal move:", data['error']);
        return;
    }

    render_board(data['board']);
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

square.addEventListener('drop', async (event) => {
  if (pos_r === null || pos_c === null) { return; }
  t_r = Number(event.target.dataset.row);
  t_c = Number(event.target.dataset.col);
  if (t_r === pos_r && t_c === pos_c) { return; }

  const pos_sq = unparse_move(pos_r, pos_c);
  const t_sq = unparse_move(t_r, t_c);

  let promotion = null;
  if (await isPromotionMove(pos_r,pos_c, t_r,t_c)) {
    promotion = await askPromotionChoice();
  }

  makemove(pos_sq, t_sq, promotion);
});
});
}

// ... all your function definitions (create_game, load_game, makemove, render_board) above ...

async function load_game(id) {
  const response = await fetch(`/game/${id}/board/`);
  const data = await response.json();
  game_id = id;
  render_board(data['board']);
}

// This is the part that actually runs when the page loads:
const savedId = localStorage.getItem('game_id');
if (savedId) {
  load_game(savedId);
} else {
  const wantsAi = confirm("Play against the computer? (Cancel = play a friend)");
  create_game(wantsAi);
}