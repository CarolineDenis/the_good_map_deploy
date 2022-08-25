from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import project_model, orga_model
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.profile = data['profile']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.projects_liked = []

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, profile, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(profile)s, %(password)s,NOW(),NOW());"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def read_one(cls, data): 
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        if results:
            user_instance = cls(results[0])
            return user_instance
        return results

    @classmethod
    def udpdate(cls, data):
        query = "UPDATE users SET  first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, profile=%(profile)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def like(cls, data):
        query= "INSERT INTO likes (user_id, project_id) VALUES (%(id)s, %(project_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_like(cls, data):
        query= "SELECT users.id, users.email, users.first_name, users.last_name, users.email, users.profile, users.password, users.created_at, users.updated_at, projects.id, projects.name, projects.description, projects.country, projects.city, projects.volunteer, projects.area, projects.image, projects.date, projects.link, projects.latitude, projects.longitude, projects.organisation_id, projects.created_at, projects.updated_at, organisations.id, organisations.name, organisations.description, organisations.email, organisations.date, organisations.logo, organisations.password, organisations.created_at, organisations.updated_at FROM users LEFT JOIN likes ON users.id= likes.user_id LEFT JOIN projects ON projects.id=likes.project_id LEFT JOIN organisations ON organisations.id=projects.organisation_id WHERE users.id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        this_user = cls(results[0])
        for b in results:
            project_data = {
                'id': b['projects.id'],
                'name': b['name'],
                'description': b['description'],
                'country': b['country'],
                'city': b['city'],
                'volunteer': b['volunteer'],
                'area': b['area'],
                'image': b['image'],
                'link': b['link'],
                'latitude': b['latitude'],
                'longitude': b['longitude'],
                'date': b['date'],
                'organisation_id': b['organisation_id'],
                'created_at': b['projects.created_at'],
                'updated_at': b['projects.updated_at'],
            }
            organisation_data = {
                'id': b['organisations.id'],
                'name': b['organisations.name'],
                'description': b['organisations.description'],
                'email': b['organisations.email'],
                'date': b['organisations.date'],
                'logo': b['logo'],
                'password': b['organisations.password'],
                'created_at':['organisations.created_at'],
                'updated_at': b['organisations.updated_at']
            }
            this_project = project_model.Project(project_data)
            this_orga = orga_model.Orga(organisation_data)
            this_project.organisation = this_orga
            this_user.projects_liked.append(this_project)
        return this_user
    @classmethod
    def unlike(cls, data):
        query= "DELETE FROM likes WHERE user_id = %(id)s AND project_id = %(project_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @staticmethod
    def validate_form(form):
        is_valid = True
        # email already exist
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,form)
        if len(results) >= 1:
            flash("Email already registered.", "err_email")
            is_valid = False
        # email doesn't match
        elif not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!", "err_email")
            is_valid = False
        # first_name too short and not only letters
        if len(form['first_name']) < 2:
            flash("First Name must be at least 2 characters.", "err_first_name")
            is_valid = False
        elif  not LETTER_REGEX.match(form['first_name']):
            flash("First Name must contain only character", "err_first_name")
            is_valid = False
        # last_name too short 
        if len(form['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", "err_last_name")
            is_valid = False
        # password too short 
        if len(form['password']) < 8:
            flash("Password must be at least 8 characters", "err_password")
            is_valid = False
        # password doesn't match confirmation
        elif form['password'] != form['confirm_password']:
            flash("Confirmation doesn't match password", "err_confirm_password")
            is_valid = False
        # password doesn't match REGEX
        elif not PASSWORD_REGEX.match(form['password']): 
            flash("Invalid password! Must be 8 characters with minimum one uppercase", "err_password")
            is_valid = False
        # return statment 
        return is_valid
