# Models

class User(db.Model):
    """User model
    Has some necessary boilerplate around flask-login and
    is storing password in an unsecure way.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    # XXX should be hashed.
    password = db.Column(db.String(80))
    
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
