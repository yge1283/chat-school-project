var socket = io.connect('/question');

const prevButton = document.getElementById('qprev');
const nextButton = document.getElementById('qnext');
const currentPageElement = document.getElementById('currentPage');
let currentPage = parseInt(currentPageElement.textContent);
// When receiving a 'success' event from the server
socket.on('success', function() {
    // Handle the success event (e.g., display a message)
    console.log('Success!');
});

socket.on('connect', function() {
    // Emit a 'question_start' event to initiate communication
    socket.emit('question_start');});

// Handle error event
socket.on('error', function(data) {
    console.log(data)
});


// Handle 'board' event to display board data
socket.on('board', function(data) {
    console.log("board");
    console.log(data);
    // Assuming data is an array of objects representing board data

    displayBoardData(JSON.parse(data),parseInt(document.querySelector('span').textContent));
});
socket.on('comment_num', function(data) {
    const { 게시물_ID, comment_count } = data;
    const commentCountElement = document.getElementById(`comment-count-${게시물_ID}`);
    if (commentCountElement) {
        commentCountElement.textContent = comment_count;
    }
    console.log(data);
});

document.addEventListener('DOMContentLoaded', function() {
  // 페이지가 로드될 때 소켓을 초기화하고 서버에 연결합니다.
    prevButton.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            updatePage();
        }
    });

    nextButton.addEventListener('click', function() {
        currentPage++;
        updatePage();
        
    });
    function updatePage() {
        currentPageElement.textContent = currentPage;
        socket.emit('board', currentPage);
    }
});


function displayBoardData(data) {
    const boardBody = document.getElementById('board-body');
    boardBody.innerHTML = ''; // 기존 데이터를 모두 지웁니다
    number=1+(currentPage-1)*6
    data.forEach(item => {
        const row = document.createElement('tr');
        bd_id=item.게시물_ID
        socket.emit('comment_num',bd_id)
        
        row.innerHTML = `
            <td>${number}</td>
            
            <td><a href="./comment?게시물_ID=${bd_id}">${item.제목}</a></td>
            <td>${item.user_name}</td>
            <td>${formatDate(item.작성시간)}</td>
            <td id="comment-count-${item.게시물_ID}">-</td>
            <td>${item.조회수}</td>
        `;
        boardBody.appendChild(row);
        number+=1
    });
}

function formatDate(datetime) {
    const date = new Date(datetime);
    return date.toLocaleString();
}