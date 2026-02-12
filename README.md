# SecureDocs – Personal Document Manager

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-orange)](https://flask.palletsprojects.com/)

SecureDocs is a **web-based personal document manager** designed to help users securely upload, manage, and share documents. Built with **Python (Flask)** and a clean **HTML/CSS dashboard**, it demonstrates full-stack capabilities and product-focused design.

---

## 📝 Features

### Core Features (V1)
- **User Authentication:** Signup and Login with secure password hashing  
- **Document Management:** Upload, download, and delete personal documents  
- **Dashboard:** View a list of uploaded files with metadata (name, type, upload date)  
- **File Sharing:** Generate unique links to share specific documents  
- **Role Management:** Admin can see all documents; users see only their own  

### Optional Polished Features
- Search and filter files  
- Preview for PDFs and images  
- File type validation and size limits  
- Recent uploads chart and statistics  
- Expiring shareable links  

---

## 💻 Tech Stack

| Layer         | Technology           |
|---------------|-------------------|
| Backend       | Python 3 + Flask   |
| Frontend      | HTML, CSS, JavaScript, Bootstrap |
| Database      | SQLite             |
| File Storage  | Local `/uploads` folder |
| Security      | Password hashing, Role-based access |

---

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+  
- pip (Python package manager)  

### Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/yourusername/securedocs.git
cd securedocsory:

2.	Create a virtual environment:
     python -m venv venv

3.	Activate the environment: 
   	•	Windows: venv\Scripts\activate
	  •	Mac/Linux: source venv/bin/activate

4.	Install dependencies:  
     pip install -r requirements.txt

5.	Run the application:
     python app.py 

6.	Open your browser at http://127.0.0.1:5000

🔮 Future Improvements
	•	Cloud storage integration (AWS S3, Google Drive API)
	•	File encryption at rest
	•	Expiring shareable links
	•	Advanced dashboard analytics

📖 About

SecureDocs is designed as a learning project for full-stack beginners with a focus on product development and GitHub presentation. The project demonstrates clean architecture, role management, and full-stack integration.

This project is licensed under the MIT License. See LICENSE￼ for details.
