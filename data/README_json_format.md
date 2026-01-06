# JSON Import Format

## Struktura JSON souboru pro import

JSON soubor musí být **pole objektů**, kde každý objekt reprezentuje jednu knihu.

### Povinná pole

| Pole | Typ | Popis | Příklad |
|------|-----|-------|---------|
| `title` | string | Název knihy (max 200 znaků) | "Foundation" |
| `author` | string | Jméno autora (max 100 znaků) | "Isaac Asimov" |
| `price` | number | Cena (musí být kladné číslo) | 299.90 |
| `published_date` | string | Datum vydání (formát YYYY-MM-DD) | "1951-05-01" |
| `categories` | array | Pole kategorií (min. 1) | ["fiction", "study"] |

### Povolené hodnoty pro categories

- `"fiction"` - Beletrie
- `"nonfiction"` - Naučná literatura
- `"study"` - Studijní materiály

## Příklad minimálního JSON souboru

```json
[
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "price": 299.90,
        "published_date": "1951-05-01",
        "categories": ["fiction"]
    }
]
```

## Příklad kompletního JSON souboru

```json
[
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "price": 299.90,
        "published_date": "1951-05-01",
        "categories": ["fiction", "study"]
    },
    {
        "title": "I, Robot",
        "author": "Isaac Asimov",
        "price": 250.00,
        "published_date": "1950-12-02",
        "categories": ["fiction"]
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "price": 399.00,
        "published_date": "2008-08-01",
        "categories": ["nonfiction", "study"]
    }
]
```

## Import v aplikaci

1. Vytvořte JSON soubor podle výše uvedeného formátu
2. V aplikaci klikněte na "Import JSON"
3. Vyberte soubor
4. Klikněte "Import"

## Co se importuje

Import vloží data do následujících tabulek:
- **author** - autoři (pokud už neexistují)
- **book** - knihy
- **category** - kategorie (pokud už neexistují)
- **book_category** - vazba M:N mezi knihami a kategoriemi

## Validace

Při importu se kontroluje:
- ✅ Všechna povinná pole jsou vyplněna
- ✅ Cena je kladné číslo
- ✅ Datum je ve správném formátu (YYYY-MM-DD)
- ✅ Alespoň jedna kategorie je zadána
- ✅ Kategorie jsou z povolených hodnot

## Chybové stavy

### Chybějící pole
```json
{
    "title": "Test Book",
    "author": "Test Author"
    // Chybí price a published_date
}
```
**Výsledek:** ❌ Chyba - Import se neprovede

### Neplatný formát data
```json
{
    "published_date": "01-01-2020"  // Špatný formát
}
```
**Výsledek:** ❌ Chyba - Import se neprovede

### Neplatná kategorie
```json
{
    "categories": ["unknown_category"]
}
```
**Výsledek:** ⚠️ Kategorie se vytvoří s výchozím typem "fiction"

### Prázdné pole kategorií
```json
{
    "categories": []
}
```
**Výsledek:** ❌ Chyba - Alespoň jedna kategorie je povinná

## Tipy pro správný import

1. **Kontrola JSON syntaxe:** Použijte JSON validator (např. jsonlint.com)
2. **Encoding:** Uložte soubor v UTF-8
3. **Datum:** Vždy formát YYYY-MM-DD
4. **Kategorie:** Kontrola na malá písmena ("fiction", ne "Fiction")
5. **Duplicity:** Stejný autor se neimportuje vícekrát (kontrola podle jména)

## Testovací data

Pro testování použijte soubor `import_template.json`, který obsahuje 10 vzorových knih.

## Příklady platných a neplatných JSON souborů

### ✅ Platný
```json
[
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "price": 399.99,
        "published_date": "1965-08-01",
        "categories": ["fiction", "study"]
    }
]
```

### ❌ Neplatný - chybějící čárka
```json
[
    {
        "title": "Dune"
        "author": "Frank Herbert"  // <-- chybí čárka
    }
]
```

### ❌ Neplatný - záporná cena
```json
[
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "price": -50,  // <-- záporná cena
        "published_date": "1965-08-01",
        "categories": ["fiction"]
    }
]
```

### ❌ Neplatný - nesprávný datový typ
```json
[
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "price": "expensive",  // <-- text místo čísla
        "published_date": "1965-08-01",
        "categories": ["fiction"]
    }
]
```

---

**Poznámka:** Pro nejlepší výsledky testujte JSON soubory nejprve na menším vzorku dat.
