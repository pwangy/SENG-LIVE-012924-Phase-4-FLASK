from . import ma, fields, validate, User


class UserSchema(ma.SQLAlchemyAutoSchema):
    #! The notes are the same as above in CrewMemberSchema ^^^
    class Meta:
        model = User
        load_instance = True
        exclude=("_password_hash",)

    username = fields.String(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True)
    password_hash = fields.String(required=True, load_only=True, validate=validate.Length(min=8, max=50))

    def load(self, data, instance=None, *, partial=False, **kwargs):
        # Load the instance using Marshmallow's default behavior
        loaded_instance = super().load(
            data, instance=instance, partial=partial, **kwargs
        )

        # Set attributes manually, triggering property setters
        for key, value in data.items():
            setattr(loaded_instance, key, value)

        return loaded_instance


#! Create schema for a single crew_member
user_schema = UserSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
users_schema = UserSchema(many=True)
