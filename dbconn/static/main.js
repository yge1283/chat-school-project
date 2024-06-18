document.addEventListener('DOMContentLoaded', function() {
    getMainboardData();
});

async function getMainboardData() {
    try {
        alert("JS실행중")
        const response = await fetch('/student/get_mainboard', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            alert("정보받아옴")
            if (data.success) {
                console.log('Mainboard data retrieved successfully');
                console.log(data);

                // 데이터 배치 로직을 여기에 추가
                displayMainboardData(data);
            } else {
                alert('Failed to retrieve mainboard data');
            }
        } else {
            alert('Server returned an error');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while retrieving mainboard data');
    }
}

function displayMainboardData(data) {
    const questionData = data.question_data || [];
    const homeworkData = data.homework_data || [];
    const memoData = data.memo_data || [];
    const fileName = data.file_name || [];

    // Display the data as needed
    console.log('Questions:', questionData);
    console.log('Homeworks:', homeworkData);
    console.log('Memos:', memoData);
    console.log('Files:', fileName);


      // 6.14  메인페이지에 메모 데이터 추가함수 
      //본 함수는 html에 있음
      displayMemoData(memoData)

      // 6.14 메인페이지에 질문게시판 데이터 추가함수 
      //본함수는 html에 있음. 
      displayQuestionData(questionData) 

   


    //6.14 메인페이지에 파일 목록 3개만 랜덤으로 표시하는 함수 시작
      function getRandomElements(arr, n) {
        const shuffled = arr.slice(); // 배열 복사
        let i = arr.length;
        const min = Math.max(i - n, 0);
        let temp, index;
        while (i-- > min) {
            index = Math.floor((i + 1) * Math.random());
            temp = shuffled[index];
            shuffled[index] = shuffled[i];
            shuffled[i] = temp;
        }
        return shuffled.slice(min);
    }
    
    // 파일 목록을 HTML에 출력하는 함수
    function displayFileList(files) {
        const fileListElement = document.getElementById('fileList1');
        fileListElement.innerHTML = ''; // 기존 목록 초기화
    
        files.forEach(file => {
            const listItem = document.createElement('div');
            listItem.textContent = file;
            listItem.style.fontSize = '20px'; // 폰트 크기 설
            listItem.style.padding = '10px'; // 내부 여백 설정
            listItem.style.textAlign = 'center'; // 텍스트 가운데 정렬
            listItem.style.overflow = 'hidden'; // 넘치는 부분 숨기기
        listItem.style.whiteSpace = 'nowrap'; // 한 줄로만 표시
        listItem.style.textOverflow = 'ellipsis'; // 넘치는 텍스트에 ... 표시
            // 첫 번째 요소는 맨 위로 이동
           
            fileListElement.appendChild(listItem);
            fileListElement.style.display = 'flex';
            fileListElement.style.flexDirection = 'column';
            fileListElement.style.alignItems = 'center';
            fileListElement.style.justifyContent = 'center';
            fileListElement.style.position='relative'
            fileListElement.style.right='15px'
    
        });
    }

        const randomFiles = getRandomElements(fileName, 3);
        displayFileList(randomFiles);
    // 메인 페이지에 랜덤으로 3개 파일 목록만 표시하는 함수 끝 




    function addBox(item) {
        const box = document.createElement('div');
        
        box.className = 'box';
        box.h
        box.innerHTML = `
            <div class="row">
                        <p><strong>주차:</strong> ${item.주차}</p>
                        <p><strong>제목:</strong> ${item.제목}</p>
                    </div>
            <p><strong>내용:</strong> ${item.내용}</p>
            <p><strong>기한:</strong> ${item.기한}</p>
            <p><strong>유형:</strong> ${item.유형}</p>
        `;
        box.addEventListener('click', () => {
            // 과제 ID 또는 다른 고유 식별자를 기반으로 URL 생성
            const url = `https://yourwebsite.com/homework/${item.과제_ID}`;
            window.location.href = url;
        });
        const colSm4 = document.querySelector('.col-sm-4'); // Find the col-sm-4 div
        if (colSm4) {
            colSm4.appendChild(box); // Append the box to the col-sm-4 div
        }
    }

    // Iterate over each homework item and add it to the col-sm-4 div
    homeworkData.forEach((item, index) => addBox(item));
}
