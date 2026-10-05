from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from database import get_db_connection, create_database
from werkzeug.utils import secure_filename
from uuid import uuid4
from pathlib import Path
import os

app = Flask(__name__)
app.secret_key = "ghrstu-find-development-key"

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
UPLOAD_FOLDER.mkdir(exist_ok=True)

create_database()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(image):
    if not image or not image.filename:
        return None

    if not allowed_file(image.filename):
        raise ValueError("Please upload a PNG, JPG, JPEG or WEBP image.")

    original = secure_filename(image.filename)
    extension = Path(original).suffix.lower()
    filename = f"{uuid4().hex}{extension}"
    image.save(UPLOAD_FOLDER / filename)
    return filename


def fetch_items(search="", item_type="", category="", limit=None):
    connection = get_db_connection()
    clauses = ["status = 'active'"]
    params = []

    if search:
        like = f"%{search}%"
        clauses.append(
            """(
                item_name LIKE ? OR
                description LIKE ? OR
                brand LIKE ? OR
                color LIKE ? OR
                location LIKE ? OR
                category LIKE ?
            )"""
        )
        params.extend([like] * 6)

    if item_type in {"lost", "found"}:
        clauses.append("item_type = ?")
        params.append(item_type)

    if category:
        clauses.append("category = ?")
        params.append(category)

    sql = """
        SELECT items.*, users.name AS reporter_name
        FROM items
        LEFT JOIN users ON users.id = items.user_id
        WHERE {where}
        ORDER BY datetime(items.created_at) DESC
    """.format(where=" AND ".join(clauses))

    if limit:
        sql += " LIMIT ?"
        params.append(limit)

    items = connection.execute(sql, params).fetchall()
    connection.close()
    return items


@app.route("/")
def home():
    search = request.args.get("q", "").strip()
    item_type = request.args.get("type", "").strip().lower()
    category = request.args.get("category", "").strip()

    items = fetch_items(search, item_type, category, limit=6)

    connection = get_db_connection()
    total = connection.execute(
        "SELECT COUNT(*) FROM items WHERE status = 'active'"
    ).fetchone()[0]
    lost = connection.execute(
        "SELECT COUNT(*) FROM items WHERE status = 'active' AND item_type = 'lost'"
    ).fetchone()[0]
    found = connection.execute(
        "SELECT COUNT(*) FROM items WHERE status = 'active' AND item_type = 'found'"
    ).fetchone()[0]
    returned = connection.execute(
        "SELECT COUNT(*) FROM items WHERE status = 'returned'"
    ).fetchone()[0]
    connection.close()

    recovery_rate = round((returned / (total + returned)) * 100) if (total + returned) else 0

    return render_template(
        "index.html",
        items=items,
        search=search,
        item_type=item_type,
        category=category,
        total=total,
        lost=lost,
        found=found,
        returned=returned,
        recovery_rate=recovery_rate,
    )


@app.route("/explore")
def explore():
    search = request.args.get("q", "").strip()
    item_type = request.args.get("type", "").strip().lower()
    category = request.args.get("category", "").strip()
    items = fetch_items(search, item_type, category)

    return render_template(
        "explore.html",
        items=items,
        search=search,
        item_type=item_type,
        category=category,
    )


@app.route("/item/<int:item_id>")
def item_detail(item_id):
    connection = get_db_connection()
    item = connection.execute(
        """
        SELECT items.*, users.name AS reporter_name
        FROM items
        LEFT JOIN users ON users.id = items.user_id
        WHERE items.id = ?
        """,
        (item_id,),
    ).fetchone()
    connection.close()

    if not item:
        return render_template("item.html", item=None), 404

    return render_template("item.html", item=item)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # image_path values from older versions may contain "uploads/" or Windows slashes.
    safe_name = os.path.basename(filename.replace("\\", "/"))
    return send_from_directory(app.config["UPLOAD_FOLDER"], safe_name)


@app.route("/report", methods=["GET", "POST"])
def report_item():
    if request.method == "POST":
        item_type = request.form.get("item_type", "lost").strip().lower()
        item_name = request.form.get("item_name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        color = request.form.get("color", "").strip()
        brand = request.form.get("brand", "").strip()
        identifying_marks = request.form.get("identifying_marks", "").strip()
        location = request.form.get("location", "").strip()
        date_reported = request.form.get("date_reported", "").strip()

        if item_type not in {"lost", "found"}:
            flash("Please choose Lost or Found.", "error")
            return redirect(url_for("report_item"))

        if not item_name or not description or not location or not date_reported:
            flash("Please fill all required fields.", "error")
            return redirect(url_for("report_item"))

        try:
            image_path = save_uploaded_image(request.files.get("image"))
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("report_item"))

        connection = get_db_connection()

        user = connection.execute(
            "SELECT id FROM users ORDER BY id LIMIT 1"
        ).fetchone()

        if not user:
            cursor = connection.execute(
                """
                INSERT INTO users (name, email, password, college_id, role)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "Demo Student",
                    "demo@ghrstu.ac.in",
                    "temporary",
                    "DEMO001",
                    "student",
                ),
            )
            user_id = cursor.lastrowid
        else:
            user_id = user["id"]

        connection.execute(
            """
            INSERT INTO items (
                user_id, item_type, item_name, category, description,
                color, brand, identifying_marks, location,
                date_reported, image_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                item_type,
                item_name,
                category,
                description,
                color,
                brand,
                identifying_marks,
                location,
                date_reported,
                image_path,
            ),
        )
        connection.commit()
        connection.close()

        flash("Your report is live on GHRSTU Find! 🎉", "success")
        return redirect(url_for("home"))

    return render_template("report.html")


if __name__ == "__main__":
    app.run(debug=True)
