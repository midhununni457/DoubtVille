from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, MultipleFileField
from wtforms.validators import InputRequired, Length, Regexp, ValidationError
from webapp.models import User

subs = [('Maths', 'Maths'), ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('Biology', 'Biology'), ('Computer', 'Computer'),
        ('Business', 'Business'), ('Accountancy', 'Accountancy'), ('Economics', 'Economics')]
stds = [('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')]

class RegistrationForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('This is a required field'), Length(min=5, max=50),
                                                Regexp(regex="[A-Z][a-z]+ [A-Z]*.", message='Should be a valid name')])
    email = StringField('Email ID registered with the school', validators=[InputRequired('This is a required field'), Length(min=23, max=35),
                                                                           Regexp(regex='.+@bhavanseroor\.ac\.in', message='Use the email provided by the school')])
    adm_no = StringField('Admission number', validators=[InputRequired('This is a required field'), Length(min=4, max=5),
                                                         Regexp(regex='\d', message='Should be a number')])
    std = SelectField('Class', validators=[InputRequired('This is a required field')], choices=stds)
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account already exists with that email. Please use your own email')

    def validate_adm_no(self, adm_no):
        user = User.query.filter_by(adm_no=adm_no.data).first()
        if user:
            raise ValidationError('Account already exists with that admission number. Please use your own admission number')

class LoginForm(FlaskForm):
    email = StringField('Enter registered email address', validators=[InputRequired('This is a required field'), Length(min=23, max=35),
                                                                      Regexp(regex=".+@bhavanseroor\.ac\.in", message='Use the email provided by the school')])
    adm_no = StringField('Admission number', validators=[InputRequired('This is a required field'), Length(min=4, max=5),
                                                         Regexp(regex="\d", message='Should be a number 4 or 5 characters long')])
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    name = StringField('Full name:', validators=[InputRequired('This is a required field'), Length(min=5, max=50),
                                                 Regexp(regex="[A-Z][a-z]+ [A-Z]*.", message='Should be a valid name')])
    std = StringField('Class:', validators=[InputRequired('This is a required field'), Length(min=1, max=2, message='Class should be between 6 and 12'),
                                            Regexp(regex="(6|7|8|9|10|11|12)", message='Class should be between 6 and 12')])
    submit = SubmitField('Update')

class NewQuestionForm(FlaskForm):
    question = TextAreaField('Write the question in 1 or 2 sentences', validators=[InputRequired('This is a required field'), Length(min=5, max=100)])
    content = TextAreaField('Provide a detailed description of the question', validators=[InputRequired()])
    post_std = SelectField('Class at which the topic of the question is covered', validators=[InputRequired('This is a required field')], choices=stds)
    subject = SelectField('Subject of the question', validators=[InputRequired('This is a required field')],
                          choices=subs)
    post_image = MultipleFileField('Insert image', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Post')