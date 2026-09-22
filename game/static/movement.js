let game_id=null
let board=null
let currentTurn = 'white';   // add near your other global lets
let lastMove = null;   // { from: [r,c], to: [r,c] }
async function create_game(vsAi, difficulty = null) {
  const response = await fetch("/game/new/", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ vs_ai: vsAi, difficulty: difficulty })
  });

  const data = await response.json();
  game_id = data['id'];
  board = data['board'];
  localStorage.setItem('game_id', game_id);
  currentTurn = 'white';
  render_board(board);
  updateStatusBanner('ongoing', 'white');
}

function showSetupModal() {
  document.getElementById('setup-modal').style.display = 'flex';
}
function hideSetupModal() {
  document.getElementById('setup-modal').style.display = 'none';
}

document.querySelectorAll('.setup-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.dataset.mode === 'human') {
      hideSetupModal();
      create_game(false);
    } else {
      document.getElementById('difficulty-row').style.display = 'flex';
    }
  });
});

document.querySelectorAll('.diff-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    hideSetupModal();
    create_game(true, btn.dataset.diff);
  });
});


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
    currentTurn = data['turn'];        // add this
    render_board(board);
    updateStatusBanner(data['status'], data['turn']);

    if (data['ai_to_move']) {
        const thinkingEl = document.getElementById('thinking-indicator');
        setBoardInteractive(false);
        if (thinkingEl) thinkingEl.style.display = 'block';

        const aiRes = await fetch(`/game/${game_id}/ai-move/`, { method: 'POST' });
        const aiData = await aiRes.json();

        if (thinkingEl) thinkingEl.style.display = 'none';
        setBoardInteractive(true);

        board = aiData['board'];
        currentTurn = aiData['turn'];   // add this
        render_board(board);
        updateStatusBanner(aiData['status'], aiData['turn']);
    }
}

function setBoardInteractive(enabled) {
    document.querySelectorAll('.square').forEach(sq => {
        sq.style.pointerEvents = enabled ? 'auto' : 'none';
    });
}



function clearHighlights() {
  document.querySelectorAll('.legal').forEach(sq => sq.classList.remove('legal'));
  document.querySelectorAll('.selected').forEach(sq => sq.classList.remove('selected'));
}
function isWhitePiece(symbol) {
  // white pieces are the unfilled/outline glyphs in your set: ♙♘♗♖♕♔
  return ['♙','♘','♗','♖','♕','♔'].includes(symbol);
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
      const piece = board[i][j] ?? '';
      div.innerText = piece;

      const pieceExists = !!piece;
      const isCorrectColor = pieceExists && (
        (currentTurn === 'white' && isWhitePiece(piece)) ||
        (currentTurn === 'black' && !isWhitePiece(piece))
      );
      div.draggable = isCorrectColor;

      outer_div.appendChild(div);
    }
  }
  if (lastMove) {
    const [fr, fc] = lastMove.from;
    const [tr, tc] = lastMove.to;
    const fromSq = document.querySelector(`[data-row="${fr}"][data-col="${fc}"]`);
    const toSq = document.querySelector(`[data-row="${tr}"][data-col="${tc}"]`);
    if (fromSq) fromSq.classList.add('last-move');
    if (toSq) toSq.classList.add('last-move');
  }
  document.querySelectorAll('.square').forEach(square => {

    square.addEventListener('dragstart', async (event) => {
      pos_r = Number(event.currentTarget.dataset.row);
      pos_c = Number(event.currentTarget.dataset.col);
      event.currentTarget.classList.add('selected');   // add this

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
  lastMove = { from: [pos_r, pos_c], to: [t_r, t_c] };   // add this

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
  const turnEl = document.getElementById('turn-indicator');

  if (status === 'ongoing') {
    banner.style.display = 'none';
    if (turnEl) {
      turnEl.style.display = 'block';
      turnEl.innerText = turn === 'white' ? "White to move" : "Black to move";
    }
    return;
  }

  banner.style.display = 'block';
  if (turnEl) turnEl.style.display = 'none';

  if (status === 'checkmate') {
    const winner = turn === 'white' ? 'Black' : 'White';
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
  currentTurn = data['turn'];

  board=data['board']
  render_board(data['board']);
    updateStatusBanner(data['status'], data['turn']);

}

// This is the part that actually runs when the page loads:
const savedId = localStorage.getItem('game_id');
//const savedId = 42;

// page load
if (savedId) {
  load_game(savedId);
} else {
  showSetupModal();
}