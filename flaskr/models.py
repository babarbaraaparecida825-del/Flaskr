from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)

    # Relacionamento 1:N (Um usuário pode ter vários posts, pode publicar mais de uma vez)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    imagem_post = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Post {self.title}>"