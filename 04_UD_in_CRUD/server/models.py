from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()


class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    description = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    crew_members = db.relationship(
        "CrewMember", back_populates="production", cascade="all, delete-orphan"
    )

    # serialize_only = ("id", "title", "genre", "director", "description", "budget", "image", "ongoing")
    serialize_rules = ("-crew_members.production",)

    def __repr__(self):
        return f"""
            <Production #{self.id}:
                Title: {self.title}
                Genre: {self.genre}
                Director: {self.director}
                Description: {self.description}
                Budget: {self.budget}
                Image: {self.image}
                Ongoing: {self.ongoing}
            />
        """

    @validates("title", "director")
    def validate_title_and_director(self, attr_name, attr_value):
        if not isinstance(attr_value, str):
            raise TypeError(f"{attr_name} must be of type str")
        elif len(attr_value) < 2:
            raise ValueError(f"{attr_name} must be at least 2 characters long")
        else:
            return attr_value

    @validates("genre")
    def validate_genre(self, _, genre): #! _ is a placeholder
        if not isinstance(genre, str):
            raise TypeError(f"Genre must be of type str")
        elif genre not in ["Drama", "Musical", "Opera"]:
            raise ValueError("Genre must be one of Musical, Opera or Drama")
        else:
            return genre

    @validates("description")
    def validate_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Descriptions must be strings")
        elif len(description) < 10:
            raise ValueError(
                f"{description} has to be a string of at least 10 characters"
            )
        return description

    @validates("budget")
    def validate_budget(self, _, budget):
        if not isinstance(budget, float):
            raise TypeError("Budgets must be floats")
        elif budget < 0 or budget > 10000000:
            raise ValueError(f"{budget} has to be a positive float under 10Millions")
        return budget

    @validates("image")
    def validate_image(self, _, image):
        if not isinstance(image, str):
            raise TypeError("Images must be strings")
        elif not re.match(r"^https?:\/\/.*\.(?:png|jpeg|jpg)$", image):
            raise ValueError(
                f"{image} has to be a string of a valid url ending in png, jpeg or jpg"
            )
        return image

    @validates("ongoing")
    def validate_ongoing(self, _, ongoing):
        if not isinstance(ongoing, bool):
            raise ValueError(f"{ongoing} has to be a boolean")
        return ongoing


class CrewMember(db.Model, SerializerMixin):
    __tablename__ = "crew_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String)
    production_id = db.Column(
        db.Integer, db.ForeignKey("productions.id", ondelete="CASCADE")
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production = db.relationship("Production", back_populates="crew_members")

    serialize_rules = ("-production.crew_members",)
    def __repr__(self):
        return f"""
            <CrewMember #{self.id}:
                Name: {self.name}
                Role: {self.role}
                Production Id: {self.production_id}
            />
        """

    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Names must be strings")
        elif len(name.split(" ")) < 2:
            raise ValueError(f"{name} has to be at least 2 words")
        return name

    @validates("role")
    def validate_role(self, _, role):
        if not isinstance(role, str):
            raise TypeError("Roles must be strings")
        elif len(role) < 3:
            raise ValueError(f"{role} has to be at least 3 characters long")
        return role

    @validates("production_id")
    def validate_production_id(self, _, production_id):
        if not isinstance(production_id, int):
            raise TypeError("Production ids must be integers")
        elif production_id < 1:
            raise ValueError(f"{production_id} has to be a positive integer")
        elif not db.session.get(Production, production_id):
            raise ValueError(
                f"{production_id} has to correspond to an existing production"
            )
        return production_id
