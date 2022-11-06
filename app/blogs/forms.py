from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired


class BlogForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired("Title cannot be empty")])
    content = TextAreaField(
        "Content", validators=[DataRequired("Content cannot be empty")]
    )
    tag = StringField(
        "Tag",
        validators=[InputRequired()],
        render_kw={"placeholder": "e.g. NSFW, Sports, Programming, Music"},
    )
    submit = SubmitField("Submit post")

    def validate_title(self, field: StringField):
        word_count = field.data.split()
        if 2 >= len(word_count) or len(word_count) > 15:
            raise ValidationError("Title should be between 2 and 15 words long")

    def validate_content(self, field: StringField):
        word_count = field.data.split()
        if not len(word_count) >= 2:
            raise ValidationError("Content cannot be less than 200 words")


class CommentForm(FlaskForm):

    comment_as = RadioField(
        "Comment as",
        validators=[InputRequired()],
        choices=("Guest", "Member - requires login"),
    )
    name = StringField(
        label="Name",
        validators=[DataRequired("Name cannot be empty")],
    )
    comment = TextAreaField("Comment", validators=[DataRequired(), Length(2, 500)])
    submit = SubmitField("Post comment")
