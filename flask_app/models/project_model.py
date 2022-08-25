from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import orga_model
from flask_app import DATABASE
from flask import flash


class Project:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.date = data['date']
        self.country = data['country']
        self.city = data['city']
        self.volunteer = data['volunteer']
        self.area = data['area']
        self.image = data['image']
        self.link = data['link']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.organisation_id = data['organisation_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_project(cls, data):
        query = "INSERT INTO projects (name, description, date, country, city, volunteer, area, image, link, latitude, longitude, organisation_id, created_at, updated_at) VALUES (%(name)s,%(description)s,%(date)s, %(country)s, %(city)s, %(volunteer)s, %(area)s, %(image)s, %(link)s, %(latitude)s, %(longitude)s, %(organisation_id)s, NOW(),NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_for_orga(cls, data):
        query= "SELECT * FROM projects WHERE organisation_id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_projects(cls):
        query= "SELECT * FROM projects JOIN organisations ON organisations.id = projects.organisation_id;"
        results= connectToMySQL(DATABASE).query_db(query)
        list_projects =[]
        for b in results:
            this_project = cls(b)
            organisation_data = {
                **b,
                'id': b['organisations.id'],
                'created_at': b['organisations.created_at'],
                'updated_at': b['organisations.updated_at']
            }
            this_orga = orga_model.Orga(organisation_data)
            this_project.organisation = this_orga
            list_projects.append(this_project)
        return list_projects

    @classmethod
    def get_hightlight_projects(cls):
        query= "SELECT * FROM projects JOIN organisations ON organisations.id = projects.organisation_id WHERE projects.id=5 or projects.id=2 or projects.id=4;"
        results= connectToMySQL(DATABASE).query_db(query)
        list_projects =[]
        for b in results:
            this_project = cls(b)
            organisation_data = {
                **b,
                'id': b['organisations.id'],
                'created_at': b['organisations.created_at'],
                'updated_at': b['organisations.updated_at']
            }
            this_orga = orga_model.Orga(organisation_data)
            this_project.organisation = this_orga
            list_projects.append(this_project)
        return list_projects

    @classmethod
    def get_all_liked(cls, data):
        query= "SELECT * FROM likes WHERE user_id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_form(form):
        is_valid = True
        # first_name too short and not only letters
        if len(form['name']) < 2:
            flash("The name of the project must be at least 2 characters.", "err_name")
            is_valid = False
        if len(form['description']) < 10:
            flash("The description must be at least 10 characters.", "err_description")
            is_valid = False
        if len(form['country']) < 2:
            flash("The country must be at specified.", "err_country")
            is_valid = False
        # return statment
        return is_valid
