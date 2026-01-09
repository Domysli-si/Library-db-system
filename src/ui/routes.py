from flask import Flask, render_template, request, redirect, url_for, flash
from src.db.connection import DatabaseConnection, DatabaseError
from src.repositories.author_repository import AuthorRepository
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.book_category_repository import BookCategoryRepository
from src.services.library_service import LibraryService
from src.services.import_service import ImportService
from src.models.author import Author
from src.models.book import Book
from src.models.category import Category
from src.models.library_user import LibraryUser
from datetime import datetime

CONFIG_PATH = "config/config.json"

def init_routes(app: Flask):
    try:
        db_conn = DatabaseConnection(CONFIG_PATH)
    except DatabaseError as e:
        print(f"FATAL ERROR: {e}")
        print("Please check config/config.json file")
        exit(1)

    library_service = LibraryService(db_conn)
    import_service = ImportService(db_conn)

    @app.route("/")
    def index():
        return render_template("index.html")

    # ========== BOOKS ==========
    @app.route("/books")
    def books():
        try:
            with db_conn.transaction() as conn:
                book_repo = BookRepository(conn)
                author_repo = AuthorRepository(conn)
                bc_repo = BookCategoryRepository(conn)
                cat_repo = CategoryRepository(conn)

                books = book_repo.get_all()
                for book in books:
                    author = author_repo.get_by_id(book.author_id)
                    book.author_name = author.name if author else "Unknown"
                    
                    # Get categories
                    cat_ids = bc_repo.get_categories_for_book(book.id)
                    cats = [cat_repo.get_by_id(cid) for cid in cat_ids]
                    book.categories = [c.name for c in cats if c]

            return render_template("books.html", books=books)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/add_book_with_categories", methods=["GET", "POST"])
    def add_book_with_categories():
        """BOD 4: Vložení do více tabulek najednou (book + book_category)"""
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            author_name = request.form.get("author", "").strip()
            price_str = request.form.get("price", "").strip()
            published_date_str = request.form.get("published_date", "").strip()
            category_ids = request.form.getlist("categories")

            errors = []
            if not title:
                errors.append("Title is required")
            if not author_name:
                errors.append("Author is required")
            if not price_str:
                errors.append("Price is required")
            if not published_date_str:
                errors.append("Published date is required")
            if not category_ids:
                errors.append("At least one category must be selected")

            try:
                price = float(price_str)
                if price < 0:
                    errors.append("Price must be positive")
            except ValueError:
                errors.append("Price must be a valid number")

            try:
                published_date = datetime.strptime(published_date_str, "%Y-%m-%d").date()
            except ValueError:
                errors.append("Invalid date format")

            if errors:
                for err in errors:
                    flash(err, "error")
                return redirect(url_for("add_book_with_categories"))

            try:
                with db_conn.transaction() as conn:
                    author_repo = AuthorRepository(conn)
                    book_repo = BookRepository(conn)
                    bc_repo = BookCategoryRepository(conn)

                    # Get or create author
                    authors = [a for a in author_repo.get_all() if a.name == author_name]
                    if authors:
                        author_id = authors[0].id
                    else:
                        author = Author(name=author_name)
                        author_id = author_repo.add(author)

                    # Add book
                    book = Book(
                        title=title,
                        author_id=author_id,
                        price=price,
                        available=True,
                        published_date=published_date
                    )
                    book_id = book_repo.add(book)

                    # Add categories (M:N)
                    for cat_id in category_ids:
                        bc_repo.add(book_id, int(cat_id))

                    flash("Book with categories added successfully!", "success")
            except DatabaseError as e:
                flash(f"Database error: {e}", "error")

            return redirect(url_for("books"))

        # GET - show form
        try:
            with db_conn.transaction() as conn:
                cat_repo = CategoryRepository(conn)
                categories = cat_repo.get_all()
            return render_template("add_book_with_categories.html", categories=categories)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
    def edit_book(book_id):
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            price_str = request.form.get("price", "").strip()
            available = request.form.get("available") == "1"

            errors = []
            if not title:
                errors.append("Title is required")
            try:
                price = float(price_str)
            except ValueError:
                errors.append("Invalid price")

            if errors:
                for err in errors:
                    flash(err, "error")
                return redirect(url_for("edit_book", book_id=book_id))

            try:
                with db_conn.transaction() as conn:
                    book_repo = BookRepository(conn)
                    book = book_repo.get_by_id(book_id)
                    if not book:
                        flash("Book not found", "error")
                        return redirect(url_for("books"))
                    
                    book.title = title
                    book.price = price
                    book.available = available
                    book_repo.update(book)
                    flash("Book updated successfully!", "success")
            except DatabaseError as e:
                flash(f"Database error: {e}", "error")

            return redirect(url_for("books"))

        # GET
        try:
            with db_conn.transaction() as conn:
                book_repo = BookRepository(conn)
                book = book_repo.get_by_id(book_id)
                if not book:
                    flash("Book not found", "error")
                    return redirect(url_for("books"))
            return render_template("edit_book.html", book=book)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("books"))

    @app.route("/delete_book/<int:book_id>", methods=["POST"])
    def delete_book(book_id):
        try:
            with db_conn.transaction() as conn:
                book_repo = BookRepository(conn)
                bc_repo = BookCategoryRepository(conn)
                
                # Delete M:N relations first
                cat_ids = bc_repo.get_categories_for_book(book_id)
                for cat_id in cat_ids:
                    bc_repo.remove(book_id, cat_id)
                
                # Delete book
                book_repo.delete(book_id)
                flash("Book deleted successfully!", "success")
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
        
        return redirect(url_for("books"))

    # ========== AUTHORS ==========
    @app.route("/authors")
    def authors():
        try:
            with db_conn.transaction() as conn:
                author_repo = AuthorRepository(conn)
                authors = author_repo.get_all()
            return render_template("authors.html", authors=authors)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/add_author", methods=["GET", "POST"])
    def add_author():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Name is required", "error")
                return redirect(url_for("add_author"))

            try:
                with db_conn.transaction() as conn:
                    author_repo = AuthorRepository(conn)
                    author = Author(name=name)
                    author_repo.add(author)
                    flash("Author added successfully!", "success")
            except DatabaseError as e:
                flash(f"Database error: {e}", "error")

            return redirect(url_for("authors"))

        return render_template("add_author.html")

    @app.route("/delete_author/<int:author_id>", methods=["POST"])
    def delete_author(author_id):
        try:
            with db_conn.transaction() as conn:
                author_repo = AuthorRepository(conn)
                author_repo.delete(author_id)
                flash("Author deleted successfully!", "success")
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
        
        return redirect(url_for("authors"))

    # ========== USERS ==========
    @app.route("/users")
    def users():
        try:
            with db_conn.transaction() as conn:
                user_repo = UserRepository(conn)
                users = user_repo.get_all()
            return render_template("users.html", users=users)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/add_user", methods=["GET", "POST"])
    def add_user():
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()

            errors = []
            if not full_name:
                errors.append("Full name is required")
            if not email:
                errors.append("Email is required")
            elif "@" not in email:
                errors.append("Invalid email format")

            if errors:
                for err in errors:
                    flash(err, "error")
                return redirect(url_for("add_user"))

            try:
                with db_conn.transaction() as conn:
                    user_repo = UserRepository(conn)
                    user = LibraryUser(
                        full_name=full_name,
                        email=email,
                        active=True,
                        created_at=datetime.now()
                    )
                    user_repo.add(user)
                    flash("User added successfully!", "success")
            except DatabaseError as e:
                flash(f"Database error: {e}", "error")

            return redirect(url_for("users"))

        return render_template("add_user.html")

    @app.route("/delete_user/<int:user_id>", methods=["POST"])
    def delete_user(user_id):
        try:
            with db_conn.transaction() as conn:
                user_repo = UserRepository(conn)
                user_repo.delete(user_id)
                flash("User deleted successfully!", "success")
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
        
        return redirect(url_for("users"))

    # ========== CATEGORIES ==========
    @app.route("/categories")
    def categories():
        try:
            with db_conn.transaction() as conn:
                cat_repo = CategoryRepository(conn)
                categories = cat_repo.get_all()
            return render_template("categories.html", categories=categories)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/add_category", methods=["GET", "POST"])
    def add_category():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            category_type = request.form.get("category_type", "").strip()

            errors = []
            if not name:
                errors.append("Name is required")
            if category_type not in ["fiction", "nonfiction", "study"]:
                errors.append("Invalid category type")

            if errors:
                for err in errors:
                    flash(err, "error")
                return redirect(url_for("add_category"))

            try:
                with db_conn.transaction() as conn:
                    cat_repo = CategoryRepository(conn)
                    category = Category(name=name, category_type=category_type)
                    cat_repo.add(category)
                    flash("Category added successfully!", "success")
            except DatabaseError as e:
                flash(f"Database error: {e}", "error")

            return redirect(url_for("categories"))

        return render_template("add_category.html")

    # ========== LOANS ==========
    @app.route("/loans")
    def loans():
        try:
            with db_conn.transaction() as conn:
                loan_repo = LoanRepository(conn)
                book_repo = BookRepository(conn)
                user_repo = UserRepository(conn)

                loans = loan_repo.get_all()
                for loan in loans:
                    book = book_repo.get_by_id(loan.book_id)
                    user = user_repo.get_by_id(loan.user_id)
                    loan.book_title = book.title if book else "Unknown"
                    loan.user_name = user.full_name if user else "Unknown"

            return render_template("loans.html", loans=loans)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/loan_book", methods=["GET", "POST"])
    def loan_book():
        if request.method == "POST":
            book_id_str = request.form.get("book_id", "").strip()
            user_id_str = request.form.get("user_id", "").strip()

            errors = []
            try:
                book_id = int(book_id_str)
                user_id = int(user_id_str)
            except ValueError:
                errors.append("Invalid book or user ID")

            if errors:
                for err in errors:
                    flash(err, "error")
                return redirect(url_for("loan_book"))

            try:
                library_service.loan_book(book_id, user_id)
                flash("Book loaned successfully!", "success")
            except (DatabaseError, ValueError) as e:
                flash(f"Error: {e}", "error")
            
            return redirect(url_for("loans"))

        return render_template("loan_book.html")

    @app.route("/return_book/<int:loan_id>", methods=["POST"])
    def return_book(loan_id):
        try:
            library_service.return_book(loan_id)
            flash("Book returned successfully!", "success")
        except (DatabaseError, ValueError) as e:
            flash(f"Error: {e}", "error")
        
        return redirect(url_for("loans"))

    # ========== IMPORT ==========
    @app.route("/import_json", methods=["GET", "POST"])
    def import_json():
        if request.method == "POST":
            file = request.files.get("file")
            if not file or file.filename == "":
                flash("No file selected!", "error")
                return redirect(url_for("import_json"))

            if not file.filename.endswith(".json"):
                flash("File must be JSON format", "error")
                return redirect(url_for("import_json"))

            try:
                file_path = f"/tmp/{file.filename}"
                file.save(file_path)
                import_service.import_from_json(file_path)
                flash("JSON imported successfully!", "success")
            except DatabaseError as e:
                flash(f"Import error: {e}", "error")
            
            return redirect(url_for("index"))

        return render_template("import.html")

    # ========== REPORTS ==========
    @app.route("/report")
    def report():
        """BOD 7: Report ze 3+ tabulek s agregacemi"""
        try:
            with db_conn.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        a.name AS author_name,
                        c.category_type,
                        COUNT(DISTINCT b.id) AS total_books,
                        AVG(b.price) AS avg_price,
                        MIN(b.price) AS min_price,
                        MAX(b.price) AS max_price,
                        SUM(CASE WHEN b.available = 1 THEN 1 ELSE 0 END) AS available_books
                    FROM book b
                    JOIN author a ON b.author_id = a.id
                    LEFT JOIN book_category bc ON b.id = bc.book_id
                    LEFT JOIN category c ON bc.category_id = c.id
                    GROUP BY a.name, c.category_type
                    ORDER BY total_books DESC
                """)
                report_data = cursor.fetchall()
            return render_template("report.html", report=report_data)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))

    @app.route("/loan_report")
    def loan_report():
        """Loan report z view"""
        try:
            with db_conn.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vw_loan_report")
                report_data = cursor.fetchall()
            return render_template("loan_report.html", report=report_data)
        except DatabaseError as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("index"))
