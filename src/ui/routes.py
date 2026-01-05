from flask import Flask, render_template, request, redirect, url_for, flash
from src.db.connection import DatabaseConnection, DatabaseError
from src.repositories.author_repository import AuthorRepository
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.loan_repository import LoanRepository
from src.services.library_service import LibraryService
from src.services.import_service import ImportService
from datetime import datetime

CONFIG_PATH = "config/config.json"

def init_routes(app: Flask):
    db_conn = DatabaseConnection(CONFIG_PATH)
    library_service = LibraryService(db_conn)
    import_service = ImportService(db_conn)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/books")
    def books():
        try:
            with db_conn.transaction() as conn:
                book_repo = BookRepository(conn)
                author_repo = AuthorRepository(conn)

                books = book_repo.get_all()

                for book in books:
                    author = author_repo.get_by_id(book.author_id)
                    book.author_name = author.name if author else "Unknown"

            return render_template("books.html", books=books)
        except DatabaseError as e:
            flash(str(e))
            return redirect(url_for("index"))

    @app.route("/add_book", methods=["GET", "POST"])
    def add_book():
        if request.method == "POST":
            title = request.form["title"]
            author_name = request.form["author"]
            price = float(request.form["price"])
            published_date = datetime.strptime(request.form["published_date"], "%Y-%m-%d").date()

            try:
                with db_conn.transaction() as conn:
                    author_repo = AuthorRepository(conn)
                    book_repo = BookRepository(conn)
                    # Check if author exists
                    authors = [a for a in author_repo.get_all() if a.name == author_name]
                    if authors:
                        author_id = authors[0].id
                    else:
                        author_id = author_repo.add(type('Author', (), {'name': author_name})())

                    book_repo.add(type('Book', (), {
                        'title': title,
                        'author_id': author_id,
                        'price': price,
                        'available': True,
                        'published_date': published_date
                    })())
                    flash("Book added successfully!")
            except DatabaseError as e:
                flash(str(e))

            return redirect(url_for("books"))

        return render_template("add_book.html")

    @app.route("/loan_book", methods=["GET", "POST"])
    def loan_book():
        if request.method == "POST":
            book_id = int(request.form["book_id"])
            user_id = int(request.form["user_id"])
            try:
                library_service.loan_book(book_id, user_id)
                flash("Book loaned successfully!", "success")
            except DatabaseError as e:
                flash(str(e), "error")
            return redirect(url_for("loan_book"))

        return render_template("loan_book.html")

    @app.route("/return_book", methods=["POST"])
    def return_book():
        loan_id = int(request.form["loan_id"])
        try:
            library_service.return_book(loan_id)
            flash("Book returned successfully!")
        except DatabaseError as e:
            flash(str(e))
        return redirect(url_for("books"))

    @app.route("/import_json", methods=["GET", "POST"])
    def import_json():
        if request.method == "POST":
            file = request.files["file"]
            if not file:
                flash("No file selected!")
                return redirect(request.url)
            try:
                file_path = f"/tmp/{file.filename}"
                file.save(file_path)
                import_service.import_from_json(file_path)
                flash("JSON imported successfully!")
            except DatabaseError as e:
                flash(str(e))
            return redirect(url_for("index"))

        return render_template("import.html")

    @app.route("/report")
    def report():
        try:
            with db_conn.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vw_loan_report")
                report_data = cursor.fetchall()
            return render_template("report.html", report=report_data)
        except DatabaseError as e:
            flash(str(e))
            return redirect(url_for("index"))

