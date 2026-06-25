from flask import Blueprint, render_template
from app.database import get_db, get_topic_progress

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    db = get_db()

    topics = db.execute('SELECT * FROM topics ORDER BY order_index').fetchall()

    topics_with_progress = []
    for topic in topics:
        prog = get_topic_progress(db, topic['id'])
        topics_with_progress.append({**dict(topic), **prog})

    total_lessons = db.execute('SELECT COUNT(*) FROM lessons').fetchone()[0]
    total_completed = db.execute(
        'SELECT COUNT(*) FROM lesson_progress WHERE completed = 1'
    ).fetchone()[0]
    total_topics = len(topics_with_progress)

    in_progress = [t for t in topics_with_progress if 0 < t['percentage'] < 100]
    not_started = [t for t in topics_with_progress if t['percentage'] == 0]
    continue_topics = in_progress or not_started[:3]

    return render_template(
        'dashboard.html',
        topics=topics_with_progress,
        continue_topics=continue_topics[:3],
        total_lessons=total_lessons,
        total_completed=total_completed,
        total_topics=total_topics,
    )
