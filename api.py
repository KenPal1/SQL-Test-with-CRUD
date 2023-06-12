from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "world_x"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/city", methods=["GET"])
def get_city():
    data = data_fetch("""SELECT * FROM city""")
    return make_response(jsonify(data), 200)


@app.route("/city/<int:ID>", methods=["GET"])
def get_city_by_id(ID):
    data = data_fetch("""SELECT * FROM city where ID = {}""".format(ID))
    return make_response(jsonify(data), 200)


@app.route("/city/<int:ID>/country", methods=["GET"])
def get_language_by_city(ID):
    data = data_fetch(
        """
        SELECT country.Code, country.Name, countrylanguage.Language
        FROM city
        INNER JOIN country
        ON city.CountryCode = country.Code 
        INNER JOIN countrylanguage
        ON country.Code = countrylanguage.CountryCode
        WHERE city.ID = {}
    """.format(
            ID
        )
    )
    return make_response(
        jsonify({"ID": ID, "count": len(data), "Country Info": data}), 200
    )


@app.route("/city", methods=["POST"])
def add_city():
    cur = mysql.connection.cursor()
    info = request.get_json()
    Name = info["Name"]
    CountryCode = info["CountryCode"]
    cur.execute(
        """ INSERT INTO city (Name, CountryCode) VALUE (%s, %s)""",
        (Name, CountryCode),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "City added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/city/<int:ID>", methods=["PUT"])
def update_city(ID):
    cur = mysql.connection.cursor()
    info = request.get_json()
    Name = info["Name"]
    CountryCode = info["CountryCode"]
    cur.execute(
        """ UPDATE city SET Name = %s, CountryCode = %s WHERE ID = %s """,
        (Name, CountryCode, ID),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "City updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/city/<int:ID>", methods=["DELETE"])
def delete_city(ID):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM city where ID = %s """, (ID,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/test_route", methods=["GET"])
def test_route():
    fmt = request.args.get("ID")
    foo = request.args.get("Test")
    return make_response(jsonify({"ID":fmt, "Test":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
