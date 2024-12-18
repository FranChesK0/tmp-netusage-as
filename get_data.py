from app.models import User


def main() -> None:
    user = User.query.filter_by(username="Александр").first()
    print(user)


if __name__ == "__main__":
    main()
