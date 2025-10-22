# Quick Start Guide

## Setup (5 minutes)

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### Frontend (New Terminal)
```powershell
cd frontend
npm install
npm run dev
```

## Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Test
1. Open http://localhost:3000
2. Upload a credit card PDF statement
3. Click "Parse Statement"
4. View extracted data

## Supported Issuers
- Chase
- American Express
- Citibank
- Discover
- Capital One

## Extracted Data
- Card Issuer
- Card Last 4 Digits
- Statement Date
- Payment Due Date
- Total Balance
- Minimum Payment
