import csv
from flask.cli import FlaskGroup

from project import app, database, Citizen


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    try:
        database.drop_all()
        database.create_all()
        database.session.commit()
        print("Database created.")
    except Exception as exception:
        print(exception)


@cli.command("fill_db")
def fill_db():
    try:
        with open("data.csv", "r") as file:
            rows = csv.DictReader(file)
            for row in rows:
                citizen = Citizen(
                    national_id=row["National ID"],
                    first_name=row["First Name"],
                    last_name=row["Last Name"],
                    health_status=row["Health Status"]
                )
                citizen.save()
        print("Database filled.")
    except Exception as exception:
        print(exception)


if __name__ == "__main__":
    cli()
