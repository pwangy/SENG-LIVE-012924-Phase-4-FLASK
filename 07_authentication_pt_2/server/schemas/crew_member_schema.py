from . import ma, CrewMember, fields, validate, validates, ValidationError

class CrewMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # name of model
        model = CrewMember
        # avoid recreating objects on updates, only applies to deserialization (load())
        # in order for this to work, flask-marshmallow (is specific to this wrapper)
        # needs to know how an instance even looks like, note how we invoked load() on line 222
        load_instance = True
        #  if you set to True, Marshmallow will preserve the order of fields as defined in the schema.
        ordered = True

    #! Setup some app-level (aka no DB involved) validations
    # * See more here https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#module-marshmallow.validate
    name = fields.String(required=True)
    role = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=1000,
            error="Role should be at least 3 chars long and 1000 chars max",
        ),
    )
    production_id = fields.Integer(required=True)
    production = fields.Nested("ProductionSchema", exclude=("crew_members",))
    #! Create hyperlinks for easy navigation of your api
    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("crewmemberbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("crewmembers"),
        }
    )

    #! Example of custom validation with marshmallow
    #! (DANGER -> VERY similar to the syntax in the models)
    @validates("name")
    def validate_word_count(self, name):
        words = name.split()
        if len(words) < 2:
            raise ValidationError("Name must contain at least two words")


#! Create schema for a single crew_member
crew_member_schema = CrewMemberSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
crew_members_schema = CrewMemberSchema(many=True)
