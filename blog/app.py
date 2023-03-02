from flask import Flask
from flask import request
from blog.views.users import users_app
from blog.views.articles import articles_app

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello web!"


@app.route("/greet/<name>/")
def greet_name(name: str):
    return f"Hello {name}!"


@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"


@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom status code
        send request using POST method
        and pass `code` in JSON body / FormData
        """

    print("raw bytes data:", request.data)

    if request.form and "code" in request.form:
        return "code from form", request.form["code"]
    
    if request.json and "code" in request.json:
        return "code from json", request.json["code"]
    
    return "", 204


@app.route("/divide-by-zero/")
def do_zero_division():
    return 1 / 0


@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    print(error) # prints str version of error: 'division by zero'
    app.logger.exception("Here's traceback for zero division error")
    return "Never divide by zero!", 400


from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(users_app, url_prefix="/users")

app.register_blueprint(articles_app, url_prefix="/articles")
