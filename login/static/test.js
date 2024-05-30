// test.js


// 해당 웹페이지에서 버튼이 실행될때, HTTP로 플라스크 서버와 통신
document.addEventListener('DOMContentLoaded', function() {
    fetchTableData();
    // login페이지 -login 버튼 누를때 실행
    document.getElementById('loginButton').addEventListener('click', signInWithEmail);


    // 마르디가 버튼 ID 붙여준다고 했음
    // signup페이지 - Sign up 버튼 누를때 실행
    document.getElementById('').addEventListener('click', signInWithEmail);
    document.getElementById('').addEventListener('click', signInWithEmail);
    document.getElementById('').addEventListener('click', signInWithEmail);

});

async function signInWithEmail() {
    const email = document.getElementById('form3Example3').value;
    const password = document.getElementById('form3Example4').value;

    alert("JS 실행중");

    axios.post('/login', { email, password })
        .then(response => {
            // 로그인 성공 시 리디렉션
            alert("로그인 성공");
        })
        .catch(error => {
            console.error('Login failed:', error);
        });
}

async function fetchTableData() {
    try {
        const response = await fetch('/api/get-table/게시판');
        const data = await response.json();

        if (response.ok) {
            generateHtmlTable(data);
        } else {
            console.error('Error fetching data:', data);
            document.getElementById('table-container').innerHTML = 'Error fetching data';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('table-container').innerHTML = 'Error fetching data';
    }
}

function generateHtmlTable(data) {
    if (data.length === 0) {
        document.getElementById('table-container').innerHTML = 'No data available';
        return;
    }

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Create table header
    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(column => {
        const th = document.createElement('th');
        th.innerText = column;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Create table body
    data.forEach(row => {
        const tr = document.createElement('tr');
        Object.values(row).forEach(cell => {
            const td = document.createElement('td');
            td.innerText = cell;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    document.getElementById('table-container').appendChild(table);
}

    

