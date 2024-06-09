document.addEventListener('DOMContentLoaded', function() {
    // login페이지 -login 버튼 누를때 실행
    document.getElementById('createbutton').addEventListener('click', createtable);
    document.getElementById('coursesbutton').addEventListener('click', mycourses);
});

// 데이터 넣는 함수
async function createtable() {
    alert("JS 실행중");

    try {
        const response = await fetch('/student/create_table');
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                alert("테이블 삽입 성공");
            } else {
                alert('유저 정보가 정확하지 않습니다');
            }
        } else {
            alert('서버에서 에러가 발생했습니다');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('뭔가 잘못됨');
    }
}

// 과목데이터 가져오는 함수
async function mycourses() {
    alert("JS 실행중");

    try {
        const response = await fetch('/student/get_my_courses');
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                alert('대시보드에서 과목정보를 불러왔습니다.');
                // 데이터 가져왔을 때 사각형으로 HTML에 나타내는 함수로 이동
                displayCourses(data.data);
            } else {
                alert('유저 정보가 정확하지 않습니다.');
            }
        } else {
            alert('서버에서 에러가 발생했습니다');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while retrieving courses');
    }
}

async function displayCourses(courses) {
    const container = document.getElementById('coursesContainer');
    container.innerHTML = '';

    courses.forEach(course => {
        const courseBox = document.createElement('div');
        courseBox.className = 'course-box';
        courseBox.innerHTML = `
            <h3>${course.과목명}</h3>
            <p>선생님: ${course.선생.선생이름}</p>
            <p>학년: ${course.학년}</p>
            <p>학급: ${course.학급}</p>
            <p>시간표: ${course.시간표}</p>
        `;
        courseBox.addEventListener('click', () => {
            setDashboardKey(course.대시보드_key);
        });
        container.appendChild(courseBox);
    });
}

// 위 대시보드를 누르면 메인 받아오기
async function setDashboardKey(dashboardKey) {
    try {
        const response = await fetch('/student/get_mainboard', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: dashboardKey })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                console.log('Mainboard data retrieved successfully');
                console.log(data);

                // 메인 페이지에 데이터를 배치하는 로직을 여기에 추가
                // 예: displayMainboardData(response.data);

                // Example of how to handle memo_data and file_name
                const questionData = data.question_data || [];
                const homeworkData = data.homework_data || [];
                const memoData = data.memo_data || [];
                const fileName = data.file_name || [];

                // If you need to do something specific with memoData or fileName
                if (memoData.length === 0) {
                    console.log('No memo data available');
                }

                if (fileName.length === 0) {
                    console.log('No files available');
                }

                // Add your logic to handle memoData and fileName here
            } else {
                alert('Failed to retrieve mainboard data');
            }
        } else {
            alert('서버에서 에러가 발생했습니다');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while setting dashboard key');
    }
}
