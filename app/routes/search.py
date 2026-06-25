from flask import Blueprint, render_template, request
from app.database import get_db

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()[:200]

    if not query:
        return render_template('search.html', topic_results=[], lesson_results=[], query='')

    db = get_db()
    pattern = f'%{query}%'

    topic_results = db.execute(
        'SELECT * FROM topics WHERE name LIKE ? OR description LIKE ? ORDER BY order_index',
        (pattern, pattern)
    ).fetchall()

    lesson_results = db.execute(
        '''SELECT lessons.*, topics.name AS topic_name, topics.id AS t_id, topics.icon AS topic_icon
           FROM lessons
           JOIN topics ON lessons.topic_id = topics.id
           WHERE lessons.title LIKE ?
              OR lessons.explanation LIKE ?
              OR lessons.tags LIKE ?
              OR lessons.real_world LIKE ?
           ORDER BY topics.order_index, lessons.order_index''',
        (pattern, pattern, pattern, pattern)
    ).fetchall()

    return render_template(
        'search.html',
        topic_results=[dict(t) for t in topic_results],
        lesson_results=[dict(l) for l in lesson_results],
        query=query,
    )
