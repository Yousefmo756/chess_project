let game_id=null
async function create_game(){
 response= await fetch("game/new",{method:'POST'})
 data= await response.json()
 game_id=data['id']
 board=data['board']
 render_board(board)

}

const squares=document.querySelectorAll('.square')
squares.addEventListener('drag',(event)=>{ event.AT_TARGET})
async function makemove(pos_sq,t_sq){
    response= fetch ('game/${game_id}/move',{method:'POST',
         headers: { 'Content-Type': 'application/json' },
body:JSON.stringify({from:pos_sq,to:t_sq})

})
data= await response.json()
board=data['board']
render_board(board)
}



function render_board(board){
outer_div=document.getElementsByClassName('chessboard')
for(let i=0;i<8;i++){
 for(let j=0;j<8;j++){
 cl_name=((i+j)%2==0)?'square light':'square dark' 
 div=document.createElement('div')
 div.setAttribute('row',i)
 div.setAttribute('col',j)
 div.innerText=board[i][j]??''
 div.className=cl_name
 
 outer_div.appendChild(div)
}
}
}


