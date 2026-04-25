from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import uuid
import os
from config import DB_CONFIG

app = Flask(__name__)


def get_db_connection():
    """Create and return a database connection."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def init_db():
    """Create the messages table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id VARCHAR(36) PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_viewed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


@app.route("/")
def index():
    """Home page - create a new message."""
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create_message():
    """Handle message creation, save to DB, return unique link."""
    content = request.form.get("message", "").strip()

    if not content:
        return render_template("index.html", error="Message cannot be empty.")

    if len(content) > 1000:
        return render_template("index.html", error="Message too long. Max 1000 characters.")

    message_id = str(uuid.uuid4())

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (id, content) VALUES (%s, %s)",
        (message_id, content)
    )
    conn.commit()
    cursor.close()
    conn.close()

    link = url_for("view_message", message_id=message_id, _external=True)
    return render_template("index.html", link=link)


@app.route("/view/<message_id>")
def view_message(message_id):
    """Show the message once, then delete it from DB."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch message
    cursor.execute(
        "SELECT * FROM messages WHERE id = %s AND is_viewed = FALSE",
        (message_id,)
    )
    message = cursor.fetchone()

    if not message:
        cursor.close()
        conn.close()
        return render_template("expired.html")

    # Mark as viewed, then delete
    cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template("view.html", content=message["content"])


@app.route("/health")
def health():
    """Health check endpoint for ALB target group."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
