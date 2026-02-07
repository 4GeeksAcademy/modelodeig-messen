from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50))

    posts: Mapped[list["Post"]] = relationship(
        back_populates="comment" 
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author"
    )

    followers: Mapped[list["Follower"]] = relationship(
        foreign_keys="Follower.user_to_id"
    )

    following: Mapped[list["Follower"]] = relationship(
        foreign_keys="Follower.user_from_id"
    )


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
            # do not serialize the password, its a security breach
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    url: Mapped[str] = mapped_column(String(150), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post: Mapped["Post"] = relationship(
        back_populates="media"
    )


    def serialize(self):
        return{
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    post: Mapped["Post"] = relationship(
        back_populates="comment"
    )

    author: Mapped["User"] = relationship(
        back_populates="comment"
    )

    def serialize(self):
        return{
          "id": self.id,
          "comment_text": self.comment_text,
          "post_id": self.post_id,
          "author_id": self.author_id
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    author: Mapped["User"] = relationship(
      back_populates="post"
    )

    comments: Mapped["Comment"] = relationship(
        back_populates="post"
    )

    media: Mapped["Media"] = relationship(
        back_populates="post"
    )

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.id
        }
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }