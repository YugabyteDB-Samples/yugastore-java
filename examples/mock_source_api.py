#!/usr/bin/env python3
"""
Mock API Server for Source Documents

This simulates an API that serves original source documents
(transcripts, emails, design docs) for the specification verifier.

Run with: python3 mock_source_api.py
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import sys


# Mock database of source documents
SOURCE_DOCUMENTS = {
    'transcript-stakeholder-meeting-2024-01-15': {
        'id': 'transcript-stakeholder-meeting-2024-01-15',
        'type': 'transcript',
        'title': 'Stakeholder Meeting - Product Requirements',
        'date': '2024-01-15',
        'participants': ['John Doe (CEO)', 'Jane Smith (Product Owner)', 'Bob Wilson (CTO)'],
        'content': '''
Stakeholder Meeting Transcript
Date: January 15, 2024
Duration: 1 hour 30 minutes

John (CEO): We need a comprehensive e-commerce solution for our bookstore. The key features we discussed are:
1. Search functionality - users need to find books by title, author, or ISBN number
2. Shopping cart that persists even if they close their browser
3. Credit card payment processing
4. The cart should show running totals with tax included

Jane (Product Owner): Regarding the search, how fast should it be?

Bob (CTO): From a technical perspective, we should aim for sub-2-second response times for search queries. That's industry standard.

John: Agreed. Also, the shopping cart is critical - we lose a lot of sales when users come back and their cart is empty. This MUST persist across sessions.

Jane: What about user accounts?

Bob: We'll need basic authentication - email and password should suffice for MVP. Standard login functionality.

John: Make sure it's secure. We can't afford any security breaches.

Bob: Absolutely. Passwords will be encrypted, all payment data over HTTPS, the works.

Jane: Should we support guest checkout?

John: For MVP, let's require account creation. We want to build our user base.

[Discussion continues about payment processing, order confirmation emails, etc.]

Jane: One more thing - we need order history so users can see their past purchases.

Bob: That's straightforward. We'll add an orders page accessible after login.

John: Great. Let's move forward with these requirements.
        '''
    },
    
    'email-product-owner-001': {
        'id': 'email-product-owner-001',
        'type': 'email',
        'title': 'RE: Search Results Display',
        'date': '2024-01-16',
        'participants': ['Jane Smith (Product Owner)', 'Design Team'],
        'content': '''
From: Jane Smith <jane.smith@company.com>
To: Design Team <design@company.com>
Date: January 16, 2024
Subject: RE: Search Results Display

Hi team,

Following up on yesterday's stakeholder meeting, I wanted to clarify the search results page requirements:

1. Each search result MUST display:
   - Book title
   - Author name
   - Book cover image (this is critical for user experience)
   - Price
   - Average rating (if available)

2. The cover images should be prominently displayed - research shows that visual browsing significantly increases conversion rates.

3. Results should be in a grid layout on desktop, single column on mobile.

4. Include a "Add to Cart" button directly on each result.

Let me know if you have any questions.

Best,
Jane
        '''
    },
    
    'email-cto-performance-requirements': {
        'id': 'email-cto-performance-requirements',
        'type': 'email',
        'title': 'Performance Requirements and SLAs',
        'date': '2024-01-18',
        'participants': ['Bob Wilson (CTO)', 'Engineering Team'],
        'content': '''
From: Bob Wilson <bob.wilson@company.com>
To: Engineering Team <engineering@company.com>
Date: January 18, 2024
Subject: Performance Requirements and SLAs

Team,

I'm establishing the following performance requirements for the bookstore application:

HARD REQUIREMENTS:
1. Homepage load time: MUST be under 3 seconds (measured at 50th percentile)
2. Search results: MUST return within 2 seconds
3. API response times: 95th percentile must be under 200ms
4. System must handle minimum 500 concurrent users without degradation

TARGETS (not hard requirements):
- 99th percentile API responses under 500ms
- Support up to 1000 concurrent users
- Homepage under 2 seconds for 95th percentile

These are non-negotiable for production launch. Build the infrastructure accordingly.

If we can't meet these with current architecture, we need to discuss scaling options NOW, not after launch.

Bob
        '''
    },
    
    'transcript-security-review-2024-01-25': {
        'id': 'transcript-security-review-2024-01-25',
        'type': 'transcript',
        'title': 'Security Review Meeting',
        'date': '2024-01-25',
        'participants': ['Bob Wilson (CTO)', 'Security Team', 'Compliance Officer'],
        'content': '''
Security Review Meeting Transcript
Date: January 25, 2024

Bob (CTO): Let's go through the security requirements systematically.

Security Lead: First, authentication. We need to ensure passwords are properly secured.

Bob: Absolutely. bcrypt with appropriate cost factor. NO plaintext storage, obviously.

Compliance: Agreed. Also, session management is critical. What's the timeout?

Security Lead: I recommend 30 minutes of inactivity. That's standard for e-commerce.

Bob: Fine. Make sure sessions are using cryptographically secure random tokens. No predictable session IDs.

Security Lead: Understood. What about logging?

Bob: Good point. We need to log authentication attempts for security monitoring, BUT we must NEVER log sensitive data. No passwords, no credit card numbers, no CVV codes in logs. Ever.

Compliance: That's a compliance requirement too. GDPR, PCI-DSS - both prohibit logging sensitive personal data.

Bob: I want this in the security requirements document explicitly. "Sensitive data must never appear in logs." Make it clear.

Security Lead: Will do. What about SQL injection protection?

Bob: Mandatory. Use parameterized queries everywhere. No string concatenation for SQL.

[Discussion continues about HTTPS, payment security, etc.]

Compliance: One more thing - we need to ensure color contrast meets WCAG standards for accessibility.

Bob: That's more of a design requirement, but yes, let's include it. WCAG 2.1 AA compliance minimum.
        '''
    },
    
    'email-support-team-feedback': {
        'id': 'email-support-team-feedback',
        'type': 'email',
        'title': 'User Feedback - Password Reset Feature Request',
        'date': '2024-01-22',
        'participants': ['Support Team Lead', 'Jane Smith (Product Owner)'],
        'content': '''
From: Support Team <support@company.com>
To: Jane Smith <jane.smith@company.com>
Date: January 22, 2024
Subject: User Feedback - Password Reset Feature Request

Hi Jane,

We've been collecting feedback from our beta users and there's one feature that's been requested repeatedly:

CRITICAL: Password reset functionality via email

Users are getting locked out of their accounts and we have no automated way to help them reset their passwords. Currently, we're manually resetting them which is:
1. Time-consuming for support
2. Security risk (we shouldn't be handling user passwords)
3. Poor user experience

Can we prioritize this for the MVP? It should be standard functionality:
- User clicks "Forgot Password"
- We send them a secure reset link via email
- Link is time-limited (1 hour is standard)
- They set a new password

This is really important for launch. We can't scale support if we're manually handling password resets.

Thanks,
Support Team Lead
        '''
    },
    
    'doc-security-requirements-v2': {
        'id': 'DOC:security-requirements-v2',
        'type': 'design_doc',
        'title': 'Security Requirements Document v2',
        'date': '2024-01-26',
        'participants': ['Security Team', 'Engineering'],
        'content': '''
SECURITY REQUIREMENTS DOCUMENT
Version: 2.0
Date: January 26, 2024
Status: APPROVED

1. AUTHENTICATION

1.1 User Registration
- System MUST support email + password registration
- Password minimum requirements:
  * Minimum 8 characters
  * At least one uppercase letter
  * At least one lowercase letter  
  * At least one number
- Passwords MUST be hashed using bcrypt (cost factor 12 minimum)
- NEVER store passwords in plaintext

1.2 User Login
- Users SHALL authenticate with email and password
- Failed login attempts MUST be logged (timestamp, email, IP - NOT password)
- Account lockout after 5 failed attempts in 15 minutes
- Session timeout: 30 minutes of inactivity
- Session tokens MUST be cryptographically secure (256-bit random minimum)

1.3 Password Reset
- Support password reset via email
- Reset tokens valid for 1 hour maximum
- Tokens single-use only
- Old password immediately invalidated

2. SQL INJECTION PROTECTION

- ALL database queries MUST use parameterized statements
- NO string concatenation for SQL construction
- Input validation on all user-provided data

3. LOGGING RESTRICTIONS

CRITICAL: The following MUST NEVER appear in logs:
- Passwords (plaintext or hashed)
- Credit card numbers
- CVV codes
- Social Security Numbers
- Any PII classified as sensitive

Log authentication events but exclude passwords.

4. FAILED AUTHENTICATION HANDLING

Log failed login attempts with:
- Timestamp
- Username/email (obfuscated if needed)
- IP address
- User agent
- Result code

DO NOT LOG:
- The password that was attempted
- Any guessed passwords
        '''
    },
    
    'email-accessibility-audit': {
        'id': 'email-accessibility-audit',
        'type': 'email',
        'title': 'Accessibility Audit Results and Requirements',
        'date': '2024-01-30',
        'participants': ['Accessibility Team', 'Design Team'],
        'content': '''
From: Accessibility Team <accessibility@company.com>
To: Design Team <design@company.com>, Engineering <engineering@company.com>
Date: January 30, 2024
Subject: Accessibility Audit Results and Requirements

Team,

We've completed our accessibility audit and have the following requirements for the bookstore application:

WCAG 2.1 AA COMPLIANCE (MANDATORY):

1. Color Contrast
   - Normal text: Minimum 4.5:1 contrast ratio
   - Large text (18pt+): Minimum 3:1 contrast ratio
   - Test all text against background colors
   
2. Screen Reader Support
   - All images MUST have alt text
   - Semantic HTML5 elements throughout
   - ARIA labels on interactive elements
   - Form inputs properly labeled
   - Skip navigation links
   
3. Keyboard Navigation
   - All interactive elements keyboard accessible
   - Visible focus indicators
   - Logical tab order
   
4. Error Identification
   - Form validation errors clearly identified
   - Errors announced to screen readers
   - Color not the only indicator of errors

These are not optional - they're legal requirements in many jurisdictions and part of our corporate policy.

Please ensure all designs meet these standards before implementation.

Best,
Accessibility Team
        '''
    }
}


class SourceDocumentHandler(BaseHTTPRequestHandler):
    """HTTP request handler for source documents API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # Check for /documents/{doc_id} endpoint
        if len(path_parts) == 2 and path_parts[0] == 'documents':
            doc_id = path_parts[1]
            self.serve_document(doc_id)
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_document(self, doc_id: str):
        """Serve a source document by ID"""
        # Check authorization (simple bearer token check)
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            self.send_error(401, "Unauthorized - Missing or invalid token")
            return
        
        # Look up document (handle both formats: with and without prefix)
        doc = None
        if doc_id in SOURCE_DOCUMENTS:
            doc = SOURCE_DOCUMENTS[doc_id]
        else:
            # Try with DOC: prefix removed
            clean_id = doc_id.replace('DOC:', '').replace('SRC:', '').replace('SOURCE:', '')
            if clean_id in SOURCE_DOCUMENTS:
                doc = SOURCE_DOCUMENTS[clean_id]
        
        if not doc:
            self.send_error(404, f"Document {doc_id} not found")
            return
        
        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(doc, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[API] {self.address_string()} - {format % args}")


def main():
    port = 8888
    server_address = ('', port)
    httpd = HTTPServer(server_address, SourceDocumentHandler)
    
    print("="*60)
    print("Mock Source Document API Server")
    print("="*60)
    print(f"Server running on http://localhost:{port}")
    print(f"\nAvailable documents ({len(SOURCE_DOCUMENTS)}):")
    for doc_id, doc in SOURCE_DOCUMENTS.items():
        print(f"  - {doc_id} ({doc['type']}): {doc['title']}")
    print(f"\nEndpoint: GET /documents/{{doc_id}}")
    print(f"Authorization: Bearer YOUR_TOKEN")
    print(f"\nExample:")
    print(f"  curl -H 'Authorization: Bearer test-token' \\")
    print(f"       http://localhost:{port}/documents/transcript-stakeholder-meeting-2024-01-15")
    print(f"\nPress Ctrl+C to stop")
    print("="*60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    main()


