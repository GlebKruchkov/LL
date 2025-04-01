from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from api.auth import auth_blueprint
from api.profile import profile_blueprint
from api.post import post_blueprint

app = Flask(__name__)

API_URL = '/static/openapi.yml'

SWAGGER_URL = '/api/docs'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User Authentication API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(auth_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(post_blueprint)

USER_SERVICE_URL = "http://user_service:5000"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
