from .. import Resource


class Logout(Resource):
    def delete(self):
        try:
            import ipdb; ipdb.set_trace()
            # if "user_id" in session:
            #     import ipdb; ipdb.set_trace()
            #     # del session['user_id'] #! delete the entire key-value pair
            return {}, 204
        except Exception as e:
            raise e

