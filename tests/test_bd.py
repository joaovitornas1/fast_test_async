# pyright: basic
from dataclasses import asdict
from fast_test_async.models import User
from sqlalchemy import select


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="test", email="test@email.com", password="secret"
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == "test"))
        assert asdict(user) == {
            "id": 1,
            "username": "test",
            "email": "test@email.com",
            "password": "secret",
            "created_at": time,
            "update_at": time,
        }
