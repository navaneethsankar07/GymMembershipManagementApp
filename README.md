🏋️ Gym Management System
📌 Overview

This Gym Management System is a web-based application designed to simplify and digitize the operations of fitness centers. The platform focuses on providing a smooth interaction between gym owners and members by handling memberships, payments, and gym data in a structured and secure way. It aims to reduce manual work, improve transparency, and enhance the overall user experience for both administrators and users.

The system is built with scalability and maintainability in mind, making it suitable for single-gym setups as well as multi-gym environments.

🎯 Objectives

Simplify gym administration and member management

Enable secure and trackable membership payments

Provide role-based access for owners and members

Maintain accurate membership and payment records

Offer a clean and user-friendly API for future expansion

👥 User Roles
Gym Owner

Register and log in securely

Add and manage gyms

View enrolled members across owned gyms

Track payment history and payment status

Monitor membership activity

Member (User)

Register and log in securely

Browse available gyms

Purchase or renew gym memberships

View membership status and validity

Track personal payment history

🔑 Key Features
Authentication & Authorization

JWT-based authentication using access and refresh tokens

Role-based access control (Owner / User)

Secure login and signup workflows

Gym Management

Create and manage gym profiles

Associate gyms with specific owners

Public listing of available gyms

Membership Management

Membership activation and renewal

Automatic membership validity extension on payment

Membership status tracking (active / inactive)

Payment Management

Secure payment recording

Payment status tracking

Owner-level and user-level payment history

Pagination support for large datasets

API Design

RESTful API structure

Consistent response formats

Pagination for listing endpoints

Centralized configuration using constants

🧱 Tech Stack
Backend

Python

Django

Django REST Framework

Simple JWT (Authentication)

Database

PostgreSQL / SQLite (development)

Authentication

JSON Web Tokens (JWT)

Role-based access control

📁 Project Structure (High Level)
gym-management-system/
│
├── owners/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│
├── config/
│   └── constants.py
│
├── manage.py
└── requirements.txt

⚙️ Configuration

Static values such as roles, messages, field names, and membership duration are centralized in a configuration file to ensure consistency and easier maintenance.

Examples include:

User roles (owner, user)

Membership duration

Payment status values

Common response messages

🔄 Membership Flow

User registers and logs in

User selects a gym

Payment is recorded successfully

Membership is created or extended automatically

Membership remains active until the expiry date

📊 Pagination

Pagination is implemented across listing endpoints such as:

Members list (for owners)

Payment history (owners and users)

Gym listings

This ensures optimal performance and better handling of large datasets.

🔐 Security Considerations

Passwords are securely hashed

JWT tokens are used for session management

Role-based permissions restrict sensitive endpoints

Only gym owners can access owner-specific data
