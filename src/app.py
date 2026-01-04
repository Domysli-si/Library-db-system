from flask import Flask
from src.ui.routes import init_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # needed for flash messages

# Initialize all routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

