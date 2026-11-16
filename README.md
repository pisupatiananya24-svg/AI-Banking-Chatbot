# AI Chatbot for Banking System

**B.Tech Third-Year Special Project**  
**Project title:** AI Chatbot for Banking System  
**Subtitle:** A data-driven customer support and complaint-resolution prototype

## 1. Project overview

This project is a web-based banking support prototype. A user logs in, views a sample banking dashboard and interacts with a chatbot through a floating chat window. The chatbot answers common banking questions by comparing words and phrases in the user's message with keywords stored in an SQLite FAQ table.

The application demonstrates a login-to-dashboard workflow, a Flask backend, a JavaScript chat interface and a database that can be extended with additional question-and-answer pairs.

> **Important:** This is an academic demonstration. It is not connected to a real bank, real customer account, payment network or live banking API. All account and transaction details are sample data.

## 2. Main features

- Login page with a demo account.
- Dashboard showing a sample customer name, masked account number, account type and balance.
- Recent-transaction display using SQLite.
- Floating chatbot button and popup chat interface.
- Quick-question buttons for common queries.
- Keyword-based FAQ matching in the Flask backend.
- `/add_answer` endpoint to add new FAQ keywords and answers to the database.
- Automatic creation of the SQLite database and initial demo records.

## 3. Technologies used

| Component | Technology | Purpose |
|---|---|---|
| Frontend | HTML | Login and dashboard structure |
| Styling | CSS | Responsive layout and visual design |
| Client-side logic | JavaScript | Chat window and API requests |
| Backend | Python, Flask | Routes, login session and chatbot logic |
| Database | SQLite | Demo customer, transactions and FAQ storage |
| Data exchange | JSON / Fetch API | Frontend-to-backend chat communication |

## 4. Project folder structure

```text
AI_Banking_Chatbot_Project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
└── static/
    ├── style.css
    └── chat.js
```

The `bank.db` database is generated automatically the first time the application runs. It is excluded from Git because it contains local demo data and can be recreated.

## 5. Requirements

- Python 3.10 or later
- pip (Python package installer)
- A modern web browser
- Internet connection only if the optional Google Fonts import in the CSS is to be loaded; the application itself runs locally

## 6. Installation instructions

### Step 1: Extract the project

Extract the ZIP file and open the `AI_Banking_Chatbot_Project` folder.

### Step 2: Open a terminal

Open Command Prompt or Terminal inside the project folder.

### Step 3: Create a virtual environment (recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

If the `pip` command is not recognised, use the `python -m pip` command shown above.

## 7. Execution steps

Run the application from the project folder:

```bash
python app.py
```

The terminal will display a local address. Open this URL in your browser:

```text
http://127.0.0.1:5000
```

1. Enter the demo login details.
2. The dashboard opens after successful login.
3. Select the circular **AI** button at the bottom-right.
4. Type a banking-related question or select a quick question.
5. The browser sends the message to the Flask `/chat` route.
6. Flask compares the message with the FAQ keywords stored in SQLite and returns a matching answer.

To stop the local server, press `Ctrl + C` in the terminal.

## 8. Demo login details

| Field | Demo value |
|---|---|
| Username | `ananya` |
| Password | `1234` |
| Account holder | Ananya Pisupati |
| Account number | XXXX XXXX 4582 |
| Account type | Savings Account |
| Sample balance | ₹48,750.00 |

These are demonstration credentials and values only. Do not use real banking credentials or personal financial information.

## 9. How the chatbot works

1. The user enters a question in the chat input.
2. `chat.js` sends the message as JSON to the `/chat` endpoint using the Fetch API.
3. Flask receives the message and converts it to lowercase.
4. Flask reads the stored keyword-and-answer pairs from the `faq` table in `bank.db`.
5. The backend checks which stored keywords appear in the user's message.
6. The answer with the strongest keyword match is returned as JSON.
7. JavaScript displays the answer in the chat window.

This version uses transparent keyword matching. It does **not** use a trained machine-learning model, an LLM or a live bank API. A question with unfamiliar wording may not match an existing keyword.

## 10. Adding new chatbot questions through the backend

The `/add_answer` route accepts a JSON request and stores a new FAQ entry in SQLite. The user must be logged in.

Example request using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/add_answer ^
  -H "Content-Type: application/json" ^
  -b cookies.txt ^
  -d "{\"keywords\":\"minimum balance, minimum account balance\",\"answer\":\"Please check the minimum-balance rules published by your bank.\"}"
```

The example above illustrates the request format. A valid authenticated session cookie is required. On macOS/Linux, replace the Windows line-continuation character `^` with `\`.

The endpoint expects:
- `keywords`: comma-separated words or phrases that may appear in a question.
- `answer`: the response the chatbot should display.

For a simple local test, you can also add a new row to the `faq` table using an SQLite database browser while the application is stopped.

## 11. Main application routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Redirects to login or dashboard |
| `/login` | GET, POST | Displays login page and checks demo credentials |
| `/dashboard` | GET | Displays customer information and transactions |
| `/chat` | POST | Matches the user's question with stored FAQ keywords |
| `/add_answer` | POST | Adds a new FAQ entry |
| `/logout` | GET | Clears the login session |

## 12. Database structure

The SQLite database contains three tables:

- **customers:** username, password, customer name, masked account number, account type and sample balance.
- **transactions:** customer username, description, amount, transaction type and date.
- **faq:** keywords and the answer associated with those keywords.

The database and initial records are created automatically by `initialize_database()` in `app.py`.

## 13. Dataset and related resources

This prototype does not require an external banking dataset. Its initial FAQ entries, customer profile and transactions are sample demonstration data generated by the application.

Optional public datasets for future NLP experimentation (not used by the current code):

- Banking77 customer-service intent dataset: https://huggingface.co/datasets/PolyAI/banking77
- CLINC150 intent-classification dataset: https://huggingface.co/datasets/clinc/clinc_oos

These datasets are intended for experimentation with intent classification. They are not real customer account records and should not be treated as live banking data.

## 14. Limitations

- The chatbot relies on keyword matching and may not understand every paraphrase.
- Account and transaction information is sample data.
- No real money transfer, bill payment, card blocking or banking operation is performed.
- The demo login uses simple sample credentials.
- The Flask development server and debug mode are for local development only.
- The `/add_answer` route is a prototype endpoint and would need administrator authorisation, stronger validation, rate limiting and audit logging before deployment.

## 15. Future enhancements

- Train and evaluate an intent-classification model for varied user phrasing.
- Add a verified knowledge base or retrieval-augmented generation (RAG).
- Add administrator authentication and a FAQ management interface.
- Add stronger password hashing, CSRF protection and secure session configuration.
- Integrate approved banking APIs only after authentication, authorisation and security review.
- Add multilingual and voice-based support.
- Add human escalation for sensitive, disputed or unresolved requests.

## 16. Conclusion

The project demonstrates how a web-based banking assistant can combine a login interface, dashboard, Flask backend, SQLite database and chatbot interface. It provides a simple and extendable first-level support prototype while highlighting the need for verified information, security controls and human assistance in real banking environments.

---

**Project:** AI Chatbot for Banking System  
**Student:** Ananya Pisupati  
**Programme:** B.Tech, Third Year
