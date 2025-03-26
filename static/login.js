inputPassword = document.getElementById("input_password");
inputEmail = document.getElementById("input_email");

loginButton = document.getElementById("login_button");

async function login(email, password) {
    const response = await fetch('./api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email' : email,
            'password' : password
        })
    });
    if (response.status == 200) {
        return response.json();
    } else {
        return { code: 500, msg: 'Internal Error' };
    }
}

loginButton.addEventListener("click", async () => {
    const email = inputEmail.value;
    const password = inputPassword.value;

    if (email == "" || password == "") {
        alert("Fill all the fields");
        return;
    }

    try {
        const response = await login(email, password);
        if (response.code == 200) {
            localStorage.setItem('ACCESS_TOKEN', response.data.access_token);
            window.location.href = "/dashboard";
        } else {
            alert(response.msg);
        }
        console.log(response);
    } catch (error) {
        console.error('Error:', error);
    }

});

document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem('ACCESS_TOKEN')) {
        window.location.href = "/dashboard";
    }
});