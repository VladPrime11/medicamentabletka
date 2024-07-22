from models.user import User, Medication, session

class Storage:
    def add_user(self, username, chat_id):
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(username=username, chat_id=chat_id)
            session.add(user)
            session.commit()
        return user

    def add_medication(self, user, name, date_time):
        medication = Medication(name=name, date_time=date_time, user=user)
        session.add(medication)
        session.commit()

    def get_user(self, chat_id):
        return session.query(User).filter_by(chat_id=chat_id).first()
