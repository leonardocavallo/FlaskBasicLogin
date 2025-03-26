const dashboardTitle = document.getElementById('title');
const logoutButton = document.getElementById('logout_button');

async function getDashboardData(access_token) {
    const response = await fetch('./api/dashboard', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
    });

    if (response.status == 200) {
        return response.json();
    } else {
        return { code: 500, msg: 'Internal Error' };
    }
}

function logout() {
    localStorage.removeItem('ACCESS_TOKEN');
    window.location.href = "/login";
}

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem('ACCESS_TOKEN');
    if (token) {
        const response = await getDashboardData(token);
        if (response.code == 200) {
            dashboardTitle.textContent = `Welcome ${response.data.username}`;
        } else {
            localStorage.removeItem('ACCESS_TOKEN');
            window.location.href = "/login";
        }
    } else {
        window.location.href = "/login";
    }
});


logoutButton.addEventListener("click", logout);