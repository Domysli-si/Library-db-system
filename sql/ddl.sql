-- Drop tables if they exist
DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS book_category;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS library_user;

-- Tables
CREATE TABLE author (
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE category (
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category_type VARCHAR(20) NOT NULL
        CHECK (category_type IN ('fiction', 'nonfiction', 'study'))
);

CREATE TABLE library_user (
    id INT IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE book (
    id INT IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INT NOT NULL,
    price FLOAT NOT NULL,
    available BIT NOT NULL DEFAULT 1,
    published_date DATE NOT NULL,
    CONSTRAINT fk_book_author
        FOREIGN KEY (author_id) REFERENCES author(id)
);

CREATE TABLE book_category (
    book_id INT NOT NULL,
    category_id INT NOT NULL,
    CONSTRAINT pk_book_category PRIMARY KEY (book_id, category_id),
    CONSTRAINT fk_bc_book FOREIGN KEY (book_id) REFERENCES book(id),
    CONSTRAINT fk_bc_category FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE loan (
    id INT IDENTITY PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    loan_date DATETIME NOT NULL DEFAULT GETDATE(),
    return_date DATETIME NULL,
    returned BIT NOT NULL DEFAULT 0,
    CONSTRAINT fk_loan_book FOREIGN KEY (book_id) REFERENCES book(id),
    CONSTRAINT fk_loan_user FOREIGN KEY (user_id) REFERENCES library_user(id)
);

