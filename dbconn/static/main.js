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
