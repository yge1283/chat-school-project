document.addEventListener('DOMContentLoaded', function() {
    // login페이지 - login 버튼 누를때 실행
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
        loginButton.addEventListener('click', signInWithEmail);
    }
    const googleButton = document.getElementById('googlebutton');
    if (googleButton) {
        googleButton.addEventListener('click', signInWithGoogle);
    }
    const kakaoButton = document.getElementById('kakaobutton');
    if (kakaoButton) {
        kakaoButton.addEventListener('click', signInWithKakao);
    }
    // signup페이지 - Sign up 버튼 누를때 실행
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            registerUser();
        });
    }

    // findpw 페이지
    const getCodeButton = document.getElementById('getCodeButton');
    if (getCodeButton) {
        getCodeButton.addEventListener('click', sendCode);
    }
    const resetSubmitButton = document.getElementById('resetSubmitButton');
    if (resetSubmitButton) {
        resetSubmitButton.addEventListener('click', function(event) {
            event.preventDefault();
            resetPassword();
        });
    }
});

    const hash = window.location.hash.substring(1);
    if (hash) {
        const params = new URLSearchParams(hash);

        const accessToken = params.get('access_token');
        const providerToken = params.get('provider_token');
        const refreshToken = params.get('refresh_token');

        if (accessToken && providerToken && refreshToken) {
            fetch('/login/callback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    access_token: accessToken,
                    provider_token: providerToken,
                    refresh_token: refreshToken
                })
            }).then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.redirect_url) {
                    alert('첫 로그인시 추가 정보를 입력해야합니다.');
                    window.location.href = data.redirect_url;
                } else {
                    alert('OAuth 콜백 처리 중 오류가 발생했습니다.');
                }
            });
        }
    }

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

async function signInWithKakao() {
    try {
        const response = await axios.get('/login/login-kakao');
        if (response.data.redirect_url) {
            // 리디렉션 URL로 이동
            alert("카카오 url로 이동중");
            //콜백으로 이동
            window.location.href = response.data.redirect_url;
        } else {
            alert('kakao 로그인 실패');
        }
    } catch (error) {
        console.error('kakao 로그인 실패:', error);
        alert('kakao 로그인 중 오류가 발생했습니다.');
    }
}


// SignUP 회원가입 코드

async function registerUser() {
    alert("JS 실행중");
    const year = document.getElementById('birth-year').value;
    const month = document.getElementById('birth-month').value;
    const day = document.getElementById('birth-day').value;

    // 예시로 YYYY-MM-DD 형식으로 날짜를 만듭니다.
    const birthdate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

    const gender = document.querySelector('input[name="gender"]:checked').value;
    const role = document.querySelector('input[name="role"]:checked').value;
    const isTeacher = (role === 'teacher');

    const userData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        phone: document.getElementById('phone').value,
        birthdate: birthdate,
        gender: gender,
        address: document.getElementById('address').value,
        isTeacher: isTeacher  // 수정: teacher -> isTeacher
    };

    try {
        const response = await axios.post('/login/register', userData);
        if (response.data.redirect_url) {
            alert("성공적으로 정보가 추가되었습니다.");
            window.location.href = response.data.redirect_url;
        } else if (response.data.success) {
            alert('성공적으로 회원가입이 완료되었습니다.');
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


async function sendCode() {
    alert("JS 코드 실행중");
    const email = document.getElementById('emailInput').value;

    try {
        const response = await fetch('/login/find-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        const data = await response.json();
        if (data.message) {
            alert(data.message);
            document.getElementById('passwordSection').style.display = 'block';
        } else if (data.error) {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error); // 216 line
    }
}

async function resetPassword() {
    const email = document.getElementById('emailInput').value;
    const token = document.getElementById('verificationCodeInput').value;
    const newPassword = document.getElementById('newPasswordInput').value;
    const confirmPassword = document.getElementById('confirmPasswordInput').value;

    if (newPassword !== confirmPassword) {
        alert('비밀번호가 서로 맞지 않습니다!');
        return;
    }

    try {
        const response = await fetch('/login/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, token, new_password: newPassword })
        });
        const data = await response.json();
        if (data.message) {
            alert(data.message);
            window.location.href = '/'; // login 페이지로 이동
        } else if (data.error) {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
