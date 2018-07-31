from flask import Flask, render_template, request
from models import db, User
from forms import SignupForm
import pdb

app = Flask(__name__)

# Add database URI to app config for connecting to db (see flask SQLalchemy docs for more)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:foobar123@localhost:5432/latitude"
# Initialise the database
db.init_app(app)

# This secret key will be used by flask to generate secure forms. We will use
# this to configure forms to protect against CSRF (cross-sight request forgery)
app.secret_key = "development-key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    # Could greatly shorten the logic below using form.validate_on_submit()
    # which returns true if the request is a POST and the form is valid. Have used
    # more verbose logic for clarity

    # POST request --> user has submitted signup information using the form
    if request.method == "POST":
        if form.validate() == False:
            # Reload the form if data doesn't validate
            return render_template("signup.html", form=form)
        else:
            # Create a new user object based on form data
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)

            # Add user to the database
            db.session.add(newuser)
            db.session.commit()
            return "Success"

    # GET request --> user is requesting the signup page
    elif request.method == "GET":
        # Send the form as an argument in render_template
        return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
