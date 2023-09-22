from flask import Flask, send_file, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.config import FILES_OUTPUT_DIR
from application.services.create_table import create_table
from application.services.csv_reader import read_csv, calculate_average_height_weight
from application.services.db_connection import DBConnection
from application.services.processing_json import output_json, getting_request
from application.services.processing_users import format_users, output_user_info
from application.services.read_file import read_file

app = Flask(__name__)


@app.route("/")
def home_page():
    return "This is homepage"


@app.route("/phones/create")
@use_args({"contact_name": fields.Str(required=True), "phone_value": fields.Int(required=True)}, location="query")
def phones_create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value)",
                {"contact_name": args["contact_name"], "phone_value": args["phone_value"]},
            )

    return "Ok"


@app.route("/phones/read-all")
def phones_read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()
    return "<br>".join([f'{phone["user_id"]}: {phone["contact_name"]} - {phone["phone_value"]}' for phone in phones])


@app.route("/phones/read/<int:user_id>")
def phones_read(user_id: int):
    with DBConnection() as connection:
        phone = connection.execute(
            "SELECT * FROM phones WHERE (user_id=:user_id);",
            {
                "user_id": user_id,
            },
        ).fetchone()

    return f'{phone["user_id"]}: {phone["contact_name"]} - {phone["phone_value"]}'


@app.route("/phones/update/<int:user_id>")
@use_args({"contact_name": fields.Str(), "phone_value": fields.Int()}, location="query")
def phone_update(args, user_id: int):
    with DBConnection() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} WHERE user_id=:user_id;",
                {
                    "user_id": user_id,
                    "contact_name": contact_name,
                    "phone_value": phone_value,
                },
            )

    return "OK"


@app.route("/phones/delete/<int:user_id>")
def phone_delete(user_id: int):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE FROM phones WHERE (user_id=:user_id);",
                {
                    "user_id": user_id,
                },
            )

    return "Ok"


@app.route("/get-content/")
def get_content():
    return read_file()


# Альтернативна реалізація для перегляду вмісту файла
@app.route("/new.txt")
def download():
    file = FILES_OUTPUT_DIR / "new.txt"
    if not file.is_file():
        read_file()
    return send_file(file)


@app.route("/generate-users/")
@use_args({"amount": fields.Int(missing=100)}, location="query")
def users_generate(args):
    amount = args["amount"]
    formatted_users = format_users(amount)
    output = output_user_info(formatted_users)
    return f"<ol>{output}</ol>"


@app.route("/space/")
def cosmonauts():
    json_file = getting_request("http://api.open-notify.org/astros.json")
    return output_json(json_file)


@app.route("/mean/")
def average_h_w():
    # Getting data - START #
    url = "https://drive.google.com/uc?export=download&id=13nk_FYpcayUck2Ctrela5Tjt9JQbjznt"
    # Getting data - END #

    read = read_csv(url)
    return calculate_average_height_weight(read)


create_table()

if __name__ == "__main__":
    app.run()
