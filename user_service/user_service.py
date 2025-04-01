from flask import Flask
from api.register import register_blueprint
from api.login import login_blueprint
from api.update_profile import update_profile_blueprint
from api.get_profile import get_profile_blueprint
from api.verify_user import verify_blueprint
from api.logout import logout_blueprint

app = Flask(__name__)

app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(update_profile_blueprint)
app.register_blueprint(get_profile_blueprint)
app.register_blueprint(verify_blueprint)
app.register_blueprint(logout_blueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
