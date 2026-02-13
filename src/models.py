from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

Follower = Table(
    "followers",
    db.metadata,
    Column("user_from_id", ForeignKey("user.id"), primary_key=True),
    Column("user_to_id", ForeignKey("user.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50))
    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary=Follower,
        primaryjoin=id==Follower.c.user_to_id,      
        secondaryjoin=id==Follower.c.user_from_id,  
        back_populates="following",
        foreign_keys=[Follower.c.user_to_id, Follower.c.user_from_id]
    )
    following: Mapped[List["User"]] = relationship(
        "User",
        secondary=Follower,
        primaryjoin=id==Follower.c.user_from_id,      
        secondaryjoin=id==Follower.c.user_to_id, 
        back_populates="followers",
        foreign_keys=[Follower.c.user_from_id, Follower.c.user_to_id]
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author" 
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author"
    )


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "followers": [User.serialize() for user in self.followers], 
            "following": [User.serialize() for user in self.following]
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
        back_populates="comments"
    )

    author: Mapped["User"] = relationship(
        back_populates="comments"
    )

    def serialize(self):
        return{
          "id": self.id,
          "comment_text": self.comment_text,
          "post_id": self.post_id,
          "author_id": self.author_id,
          "post": [Comment.serialize() for comment in self.post]
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    author: Mapped["User"] = relationship(
      back_populates="posts"
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
            "user_id": self.user_id,
            "comments": self.comments
            
        }
    