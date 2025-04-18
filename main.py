from app import create_app, db


def main():
    app = create_app("dev")

    with app.app_context():
        db.create_all()

    app.run(debug=True)


if __name__ == '__main__':
    main()
