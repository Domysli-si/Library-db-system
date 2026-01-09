# Library DB System

Webová aplikace pro správu knihovny s použitím Repository Pattern (D1).

## Instalace

### Požadavky

- Python 3.10 nebo novější
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

### Postup instalace

1. **Klonování repozitáře**

```bash
git clone <URL>
cd library-db-system
```

2. **Instalace Python závislostí**

```bash
pip install -r requirements.txt
```

3. **Konfigurace databáze**

Upravte soubor `config/config.json`:

```json
{
    "server": "localhost",
    "database": "library",
    "username": "sa",
    "password": "your_password",
    "driver": "ODBC Driver 17 for SQL Server"
}
```

4. **Inicializace databáze**

```bash
python setup.py
```

Tento script automaticky:
- Vytvoří databázi
- Vytvoří tabulky a views
- Ověří správnost instalace
- Nabídne vložení vzorových dat

5. **Spuštění aplikace**

```bash
python -m src.app
```

Aplikace běží na: http://localhost:5000

## Struktura projektu

```
library-db-system/
├── config/
│   ├── config.json              # Konfigurace databáze
│   └── config.example.json      # Vzorová konfigurace
├── sql/
│   ├── ddl.sql                  # Databázové tabulky
│   └── views.sql                # Pohledy
├── src/
│   ├── db/
│   │   └── connection.py        # Správa připojení
│   ├── models/                  # Datové modely
│   ├── repositories/            # Repository Pattern (D1)
│   ├── services/                # Business logika
│   ├── ui/
│   │   ├── routes.py           # Flask routes
│   │   └── templates/          # HTML šablony
│   ├── static/
│   │   └── style.css           # Styly
│   └── app.py                  # Hlavní aplikace
├── data/
│   ├── import_template.json    # Vzorová data pro import
│   └── README_json_format.md   # Dokumentace JSON formátu
├── test/                       # Testovací scénáře
├── doc/                        # Dokumentace
├── setup.py                    # Instalační script
├── requirements.txt            # Python závislosti
└── README.md                   # Tento soubor
```

## Databázová struktura

### Tabulky

- **author** - Autoři knih
- **category** - Kategorie (fiction, nonfiction, study)
- **library_user** - Uživatelé knihovny
- **book** - Knihy
- **book_category** - M:N vazba mezi knihami a kategoriemi
- **loan** - Půjčky knih

### Views

- **vw_books_overview** - Přehled knih s autory
- **vw_loan_report** - Statistiky půjček

## Funkce aplikace

### Správa knih
- Přidání knihy s kategoriemi (vložení do více tabulek současně)
- Zobrazení seznamu knih
- Úprava knihy
- Smazání knihy

### Správa autorů, kategorií a uživatelů
- Přidání nových záznamů
- Zobrazení seznamů
- Smazání záznamů

### Půjčování knih
- Půjčení knihy uživateli (transakční operace)
- Vrácení knihy (transakční operace)
- Zobrazení historie půjček

### Import dat
- Import knih, autorů a kategorií z JSON souboru
- Automatické vytvoření M:N vazeb

### Reporty
- Statistika knih podle autora a kategorie (agregace z 3 tabulek)
- Statistika půjček podle uživatelů

## Repository Pattern (D1)

Projekt implementuje Repository Pattern pro oddělení datové vrstvy od business logiky.

```python
with db_conn.transaction() as conn:
    book_repo = BookRepository(conn)
    
    # CRUD operace
    books = book_repo.get_all()
    book = book_repo.get_by_id(1)
    book_id = book_repo.add(new_book)
    book_repo.update(book)
    book_repo.delete(book_id)
```

### Implementované repositories

- BaseRepository - Základní třída s metodou execute()
- AuthorRepository
- BookRepository
- CategoryRepository
- UserRepository
- LoanRepository
- BookCategoryRepository

## Testování

Projekt obsahuje 3 testovací scénáře v PDF formátu:

1. **test_scenario_1_installation.pdf** - Instalace a spuštění aplikace
2. **test_scenario_2_functionality.pdf** - Testování funkcionalit
3. **test_scenario_3_errors.pdf** - Testování chyb a výjimečných stavů

## Řešení problémů

### Chyba: ODBC Driver not found

Nainstalujte ODBC Driver 17 for SQL Server:
https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Chyba: Login failed

Zkontrolujte přihlašovací údaje v `config/config.json`.

Pro Windows Authentication použijte prázdné username a password a upravte `src/db/connection.py`:

```python
return pyodbc.connect(
    f"DRIVER={{{self._config['driver']}}};"
    f"SERVER={self._config['server']};"
    f"DATABASE={self._config['database']};"
    f"Trusted_Connection=yes;",
    autocommit=False
)
```

### Port 5000 je obsazen

Změňte port v `src/app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Technologie

- Python 3.10+
- Flask
- pyodbc
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

## Autor

Samuel Majer  
C4c  
Datum: 9. 1. 2025
