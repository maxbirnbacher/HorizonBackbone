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

        // Hash the password with sha256
        var hashedPass = crypto
            .createHash('sha256')
            .update(password)
            .digest('hex');

        axios
            .post('http://10.0.0.9:8002/users/login', {
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
