# Testovací scénář 1: Instalace a spuštění aplikace

**Projekt:** Library DB System (D1)  
**Verze:** 1.0  
**Datum:** 2025-01-11

---

## 1. Předpoklady

- Počítač s nainstalovaným:
  - Python 3.10 nebo novější
  - Microsoft SQL Server (nebo přístup k SQL Serveru)
  - Microsoft SQL Server ODBC Driver 17 for SQL Server
  - Git

---

## 2. Stažení projektu

### Krok 1: Klonování repozitáře
```bash
git clone <URL_REPOZITARE>
cd library-db-system
```

**Očekávaný výsledek:** Projekt je stažen do složky `library-db-system`.

---

## 3. Instalace závislostí

### Krok 2: Instalace Python knihoven
```bash
pip install -r requirements.txt
```

**Očekávaný výsledek:**  
- Flask a pyodbc jsou nainstalovány bez chyb
- Výpis: `Successfully installed flask pyodbc`

---

## 4. Konfigurace databáze

### Krok 3: Vytvoření databáze

Otevřete SQL Server Management Studio (nebo Azure Data Studio) a vytvořte novou databázi:

```sql
CREATE DATABASE library_db;
```

**Očekávaný výsledek:** Databáze `library_db` je vytvořena.

### Krok 4: Import databázové struktury

Spusťte SQL skripty v tomto pořadí:

1. **DDL (tabulky):**
```bash
# V SSMS nebo Azure Data Studio otevřete soubor:
sql/ddl.sql
# A spusťte ho (F5)
```

**Očekávaný výsledek:** 
- 6 tabulek vytvořeno: `author`, `category`, `library_user`, `book`, `book_category`, `loan`
- Žádné chyby

2. **Views:**
```bash
# Otevřete a spusťte:
sql/views.sql
```

**Očekávaný výsledek:**
- 2 views vytvořeny: `vw_books_overview`, `vw_loan_report`
- Žádné chyby

### Krok 5: Vytvoření uživatelského účtu (volitelné)

Pokud chcete použít samostatný účet pro aplikaci:

```sql
CREATE LOGIN library_app WITH PASSWORD = 'StrongPassword123!';
CREATE USER library_app FOR LOGIN library_app;

ALTER ROLE db_datareader ADD MEMBER library_app;
ALTER ROLE db_datawriter ADD MEMBER library_app;
```

**Očekávaný výsledek:** Uživatel `library_app` má přístup k databázi.

---

## 5. Konfigurace aplikace

### Krok 6: Nastavení config.json

Otevřete soubor `config/config.json` a vyplňte údaje:

```json
{
    "server": "localhost",
    "database": "library_db",
    "username": "library_app",
    "password": "StrongPassword123!",
    "driver": "ODBC Driver 17 for SQL Server"
}
```

**Poznámka:** Pokud používáte Windows Authentication, použijte:
```json
{
    "server": "localhost",
    "database": "library_db",
    "username": "",
    "password": "",
    "driver": "ODBC Driver 17 for SQL Server"
}
```
A připojovací string v kódu upravte na `Trusted_Connection=yes;`.

**Očekávaný výsledek:** Konfigurace je nastavena.

---

## 6. Spuštění aplikace

### Krok 7: Spuštění Flask aplikace

```bash
python src/app.py
```

**Očekávaný výsledek:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Krok 8: Otevření aplikace v prohlížeči

Otevřete webový prohlížeč a přejděte na:
```
http://localhost:5000
```

**Očekávaný výsledek:**
- Zobrazí se domovská stránka "Library Management System"
- Menu obsahuje odkazy:
  - Books, Authors, Categories, Users, Loans
  - Import JSON
  - Reports

---

## 7. Test základní funkcionality

### Krok 9: Přidání kategorie

1. Klikněte na "Add Category"
2. Vyplňte:
   - Name: `Science Fiction`
   - Type: `fiction`
3. Klikněte "Add Category"

**Očekávaný výsledek:**
- Zpráva: "Category added successfully!"
- Kategorie se zobrazí v seznamu

### Krok 10: Přidání autora

1. Klikněte na "Add Author"
2. Vyplňte Name: `Isaac Asimov`
3. Klikněte "Add Author"

**Očekávaný výsledek:**
- Zpráva: "Author added successfully!"
- Autor se zobrazí v seznamu

### Krok 11: Přidání uživatele

1. Klikněte na "Add User"
2. Vyplňte:
   - Full Name: `John Doe`
   - Email: `john@example.com`
3. Klikněte "Add User"

**Očekávaný výsledek:**
- Zpráva: "User added successfully!"
- Uživatel se zobrazí v seznamu

---

## 8. Možné problémy a řešení

### Problém 1: "ODBC Driver not found"
**Řešení:** Nainstalujte Microsoft ODBC Driver 17 for SQL Server z:
https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Problém 2: "Login failed for user"
**Řešení:** 
- Zkontrolujte username a password v `config/config.json`
- Zkuste použít Windows Authentication

### Problém 3: "Database not found"
**Řešení:**
- Zkontrolujte, že databáze `library_db` existuje
- Zkontrolujte název databáze v `config/config.json`

### Problém 4: "ModuleNotFoundError: No module named 'flask'"
**Řešení:**
```bash
pip install flask pyodbc
```

### Problém 5: Port 5000 je obsazen
**Řešení:** Změňte port v `src/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 9. Ukončení aplikace

Pro zastavení aplikace stiskněte `Ctrl+C` v terminálu.

---

## 10. Závěr

Po úspěšném dokončení tohoto scénáře:
- ✅ Aplikace je nainstalována
- ✅ Databáze je vytvořena a nakonfigurována
- ✅ Aplikace běží na http://localhost:5000
- ✅ Základní funkce fungují (přidání kategorie, autora, uživatele)

**Tester:** ___________________  
**Datum:** ___________________  
**Výsledek:** ✅ PASS / ❌ FAIL  
**Poznámky:**
