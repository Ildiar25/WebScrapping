from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from flask_login import UserMixin

from app import db, bcrypt, login_manager


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(20))
    user_email = Column(String(60), unique=True, index=True)
    user_password = Column(String(80))
    create_date = Column(DateTime, default=datetime.now)

    def __init__(
            self,
            user_name: str | None = None,
            user_email: str | None = None,
            user_password: str | None = None
    ) -> None:
        self.user_name: str | None = user_name
        self.user_email: str | None = user_email
        self.user_password: str | None = user_password

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.user_password, password)

    @classmethod
    def create_user(cls, user: str, email: str, password: str) -> "User":
        user = cls(
            user_name=user,
            user_email=email,
            user_password=bcrypt.generate_password_hash(password).decode("utf-8")
        )

        # Save user into database
        db.session.add(user)
        db.session.commit()

        return user


@login_manager.user_loader
def load_user(id: int) -> User | None:
    return User.query.get(int(id))


def main():
    user = User.create_user("Joan", "joan@gmail.com", "admin1234")
    print(user)
    print(user.user_id, user.user_name, user.user_email, user.user_password, user.create_date)

    user2 = User()
    print(user2)
    print(user2.user_id, user2.user_name, user2.user_email, user2.user_password, user2.create_date)


if __name__ == '__main__':
    main()
