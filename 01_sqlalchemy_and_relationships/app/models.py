from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    PrimaryKeyConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    CheckConstraint,
    func,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
Base = declarative_base(metadata=metadata)

class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(Integer, nullable=False, unique=True)
    address = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, onupdate=func.now())

    pets = relationship("Pet", back_populates="owner")
    
    def __repr__(self):
        return f"""
            <Owner #{self.id}:
                Name: {self.name} - 
                Email: {self.email} - 
                Phone: {self.phone} - 
            >
        """

class Pet(Base):
    __tablename__ = 'pets'
    __table_args__ = (
        # PrimaryKeyConstraint("id", name="pk_owners"),
        CheckConstraint("length(name) > 0", name="ck_pets_names"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    temperament = Column(String)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    created_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, onupdate=func.now())

    owner = relationship("Owner", back_populates="pets")

    def __repr__(self):
        return f"""
            <Pet #{self.id}:
                Name: {self.name} - 
                Owner ID: {self.owner_id} - 
            >
        """
