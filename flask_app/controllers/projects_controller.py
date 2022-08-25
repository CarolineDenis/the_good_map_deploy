from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user_model, orga_model, project_model

@app.route('/new_project')
def new_project():
    orga = orga_model.Orga.get_by_id({'id':session['org_id']})
    return render_template ('new_project.html', orga=orga)

@app.route('/create_project', methods=['POST'])
def create_project():
    if not project_model.Project.validate_form(request.form):
        return redirect('/new_project')
    data = {
        **request.form,
        'organisation_id': session['org_id'],
    }
    if 'volunteer' not in request.form:
        data['volunteer'] = 0
    project_model.Project.create_project(data)
    return redirect('/dashboard_orga')

@app.route('/projects')
def projects():
    projects = project_model.Project.get_all_projects()
    if 'id' in session:
        data = {
            'id' : session['id']
        }
        liked = project_model.Project.get_all_liked(data)
    else:
        liked = []
    return render_template('projects.html', projects=projects, liked=liked)

@app.route('/volunteer/<int:id>')
def volunteer(id):
    data = {
        'id': id
    }
    orga = orga_model.Orga.read_one(data)
    return render_template('volunteer.html', orga=orga)