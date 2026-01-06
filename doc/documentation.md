# Dokumentace projektu: Library DB System

**Autor:** Samuel Majer  
**Třída:** C4c
**Datum:** 11. 1. 2025  
**Typ řešení:** D1 - Repository Pattern

---

## 1. Popis projektu

### 1.1 Účel aplikace

Library DB System je webová aplikace pro správu knihovny. Umožňuje:
- Správu knih, autorů, kategorií a uživatelů
- Půjčování a vracení knih
- Import dat z JSON souborů
- Generování reportů a statistik

### 1.2 Technologie

- **Programovací jazyk:** Python 3.10+
- **Web framework:** Flask
- **Databáze:** Microsoft SQL Server
- **DB driver:** pyodbc (ODBC Driver 17 for SQL Server)
- **Design pattern:** Repository Pattern (D1)

---

## 2. Struktura projektu

```
library-db-system/
├── config/
│   └── config.json           # Konfigurace databáze
├── sql/
│   ├── ddl.sql              # Databázová struktura (tabulky)
│   └── views.sql            # Pohledy (views)
├── src/
│   ├── db/
│   │   └── connection.py    # Správa připojení k DB
│   ├── models/
│   │   ├── author.py        # Model Author
│   │   ├── book.py          # Model Book
│   │   ├── category.py      # Model Category
│   │   ├── library_user.py  # Model LibraryUser
│   │   └── loan.py          # Model Loan
│   ├── repositories/
│   │   ├── base_repository.py          # Základní repository
│   │   ├── author_repository.py        # Repository pro autory
│   │   ├── book_repository.py          # Repository pro knihy
│   │   ├── category_repository.py      # Repository pro kategorie
│   │   ├── user_repository.py          # Repository pro uživatele
│   │   ├── loan_repository.py          # Repository pro půjčky
│   │   └── book_category_repository.py # Repository pro M:N vazbu
│   ├── services/
│   │   ├── library_service.py  # Business logika (transakce)
│   │   └── import_service.py   # Import z JSON
│   ├── ui/
│   │   ├── routes.py         # Flask routes (controller)
│   │   └── templates/        # HTML šablony
│   ├── static/
│   │   └── style.css         # CSS styly
│   └── app.py                # Hlavní aplikace
├── test/
│   ├── test_scenario_1_installation.md
│   ├── test_scenario_2_functionality.md
│   └── test_scenario_3_errors.md
├── doc/
│   └── documentation.md      # Tato dokumentace
├── requirements.txt          # Python závislosti
└── README.md                 # Základní informace
```

---

## 3. Databázová struktura

### 3.1 Tabulky

#### 3.1.1 author
```sql
id           INT IDENTITY PRIMARY KEY
name         VARCHAR(100) NOT NULL
```

#### 3.1.2 category
```sql
id             INT IDENTITY PRIMARY KEY
name           VARCHAR(50) NOT NULL
category_type  VARCHAR(20) NOT NULL CHECK (category_type IN ('fiction', 'nonfiction', 'study'))
```

#### 3.1.3 library_user
```sql
id          INT IDENTITY PRIMARY KEY
full_name   VARCHAR(100) NOT NULL
email       VARCHAR(100) NOT NULL
active      BIT NOT NULL DEFAULT 1
created_at  DATETIME NOT NULL DEFAULT GETDATE()
```

#### 3.1.4 book
```sql
id              INT IDENTITY PRIMARY KEY
title           VARCHAR(200) NOT NULL
author_id       INT NOT NULL
price           FLOAT NOT NULL
available       BIT NOT NULL DEFAULT 1
published_date  DATE NOT NULL
FOREIGN KEY (author_id) REFERENCES author(id)
```

#### 3.1.5 book_category (M:N)
```sql
book_id      INT NOT NULL
category_id  INT NOT NULL
PRIMARY KEY (book_id, category_id)
FOREIGN KEY (book_id) REFERENCES book(id)
FOREIGN KEY (category_id) REFERENCES category(id)
```

#### 3.1.6 loan
```sql
id           INT IDENTITY PRIMARY KEY
book_id      INT NOT NULL
user_id      INT NOT NULL
loan_date    DATETIME NOT NULL DEFAULT GETDATE()
return_date  DATETIME NULL
returned     BIT NOT NULL DEFAULT 0
FOREIGN KEY (book_id) REFERENCES book(id)
FOREIGN KEY (user_id) REFERENCES library_user(id)
```

### 3.2 Views

#### 3.2.1 vw_books_overview
Přehled knih s autory:
```sql
SELECT b.id, b.title, a.name AS author, b.price, b.available, b.published_date
FROM book b
JOIN author a ON b.author_id = a.id
```

#### 3.2.2 vw_loan_report
Statistiky půjček podle uživatelů:
```sql
SELECT u.full_name, COUNT(l.id) AS total_loans, 
       SUM(CASE WHEN l.returned = 0 THEN 1 ELSE 0 END) AS active_loans,
       MAX(l.loan_date) AS last_loan_date
FROM library_user u
LEFT JOIN loan l ON u.id = l.user_id
GROUP BY u.full_name
```

### 3.3 Datové typy

| Typ | Použití | Příklad |
|-----|---------|---------|
| **FLOAT** | price | 299.90 |
| **BIT** | available, active, returned | 0/1 |
| **VARCHAR** | name, title, email | "Isaac Asimov" |
| **DATE** | published_date | 2020-01-15 |
| **DATETIME** | created_at, loan_date | 2025-01-11 14:30:00 |
| **ENUM (CHECK)** | category_type | 'fiction', 'nonfiction', 'study' |

---

## 4. Repository Pattern (D1)

### 4.1 Implementace

Projekt používá **Repository Pattern** pro oddělení business logiky od přístupu k datům.

#### Struktura:
1. **BaseRepository** - základní třída s metodou `execute()`
2. **Konkrétní repositories** - dědí z BaseRepository:
   - AuthorRepository
   - BookRepository
   - CategoryRepository
   - UserRepository
   - LoanRepository
   - BookCategoryRepository

#### Příklad použití:
```python
with db_conn.transaction() as conn:
    book_repo = BookRepository(conn)
    books = book_repo.get_all()
    
    new_book = Book(title="Foundation", author_id=1, price=299.90, ...)
    book_id = book_repo.add(new_book)
```

### 4.2 Výhody

- Oddělení logiky od databáze
- Snadná testovatelnost
- Jednotné rozhraní pro CRUD operace
- Transakční podpora

---

## 5. Splnění požadavků zadání

### ✅ BOD 1: Repository Pattern (D1)
Implementováno pomocí base repository a 6 konkrétních repositories.

### ✅ BOD 2: RDBMS
Microsoft SQL Server.

### ✅ BOD 3: Min. 5 tabulek, 2 views, 1 M:N
- Tabulky: 6 (author, category, library_user, book, book_category, loan)
- Views: 2 (vw_books_overview, vw_loan_report)
- M:N: book_category

### ✅ BOD 4: Všechny datové typy
- FLOAT: price
- BIT: available, active, returned
- ENUM: category_type (CHECK constraint)
- VARCHAR: name, title, email
- DATE/DATETIME: published_date, created_at, loan_date

### ✅ BOD 5: Vložení do více tabulek
Formulář "Add Book with Categories" vkládá data do:
- book (kniha)
- author (pokud neexistuje)
- book_category (M:N vazba)

### ✅ BOD 6: Transakce
Metody v `LibraryService`:
- `loan_book()` - půjčení knihy (book.available + loan záznam)
- `return_book()` - vrácení knihy (loan.returned + book.available)

### ✅ BOD 7: Report ze 3+ tabulek
Report "Books by Author & Category" agreguje data z:
- book
- author
- category (přes book_category)

Agregace: COUNT, AVG, MIN, MAX, SUM

### ✅ BOD 8: Import JSON do 2+ tabulek
Import z JSON vkládá data do:
- author
- book
- category
- book_category

### ✅ BOD 9: Konfigurace
Soubor `config/config.json` umožňuje nastavit:
- server
- database
- username
- password
- driver

### ✅ BOD 10: Ošetření chyb
- Validace vstupů
- Try-catch bloky
- User-friendly chybové hlášky
- Kontrola konfigurace při startu

---

## 6. Instalace a spuštění

### 6.1 Požadavky
- Python 3.10+
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

### 6.2 Instalace

```bash
# 1. Klonování repozitáře
git clone <URL>
cd library-db-system

# 2. Instalace závislostí
pip install -r requirements.txt

# 3. Vytvoření databáze
# V SSMS spusťte:
CREATE DATABASE library_db;

# 4. Import struktury
# Spusťte sql/ddl.sql
# Spusťte sql/views.sql

# 5. Konfigurace
# Upravte config/config.json
```

### 6.3 Spuštění

```bash
python src/app.py
```

Aplikace běží na: http://localhost:5000

---

## 7. Uživatelská příručka

### 7.1 Správa knih

1. **Přidání knihy s kategoriemi:**
   - Klikněte "Add Book with Categories"
   - Vyplňte název, autora, cenu, datum vydání
   - Vyberte alespoň 1 kategorii
   - Klikněte "Add Book"

2. **Zobrazení knih:**
   - Klikněte "View Books"
   - Zobrazí se seznam všech knih

3. **Úprava knihy:**
   - V seznamu klikněte "Edit"
   - Změňte údaje
   - Klikněte "Update Book"

4. **Smazání knihy:**
   - V seznamu klikněte "Delete"
   - Potvrďte smazání

### 7.2 Půjčování knih

1. **Půjčení knihy:**
   - Klikněte "Loan Book"
   - Zadejte ID knihy a ID uživatele
   - Klikněte "Loan Book"

2. **Vrácení knihy:**
   - Klikněte "View Loans"
   - U aktivní půjčky klikněte "Return"

### 7.3 Import dat

1. **Import z JSON:**
   - Vytvořte JSON soubor podle formátu (viz kapitola 8.2)
   - Klikněte "Import JSON"
   - Vyberte soubor
   - Klikněte "Import"

### 7.4 Reporty

1. **Report knih podle autora:**
   - Klikněte "Books by Author & Category"
   - Zobrazí agregovaná data

2. **Statistiky půjček:**
   - Klikněte "Loan Statistics"
   - Zobrazí přehled půjček pro každého uživatele

---

## 8. Formáty dat

### 8.1 Struktura JSON pro import

```json
[
    {
        "title": "Název knihy",
        "author": "Jméno autora",
        "price": 299.90,
        "published_date": "2020-01-15",
        "categories": ["fiction", "study"]
    }
]
```

### 8.2 Příklad JSON

```json
[
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "price": 299.90,
        "published_date": "1951-05-01",
        "categories": ["fiction"]
    },
    {
        "title": "I, Robot",
        "author": "Isaac Asimov",
        "price": 250.00,
        "published_date": "1950-12-02",
        "categories": ["fiction", "study"]
    }
]
```

---

## 9. Známé problémy a řešení

### 9.1 "ODBC Driver not found"
**Řešení:** Nainstalujte ODBC Driver 17 for SQL Server.

### 9.2 "Login failed"
**Řešení:** Zkontrolujte `config/config.json` nebo použijte Windows Authentication.

### 9.3 Port 5000 obsazen
**Řešení:** Změňte port v `src/app.py`:
```python
app.run(debug=True, port=5001)
```

---

## 10. Testování

### 10.1 Testovací scénáře

Projekt obsahuje 3 testovací scénáře:
1. **test_scenario_1_installation.md** - Instalace a spuštění
2. **test_scenario_2_functionality.md** - Testování funkcionalit
3. **test_scenario_3_errors.md** - Testování chyb

### 10.2 Spuštění testů

Testy se provádějí manuálně podle testovacích scénářů v PDF formátu.

---

## 11. Architektura aplikace

### 11.1 Vrstvová architektura

```
┌─────────────────────────────────┐
│   Presentation Layer (UI)       │
│   - Flask routes                │
│   - HTML templates              │
└─────────────────────────────────┘
            ↓
┌─────────────────────────────────┐
│   Service Layer                 │
│   - LibraryService              │
│   - ImportService               │
│   - Business logic              │
└─────────────────────────────────┘
            ↓
┌─────────────────────────────────┐
│   Repository Layer (D1)         │
│   - Repositories                │
│   - Data access                 │
└─────────────────────────────────┘
            ↓
┌─────────────────────────────────┐
│   Database Layer                │
│   - MS SQL Server               │
│   - Tables, Views               │
└─────────────────────────────────┘
```

### 11.2 Design patterns

- **Repository Pattern (D1)** - oddělení business logiky od DB
- **Transaction Script** - transakční operace v service layer
- **MVC** - Model-View-Controller (Flask routes)

---

## 12. Bezpečnost

### 12.1 SQL Injection prevence
- Použití parametrizovaných dotazů (`cursor.execute(query, params)`)
- Žádné dynamické skládání SQL stringů

### 12.2 Validace vstupů
- HTML5 validace (required, type="email", atd.)
- Server-side validace v routes
- Kontrola datových typů


