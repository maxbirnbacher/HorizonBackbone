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

document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/files/all')
        .then(response => response.json())
        .then(files => {
            const table = document.getElementById('table_files_body');
            files.forEach(file => {
                const row = document.createElement('tr');
                row.classList.add('pf-v5-c-table__tr');
                row.innerHTML = `
                    <td class="pf-v5-c-table__td" role="cell">${file._id}</td>
                    <td class="pf-v5-c-table__td" role="cell">${file.filename}</td>
                    <td class="pf-v5-c-table__td" role="cell">${file.filepath}</td>
                    <td class="pf-v5-c-table__td" role="cell">${file.timestamp}</td>
                    <td class="pf-v5-c-table__td" role="cell"><button class="pf-v5-c-button pf-m-primary download-btn" data-id="${file._id}">Download</button></td>
                `;
                table.appendChild(row);
            });
        }
    );
});