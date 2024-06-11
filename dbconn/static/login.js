// test.js


// 해당 웹페이지에서 버튼이 실행될때, HTTP로 플라스크 서버와 통신
document.addEventListener('DOMContentLoaded', function() {
    // 로그인 페이지 처음 실행될 경우
    // 로그인 상태인지 확인 하기


    // login페이지 -login 버튼 누를때 실행
    document.getElementById('loginButton').addEventListener('click', signInWithEmail);
    document.getElementById('googlebutton').addEventListener('click', signInWithGoogle);

    // signup페이지 - Sign up 버튼 누를때 실행
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault();
        registerUser();
    });
    


});

async function signInWithEmail() {
    const email = document.getElementById('form3Example3').value;
    const password = document.getElementById('form3Example4').value;

    alert("JS 실행중");

    axios.post('/login', { email, password })
        .then(response => {
            
            if (response.data.isSuccess) {
                // 로그인 성공 시 리디렉션
                // alert("로그인 성공")
                window.location.href = response.data.redirect_url;
            } else {
                alert('유저 정보가 정확하지 않습니다');
            }
        })
        .catch(error => {
            console.error('Login failed:', error);
            alert('잘못된 이메일이나 비밀번호를 입력하셨습니다.');
        });
}
async function signInWithGoogle() {
    try {
        const response = await axios.get('/login/login-google');
        if (response.data.redirect_url) {
            // 리디렉션 URL로 이동
            alert("구글 url로 이동중");
            //콜백으로 이동
            window.location.href = response.data.redirect_url;
        } else {
            alert('Google 로그인 실패');
        }
    } catch (error) {
        console.error('Google 로그인 실패:', error);
        alert('Google 로그인 중 오류가 발생했습니다.');
    }
}

//콜백 함수
async function handleOAuthCallback() {
    try {
        const response = await axios.get('/login/callback');
        if (response.data.isSuccess) {
            // 로그인 성공 시 리디렉션
            window.location.href = response.data.redirect_url;
        } else {
            // 로그인 실패 시 처리
            alert(response.data.message);
            if (response.data.redirect_url) {
                window.location.href = response.data.redirect_url;
            }
        }
    } catch (error) {
        console.error('OAuth 콜백 처리 실패:', error);
        alert('OAuth 콜백 처리 중 오류가 발생했습니다.');
    }
}

// OAuth 콜백이 실행될 때 호출될 함수
window.onload = function() {
    if (window.location.pathname === '/login/callback') {
        handleOAuthCallback();
    }
};

// SignUP 회원가입 코드

async function registerUser() {
    const year = document.getElementById('birth-year').value;
    const month = document.getElementById('birth-month').value;
    const day = document.getElementById('birth-day').value;

    // 예시로 YYYY-MM-DD 형식으로 날짜를 만듭니다.
    const birthdate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

    const gender = document.querySelector('input[name="gender"]:checked').value;
    const isTeacher = document.getElementById('teacher-checkbox').checked;
    
    const userData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        phone: document.getElementById('phone').value,
        birthdate: birthdate,
        gender: gender,
        address: document.getElementById('address').value,
        teacher: document.getElementById('teacher').checked // assuming it's a checkbox
    };

    try {
        const response = await axios.post('/login/register', userData);
        if (response.data.success) {
            alert('Registration successful');
            window.location.href = '/login/';
        } else {
            alert('Registration failed: ' + response.data.error);
        }
    } catch (error) {
        console.error('Registration failed:', error);
        alert('Registration failed: ' + error.response.data.error);
    }
}




// 로그아웃 참고 JS 코드
async function logout() {
    try {
        const response = await axios.post('/login/logout', {}, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            window.location.href = '/'; // 로그아웃 후 리디렉션할 URL = 현재: 로그인페이지
        } else {
            alert('Logout failed');
        }
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Logout failed');
    }
}
