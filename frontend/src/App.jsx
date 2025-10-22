import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const supportedIssuers = [
    'HDFC',
    'ICICI',
    'SBI',
    'BOB',
    'AXIS'
  ];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (selectedFile) => {
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    } else {
      setError('Please select a PDF file');
      setFile(null);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/api/parse', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.message || 'Error parsing PDF');
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>Credit Card Statement Parser</h1>
          <p className="subtitle">Extract key data from your credit card statements</p>
        </header>

        <div className="supported-issuers">
          <h3>Supported Issuers:</h3>
          <div className="issuer-tags">
            {supportedIssuers.map((issuer) => (
              <span key={issuer} className="issuer-tag">{issuer}</span>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="upload-form">
          <div
            className={`drop-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="file-input"
              accept=".pdf"
              onChange={handleFileChange}
              className="file-input"
            />
            <label htmlFor="file-input" className="file-label">
              {file ? (
                <div className="file-info">
                  <svg className="icon" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" />
                  </svg>
                  <span className="file-name">{file.name}</span>
                  <button type="button" onClick={resetForm} className="remove-btn">
                    Remove
                  </button>
                </div>
              ) : (
                <div className="upload-prompt">
                  <svg className="icon" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
                  </svg>
                  <p>Drag and drop your PDF here, or click to browse</p>
                  <span className="file-hint">PDF files only</span>
                </div>
              )}
            </label>
          </div>

          {file && (
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Parsing...
                </>
              ) : (
                'Parse Statement'
              )}
            </button>
          )}
        </form>

        {error && (
          <div className="alert error">
            <svg className="alert-icon" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        {result && result.status === 'success' && (
          <div className="result-card">
            <h2>Extracted Data</h2>
            <div className="result-grid">
              <div className="result-item">
                <span className="result-label">Issuer</span>
                <span className="result-value">{result.issuer}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Card Last 4 Digits</span>
                <span className="result-value">**** {result.card_last_4}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Statement Date</span>
                <span className="result-value">{result.statement_date}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Payment Due Date</span>
                <span className="result-value">{result.payment_due_date}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Total Balance</span>
                <span className="result-value amount">${result.total_balance}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Minimum Payment</span>
                <span className="result-value amount">${result.minimum_payment}</span>
              </div>
            </div>
            <button onClick={resetForm} className="reset-btn">
              Parse Another Statement
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
