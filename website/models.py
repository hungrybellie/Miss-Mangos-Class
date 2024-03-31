from . import db # import the db from the current package
from flask_login import UserMixin # UserMixin provides generic implementations of several methods that Flask-Login requires
from sqlalchemy.sql import func # func allows access to important SQL functions
import enum
from sqlalchemy import Enum

# Enum for study set visibility options
class StudySetVisibility(enum.Enum):
    PRIVATE = 'private'
    FRIENDS_ONLY = 'friends only'
    PUBLIC = 'public'

# Enum for friendship status options
class FriendshipStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'

# Enum for permissions for shared study sets
class StudySetSharedPermissions(enum.Enum):
    VIEW = 'view'
    EDIT = 'edit'

# Represents friendships between users
class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(Enum(FriendshipStatus), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

# Represents shared study set relationships in which a user shares a study set with another user
class SharedStudySet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_set_id = db.Column(db.Integer, db.ForeignKey('study_set.id', ondelete='CASCADE'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    shared_user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    permissions = db.Column(Enum(StudySetSharedPermissions), nullable=False)
    shared_on = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    owner = db.relationship('User', foreign_keys=[owner_id], backref='shared_study_sets', passive_deletes=True)

# Represents users in the system
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    friends = db.relationship( # dynamic relationship for friendships, combining requested and received friendships
        'Friendship',
        foreign_keys=[Friendship.requester_id, Friendship.receiver_id],
        primaryjoin='or_(User.id==Friendship.requester_id, User.id==Friendship.receiver_id)',
        backref='related_users',
        lazy='dynamic',
        passive_deletes=True)
    study_sets = db.relationship('StudySet', backref='user', passive_deletes=True)
    shared_study_sets = db.relationship(
        'SharedStudySet',
        foreign_keys=[SharedStudySet.shared_user_id],
        backref='shared_user',
        lazy='dynamic',
        passive_deletes=True)

    # Gets friendships that the user requested and are still pending
    def get_requested_pending_friend_requests(self):
        return Friendship.query.filter_by(
            requester_id=self.id, 
            status=FriendshipStatus.PENDING
        ).all()
    
    # Gets friendships that have been received by the user and are still pending
    def get_received_pending_friend_requests(self):
        return Friendship.query.filter_by(
            receiver_id=self.id, 
            status=FriendshipStatus.PENDING
        ).all()
    
    # Gets friendships that the user is actually friends with
    def get_accepted_friends(self):
        return Friendship.query.filter_by(
            or_(requester_id == self.id, receiver_id == self.id), 
            status=FriendshipStatus.ACCEPTED
        ).all()

# Represents study sets created by users
class StudySet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False, default='')
    visibility = db.Column(Enum(StudySetVisibility), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    question_answers = db.relationship('QuestionAnswer', backref='study_set', passive_deletes=True)
    audio = db.relationship('Audio', backref='study_set', uselist=False, passive_deletes=True)
    shared_with = db.relationship('SharedStudySet', backref='study_set', passive_deletes=True)

# Represents questions and answers associated with a study set
class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_set_id = db.Column(db.Integer, db.ForeignKey('study_set.id', ondelete='CASCADE'), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

# Represents audios associated with a study set
class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_set_id = db.Column(db.Integer, db.ForeignKey('study_set.id', ondelete='CASCADE'), nullable=False)
    audio_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())