from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

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
