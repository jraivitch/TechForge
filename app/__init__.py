import os
from flask import Flask
from .database import get_db, init_app as init_db_app


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'techforge.db'),
    )

    os.makedirs(app.instance_path, exist_ok=True)

    init_db_app(app)

    from .routes.dashboard import dashboard_bp
    from .routes.topics import topics_bp
    from .routes.lessons import lessons_bp
    from .routes.search import search_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(topics_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(search_bp)

    @app.context_processor
    def inject_globals():
        db = get_db()
        sidebar_topics = db.execute(
            'SELECT id, name, icon FROM topics ORDER BY order_index'
        ).fetchall()
        return {
            'sidebar_topics': [dict(t) for t in sidebar_topics],
            'current_topic_id': None,
        }

    return app
