import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from base_classes import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Many to One with Category
    boards = relationship("Board", back_populates="forum")

    def create_board(self, board):
        self.boards.append(board)


class HumanReadableMixin(object):
    def human_readable_time(self):
        """Human readable datetime string.

        See https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior

        Currently returns formatted like:
        Jan. 28 1:17pm
        """
        return self.timestamp.strftime("%b. %d %I:%M%p")


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    forum_id = Column(Integer, ForeignKey('forum.id'))
    forum = relationship("Forum", back_populates="boards")

    # Many to One with Threads
    threads = relationship("Thread", back_populates="board")

    title = Column(String)

    def __init__(self, title):
        self.title = title

    def create_thread(self, thread):
        self.threads.append(thread)

    def get_post_count(self):
        return sum((len(thread.posts) for thread in self.threads))

    @hybrid_property
    def most_recent_post(self):
        return max((thread.most_recent_post
                    for thread in self.threads
                    if thread.most_recent_post),
                   key=lambda p: p.timestamp, default=None)

    def get_most_recent_post(self):
        """Return a Post object that is the most recent among all threads.

        Should return a Post object. It should query the database for the most
        recent post which is a property of this board
        ie.
        for thread in self.threads:
             for post in thread.posts:
                  find most recent
        """

        return self.most_recent_post


class Thread(HumanReadableMixin, Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    board_id = Column(Integer, ForeignKey('board.id'))
    board = relationship("Board", back_populates="threads")

    # Many to One with Posts
    posts = relationship("Post", back_populates="thread")

    @hybrid_property
    def most_recent_post(self):
        return max((post for post in self.posts), key=lambda p: p.timestamp,
                   default=None)

    title = Column(String)
    creator = Column(String)
    description = Column(String)
    category = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, title="unnamed thread", creator="None", description="", category="General"):
        self.title = title
        self.creator = creator.title()
        self.description = description
        self.category = category
        self.timestamp = datetime.datetime.utcnow()

    def write_post(self, post):
        self.posts.append(post)


class Post(HumanReadableMixin, Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to Many with Thread.
    thread_id = Column(Integer, ForeignKey('thread.id'))
    thread = relationship("Thread", back_populates="posts")

    content = Column(String)
    author = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, content="Error: Content missing", author="Unknown author"):
        self.content = content
        self.author = author
        self.timestamp = datetime.datetime.utcnow()