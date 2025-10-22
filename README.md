# Credit Card Statement Parser

A full-stack application that extracts key data from credit card statements across 5 major issuers using Python (Flask) and React.

## Features

- **5 Supported Credit Card Issuers:**
  - Chase
  - American Express (Amex)
  - Citibank
  - Discover
  - Capital One

- **5 Extracted Data Points:**
  1. Card Issuer
  2. Card Last 4 Digits
  3. Statement Date
  4. Payment Due Date
  5. Total Balance
  6. Minimum Payment

- **Modern UI Features:**
  - Drag & drop PDF upload
  - Real-time parsing feedback
  - Clean, responsive design
  - Error handling

## Project Structure

```
pipe/
├── backend/
│   ├── app.py              # Flask API with PDF parsing logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Styling
│   │   ├── main.jsx       # React entry point
│   │   └── index.css      # Global styles
│   ├── index.html         # HTML template
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
└── README.md
```

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **pdfplumber** - PDF text extraction
- **flask-cors** - CORS handling

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Modern CSS** - Styling

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create a virtual environment (recommended):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install Python dependencies:
```powershell
pip install -r requirements.txt
```

4. Run the Flask server:
```powershell
python app.py
```

The backend will start at `http://localhost:5000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```powershell
cd frontend
```

2. Install Node dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm run dev
```

The frontend will start at `http://localhost:3000`

## Usage

1. **Start both servers** (backend on port 5000, frontend on port 3000)

2. **Open your browser** and go to `http://localhost:3000`

3. **Upload a PDF statement**:
   - Drag and drop a PDF file, or
   - Click to browse and select a file

4. **Click "Parse Statement"** to extract data

5. **View the results** displaying:
   - Credit card issuer
   - Card last 4 digits
   - Statement date
   - Payment due date
   - Total balance
   - Minimum payment

## How It Works

### Backend (PDF Parsing)
1. **File Upload**: Receives PDF via POST request
2. **Text Extraction**: Uses pdfplumber to extract text from all pages
3. **Issuer Detection**: Identifies the credit card issuer from keywords
4. **Data Extraction**: Uses regex patterns to find specific data points
5. **Response**: Returns JSON with extracted data

### Frontend (React UI)
1. **File Selection**: Accepts PDF through drag-drop or file picker
2. **API Call**: Sends PDF to backend via FormData
3. **Display Results**: Shows extracted data in a clean card layout
4. **Error Handling**: Displays user-friendly error messages

## API Endpoints

### `POST /api/parse`
Parses a credit card statement PDF

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file with key `file`

**Response:**
```json
{
  "status": "success",
  "issuer": "Chase",
  "card_last_4": "1234",
  "statement_date": "12/31/2023",
  "payment_due_date": "01/25/2024",
  "total_balance": "1,234.56",
  "minimum_payment": "35.00"
}
```

### `GET /api/supported-issuers`
Returns list of supported credit card issuers

### `GET /api/health`
Health check endpoint

## Extending the Parser

To add support for more credit card issuers:

1. Add a new parsing method in `backend/app.py`:
```python
def parse_new_issuer(self, text):
    return {
        'issuer': 'New Issuer',
        'card_last_4': self.extract_card_digits(text),
        # ... other fields
    }
```

2. Update the `parsers` dictionary in `__init__`:
```python
self.parsers = {
    # ... existing parsers
    'new_issuer': self.parse_new_issuer
}
```

3. Update the `detect_issuer` method to recognize the new issuer

## Testing

To test the parser:

1. Obtain sample PDF statements from supported issuers
2. Upload through the web interface
3. Verify extracted data matches the statement

**Note:** Due to privacy concerns, this repository does not include sample statements.

## Limitations

- Works best with standard statement formats
- May not extract data if PDF format significantly differs
- Requires clear, text-based PDFs (not scanned images)
- "Not found" displayed if a data point cannot be extracted

## Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Transaction detail extraction
- [ ] Export to CSV/JSON
- [ ] Batch processing multiple files
- [ ] Database storage
- [ ] User authentication
- [ ] Historical statement comparison

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check all dependencies are installed: `pip list`
- Try: `pip install --upgrade -r requirements.txt`

**Frontend won't start:**
- Ensure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again
- Try clearing npm cache: `npm cache clean --force`

**CORS errors:**
- Ensure backend is running on port 5000
- Check flask-cors is installed
- Verify frontend is making requests to `http://localhost:5000`

**Parsing errors:**
- Verify PDF is from a supported issuer
- Ensure PDF is text-based (not scanned image)
- Check console for detailed error messages

## License

This project is for educational purposes.

## Author

Created for the Credit Card Statement Parser Assignment
