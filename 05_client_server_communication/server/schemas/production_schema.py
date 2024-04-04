from . import ma, fields, validate, Production


class ProductionSchema(ma.SQLAlchemyAutoSchema):
    #! The notes are the same as above in CrewMemberSchema ^^^
    class Meta:
        model = Production
        load_instance = True

    crew_members = fields.Nested(
        "CrewMemberSchema",
        only=("id", "name", "role"),
        exclude=("production",),
        many=True,
    )
    title = fields.String(required=True, validate=validate.Length(min=2, max=50))
    director = fields.String(required=True, validate=validate.Length(min=2, max=50))
    description = fields.String(
        required=True, validate=validate.Length(min=30, max=500)
    )
    genre = fields.String(required=True, validate=validate.Length(min=2, max=50))
    image = fields.String(
        required=True,
        validate=validate.Regexp(
            r".*\.(jpeg|png|jpg)", error="File URI must be in JPEG, JPG, or PNG format"
        ),
    )
    budget = fields.Float(
        required=True, validate=validate.Range(min=0, max=500000000)
    )

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("productionbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("productions"),
            "crewmembers": ma.URLFor("crewmembers"),
        }
    )


#! Create schema for a single crew_member
production_schema = ProductionSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
productions_schema = ProductionSchema(many=True, exclude=("crew_members",))
