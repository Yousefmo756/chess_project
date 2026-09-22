let game_id=null
let board=null
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
    updateStatusBanner('ongoing', 'white'); // fresh game, always ongoing

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
 function isPromotionMove(pos_r,pos_c, t_r,t_c) {
  // landing on rank 8 (row 0) or rank 1 (row 7)
   //response=await fetch(`/game/${game_id}/board`)
   //data=await response.json()
   //board=data['board']
   if(board[pos_r][pos_c]=='♟'){return t_r === 7}
if(board[pos_r][pos_c]=='♙'){return t_r === 0;}
  else{return false;}
}

function askPromotionChoice() {
  return new Promise((resolve) => {
    const picker = document.getElementById('promotion-picker');
    picker.style.display = 'flex';

    const choices = picker.querySelectorAll('.promo-choice');
    function handleClick(event) {
      const value = Number(event.currentTarget.dataset.value);
      picker.style.display = 'none';
      choices.forEach(c => c.removeEventListener('click', handleClick));
      resolve(value);
    }

    choices.forEach(c => c.addEventListener('click', handleClick));
  });
}

async function makemove(pos_sq, t_sq, promotion = null) {
    const response = await fetch(`/game/${game_id}/move/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from: pos_sq, to: t_sq, promotion })
    });
    const data = await response.json();

    if (!response.ok) {
        console.log("Illegal move:", data['error']);
        return;
    }

    board = data['board'];
    render_board(board);                            // player's move shows immediately
    updateStatusBanner(data['status'], data['turn']);

    if (data['ai_to_move']) {
        const aiRes = await fetch(`/game/${game_id}/ai-move/`, { method: 'POST' });
        const aiData = await aiRes.json();
        board = aiData['board'];
        render_board(board);                         // AI's move shows once it's computed
        updateStatusBanner(aiData['status'], aiData['turn']);
    }
}



function clearHighlights() {
  document.querySelectorAll('.legal').forEach(sq => sq.classList.remove('legal'));
}

function render_board(board) {
  const outer_div = document.querySelector('.chessboard');
  outer_div.innerHTML = '';

  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      const div = document.createElement('div');
      div.className = (i + j) % 2 === 0 ? 'square light' : 'square dark';
      div.dataset.row = i;
      div.dataset.col = j;
      div.innerText = board[i][j] ?? '';
      div.draggable = !!board[i][j];   // only pieces can be dragged
      outer_div.appendChild(div);
    }
  }

  document.querySelectorAll('.square').forEach(square => {

    square.addEventListener('dragstart', async (event) => {
      pos_r = Number(event.currentTarget.dataset.row);
      pos_c = Number(event.currentTarget.dataset.col);

      const res = await fetch(`/game/${game_id}/renderlegal?row=${pos_r}&col=${pos_c}`);
      const data = await res.json();   // assumed: [[r, c], [r, c], ...]
     console.log('legal moves response:', data);   // <-- check this in the console
      // ignore stale response if the drag already ended or changed
      if (pos_r === null) return;

      data.moves.forEach(([r, c]) => {
        const target = document.querySelector(`[data-row="${r}"][data-col="${c}"]`);
          console.log(r, c, target);   // <-- see if target is found

        if (target) {target.classList.add('legal');    console.log(target.outerHTML);   // <-- shows the class list at the moment it's added
}
      });
    });

    square.addEventListener('dragover', (event) => {
      event.preventDefault();   // required, or 'drop' never fires
    });

    square.addEventListener('drop', async (event) => {
      event.preventDefault();
      if (pos_r === null || pos_c === null) return;

      const target = event.currentTarget;
      const t_r = Number(target.dataset.row);
      const t_c = Number(target.dataset.col);
      const isLegal = target.classList.contains('legal');

      clearHighlights();
      if (!isLegal || (t_r === pos_r && t_c === pos_c)) return;

      const pos_sq = unparse_move(pos_r, pos_c);
      const t_sq = unparse_move(t_r, t_c);

      let promotion = null;
      if (isPromotionMove(pos_r, pos_c, t_r, t_c)) {
        promotion = await askPromotionChoice();
      }

      makemove(pos_sq, t_sq, promotion);
    });

    square.addEventListener('dragend', () => {
      clearHighlights();   // covers drops outside the board or on illegal squares
      pos_r = pos_c = null;
    });
  });
}


function updateStatusBanner(status, turn) {
  const banner = document.getElementById('status-banner');

  if (status === 'ongoing') {
    banner.style.display = 'none';
    return;
  }

  banner.style.display = 'block';

  if (status === 'checkmate') {
    const winner = turn === 'white' ? 'Black' : 'White'; // turn is whoever's stuck, so the OTHER side won
    banner.innerText = `Checkmate! ${winner} wins.`;
    banner.className = 'status-banner ended';
  } else if (status === 'stalemate') {
    banner.innerText = 'Stalemate — draw.';
    banner.className = 'status-banner ended';
  } else if (status === 'draw') {
    banner.innerText = 'Draw.';
    banner.className = 'status-banner ended';
  }
}

// ... all your function definitions (create_game, load_game, makemove, render_board) above ...

async function load_game(id) {
  const response = await fetch(`/game/${id}/board/`);
  const data = await response.json();
  game_id = id;
  board=data['board']
  render_board(data['board']);
    updateStatusBanner(data['status'], data['turn']);

}

// This is the part that actually runs when the page loads:
const savedId = localStorage.getItem('game_id');
//const savedId = 42;

if (savedId) {
  load_game(savedId);
} else {
  const wantsAi = confirm("Play against the computer? (Cancel = play a friend)");
  create_game(wantsAi);
}