from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, LoginForm
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
    # If user is already logged in, redirect to home page
    if "email" in session:
        return redirect(url_for("home"))
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

            # Create a session for that user - use email as ID for session
            session["email"] = newuser.email

            # Redirect to the home page
            return redirect(url_for("home"))

    # Strictly speaking don't need elif statement here as all code paths
    # in above if statement end in return, so this code cannot be reached
    # if the first statement (i.e. POST request) passes as True
    # GET request --> user is requesting the signup page
    elif request.method == "GET":
        # Send the form as an argument in render_template
        return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in, redirect to home page
    if "email" in session:
        return redirect(url_for("home"))
    form = LoginForm()

    # POST request --> user has submitted login information using the form
    if request.method == "POST":
        if form.validate() == False:
            # Reload the form if data doesn't validate
            return render_template("login.html", form=form)
        else:
            # Log user in
            email = form.email.data
            password = form.password.data

            # Query the database for that user (by email, which is unique)
            user = User.query.filter_by(email=email).first()

            # Check if the password is valid (and user exists)
            if user is not None and user.check_password(password):
                # Add email to session cookie and redirect to their home page
                session["email"] = email
                return redirect(url_for("home"))
            else:
                return redirect(url_for("login"))

    # GET request --> user is requesting the login page
    elif request.method == "GET":
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    # Remove the user email from the session cookie and redirect to index
    session.pop("email", None)
    return redirect(url_for("index"))


@app.route("/home")
def home():
    # Check if email has been set in session - if not, user is not
    # logged in and should be redirected to log in page
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
