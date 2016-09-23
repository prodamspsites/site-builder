# coding: utf-8
from datetime import datetime
from builder.models import Model, db, User


class Invite(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'invite'
    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    guest_id = db.Column(db.Integer, db.ForeignKey(User.id))

    # Statuses
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    sent_at = db.Column(db.DateTime, index=True)
    viewed_at = db.Column(db.DateTime, index=True)
    accepted_at = db.Column(db.DateTime, index=True)
    current_status = db.Column(db.String(20), default='created')
    sent_count = db.Column(db.Integer(), default=0)

    @property
    def host(self):
        return User.query.get(self.host_id)

    @property
    def guest(self):
        return User.query.get(self.guest_id)

    @staticmethod
    def create_invite(host, guest_name, guest_email):
        guest = User.create(email=guest_email, name=guest_name, invite=True)
        invite = Invite()
        invite.host_id = host.id
        invite.guest_id = guest.id
        invite.save(commit=True)
        return invite
