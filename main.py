from flask import Flask
from flask_bootstrap import Bootstrap

import views

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Yet another secret key'

app.register_blueprint(views.hello)
Bootstrap(app)

if __name__ == "__main__":
    app.run(debug=True)
