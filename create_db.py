import sqlite3
from werkzeug.security import generate_password_hash

def create_db():
    print("Start script")  #test of het werkt
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

#tabellen maken
    c.execute('''
    CREATE TABLE IF NOT EXISTS eten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        naam TEXT UNIQUE NOT NULL,
        categorie TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS mo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        naam TEXT UNIQUE NOT NULL,
        herkenning TEXT,
        risiconiveau TEXT,
        actie TEXT,
        symptomen TEXT,
        beschrijving TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS mo_met_eten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mo_id INTEGER,
        eten_id INTEGER,
        FOREIGN KEY (mo_id) REFERENCES mo (id),
        FOREIGN KEY (eten_id) REFERENCES eten (id)
        UNIQUE (mo_id, eten_id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS inlog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gebruikersnaam TEXT UNIQUE NOT NULL,
        wachtwoord TEXT NOT NULL
    )
    ''')
    users = [
        ("yael", generate_password_hash("wachtwoord")),
        ("cool", generate_password_hash("hoi")),
    ]

    # Voeg gebruikers toe
    # c.execute("DELETE FROM inlog")
    c.executemany(
        "INSERT INTO inlog (gebruikersnaam, wachtwoord) VALUES (?, ?)",
        users
    )
    eten = [
        ('Droge pasta', 'Graanproducten'),
        ('Koekjes en ontbijtgranen', 'Zoetigheden'),
        ("Melk (ongeopend)", "Zuivel"),
        ("Conserven", "Ingeblikt voedsel"), 
        ("Eieren", "Dierlijke producten"), 
        ("Frisdrank", "Dranken"), 
        ("Chocolade", "Zoetigheden"), 
        ("Koffie en thee", "Dranken")
    ]

    c.executemany("INSERT OR IGNORE INTO eten (naam, categorie) VALUES (?, ?)", eten)

    mo = [
        ('Bacillus cereus', 'Korrelige witte schimmel op rijst of pasta, slechte geur', 'Middel', 'Weggooien, goed koken', 'Misselijkheid, diarree', 'Komt voor in droge pasta en rijst'),
        ("Listeria monocytogenes", "Zure geur, schimmel in melk", "Hoog", "Niet consumeren, weggooien", "Koorts, misselijkheid", "Bacterie die vooral in zuivel voorkomt"),
        ("Clostridium botulinum", "Blikken staan bol, gasvorming", "Hoog", "Niet openen, direct weggooien", "Ernstige verlammingen", "Gevaarlijke bacterie in conserven"), 
        ("Schimmels (Aspergillus)", "Groene/blauwe vlekken", "Laag", "Weggooien", "Allergieën, vergiftiging", "Groeit op droge producten"),
        ("Salmonella", "Eieren ruiken zwavelachtig, slijmerig", "Hoog", "Eieren weggooien", "Erge buikpijn, diarree", "Komt vaak voor in rauwe eieren"),
        ("Gist", "Bubbels in frisdrank, afwijkende geur", "Laag", "Niet drinken", "Opgeblazen gevoel, misselijkheid", "Ongunstige gisting in frisdrank"), 
        ("Penicillium", "Blauwe schimmel op chocolade", "Middel", "Weggooien", "Allergieën", "Schimmel die op chocolade groeit"), 
        ("Ongewenste fermentatie", "Bitters, verkleuring in thee/koffie", "Laag", "Niet consumeren", "Geen ernstige symptomen", "Fout in fermentatieproces bij thee/koffie")
    ]

    c.executemany("""
        INSERT OR IGNORE INTO mo (naam, herkenning, risiconiveau, actie, symptomen, beschrijving)
        VALUES (?, ?, ?, ?, ?, ?)
        """, mo)

    # IDs koppelen
    c.execute('SELECT id, naam FROM eten')
    eten_ids = {naam: fid for fid, naam in c.fetchall()}

    c.execute('SELECT id, naam FROM mo')
    mo_ids = {naam: mid for mid, naam in c.fetchall()}

    mo_met_eten_links = [
        (mo_ids['Bacillus cereus'], eten_ids['Droge pasta']),
        (mo_ids['Bacillus cereus'], eten_ids['Koekjes en ontbijtgranen']),
        (mo_ids["Listeria monocytogenes"], eten_ids["Melk (ongeopend)"]),
        (mo_ids["Clostridium botulinum"], eten_ids["Conserven"]), 
        (mo_ids["Schimmels (Aspergillus)"], eten_ids["Koekjes en ontbijtgranen"]), 
        (mo_ids["Salmonella"], eten_ids["Eieren"]), 
        (mo_ids["Gist"], eten_ids["Frisdrank"]), 
        (mo_ids["Penicillium"], eten_ids["Chocolade"]), 
        (mo_ids["Ongewenste fermentatie"], eten_ids["Koffie en thee"])
    ]

    c.executemany('INSERT OR IGNORE INTO mo_met_eten (mo_id, eten_id) VALUES (?, ?)', mo_met_eten_links)


    conn.commit()
    conn.close()
    print("Database met startdata is aangemaakt")

if __name__ == "__main__":
    create_db()