// 감정 분석 요청을 보내고 서버로부터 결과를 처리하는 함수
function emo_analyze() {
    // 감정 분석 요청을 소켓을 통해 서버에 전송
    socket.emit('analyze_emotion', {"uid": "asd"});
    alert('서버로 데이터 보냄');

    // 서버로부터 감정 분석 결과를 받는 이벤트 리스너 등록
    socket.on('emotion_analyze_result', (data) => {
        alert('서버로 데이터 받음');

        // 받은 데이터를 localStorage에 JSON 문자열로 저장
        localStorage.setItem('emotion_analyze_result', JSON.stringify(data));
        alert("감정 데이터를 받음");
        console.log(data);
        

        // 데이터를 서버로 전송하는 함수 호출
        sendDataToServer();
    });
}

// 서버로 데이터를 전송하는 함수
function sendDataToServer() {
    try {
        // 서버에 전송할 데이터 준비

        const storedData = localStorage.getItem('emotion_analyze_result');
        const data = JSON.parse(storedData);
    
        // 서버로 데이터 전송
        fetch('/teacher/checkstudentmind', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), // JSON 형식으로 변환하여 전송
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            
            // 서버로부터 받은 데이터를 처리하거나 화면에 표시할 수 있음
            // 여기서는 예시로 console.log로만 표시
          

            const tableBody = document.getElementById('tableBody');
            let tableRows = '';

            const allowedEmotions = ["분노", "슬픔", "기쁨", "중립", "불안", "걱정", "당황", "상처"];
            const emotionEmojis = {
                "분노": "😡",
                "슬픔": "😢",
                "기쁨": "😄",
                "중립": "😐",
                "불안": "😰",
                "걱정": "😟",
                "당황": "😳",
                "상처": "😞"
            };

            // 학생 정보를 테이블에 추가
            data.student_info.forEach(item => {
                if (allowedEmotions.includes(item.emotion)) {
                    tableRows += '<tr>';
                    tableRows += `<td>${item.student_name}</td>`;
                    tableRows += `<td><span class="emoji">${emotionEmojis[item.emotion]}</span></td>`; // 감정 이모지 추가
                    tableRows += `<td></td>`;
                    tableRows += `<td></td>`;
                    tableRows += `<td></td>`;
                    tableRows += `<td></td>`;
                    tableRows += '</tr>';
                }
            });

            // 테이블에 추가한 학생 정보 표시
            tableBody.innerHTML = tableRows;

        })
        .catch(error => {
            console.error('서버 응답 처리 중 오류 발생:', error);
        });

    } catch (error) {
        console.error('데이터 전송 중 오류 발생:', error);
    }
}

// emo_analyze() 함수 호출 (분석하기 버튼 등에 연결하여 사용)
