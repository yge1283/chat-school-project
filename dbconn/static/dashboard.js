document.addEventListener('DOMContentLoaded', function() {
    // login페이지 -login 버튼 누를때 실행
    document.getElementById('createbutton').addEventListener('click', createtable);
    document.getElementById('coursesbutton').addEventListener('click', mycourses);
    document.getElementById('coursecreate').addEventListener('click', insertDashboardKey);

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
               
                //chatupcall 페이지에서 시간표 색칠을 위한 함수 
                //6.11 (양지은) 코드  추가
                applyCourseData(data.data);
                 //6.11 (양지은) 코드 끝



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

       
             // 6.10 양지은 대시보드 스타일 코드 추가 
             courseBox.style.margin='20px auto'
             courseBox.style.position = 'relative';
             courseBox.style.right = '60px';
             courseBox.style.width = '50%';
             courseBox.style.backgroundColor = ' rgb(228, 247, 255)';
             courseBox.style.height = '180px';
             courseBox.style.borderRadius = '15px';
             courseBox.style.border = 'white';
             courseBox.style.textAlign='center'
             //6.10 양지은 대사보드 스타일 코드 끝

        courseBox.innerHTML = `
            <h3>${course.과목명}</h3>
            <p>선생님: ${course.선생.선생이름}</p>
            <p>${course.학년}학년${course.학급}반</p>
            <p>시간표: ${course.시간표}</p>
        `;
        courseBox.addEventListener('click', () => {
            setDashboardKey(course.대시보드_key);
        });
        container.appendChild(courseBox);
    });
}
// 위 대시보드를 누르면 키값 보내고 메인 받아오기
async function setDashboardKey(dashboardKey) {
    try {
        const response = await fetch('/student/get_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: dashboardKey })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                // 메인 페이지로 이동
                window.location.href = '/student/main';
            } else {
                alert('Failed to set dashboard key');
            }
        } else {
            alert('Server returned an error');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while setting dashboard key');
    }
}

// 
// <button id="coursecreate">Create</button>
// 과목 추가하는 함수
async function insertDashboardKey() {
    const dashboardKey = document.getElementById('dashboard').value;

    if (!dashboardKey) {
        alert('정확한 대시보드 코드를 입력해주세요');
        return;
    }

    try {
        const response = await fetch('/student/insert_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: dashboardKey })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                alert('정상적으로 수강중인 과목이 추가 되었습니다.');
            } else {
                alert('정확한 과목 코드가 아닐 수 있습니다.');
            }
        } else {
            alert('Server returned an error');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while inserting the dashboard key');
    }
}

/// 선생님용 코드 학생용과 거의 엔드포인트 이름 빼고 똑같습니다.