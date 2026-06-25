from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from app.database import get_db

lessons_bp = Blueprint('lessons', __name__)


@lessons_bp.route('/lessons/<int:lesson_id>')
def detail(lesson_id):
    db = get_db()

    lesson = db.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
    if lesson is None:
        abort(404)

    topic = db.execute(
        'SELECT * FROM topics WHERE id = ?', (lesson['topic_id'],)
    ).fetchone()

    prev_lesson = db.execute(
        '''SELECT id, title FROM lessons
           WHERE topic_id = ? AND order_index < ?
           ORDER BY order_index DESC LIMIT 1''',
        (lesson['topic_id'], lesson['order_index'])
    ).fetchone()

    next_lesson = db.execute(
        '''SELECT id, title FROM lessons
           WHERE topic_id = ? AND order_index > ?
           ORDER BY order_index ASC LIMIT 1''',
        (lesson['topic_id'], lesson['order_index'])
    ).fetchone()

    progress = db.execute(
        'SELECT completed FROM lesson_progress WHERE lesson_id = ?',
        (lesson_id,)
    ).fetchone()
    is_completed = bool(progress['completed']) if progress else False

    tags = [t.strip() for t in lesson['tags'].split(',') if t.strip()] if lesson['tags'] else []
    commands = [c.strip() for c in lesson['commands'].split('\n') if c.strip()] if lesson['commands'] else []

    note_row = db.execute(
        'SELECT body, updated_at FROM notes WHERE lesson_id = ?', (lesson_id,)
    ).fetchone()
    note = note_row['body'] if note_row else ''
    note_updated = note_row['updated_at'] if note_row else None

    return render_template(
        'lesson.html',
        lesson=dict(lesson),
        topic=dict(topic),
        prev_lesson=dict(prev_lesson) if prev_lesson else None,
        next_lesson=dict(next_lesson) if next_lesson else None,
        is_completed=is_completed,
        tags=tags,
        commands=commands,
        note=note,
        note_updated=note_updated,
        current_topic_id=topic['id'],
    )


@lessons_bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
def mark_complete(lesson_id):
    db = get_db()

    lesson = db.execute('SELECT id FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
    if lesson is None:
        abort(404)

    existing = db.execute(
        'SELECT id FROM lesson_progress WHERE lesson_id = ?', (lesson_id,)
    ).fetchone()

    if existing:
        db.execute(
            "UPDATE lesson_progress SET completed = 1, completed_at = datetime('now') WHERE lesson_id = ?",
            (lesson_id,)
        )
    else:
        db.execute(
            "INSERT INTO lesson_progress (lesson_id, completed, completed_at) VALUES (?, 1, datetime('now'))",
            (lesson_id,)
        )

    db.commit()
    return redirect(url_for('lessons.detail', lesson_id=lesson_id))


@lessons_bp.route('/lessons/<int:lesson_id>/note', methods=['POST'])
def save_note(lesson_id):
    db = get_db()

    lesson = db.execute('SELECT id FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
    if lesson is None:
        abort(404)

    body = request.form.get('body', '').strip()

    existing = db.execute(
        'SELECT id FROM notes WHERE lesson_id = ?', (lesson_id,)
    ).fetchone()

    if existing:
        db.execute(
            "UPDATE notes SET body = ?, updated_at = datetime('now') WHERE lesson_id = ?",
            (body, lesson_id)
        )
    else:
        db.execute(
            "INSERT INTO notes (lesson_id, body, updated_at) VALUES (?, ?, datetime('now'))",
            (lesson_id, body)
        )

    db.commit()
    flash('Note saved.' if body else 'Note cleared.')
    # Jump straight back to the notes section after saving (PRG pattern).
    return redirect(url_for('lessons.detail', lesson_id=lesson_id) + '#notes-section')
