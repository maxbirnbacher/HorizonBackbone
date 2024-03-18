function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    try {
        const hashBuffer = crypto
            .subtle
            .digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashedPassword = hashArray
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
        return str(hashedPassword);
    } catch (error) {
        console.error('Error hashing password:', error);
        return null;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // logic for login page
    document
        .querySelector('#login-form')
        .addEventListener('submit', function (event) {
            event.preventDefault();

            var username = document
                .querySelector('#login-form-username')
                .value;
            var password = document
                .querySelector('#login-form-password')
                .value;

            // hash the password with sha256
            var hashedPass = hashPassword(password);

            console.log('username: ' + username);
            console.log('password: ' + password);
            console.log('hashedPass: ' + hashedPass);

            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: username, password: hashedPass})
            })
                .then(response => response.json())
                .then(data => {
                    // Login successful, save the token
                    localStorage.setItem('token', data.access_token);
                    window.location.href = '/';
                })
                .catch((error) => {
                    // Login failed
                    console.error('Login failed:', error);
                    alert('Invalid username or password');
                });
        });
});
