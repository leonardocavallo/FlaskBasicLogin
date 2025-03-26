# FlaskBasicLogin 🚀
## Overview

FlaskBasicLogin is a simple web application that demonstrates a basic login system using Flask. It includes user registration, login, and logout functionalities.

## Features ✨

- User registration 📝
- User login 🔑
- User logout 🚪
- Password hashing for security 🔒
- Database with MongoDB 🗄️

## Installation 💻

1. Clone the repository:
    ```bash
    git clone https://github.com/leonardocavallo/FlaskBasicLogin
    ```
2. Navigate to the project directory:
    ```bash
    cd FlaskBasicLogin
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up environment variables**:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and change the following variables:
    - `JWT_SECRET_KEY`: Change this to a strong secret key.
    - `DB_CONNECTION_STRING`: Change this to your MongoDB connection string.

## Usage 🚀

1. Run the application:
    ```bash
    python main.py
    ```
2. Open your web browser and go to `http://127.0.0.1:5000/login`.

## License 📄

This project is licensed under the MIT License.