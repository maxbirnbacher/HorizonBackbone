window.addEventListener('DOMContentLoaded', (event) => {
    const tabButtons = document.querySelectorAll('.pf-v5-c-tabs__link');
    const tabSections = document.querySelectorAll('.pf-v5-c-tab-content');
    const commandButton = document.getElementById('command_Button');
    const alertGroup = document.getElementById('alert_group');
    const tableTasks = document.getElementById('table_tasks');

    tabButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            // Remove 'pf-m-current' class from all tabs
            tabButtons.forEach(btn => btn.parentElement.classList.remove('pf-m-current'));

            // Add 'pf-m-current' class to the clicked tab
            button.parentElement.classList.add('pf-m-current');

            // Hide all sections
            tabSections.forEach(section => section.setAttribute('hidden', 'hidden'));

            // Show the corresponding section
            tabSections[index].removeAttribute('hidden');
        });
    });

    commandButton.addEventListener('click', () => {
        const commandInput = document.getElementById('command_textarea');
        const command = commandInput.value;

        if (command === '' || command === null || command === undefined || command === ' ' || command === '  ' || command === '   ') {
            return;
        }

        // encode command with base64 using UTF-8
        let utf8str = unescape(encodeURIComponent(command));
        let base64str = btoa(utf8str);

        // send command to server
        // const agentID = document.getElementById('agent_id').value;
        // console.log('agentID: ' + agentID);

        // get the agentID from the url path 
        let url = window.location.pathname;
        let agentID = url.substring(url.lastIndexOf('/') + 1);
        console.log('agentID: ' + agentID);

        fetch('/api/agent/' + agentID + '/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'agentID': agentID,
            },
            body: JSON.stringify({command: base64str})
        })

        commandInput.value = '';
    });

    // get the agentID from the url path
    let url = window.location.pathname;
    let agentID = url.substring(url.lastIndexOf('/') + 1);
    
    // make a get request to the agent-api for the tasks
    fetch('/api/agent/' + agentID + '/tasks')
    .then(response => {
        if (response.status === 200) {
            console.log('response: ' + response.json);
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        console.log(data.tasks);
        data.tasks.forEach(task => {
            console.log(task);
            const rowTable = document.createElement('tr');
            rowTable.setAttribute('class', 'pf-v5-c-table__tr');
            rowTable.innerHTML = `
                <td class="pf-v5-c-table__td pf-v5-c-table__toggle" role="cell">
                    <button
                        class="pf-v5-c-button pf-m-plain pf-m-expanded"
                        aria-labelledby="table-expandable-node1 table-expandable-expandable-toggle1"
                        id="table-expandable-expandable-toggle1"
                        onclick="document.getElementById('table-expandable-content-${task._id}').classList.toggle('pf-m-expanded'); document.getElementById('icon-${task._id}').classList.remove('fa-angle-right'); document.getElementById('icon-${task._id}').classList.add('fa-angle-down');"
                        aria-label="Details"
                        aria-controls="table-expandable-content1"
                        aria-expanded="true">
                        <div class="pf-v5-c-table__toggle-icon">
                            <i class="fas fa-angle-right" id="icon-${task._id}" aria-hidden="true"></i>
                        </div>
                    </button>
                </td>
                <td class="pf-v5-c-table__td " role="cell">${task._id}</td>
                <td class="pf-v5-c-table__td" role="cell">${task.command}</td>
                <td class="pf-v5-c-table__td" role="cell">${task.status}</td>
                <td class="pf-v5-c-table__td" role="cell">${task.timestamp}</td>
            `;
            tableTasks.appendChild(rowTable);
            // create a new tr element in the table for the task details
            const tr = document.createElement('tr');
            tr.setAttribute('class', 'pf-v5-c-table__tr pf-v5-c-table__expandable-row');

            // create a new td element in the tr
            const td = document.createElement('td');
            td.setAttribute('class', 'pf-v5-c-table__td');
            td.setAttribute('colspan', '4');
            td.setAttribute('role', 'cell');

            // create a new div element in the td
            const div = document.createElement('div');
            div.setAttribute('class', 'pf-v5-c-table__expandable-row-content');
            div.setAttribute('id', 'table-expandable-content-' + task._id);
            div.innerHTML = `
                <h4>Input</h4>
                <p>${task.input}</p>
                <h4>Output</h4>
                <p>${task.output}</p>
            `;

            // append the div to the td
            td.appendChild(div);
            // append the td to the tr
            tr.appendChild(td);
            // append the tr to the table
            tableTasks.appendChild(tr);
            const row = document.createElement('tr');
            row.setAttribute('class', 'pf-v5-c-table__tr');

        });
    });

});