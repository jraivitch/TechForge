from flask import Blueprint, render_template, abort
from app.database import get_db, get_topic_progress

topics_bp = Blueprint('topics', __name__)


@topics_bp.route('/topics')
def index():
    db = get_db()
    topics = db.execute('SELECT * FROM topics ORDER BY order_index').fetchall()

    topics_with_progress = []
    for topic in topics:
        prog = get_topic_progress(db, topic['id'])
        topics_with_progress.append({**dict(topic), **prog})

    return render_template('topics.html', topics=topics_with_progress)


@topics_bp.route('/topics/<int:topic_id>')
def detail(topic_id):
    db = get_db()

    topic = db.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    if topic is None:
        abort(404)

    lessons = db.execute(
        'SELECT * FROM lessons WHERE topic_id = ? ORDER BY order_index',
        (topic_id,)
    ).fetchall()

    lessons_with_status = []
    for lesson in lessons:
        progress = db.execute(
            'SELECT completed FROM lesson_progress WHERE lesson_id = ?',
            (lesson['id'],)
        ).fetchone()
        lessons_with_status.append({
            **dict(lesson),
            'completed': progress['completed'] if progress else 0,
        })

    prog = get_topic_progress(db, topic_id)

    return render_template(
        'topic_detail.html',
        topic=dict(topic),
        lessons=lessons_with_status,
        progress=prog['percentage'],
        completed=prog['completed'],
        total=prog['total'],
        current_topic_id=topic_id,
    )
