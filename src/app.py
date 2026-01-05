from flask import Flask
from src.ui.routes import init_routes
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "templates")
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'supersecretkey'

# Inicializace rout
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

