async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    try {
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashedPassword;
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

            axios
                .post('http://localhost:3000/api/login', {
                    username: username,
                    password: hashedPass
                })
                .then(function (response) {
                    // Login successful, save the token
                    localStorage.setItem('token', response.data.access_token);
                    window.location.href = '/';
                })
                .catch(function (error) {
                    // Login failed
                    console.log('Login failed');
                    alert('Invalid username or password');
                });
        });
});
