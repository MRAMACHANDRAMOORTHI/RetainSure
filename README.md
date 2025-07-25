# URL Shortener Service

A simple URL Shortener built using **Flask** as part of the RetainSure SDE Internship Assignment.

---

## ✅ Features
- Shorten long URLs into 6-character alphanumeric codes
- Redirect to original URL via short code
- Track click count and creation timestamp
- Validate URLs (must start with `http://` or `https://`)
- In-memory storage (dictionary)
- Thread-safe implementation using `threading.Lock`

---

## ✅ API Endpoints
### 1. Shorten URL
**POST** `/api/shorten`  
Request:
```json
{"url": "https://www.example.com"}
