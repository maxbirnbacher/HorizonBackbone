// logic for login page
document
    .querySelector('#login-form')
    .addEventListener('submit', function (event) {
        event.preventDefault();

        var username = document
            .querySelector('#login-demo-form-username')
            .value;
        var password = document
            .querySelector('#login-demo-form-password')
            .value;

        // TODO: change login to the new user api
        axios
            .post('http://localhost:3000/api/login', {
                username: username,
                password: password
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
