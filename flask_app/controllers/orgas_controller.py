from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user_model, orga_model, project_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create_orga', methods=['POST'])
def create_orga():
    if not orga_model.Orga.validate_form(request.form):
        return redirect('/register_orga')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'email': request.form['email'],
        'date': request.form['date'],
        'logo': request.form['logo'],
        'password': pw_hash
    }
    org_id = orga_model.Orga.create_orga(data)
    session['email'] = request.form['email']
    session['org_id'] = org_id
    return redirect('/dashboard_orga')

@app.route('/register_orga')
def register_orga():
    return render_template("sign_up_orga.html")

@app.route('/login_orga', methods=['POST'])
def log_in_orga():
    data = {
        'email': request.form['email'],
    }
    user_in_db = orga_model.Orga.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credential", "err_log")
        return redirect('/sign_in')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Credential", "err_log")
            return redirect('/sign_in')
    if user_in_db:
        session['email'] = user_in_db.email
        session['org_id'] = user_in_db.id
        return redirect('/dashboard_orga')

@app.route('/dashboard_orga')
def dashboard_orga():
    if not "email" in session:
        return redirect('/')
    data = {
        'email': session['email'],
        'id': session['org_id']
    }
    orga = orga_model.Orga.get_by_email(data)
    orga_projects = project_model.Project.get_all_for_orga(data)
    return render_template("organisation.html", orga=orga, orga_projects=orga_projects)

@app.route("/orga/<int:id>/edit")
def edit_orga(id):
    if not "org_id" in session:
        return redirect('/')
    data = {
        "id": id
    }
    orga = orga_model.Orga.read_one(data)
    return render_template("sign_up_orga_edit.html", orga=orga)

#save updates
@app.route("/orga/<int:id>/update", methods=["POST"])
def update_orga(id):
    if not "org_id" in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'email': request.form['email'],
        'date': request.form['date'],
        'logo': request.form['logo'],
        'id': session['org_id']
    }
    orga_model.Orga.udpdate(data)
    return redirect("/dashboard_orga")

#one orga 
@app.route('/organisations/<int:id>')
def organisation_detail(id):
    data= {
        'id': id
    }
    organisations_list = orga_model.Orga.get_all_2()
    projects_orga = project_model.Project.get_all_for_orga(data)
    projects = project_model.Project.get_all_projects()
    orga = orga_model.Orga.read_one(data)
    return render_template('organisation_page.html', organisations_list=organisations_list, projects_orga=projects_orga, projects=projects, orga=orga)