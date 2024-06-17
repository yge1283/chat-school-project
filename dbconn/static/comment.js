let comments = [];
socket.io




document.getElementById('postCommentButton').addEventListener('click', function () {
    const commentText = document.getElementById('textAreaExample').value;
    if (commentText.trim() !== '') {
        const newComment = {
            text: commentText,
            date: new Date().toLocaleString()
        };
        comments.push(newComment);
        document.getElementById('textAreaExample').value = '';
        displayComments();
    }
});

function displayComments() {
    const commentsContainer = document.getElementById('commentsContainer');
    commentsContainer.innerHTML = comments.map((comment, index) => `
<div class="card mb-3">
    <div class="card-body">
        <div class="d-flex flex-start">
            <img class="rounded-circle shadow-1-strong me-3"
                src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                alt="avatar" width="40" height="40" />
            <div class="w-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="text-primary fw-bold mb-0">
                        홍길동
                        <span class="text-body ms-2">${comment.text}</span>
                    </h6>
                    <p class="mb-0">${comment.date}</p>
                </div>
                <button class="btn btn-secondary btn-sm" onclick="editComment(${index})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteComment(${index})">Delete</button>
            </div>
        </div>
    </div>
</div>
`).join('');
}

function editComment(index) {
    const comment = comments[index];
    const newCommentText = prompt("Edit your comment:", comment.text);
    if (newCommentText !== null && newCommentText.trim() !== '') {
        comments[index].text = newCommentText;
        displayComments();
    }
}

function deleteComment(index) {
    comments.splice(index, 1);
    displayComments();
}