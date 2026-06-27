import sqlite3
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS topics (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            description TEXT,
            difficulty  TEXT    DEFAULT 'beginner',
            icon        TEXT    DEFAULT '📚',
            order_index INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS lessons (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id           INTEGER NOT NULL,
            title              TEXT    NOT NULL,
            explanation        TEXT,
            real_world         TEXT,
            commands           TEXT    DEFAULT '',
            code_example       TEXT    DEFAULT '',
            quiz_question      TEXT,
            quiz_answer        TEXT,
            difficulty         TEXT    DEFAULT 'beginner',
            estimated_minutes  INTEGER DEFAULT 10,
            tags               TEXT    DEFAULT '',
            analogy            TEXT    DEFAULT '',
            steps              TEXT    DEFAULT '',
            step_codes         TEXT    DEFAULT '',
            pitfalls           TEXT    DEFAULT '',
            takeaways          TEXT    DEFAULT '',
            order_index        INTEGER DEFAULT 0,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        );

        CREATE TABLE IF NOT EXISTS lesson_progress (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id    INTEGER NOT NULL UNIQUE,
            completed    INTEGER DEFAULT 0,
            completed_at TEXT,
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        );

        CREATE TABLE IF NOT EXISTS notes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id  INTEGER NOT NULL UNIQUE,
            body       TEXT    DEFAULT '',
            updated_at TEXT,
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        );
    """)

    # Additive migration: add deeper-content columns to lessons if an older
    # database is missing them. CREATE TABLE IF NOT EXISTS won't alter an
    # existing table, so we add columns explicitly. Safe to run repeatedly.
    existing_cols = {row[1] for row in db.execute('PRAGMA table_info(lessons)')}
    for col in ('analogy', 'steps', 'step_codes', 'pitfalls', 'takeaways'):
        if col not in existing_cols:
            db.execute(f"ALTER TABLE lessons ADD COLUMN {col} TEXT DEFAULT ''")

    db.commit()


def get_topic_progress(db, topic_id):
    """Return total/completed lesson counts and percentage for a topic."""
    total = db.execute(
        'SELECT COUNT(*) FROM lessons WHERE topic_id = ?', (topic_id,)
    ).fetchone()[0]

    completed = db.execute(
        '''SELECT COUNT(*) FROM lesson_progress
           JOIN lessons ON lesson_progress.lesson_id = lessons.id
           WHERE lessons.topic_id = ? AND lesson_progress.completed = 1''',
        (topic_id,)
    ).fetchone()[0]

    return {
        'total': total,
        'completed': completed,
        'percentage': round((completed / total * 100) if total > 0 else 0),
    }


@click.command('init-db')
def init_db_command():
    """Initialize the database schema."""
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
