# Contributing to Iceberg AI

Thanks for your interest in improving Iceberg AI.

## Development workflow

1. Fork the repository.
2. Create a feature branch from the latest main branch.
3. Keep changes focused and easy to review.
4. Run the relevant validation commands before submitting your PR.
5. Open a pull request with a clear summary and testing notes.

## Local setup

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file using the example in `backend/.env.example`.

```powershell
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Validation

Before opening a pull request, run the project checks relevant to your area:

```powershell
cd backend
python -m compileall app

cd ../frontend
npx tsc --noEmit
```

## PR guidance

- Keep commits small and descriptive.
- Prefer readable, maintainable code over clever shortcuts.
- Add comments or docstrings when logic is non-obvious.
- Update relevant documentation when behavior changes.

## Code style

- Python: prefer readable function structure and explicit variable names.
- TypeScript: keep component logic simple and typed.
- Document public functions and non-trivial flows.
