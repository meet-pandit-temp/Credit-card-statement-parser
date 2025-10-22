from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re
from datetime import datetime
import io

app = Flask(__name__)
CORS(app)

class CreditCardParser:
    """Parser for extracting data from credit card statements"""
    
    def __init__(self):
        self.parsers = {
            'chase': self.parse_chase,
            'amex': self.parse_amex,
            'citibank': self.parse_citibank,
            'discover': self.parse_discover,
            'capital_one': self.parse_capital_one
        }
    
    def detect_issuer(self, text):
        """Detect the credit card issuer from PDF text"""
        text_lower = text.lower()
        
        if 'chase' in text_lower or 'jpmorgan' in text_lower:
            return 'chase'
        elif 'american express' in text_lower or 'amex' in text_lower:
            return 'amex'
        elif 'citibank' in text_lower or 'citi' in text_lower:
            return 'citibank'
        elif 'discover' in text_lower:
            return 'discover'
        elif 'capital one' in text_lower or 'capitalone' in text_lower:
            return 'capital_one'
        
        return 'unknown'
    
    def extract_date(self, text, patterns):
        """Extract date using multiple patterns"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return 'Not found'
    
    def extract_amount(self, text, patterns):
        """Extract monetary amount using multiple patterns"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return 'Not found'
    
    def extract_card_digits(self, text):
        """Extract last 4 digits of card"""
        patterns = [
            r'(?:card|account).*?(\d{4})',
            r'x{4,}(\d{4})',
            r'ending.*?(\d{4})',
            r'\*{4,}(\d{4})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return 'Not found'
    
    def parse_chase(self, text):
        """Parse Chase credit card statement"""
        return {
            'issuer': 'Chase',
            'card_last_4': self.extract_card_digits(text),
            'statement_date': self.extract_date(text, [
                r'statement\s+(?:closing\s+)?date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'closing\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'payment_due_date': self.extract_date(text, [
                r'payment\s+due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'total_balance': self.extract_amount(text, [
                r'new\s+balance[:\s]+\$?([\d,]+\.\d{2})',
                r'total\s+balance[:\s]+\$?([\d,]+\.\d{2})'
            ]),
            'minimum_payment': self.extract_amount(text, [
                r'minimum\s+payment[:\s]+\$?([\d,]+\.\d{2})',
                r'minimum\s+due[:\s]+\$?([\d,]+\.\d{2})'
            ])
        }
    
    def parse_amex(self, text):
        """Parse American Express statement"""
        return {
            'issuer': 'American Express',
            'card_last_4': self.extract_card_digits(text),
            'statement_date': self.extract_date(text, [
                r'closing\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'statement\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'payment_due_date': self.extract_date(text, [
                r'payment\s+due[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'total_balance': self.extract_amount(text, [
                r'total\s+balance[:\s]+\$?([\d,]+\.\d{2})',
                r'new\s+balance[:\s]+\$?([\d,]+\.\d{2})'
            ]),
            'minimum_payment': self.extract_amount(text, [
                r'minimum\s+payment[:\s]+\$?([\d,]+\.\d{2})',
                r'payment\s+due[:\s]+\$?([\d,]+\.\d{2})'
            ])
        }
    
    def parse_citibank(self, text):
        """Parse Citibank statement"""
        return {
            'issuer': 'Citibank',
            'card_last_4': self.extract_card_digits(text),
            'statement_date': self.extract_date(text, [
                r'statement\s+(?:closing\s+)?date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'closing\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'payment_due_date': self.extract_date(text, [
                r'payment\s+due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'total_balance': self.extract_amount(text, [
                r'new\s+balance[:\s]+\$?([\d,]+\.\d{2})',
                r'closing\s+balance[:\s]+\$?([\d,]+\.\d{2})'
            ]),
            'minimum_payment': self.extract_amount(text, [
                r'minimum\s+(?:payment\s+)?due[:\s]+\$?([\d,]+\.\d{2})',
                r'minimum\s+payment[:\s]+\$?([\d,]+\.\d{2})'
            ])
        }
    
    def parse_discover(self, text):
        """Parse Discover statement"""
        return {
            'issuer': 'Discover',
            'card_last_4': self.extract_card_digits(text),
            'statement_date': self.extract_date(text, [
                r'statement\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'closing\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'payment_due_date': self.extract_date(text, [
                r'payment\s+due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'total_balance': self.extract_amount(text, [
                r'new\s+balance[:\s]+\$?([\d,]+\.\d{2})',
                r'total\s+balance[:\s]+\$?([\d,]+\.\d{2})'
            ]),
            'minimum_payment': self.extract_amount(text, [
                r'minimum\s+payment[:\s]+\$?([\d,]+\.\d{2})',
                r'minimum\s+due[:\s]+\$?([\d,]+\.\d{2})'
            ])
        }
    
    def parse_capital_one(self, text):
        """Parse Capital One statement"""
        return {
            'issuer': 'Capital One',
            'card_last_4': self.extract_card_digits(text),
            'statement_date': self.extract_date(text, [
                r'statement\s+(?:closing\s+)?date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'closing\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'payment_due_date': self.extract_date(text, [
                r'payment\s+due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})',
                r'due\s+date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})'
            ]),
            'total_balance': self.extract_amount(text, [
                r'new\s+balance[:\s]+\$?([\d,]+\.\d{2})',
                r'statement\s+balance[:\s]+\$?([\d,]+\.\d{2})'
            ]),
            'minimum_payment': self.extract_amount(text, [
                r'minimum\s+payment[:\s]+\$?([\d,]+\.\d{2})',
                r'minimum\s+due[:\s]+\$?([\d,]+\.\d{2})'
            ])
        }
    
    def parse_pdf(self, pdf_file):
        """Main method to parse PDF and extract data"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                # Extract text from all pages
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"
                
                # Detect issuer
                issuer = self.detect_issuer(full_text)
                
                # Parse based on issuer
                if issuer in self.parsers:
                    result = self.parsers[issuer](full_text)
                    result['status'] = 'success'
                    return result
                else:
                    return {
                        'status': 'error',
                        'message': 'Unable to detect credit card issuer. Supported: Chase, Amex, Citibank, Discover, Capital One'
                    }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error parsing PDF: {str(e)}'
            }

@app.route('/api/parse', methods=['POST'])
def parse_statement():
    """API endpoint to parse credit card statement"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400
    
    try:
        # Parse the PDF
        parser = CreditCardParser()
        result = parser.parse_pdf(io.BytesIO(file.read()))
        
        if result.get('status') == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/supported-issuers', methods=['GET'])
def get_supported_issuers():
    """Get list of supported credit card issuers"""
    return jsonify({
        'issuers': [
            'Chase',
            'American Express',
            'Citibank',
            'Discover',
            'Capital One'
        ]
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
