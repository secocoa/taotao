# from flask_cache import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
# rom flask_cors import CORS

from app.models import db

sess = Session()
migrate = Migrate(db=db)
# cache = Cache(with_jinja2_ext=False)

# cors = CORS()
mail = Mail()

def init_ext(app):
    sess.init_app(app)
    migrate.init_app(app)
    # cache.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    # cors.init_app(app)
