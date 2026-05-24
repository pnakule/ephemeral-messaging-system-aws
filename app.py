from flask import Flask, render_template, request, url_for, jsonify, abort
import mysql.connector
import uuid
from datetime import datetime, timedelta
from config import DB_CONFIG

app = Flask(__name__)

@app.before_request
def restrict_access():

    if request.path == "/health":
        return

 #   if request.headers.get("xxx") != "xxx":
 #      abort(403)

# ── Database ──────────────────────────────────────────────────────────────────
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id VARCHAR(36) PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 HOUR),
            is_viewed BOOLEAN DEFAULT FALSE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create_message():

    content = request.form.get("message", "").strip()

    if not content:
        return render_template(
            "index.html",
            error="Message cannot be empty."
        )

    if len(content) > 1000:
        return render_template(
            "index.html",
            error="Message too long. Max 1000 characters."
        )

    message_id = str(uuid.uuid4())

    # Message expires after 1 hour
    expires_at = datetime.utcnow() + timedelta(hours=1)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (id, content, expires_at)
        VALUES (%s, %s, %s)
        """,
        (message_id, content, expires_at)
    )

    conn.commit()

    cursor.close()
    conn.close()

    link = url_for(
        "view_message",
        message_id=message_id,
        _external=True
    )

    return render_template("index.html", link=link)


@app.route("/view/<message_id>")
def view_message(message_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM messages
        WHERE id = %s
        AND is_viewed = FALSE
        AND expires_at > NOW()
        """,
        (message_id,)
    )

    message = cursor.fetchone()

    if not message:
        cursor.close()
        conn.close()
        return render_template("expired.html")

    # Delete message after first view
    cursor.execute(
        "DELETE FROM messages WHERE id = %s",
        (message_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return render_template(
        "view.html",
        content=message["content"]
    )


@app.route("/health")
def health():

    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "healthy"
        }), 200

    except Exception as e:

        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=False)
