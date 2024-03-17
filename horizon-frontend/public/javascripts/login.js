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
            var hashedPass = sha256(password.toString());

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
