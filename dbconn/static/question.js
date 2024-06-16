var socket = io.connect('/question');
function displayBoardData(data,number=1) {
    const boardBody = document.getElementById('board-body');
    boardBody.innerHTML = ''; // 기존 데이터를 모두 지웁니다
    var num=1+(number-1)*6;
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${num}</td>
            <td><a href="./comment">${item.제목}</a></td>
            <td>${item.user_name}</td>
            <td>${formatDate(item.작성시간)}</td>
            <td>${item.상태}</td>
            <td>${item.조회}</td>
        `;
        boardBody.appendChild(row);
        num+=1;
    });
}
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    return date.toLocaleDateString('ko-KR', options);
}
document.addEventListener('DOMContentLoaded', function() {
  // 페이지가 로드될 때 소켓을 초기화하고 서버에 연결합니다.


socket.on('connect', function() {
    // Emit a 'question_start' event to initiate communication
    socket.emit('question_start');

    const prevButton = document.getElementById('qprev');
    const nextButton = document.getElementById('qnext');

    prevButton.addEventListener('click', function() {
        // 이전 페이지로 이동하는 로직을 여기에 추가
        console.log('이전 페이지로 이동');
        // 예: 현재 페이지 번호를 가져와서 1 감소시키는 로직
        let currentPage = parseInt(document.querySelector('span').textContent);
        if (currentPage > 1) {
            document.querySelector('span').textContent = currentPage - 1;
            socket.emit('board', currentPage - 1);
        }
    });

    nextButton.addEventListener('click', function() {
        // 다음 페이지로 이동하는 로직을 여기에 추가
        console.log('다음 페이지로 이동');
        // 예: 현재 페이지 번호를 가져와서 1 증가시키는 로직
        let currentPage = parseInt(document.querySelector('span').textContent);
        document.querySelector('span').textContent = currentPage + 1;
        socket.emit('board', currentPage + 1);
    });
});

// When receiving a 'success' event from the server
socket.on('success', function() {
    // Handle the success event (e.g., display a message)
    console.log('Success!');
});


// Handle error event
socket.on('error', function(data) {
    console.log(data)
});
})

// Handle 'board' event to display board data
socket.on('board', function(data) {
    console.log(data)
    // Assuming data is an array of objects representing board data

    displayBoardData(JSON.parse(data),parseInt(document.querySelector('span').textContent));
});
