
document.addEventListener('DOMContentLoaded', function() {
  // 페이지가 로드될 때 소켓을 초기화하고 서버에 연결합니다.
var socket = io.connect();

socket.on('connect', function() {
    // Emit a 'question_start' event to initiate communication
    socket.emit('question_start');
});

// When receiving a 'success' event from the server
socket.on('success', function() {
    // Handle the success event (e.g., display a message)
    console.log('Success!');
});

// Handle 'board' event to display board data
socket.on('board', function(data) {
    console.log(data)
    // Assuming data is an array of objects representing board data

    displayBoardData(JSON.parse(data));
});

// Handle error event
socket.on('error', function(data) {
    console.log(data)
});
})
function displayBoardData(data) {
    const boardBody = document.getElementById('board-body');
    boardBody.innerHTML = ''; // 기존 데이터를 모두 지웁니다

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.게시물_ID}</td>
            <td><a href="./comment">${item.제목}</a></td>
            <td>${item.user_name}</td>
            <td>${formatDate(item.작성시간)}</td>
            <td>${item.상태}</td>
            <td>${item.조회}</td>
        `;
        boardBody.appendChild(row);
    });
}
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    return date.toLocaleDateString('ko-KR', options);
}