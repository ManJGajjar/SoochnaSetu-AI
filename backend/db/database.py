import json
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "soochna_setu.db"
SEED_PATH = Path(__file__).parent.parent / "data" / "schemes_seed.json"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Create tables and seed scheme data."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            schemeId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            nameLocal TEXT,
            description TEXT,
            simpleDescription TEXT,
            analogy TEXT,
            category TEXT,
            state TEXT DEFAULT 'ALL',
            eligibility TEXT,
            benefits TEXT,
            benefitAmount TEXT,
            benefitType TEXT,
            requiredDocuments TEXT,
            applicationProcess TEXT,
            officialLink TEXT,
            helplineNumber TEXT,
            deadline TEXT,
            commonRejectionReasons TEXT,
            tags TEXT,
            lastUpdated TEXT,
            isActive INTEGER DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userId TEXT PRIMARY KEY,
            phone TEXT UNIQUE,
            name TEXT,
            age INTEGER,
            incomeBracket TEXT,
            occupation TEXT,
            state TEXT,
            district TEXT,
            category TEXT DEFAULT 'General',
            disability INTEGER DEFAULT 0,
            disabilityType TEXT,
            gender TEXT,
            language TEXT DEFAULT 'en',
            needs TEXT,
            createdAt TEXT,
            updatedAt TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            documentId TEXT PRIMARY KEY,
            userId TEXT,
            fileName TEXT,
            fileSize INTEGER,
            fileType TEXT,
            s3Key TEXT,
            uploadedAt TEXT,
            processingStatus TEXT DEFAULT 'pending',
            processingProgress INTEGER DEFAULT 0,
            pageCount INTEGER,
            extractedText TEXT,
            error TEXT
        )
    """)

    db.commit()

    # Seed schemes if table is empty
    count = cur.execute("SELECT COUNT(*) FROM schemes").fetchone()[0]
    if count == 0:
        seed_schemes(db)

    db.close()


def seed_schemes(db):
    """Load schemes from JSON seed file into database."""
    if not SEED_PATH.exists():
        print(f"Warning: Seed file not found at {SEED_PATH}")
        return

    with open(SEED_PATH, "r", encoding="utf-8") as f:
        schemes = json.load(f)

    cur = db.cursor()
    for s in schemes:
        cur.execute("""
            INSERT OR REPLACE INTO schemes
            (schemeId, name, nameLocal, description, simpleDescription, analogy,
             category, state, eligibility, benefits, benefitAmount, benefitType,
             requiredDocuments, applicationProcess, officialLink, helplineNumber,
             deadline, commonRejectionReasons, tags, lastUpdated, isActive)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["schemeId"], s["name"], s.get("nameLocal"),
            s["description"], s.get("simpleDescription"), s.get("analogy"),
            s["category"], s.get("state", "ALL"),
            json.dumps(s.get("eligibility", {})),
            json.dumps(s.get("benefits", [])),
            s.get("benefitAmount"), s.get("benefitType"),
            json.dumps(s.get("requiredDocuments", [])),
            json.dumps(s.get("applicationProcess", [])),
            s.get("officialLink", ""), s.get("helplineNumber"),
            s.get("deadline"),
            json.dumps(s.get("commonRejectionReasons", [])),
            json.dumps(s.get("tags", [])),
            s.get("lastUpdated", ""), 1 if s.get("isActive", True) else 0,
        ))
    db.commit()
    print(f"Seeded {len(schemes)} schemes into database.")


def get_all_schemes():
    """Return all active schemes as dicts."""
    db = get_db()
    rows = db.execute("SELECT * FROM schemes WHERE isActive = 1").fetchall()
    db.close()
    result = []
    for r in rows:
        d = dict(r)
        for field in ("eligibility", "benefits", "requiredDocuments",
                       "applicationProcess", "commonRejectionReasons", "tags"):
            if d.get(field):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        d["isActive"] = bool(d.get("isActive", 1))
        result.append(d)
    return result


def get_scheme_by_id(scheme_id: str):
    """Return a single scheme by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM schemes WHERE schemeId = ?", (scheme_id,)).fetchone()
    db.close()
    if not row:
        return None
    d = dict(row)
    for field in ("eligibility", "benefits", "requiredDocuments",
                   "applicationProcess", "commonRejectionReasons", "tags"):
        if d.get(field):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                pass
    d["isActive"] = bool(d.get("isActive", 1))
    return d
