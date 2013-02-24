import database as db

def sqlalchemy_middleware(app):
    def sqlalchemy_middleware_inner(environ, start_response):
        # This is a WSGI middleware because Flask cannot be trusted with
        # calling after_request handlers; don't ask me why, it just cannot.
        session = db.Session()
        try:
            result = app(environ, start_response)
            session.commit()
            return result
        finally:
            session.rollback()
            db.Session.remove()
    return sqlalchemy_middleware_inner
