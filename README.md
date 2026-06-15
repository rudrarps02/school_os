# 🏫 School OS - Administrative & Admissions Ecosystem

School OS is a modern, responsive Flask web application designed to optimize internal school administrative processes, streamline candidate enrollment channels, and enforce strict secure workflow guardrails using **Role-Based Access Control (RBAC)**.

---

## ✨ Features Built & Secured

- **🔐 Multi-Role Authentication Gates:** Full session lifecycle tracking utilizing robust security protections via custom Flask-Login configurations.
- **🛡️ Secure Access Matrix Controls:** Complete functional partitioning between standard view-only (`Viewer`) staff accounts and master supervisor (`Admin`) accounts.
- **📊 Interactive Admissions Pipeline:** Data dashboards capturing total system logs, follow-ups, and active registrations mapped cleanly into interactive layout modules.
- **📦 Production-Grade Configuration:** Environment-variable parsing (`python-dotenv`) designed to separate hardcoded runtime architecture variables from production infrastructure secrets.

---

## 🛠️ Tech Stack & Architecture

- **Backend Logic:** Python 3.x, Flask Web Framework
- **Session Layer & Guards:** Flask-Login & Werkzeug Encryption Security
- **Database & Object Mapping:** SQLite Engine backed by Flask-SQLAlchemy (ORM)
- **Frontend Presentation Layer:** Jinja2 Template Compilation, Bootstrap 5 UI Framework

---

## 🚀 Installation & Local Environment Setup

Follow these structural steps to install and boot the system ecosystem locally on your development machine:

### 1. Clone the Repository Workspace
```bash
git clone [https://github.com/YOUR_USERNAME/school_os.git](https://github.com/YOUR_USERNAME/school_os.git)
cd school_os
