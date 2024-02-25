function showUpload() {
    let modal = `
    <div
        class="pf-v5-c-modal-box pf-m-md"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-md-title"
        aria-describedby="modal-md-description"
        style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);"
    >
        <div class="pf-v5-c-modal-box__close">
            <button class="pf-v5-c-button pf-m-plain" type="button" aria-label="Close" onclick="document.body.removeChild(this.parentElement.parentElement)">
                <i class="fas fa-times" aria-hidden="true"></i>
            </button>
        </div>
        <header class="pf-v5-c-modal-box__header">
            <h1 class="pf-v5-c-modal-box__title" id="modal-md-title">Upload file</h1>
        </header>
        <div class="pf-v5-c-modal-box__body" id="modal-md-description">
            Use this url:
            <div class="pf-v5-c-code-block">
                <div class="pf-v5-c-code-block__content">
                    <pre class="pf-v5-c-code-block__pre"><code class="pf-v5-c-code-block__code">http://file-api:8003/file-exfil/upload</code></pre>
                </div>
            </div>
            to upload a file to the server.
        </div>
        <footer class="pf-v5-c-modal-box__footer">Modal footer</footer>
    </div>
    `

    // append modal to body
    document.body.insertAdjacentHTML('beforeend', modal);
}

function downloadFile(id) {
    console.log('downloading file: ' + id);
    fetch('/api/files/download/' + id)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = id;
            document.body.appendChild(a);
            a.click();
            a.remove();
        });
}

function rawFile(id) {
    // open a new tab with the raw file content
    window.open('/api/files/raw/' + id);
}

function removeFile(id) {
    fetch('/api/files/remove/' + id)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('File removed successfully');
                window.location.reload();
            } else {
                alert('Failed to remove file');
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/files/all')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('table_files_body');
            table.innerHTML = '';
            data.files.forEach(file => {
                const row = document.createElement('tr');
                row.classList.add('pf-v5-c-table__tr');
                row.innerHTML = `
                    <td class="pf-v5-c-table__td" role="cell">${file._id}</td>
                    <td class="pf-v5-c-table__td" role="cell">${file.filename}</td>
                    <td class="pf-v5-c-table__td" role="cell">${file.length}b</td>
                    <td class="pf-v5-c-table__td" role="cell">${file.uploadDate}</td>
                    <td class="pf-v5-c-table__td" role="cell">
                        <button class="pf-v5-c-button pf-m-primary download-btn pf-m-inline" data-id="${file._id} onclick="downloadFile('${file._id}')>Download</button>
                        <button class="pf-v5-c-button pf-m-secondary download-btn pf-m-inline" data-id="${file._id} onclick="rawFile('${file._id}')">Raw content</button>
                        <button class="pf-v5-c-button pf-m-secondary remove-btn pf-m-inline" data-id="${file._id} onclick="removeFile('${file._id}')">Remove</button>
                    </td>
                `;
                table.appendChild(row);
            });
        }
    );
});