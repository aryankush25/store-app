from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help="name field can not be left blank")

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json(), 200
        else:
            return {"message": "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f'An store with name {name} already exists.'}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while inserting store "}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {"message": f'An store with name {name} does not exists.'}, 400

        store.delete_from_db()

        return {'message': 'Store deleted.'}, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.get_all_from_db()]}, 200
