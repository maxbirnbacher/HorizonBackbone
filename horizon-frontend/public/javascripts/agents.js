document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/agents/all')
        .then(response => response.json())
        .then(agents => {
            const table = document.getElementById('table_agents_body');
            agents.forEach(agent => {
                const row = document.createElement('tr');
                row.classList.add('pf-v5-c-table__tr');
                row.innerHTML = `
                    <td class="pf-v5-c-table__td" role="cell">${agent._id}</td>
                    <td class="pf-v5-c-table__td" role="cell"><a href="/c2/agent/${agent._id}">${agent.hostname}</a></td>
                    <td class="pf-v5-c-table__td" role="cell">${agent.os}</td>
                    <td class="pf-v5-c-table__td" role="cell">${agent.ip_address}</td>
                    <td class="pf-v5-c-table__td" role="cell">${agent.username}</td>
                    <td class="pf-v5-c-table__td" role="cell">${agent.timestamp}</td>
                    <td class="pf-v5-c-table__td" role="cell"><button class="pf-v5-c-button pf-m-danger remove-btn" data-id="${agent._id}">Remove</button></td>
                `;
                table.appendChild(row);
            });
        });
});
