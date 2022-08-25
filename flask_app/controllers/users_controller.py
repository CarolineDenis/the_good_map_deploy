from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user_model, orga_model, project_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    projects = project_model.Project.get_hightlight_projects()
    if 'id' in session:
        data = {
            'id' : session['id']
        }
        liked = project_model.Project.get_all_liked(data)
    else:
        liked = []
    return render_template("index.html", projects=projects, liked=liked)

@app.route('/post_like', methods=['POST'])
def like():
    data = {
        'id': session['id'],
        'project_id': request.form['project_id']
        }
    user_model.User.like(data)
    return redirect('/')

@app.route('/unlike', methods=['POST'])
def unlike():
    data = {
        'id': session['id'],
        'project_id': request.form['project_id']
        }
    user_model.User.unlike(data)
    return redirect('/')

@app.route('/create_user', methods=['POST'])
def create():
    if not user_model.User.validate_form(request.form):
        return redirect('/register_user')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'profile': request.form['profile'],
        'password': pw_hash
    }
    id = user_model.User.create(data)
    session['id'] = id
    session['email'] = request.form['email']
    return redirect('/dashboard_user')

@app.route('/register_user')
def register_user():
    return render_template("sign_up_user.html")

@app.route('/sign_in')
def sign_in_user():
    return render_template("sign_in.html")

@app.route('/login_user', methods=['POST'])
def log_in():
    data = {
        'email': request.form['email'],
    }
    user_in_db = user_model.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credential", "err_log")
        return redirect('/sign_in')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Credential", "err_log")
            return redirect('/')
    if user_in_db:
        session['email'] = user_in_db.email
        session['id'] = user_in_db.id
        return redirect('/dashboard_user')

@app.route('/dashboard_user')
def dashboard():
    if not "email" in session:
        return redirect('/')
    data = {
        'email': session['email'],
        'id': session['id']
    }
    project_liked = user_model.User.get_like(data)
    user = user_model.User.get_by_email(data)
    return render_template("user.html", user=user, project_liked=project_liked)


@app.route("/user/<int:id>/edit")
def edit_user(id):
    if not "id" in session:
        return redirect('/')
    data = {
        "id": id
    }
    user = user_model.User.read_one(data)
    return render_template("sign_up_user_edit.html", user=user)

#save updates
@app.route("/user/<int:id>/update", methods=["POST"])
def update_user(id):
    if not "id" in session:
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'profile': request.form['profile'],
        'id': session['id']
    }
    user_model.User.udpdate(data)
    return redirect("/dashboard_user")

@app.route("/logout")
def delete_session():
    session.clear()
    return redirect("/")

@app.route("/orga_or_user")
def orga_or_user():
    return render_template("orga_or_user.html")

@app.route("/map")
def map():
    projects = project_model.Project.get_all_projects()
    print(projects)
    return render_template("maps.html", projects = projects)