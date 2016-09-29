# coding: utf-8
from base64 import b64encode
from datetime import datetime, timedelta
from flask import current_app, request, url_for
from builder.exceptions import InvalidToken, InviteNotFound
from builder.models import Model, db, User


class Invite(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'invite'
    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    guest_id = db.Column(db.Integer, db.ForeignKey(User.id))

    # Statuses
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    last_sent_at = db.Column(db.DateTime, index=True)
    expire_at = db.Column(db.DateTime, index=True)
    viewed_at = db.Column(db.DateTime, index=True)
    accepted_at = db.Column(db.DateTime, index=True)
    current_status = db.Column(db.String(20), default='criado')
    sent_count = db.Column(db.Integer(), default=0)

    @property
    def host(self):
        return User.query.get(self.host_id)

    @property
    def guest(self):
        return User.query.get(self.guest_id)

    @property
    def activation_url(self):
        encoded_bytes = '{}:{}'.format(self.guest.email, self.guest.temporary_token).encode()
        base64_string = b64encode(encoded_bytes).decode()
        url_prefix = request.host
        url_suffix = url_for('security.confirm_invite')
        return 'http://{}{}?t={}'.format(url_prefix, url_suffix, base64_string)

    @staticmethod
    def create_invite(host, guest_name, guest_email):
        guest = User.create(email=guest_email, name=guest_name, invite=True)
        invite = Invite()
        invite.host_id = host.id
        invite.guest_id = guest.id
        invite.expire_at = datetime.now() + timedelta(days=current_app.config['INVITE_EXPIRE'])
        invite.current_status = 'criado'
        invite.save(commit=True)
        return invite

    @classmethod
    def get_invite(cls, guest_email):
        user = User.by_email(guest_email)
        invite = cls.query.filter(cls.guest_id == user.id).first()

        if not invite:
            raise InviteNotFound

        return invite

    def is_valid(self):
        if self.current_status == 'aceito':
            return False

        if datetime.now() < self.expire_at:
            return True

        self.current_status = 'inválido'
        self.save(commit=True)
        return False

    def view(self):
        if self.is_valid():
            self.viewed_at = datetime.now()
            self.current_status = 'visualizado'
            self.save(commit=True)
            return True

    def accept(self, temporary_token, password, confirm_password):
        if self.is_valid():
            self.guest.create_password(temporary_token=temporary_token,
                                       password=password,
                                       confirm_password=confirm_password)
            self.accepted_at = datetime.now()
            self.current_status = 'aceito'
            self.save(commit=True)
            return True
        else:
            raise InvalidToken

    def send(self):
        if not self.is_valid():
            self.expire_at = datetime.now() + timedelta(days=current_app.config['INVITE_EXPIRE'])

        self.current_status = 'enviado'
        if self.sent_count > 0:
            self.current_status = 'reenviado'

        self.sent_count += 1
        self.save(commit=True)
        # function for send email
