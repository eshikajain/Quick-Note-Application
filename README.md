A full-stack Quick Note Application built using Python Flask, SQLite, HTML, CSS, and JavaScript. Features include user registration, secure login and logout, creating, viewing, editing, deleting, and searching personal notes with database integration.
# 📝 Quick Note Application

A simple and user-friendly **Quick Note Application** built using Python Flask, SQLite, HTML, CSS, and JavaScript. It allows users to securely register, log in, and manage their personal notes in one place.

## 🚀 Features

- **User Registration:** Create a new account.
- **User Login:** Log in using your registered credentials.
- **User Logout:** Securely log out of your account.
- **Add Notes:** Create and save personal notes.
- **View Notes:** Display all your saved notes.
- **Edit Notes:** Update existing notes whenever needed.
- **Delete Notes:** Remove notes you no longer need.
- **Search Notes:** Quickly find notes using the search feature.
- **Database Integration:** Store user accounts and notes using SQLite.
- **User-specific Notes:** Each user can access their own notes.

## 🛠️ Technologies Used

| Technology | Purpose |
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database management |
| HTML | Webpage structure |
| CSS | Styling and UI design |
| JavaScript | Frontend functionality |

## 📂 Project Structure

```text
Quick-Note-App/
│
├── app.py
├── notes.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/eshikajain/Quick-Note-Application.git
```

### 2. Open the Project Folder

```bash
cd Quick-Note-Application
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Flask

```bash
python -m pip install flask
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

Visit:

```text
http://127.0.0.1:5000
```

## 🗄️ Database

This project uses **SQLite** to store:

- User registration details
- User login information (passwords stored as hashes)
- Personal notes
- Note content and related user information

The database file `notes.db` is created automatically when the application runs.

## 🎯 Project Objective

The main objective of this project is to understand Flask backend development, frontend-backend communication, user authentication, CRUD operations, and database integration.

GitHub: [@eshikajain](https://github.com/eshikajain)

---

⭐ If you find this project useful, consider giving it a star!
