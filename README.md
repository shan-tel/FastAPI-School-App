# FastAPI School APP

This is a backend application for a school management system. It provides the core functionality needed to handle user accounts, secure logins, and course creation. 

Features
User Accounts: Users can register, view, update, and delete their own profiles safely.

Security: A secure login system using hashed passwords and access tokens. It includes a refresh token system so users stay logged in without needing to enter their password constantly.

Roles and Permissions: The system recognizes different types of users (Admins, Teachers, and Students). For example, users can only edit their own profiles, while Admins have permission to view all users.

Technology Used

FastAPI: To build the web framework and routes.

PostgreSQL: To store all user and course data.

SQLAlchemy: To connect the Python code to the database.
Bcrypt and PyJWT: To protect user passwords and handle login security.
