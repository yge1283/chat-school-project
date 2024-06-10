document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadbutton').addEventListener('click', uploadtable);
});

// 업로드기능이 필요한 HTML에 <input type="file" id="fileInput" multiple> 추가.
async function uploadtable() {
    alert("JS 실행중");
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    
    if (files.length === 0) {
        alert("No files selected");
        return;
    }
    
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch('/teacher/send_upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                alert('Files uploaded successfully');
            } else {
                alert('Failed to upload files');
                console.error(data.responses);
            }
        } else {
            alert('Server returned an error');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading files');
    }
}