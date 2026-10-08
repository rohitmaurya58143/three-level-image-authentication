function showLogin() {

    document.getElementById("content").innerHTML = `
        <h2>Login</h2>

        <input type="text" placeholder="Username">
        <br><br>

        <input type="password" placeholder="Password">
        <br><br>

        <button>Continue</button>
    `;
}


function showRegister() {

    document.getElementById("content").innerHTML = `
        <h2>Register</h2>

        <input type="text" placeholder="Username">
        <br><br>

        <input type="email" placeholder="Email">
        <br><br>

        <input type="password" placeholder="Password">
        <br><br>

        <button>Register</button>
    `;
}