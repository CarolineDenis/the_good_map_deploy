from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import project_model 
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")

class Orga:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.email = data['email']
        self.date = data['date']
        self.logo= data['logo']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.projects = []

    @classmethod
    def create_orga(cls,data):
        query = "INSERT INTO organisations (name, description, email, date, logo, password, created_at, updated_at) VALUES (%(name)s,%(description)s,%(email)s, %(date)s, %(logo)s, %(password)s,NOW(),NOW())"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM organisations WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM organisations WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def read_one(cls, data): 
        query = "SELECT * FROM organisations WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        if results:
            orga_instance = cls(results[0])
            return orga_instance
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM organisations LEFT JOIN projects ON organisations.id = projects.organisation_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) < 1:
            return False
        list_organisations = []
        for b in results:
            this_orga = cls(b)
            project_data = {
                **b, 
                'id': b['projects.id'],
                'name': b['projects.name'],
                'description': b['projects.description'],
                'date': b['projects.date'],
                'created_at': b['projects.created_at'],
                'updated_at': b['projects.updated_at']
            }
            this_project = project_model.Project(project_data)
            this_orga.projects.append(this_project)
            list_organisations.append(this_orga)
        return list_organisations

    @classmethod
    def get_all_2(cls):
        query = "SELECT * FROM organisations;"
        return connectToMySQL(DATABASE).query_db(query)

    @classmethod
    def udpdate(cls, data):
        query = "UPDATE organisations SET  name=%(name)s, description=%(description)s, email=%(email)s, date=%(date)s, logo=%(logo)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validate_form(form):
        is_valid = True
        # email already exist
        query = "SELECT * FROM organisations WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,form)
        if len(results) >= 1:
            flash("Email already registered.", "err_email")
            is_valid = False
        # email doesn't match
        elif not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!", "err_email")
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
