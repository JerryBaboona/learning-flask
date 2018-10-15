from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Inherit from base class FlaskForm
class SignupForm(FlaskForm):
    # Fields
    # Use validators to validate the fields in the form. The DataRequired
    # validator checks to see if the field has been left empty.
    # Can customise validation message text, but for this to be seen by the user
    # we have to ensure in the template that the corresponding form field doesn't
    # use the "required" HTML attributed
    first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."),
                                                     Length(min=6, message="Passwords must be 6 characters or more.")])

    # Submit button
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    # Fields
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])

    # Submit button
    submit = SubmitField('Log in')
