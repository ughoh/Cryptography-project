# AES Cryptographer 🔐

A secure full-stack web application designed for file encryption and decryption using modern cryptographic standards. The project features a robust Python backend built with FastAPI and an interactive, clean user interface built with Vue 3 and Tailwind CSS v4.

## 🚀 Features

- **AES Encryption/Decryption**: Protects your files using reliable, industry-standard cryptographic algorithms.
- **Stream-based Processing**: Efficiently handles large file uploads and downloads using streaming responses.
- **Strict Validation**: Integrated Pydantic v2 validation ensuring secure, client-side and server-side data integrity (e.g., minimum 8-character password enforcement).
- **Modern UI/UX**: Sleek, cyberpunk-inspired dark mode interface with clean, decoupled JavaScript business logic (Vue Composables).

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Dependency & Package Management**: Poetry
- **Validation**: Pydantic v2
- **Server**: Uvicorn

### Frontend
- **Framework**: Vue 3 (Composition API / `<script setup>`)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS v4 (PostCSS)
- **HTTP Client**: Axios

---

## 📂 Project Structure

```text
cryptography_project/
├── backend/            # Python FastAPI backend (Isolated Poetry project)
│   ├── .venv/          # Local virtual environment
│   ├── app/
│   │   ├── api/        # API routers and endpoints (v1)
│   │   ├── core/       # Cryptography logic and configuration
│   │   └── main.py     # FastAPI application entry point
│   ├── poetry.lock
│   └── pyproject.toml
└── frontend/           # Vue 3 frontend (Vite project)
    ├── src/
    │   ├── assets/     # Global styles (Tailwind configuration)
    │   ├── components/ # UI Components (CryptoForm.vue)
    │   ├── composables/# Decoupled JS logic (useCrypto.js)
    │   └── App.vue
    ├── package.json
    └── postcss.config.js
```

## 🔧 Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- **Python (3.10+)**
- **Poetry**
- **Node.js (18+) & npm**

### 1. Backend Setup
- **Navigate to the backend directory from the root folder**: cd backend
- **Install all required dependencies using Poetry**: poetry install
- **Start the local development server using Uvicorn**: uvicorn app.main:app --reload
- **Backend server URL**: The backend server will run at http://127.0.0.1:8000.

### 2. Frontend Setup
- **Open a new terminal window and navigate to the frontend directory**: cd frontend
- **Install the project dependencies**: npm install
- **Start the Vite development server**: npm run dev
- **Frontend application URL**: The frontend application will be available at http://localhost:5173.

---

## 🌐 API & Proxy Configuration

- **Vite Proxy**: The frontend includes a pre-configured Vite Proxy to seamlessly handle requests to the FastAPI server and completely bypass CORS restrictions.
- **Routing**: Any frontend request starting with the /api prefix is automatically routed to http://127.0.0.1:8000.

### Endpoints
- **Encryption**: POST /api/v1/encrypt (Expects multipart/form-data with file and password)
- **Decryption**: POST /api/v1/decrypt (Expects multipart/form-data with file and password)

---

## 🛡️ License

- **Project License**: This project is open-source and available under the MIT License.