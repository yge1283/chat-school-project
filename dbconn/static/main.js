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

    // Add your logic to display the data in the HTML
}
