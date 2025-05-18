# AvaxAudits Backend

This is the backend for **AvaxAudits**, an automated smart contract security audit tool focused on Avalanche and EVM-compatible blockchains. It provides RESTful APIs for uploading contracts, running automated analyses (using tools like Slither and Mythril), storing findings, and generating reports.

---

## Features

- **Smart Contract Upload & Management**
- **Automated Analysis**  
  - Integrates with Slither, Mythril, and custom Avalanche/EVM rule engines
- **Findings & Vulnerability Storage**
- **Audit Reports**  
  - Export as CSV or PDF
- **PostgreSQL Database with Alembic Migrations**
- **Async FastAPI Backend**
- **Background Task Processing**
- **Extensible Analyzer & Rule Engine Architecture**

---

## Project Structure

```
backend/
│
├── app/
│   ├── analyzers/           # Static analysis engines (Slither, Mythril, custom rules)
│   ├── db/                  # Database models and session management
│   ├── models/              # SQLAlchemy ORM models
│   ├── routers/             # FastAPI API routes
│   ├── services/            # Business logic/services
│   ├── tasks/               # Background task runners
│   └── utils/               # Utilities (optional)
│
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Getting Started

### 1. **Clone the repository**

```sh
git clone https://github.com/AHKAYY007/avaxaudits.git
cd avaxaudits/backend
```

### 2. **Install dependencies**

It is recommended to use a virtual environment:

```sh
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

### 3. **Configure environment variables**

Create a `.env` file in the `backend/` directory. Example:

```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/avaxaudits
```

### 4. **Run database migrations**

```sh
alembic upgrade head
```

### 5. **Start the FastAPI server**

```sh
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

---

## Usage

- **Upload a contract:**  
  `POST /contracts/`
- **Start an audit:**  
  `POST /audits/start`
- **Get audit status/results:**  
  `GET /audits/{audit_id}`  
  `GET /audits/{audit_id}/results`
- **Export reports:**  
  `GET /reports/export/csv`  
  `GET /reports/export/pdf`

See `/docs` for full API details.

---

## Development

- **Run tests:**  
  (If you have a `tests/` folder)
  ```sh
  pytest
  ```

- **Add new analyzers or rules:**  
  Implement in `app/analyzers/` or `app/analyzers/custom_rules/` and register in the rule engine.

---

## Requirements

- Python 3.10+
- PostgreSQL
- [Slither](https://github.com/crytic/slither) and [Mythril](https://github.com/ConsenSys/mythril) installed and available in your PATH for full analysis capabilities.

---

## License

MIT License

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Slither](https://github.com/crytic/slither)
- [Mythril](https://github.com/ConsenSys/mythril)

---

**Happy auditing!**