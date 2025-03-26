inputPassword = document.getElementById("input_password");
inputConfirmPassword = document.getElementById("input_confirm_password");
inputEmail = document.getElementById("input_email");
inputUsername = document.getElementById("input_username");

registerButton = document.getElementById("register_button");

function validateEmail (email){
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

async function register(email, username, password) {
    const response = await fetch('./api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email' : email,
            'password' : password,
            'username' : username
        })
    });
    if (response.status == 200) {
        return response.json();
    } else {
        return { code: 500, msg: 'Internal Error' };
    }
}

registerButton.addEventListener("click", async () => {
    const email = inputEmail.value;
    const password = inputPassword.value;
    const confirmPassword = inputConfirmPassword.value
    const username = inputUsername.value;
    
    if (password != confirmPassword) {
        alert("The passwords do not match");
        return;
    }

    if (email == "" || password == "" || username == "") { 
        alert("Fill all the fields");
        return;
    }

    if (password.length < 8) {
        alert("Password must be at least 8 characters long");
        return
    }

    if (!validateEmail(email)) {
        alert("Invalid email");
        return;
    }

    try {
        const response = await register(email, username, password);
        if (response.code == 200) {
            window.location.href = "/login";
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