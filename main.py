from flask import Flask, url_for, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import colorgram
import os


app = Flask(__name__)
# delete os.environ.get("SECRET_KEY") and make up your own random string. ex. "alasjnfKHNsdf"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)


class PhotoForm(FlaskForm):
    photo = FileField("Upload image", validators=[FileRequired(),
                                                  FileAllowed([".gif", ".jpeg", "jpg", "png"],
                                                              message="Must be .gif, .jpeg, .jpg, .png image file.")])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def add_picture():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            "static", "img", filename
        ))
        return redirect(url_for("show_colors", file_path=filename))
    return render_template("index.html", form=form)


# TODO: make copy color one click (learn javascript)
@app.route("/upload/<file_path>")
def show_colors(file_path):
    path = f"static/img/{file_path}"
    colors = colorgram.extract(path, 10)
    all_colors = []
    for color in colors:
        r = color.rgb[0]
        g = color.rgb[1]
        b = color.rgb[2]
        all_colors.append((r, g, b))
    os.remove(path)
    return render_template("show_colors.html", colors=all_colors)


if __name__ == "__main__":
    app.run(debug=False)
