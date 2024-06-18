const socket = io('https://7a87-125-184-48-169.ngrok-free.app', { // ai서버 주소
  autoConnect: true,
  extraHeaders: {
      "ngrok-skip-browser-warning": true
  },
  path: '/socket.io',
  transports: ['websocket', 'polling'],
  allowEIO3: true
});

const fsocket=io.connect('/chatbot');
uid=""
socket.on('connect', () => {
  console.log('Connected to WebSocket server.');
});

socket.on('connect_error', (error) => {
  console.error('Connection Error:', error);
});

socket.on('error', (error) => {
  console.error('WebSocket Error:', error);
});

socket.on('disconnect', (reason) => {
  console.log('Disconnected:', reason);
});

socket.on('summary_result', (data) => {
  console.log('Received file data:', data);
  fsocket.emit('file_data', data);
  // Handle the file data
  appendMessage(data, false);

});
fsocket.on('chatting',(data)=>{
  console.log("connected")
  setchat(JSON.parse(data))
  function setchat(data){
      console.log(data)
      uid=data.학생_ID
  }
})

document.addEventListener('DOMContentLoaded', () => {
  const submitButton = document.getElementById('submitButton');
  const fileInput = document.getElementById('fileInput');

  if (submitButton && fileInput) {
      submitButton.addEventListener('click', uploadFile);

      function uploadFile() {
          console.log("실행됨");
          const file = fileInput.files[0];

          if (file) {
              const reader = new FileReader();
              reader.onload = function (event) {
                  const arrayBuffer = event.target.result;
                  const bytes = new Uint8Array(arrayBuffer);
                  socket.emit('make_summary', { filename: file.name, data: bytes, uid: uid });
              };
              reader.readAsArrayBuffer(file);
          } else {
              alert("Please select a file first."); // 파일 선택 안된상태로 업로드누를시 경고
          }
      }
  }
  fsocket.emit('connect')

  

});
