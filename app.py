from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
from pathlib import Path
from functools import wraps

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bank.db"

app = Flask(__name__)
app.secret_key = "replace-this-demo-secret-key-before-deployment"

DEMO_USERNAME = "ananya"
DEMO_PASSWORD = "1234"


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the demo account, transactions and editable FAQ table."""
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                account_number TEXT NOT NULL,
                account_type TEXT NOT NULL,
                balance REAL NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                transaction_date TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keywords TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)

        customer = db.execute(
            "SELECT id FROM customers WHERE username = ?", (DEMO_USERNAME,)
        ).fetchone()
        if customer is None:
            db.execute("""
                INSERT INTO customers
                (username, password, full_name, account_number, account_type, balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (DEMO_USERNAME, DEMO_PASSWORD, "Ananya Pisupati",
                  "XXXX XXXX 4582", "Savings Account", 48750.00))

            demo_transactions = [
                ("UPI transfer", 750.00, "debit", "2026-11-12"),
                ("Bill payment", 1850.00, "debit", "2026-11-10"),
                ("Monthly stipend", 12000.00, "credit", "2026-11-05")
            ]
            db.executemany("""
                INSERT INTO transactions
                (username, description, amount, transaction_type, transaction_date)
                VALUES (?, ?, ?, ?, ?)
            """, [(DEMO_USERNAME, *item) for item in demo_transactions])

        count = db.execute("SELECT COUNT(*) AS total FROM faq").fetchone()["total"]
        if count == 0:
            starter_faqs = [
                ("balance, account balance, how much money",
                 "Your available demo account balance is ₹48,750.00."),
                ("transaction, recent transactions, payment history",
                 "You can view your recent transactions in the Recent Activity section of your dashboard."),
                ("ifsc, IFSC code",
                 "The IFSC code is a demo value in this prototype. Please check your bank's official website for a real IFSC code."),
                ("loan, loans, apply for loan",
                 "Loan eligibility depends on your bank's policies and customer profile. Please contact an authorised bank representative."),
                ("debit card, credit card, card",
                 "For card activation, blocking or replacement, contact your bank through its official verified channel."),
                ("atm, cash, withdraw",
                 "You can use an authorised ATM to withdraw cash. Check your bank's official fee and withdrawal limits."),
                ("branch, bank location, address",
                 "Please use your bank's official branch locator to find a verified branch near you."),
                ("hello, hi, hey",
                 "Hello! Welcome to the banking assistant. How can I help you today?"),
                ("thank you, thanks",
                 "You're welcome! Let me know if you have another banking question.")
            ]
            db.executemany(
                "INSERT INTO faq (keywords, answer) VALUES (?, ?)", starter_faqs
            )


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/", methods=["GET"])
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with get_db() as db:
            customer = db.execute(
                "SELECT * FROM customers WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()

        if customer:
            session.clear()
            session["username"] = customer["username"]
            return redirect(url_for("dashboard"))

        flash("Invalid username or password. Please try again.", "error")
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    username = session["username"]
    with get_db() as db:
        customer = db.execute(
            "SELECT * FROM customers WHERE username = ?", (username,)
        ).fetchone()
        transactions = db.execute("""
            SELECT description, amount, transaction_type, transaction_date
            FROM transactions WHERE username = ?
            ORDER BY id DESC
        """, (username,)).fetchall()

    return render_template(
        "dashboard.html", customer=customer, transactions=transactions
    )


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("message", "")).strip().lower()

    if not question:
        return jsonify({"answer": "Please type a question so I can help."}), 400

    with get_db() as db:
        faqs = db.execute("SELECT keywords, answer FROM faq").fetchall()

    # Simple transparent keyword matching. This is not a trained ML model.
    best_answer = None
    best_score = 0
    question_words = set(question.replace("?", " ").replace(",", " ").split())

    for faq in faqs:
        keywords = [word.strip().lower() for word in faq["keywords"].split(",")]
        score = 0
        for keyword in keywords:
            if keyword and keyword in question:
                score += max(1, len(keyword.split()))
            elif keyword and keyword in question_words:
                score += 1
        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    if best_answer:
        return jsonify({"answer": best_answer})

    return jsonify({
        "answer": "Sorry, I don't have an answer for that yet. Please contact bank support for assistance, or ask the project administrator to add this question to the FAQ database."
    })


@app.route("/add_answer", methods=["POST"])
@login_required
def add_answer():
    """Add a question pattern and answer to the FAQ database."""
    data = request.get_json(silent=True) or {}
    keywords = str(data.get("keywords", "")).strip()
    answer = str(data.get("answer", "")).strip()

    if not keywords or not answer:
        return jsonify({"message": "Both keywords and answer are required."}), 400
    if len(keywords) > 500 or len(answer) > 2000:
        return jsonify({"message": "Input is too long."}), 400

    with get_db() as db:
        db.execute(
            "INSERT INTO faq (keywords, answer) VALUES (?, ?)",
            (keywords, answer)
        )
    return jsonify({"message": "New FAQ answer saved successfully."}), 201


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
