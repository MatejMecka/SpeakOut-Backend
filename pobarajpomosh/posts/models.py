"""
models.py

Responsible for Handling the Posts, Likes and Categories

"""
from sqlalchemy import Column, Integer, String, Text, DateTime
import datetime
from .. import db, ma


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return'<Post {}>'.format(self.id)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(1024), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    approved = db.Column(db.Integer, nullable=False, default=0)
    reported = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.datetime.utcnow)

    def __repr__(self):
        return'<Post {}>'.format(self.id)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    body = db.Column(db.String(1024), nullable=False)
    approved = db.Column(db.Integer, nullable=False, default=0)
    reported = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.datetime.utcnow)

    def __repr__(self):
        return'<Post {}>'.format(self.id)


class PostSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'author_id', 'title', 'body', 'category',
                  'likes', 'approved', 'created')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class CommentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'author_id', 'body', 'likes', 'approved', 'created')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return'<Like {}>'.format(self.id)

class LikeComment(db.Model):
    __tablename__ = "comment_likes"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return'<Comment Like {}>'.format(self.id)
