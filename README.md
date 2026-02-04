# 🏋️ Gym Management System

## 📌 Overview

**Gym Management System** is a web-based application designed to simplify and digitize the operations of fitness centers. The platform focuses on creating a smooth interaction between gym owners and members by managing **gyms, memberships, and payments** in a structured and secure way.

The system reduces manual work, improves transparency, and provides a reliable experience for both administrators and users.

---

## 🎯 Objectives

- **Simplify** gym administration and member management  
- Enable **secure and trackable** membership payments  
- Provide **role-based access control**  
- Maintain accurate **membership and payment records**  
- Offer a clean and scalable **REST API**

---

## 👥 User Roles

### 🧑‍💼 Gym Owner
- Register and log in securely  
- Add and manage gyms  
- View members across owned gyms  
- Track payment history and payment status  
- Monitor membership activity  

### 🧑‍🤝‍🧑 Member (User)
- Register and log in securely  
- Browse available gyms  
- Purchase or renew memberships  
- View membership status and validity  
- Track personal payment history  

---

## 🔑 Key Features

### 🔐 Authentication & Authorization
- JWT-based authentication (Access & Refresh tokens)  
- Role-based access control (Owner / User)  
- Secure signup and login workflows  

### 🏢 Gym Management
- Create and manage gym profiles  
- Associate gyms with specific owners  
- Public listing of available gyms  

### 📅 Membership Management
- Membership activation and renewal  
- Automatic validity extension after payment  
- Active / inactive membership tracking  

### 💳 Payment Management
- Secure payment recording  
- Payment status tracking  
- Owner-level and user-level payment history  
- Pagination support for large datasets  

### 🔗 API Design
- RESTful API architecture  
- Consistent request and response formats  
- Pagination for listing endpoints  
- Centralized configuration using constants  

---

## 🧱 Tech Stack

### Backend
- **Python**
- **Django**
- **Django REST Framework**
- **Simple JWT**

### Database
- **PostgreSQL** (Production)
- **SQLite** (Development)

### Authentication
- **JSON Web Tokens (JWT)**
- **Role-based permissions**

---

## 📁 Project Structure

```

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

```

---

## ⚙️ Configuration

All static values such as **roles, messages, field names, and membership duration** are centralized in a configuration file for better consistency and maintainability.

This includes:
- User roles  
- Membership duration  
- Payment status values  
- Common response messages  

---

## 🔄 Membership Flow

1. User registers and logs in  
2. User selects a gym  
3. Payment is recorded successfully  
4. Membership is created or extended automatically  
5. Membership remains active until expiry  

---

## 📊 Pagination

Pagination is implemented for:
- Member listings (owner view)  
- Payment history (owners and users)  
- Gym listings  

This ensures better performance and scalable data handling.

---

## 🔐 Security Considerations

- Passwords are **securely hashed**  
- JWT tokens handle authentication securely  
- Role-based permissions restrict sensitive endpoints  
- Owners can access only their own gym data  

---


## ⚡ Setup Instructions

1. Clone the repository  
2. Create and activate a virtual environment  
3. Install dependencies using `requirements.txt`  
4. Apply database migrations  
5. Run the development server  

---

## 📄 License

This project is intended for **educational and demonstration purposes**.  
Licensing can be added based on future usage requirements.
```
