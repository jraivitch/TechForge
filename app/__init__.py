import os
from flask import Flask
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from .database import get_db, init_app as init_db_app

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    secret = os.environ.get('SECRET_KEY')
    if not secret:
        if os.environ.get('FLASK_ENV') == 'production':
            raise RuntimeError('SECRET_KEY environment variable must be set in production')
        secret = 'dev-only-do-not-use-in-production'

    app.config.from_mapping(
        SECRET_KEY=secret,
        DATABASE=os.path.join(app.instance_path, 'techforge.db'),
        WTF_CSRF_TIME_LIMIT=3600,
    )

    os.makedirs(app.instance_path, exist_ok=True)

    csrf.init_app(app)

    csp = {
        'default-src': "'self'",
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'img-src': "'self' data:",
    }
    Talisman(
        app,
        content_security_policy=csp,
        force_https=False,
    )

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
