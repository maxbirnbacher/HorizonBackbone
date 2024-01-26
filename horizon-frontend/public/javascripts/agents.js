document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/agents/all')
        .then(response => response.json())
        .then(agents => {
            const table = document.getElementById('basic-table');
            agents.forEach(agent => {
                const row = document.createElement('tr');
                row.classList.add('pf-c-table__tr');
                row.innerHTML = `
                    <td class="pf-c-table__td">${agent.id}</td>
                    <td class="pf-c-table__td"><a href="/agent/${agent.id}">${agent.hostname}</a></td>
                    <td class="pf-c-table__td">${agent.os}</td>
                    <td class="pf-c-table__td">${agent.ip}</td>
                    <td class="pf-c-table__td">${agent.username}</td>
                    <td class="pf-c-table__td">${agent.lastSeen}</td>
                    <td class="pf-c-table__td"><button class="pf-c-button pf-m-danger remove-btn" data-id="${agent.id}">Remove</button></td>
                `;
                table.appendChild(row);
            });
        });
});
