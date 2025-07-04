from flask import Blueprint, json, request

healthcheck = Blueprint('Healthcheck', __name__)

@healthcheck.route('/healthcheck', methods=["GET"])
def check_server_status():
    return {'status_code': 200, 'msg':'Server is up and running ...', }, 200

