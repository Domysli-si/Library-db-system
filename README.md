# Library DB System# Library DB System

Webová aplikace pro správu knihovny s použitím **Repository Pattern (D1)**.

## 🚀 Rychlý start

```bash
# 1. Klonování
git clone <URL>
cd library-db-system

# 2. Instalace
pip install -r requirements.txt

# 3. Konfigurace databáze
# Vytvořte databázi v MS SQL Server
CREATE DATABASE library_db;

# 4. Import struktury
# Spusťte v SSMS:
# - sql/ddl.sql
# - sql/views.sql

# 5. Nastavení config/config.json
{
    "server": "localhost",
    "database": "library_db",
    "username": "your_user",
    "password": "your_password",
    "driver": "ODBC Driver 17 for SQL Server"
}

# 6. Spuštění
python src/app.py

# 7. Otevřete prohlížeč
http://localhost:5000
```

## 📁 Struktura projektu

```
library-db-system/
├── config/
│   └── config.json           # Konfigurace DB
├── sql/
│   ├── ddl.sql              # Tabulky
│   └── views.sql            # Pohledy
├── src/
│   ├── db/
│   │   └── connection.py    # DB připojení
│   ├── models/              # Entity (Author, Book, ...)
│   ├── repositories/        # D1 - Repository Pattern
│   ├── services/            # Business logika
│   ├── ui/                  # Flask routes + templates
│   ├── static/              # CSS
│   └── app.py               # Hlavní aplikace
├── test/                    # Testovací scénáře (3x PDF)
├── doc/                     # Dokumentace
└── requirements.txt         # Závislosti
```

## 🗄️ Databázové tabulky

1. **author** - Autoři knih
2. **category** - Kategorie (fiction, nonfiction, study)
3. **library_user** - Uživatelé knihovny
4. **book** - Knihy
5. **book_category** - M:N vazba mezi knihami a kategoriemi
6. **loan** - Půjčky knih

## 🎯 Hlavní funkce

### Správa knih
- Přidání knihy s kategoriemi (vložení do více tabulek)
- Zobrazení, úprava, smazání knih

### Půjčování
- Půjčení knihy (transakce: book.available + loan)
- Vrácení knihy (transakce: loan.returned + book.available)

### Import dat
- Import z JSON do 2+ tabulek (authors, books, categories)

### Reporty
- Books by Author & Category (3+ tabulky, agregace)
- Loan Statistics (z view)

## 📊 Repository Pattern (D1)

```python
# Příklad použití
with db_conn.transaction() as conn:
    book_repo = BookRepository(conn)
    
    # CRUD operace
    books = book_repo.get_all()
    book = book_repo.get_by_id(1)
    book_id = book_repo.add(new_book)
    book_repo.update(book)
    book_repo.delete(book_id)
```

## 📝 Testování

Projekt obsahuje 3 testovací scénáře:

1. **test_scenario_1_installation.md** - Instalace a spuštění
2. **test_scenario_2_functionality.md** - Testování funkcí
3. **test_scenario_3_errors.md** - Testování chyb

Pro konverzi do PDF použijte:
```bash
pandoc test_scenario_1_installation.md -o test_scenario_1.pdf
```

## 🔧 Technologie

- Python 3.10+
- Flask (web framework)
- pyodbc (DB driver)
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

## 📖 Dokumentace

Kompletní dokumentace v `doc/documentation.md` obsahuje:
- Popis projektu
- Databázovou strukturu
- Repository Pattern implementaci
- Uživatelskou příručku
- Testování
- Známé problémy a řešení

## ⚠️ Možné problémy

### ODBC Driver not found
```bash
# Stáhněte a nainstalujte:
https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### Login failed
```json
// Pro Windows Authentication použijte:
{
    "server": "localhost",
    "database": "library_db",
    "username": "",
    "password": "",
    "driver": "ODBC Driver 17 for SQL Server"
}
```
A v `connection.py` změňte na `Trusted_Connection=yes;`

### Port 5000 obsazen
```python
# V src/app.py změňte:
app.run(debug=True, port=5001)
```

## 📄 Licence

Školní projekt pro předmět Databázové systémy.

## 👤 Autor

Samuel Majer  
C4c

