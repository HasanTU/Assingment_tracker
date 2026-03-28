from flask import Flask, jsonify
from database import SessionLocal  # import session factory

from controllers.user_controller import user_bp
from controllers.assignment_controller import assignment_bp



app = Flask(__name__)
db = SessionLocal()


app.register_blueprint(user_bp)
app.register_blueprint(assignment_bp)

# This is a route. It listens for GET requests at /api/health
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success", 
        "message": "Assignment System Backend is running!"
    }), 200

if __name__ == '__main__':
    # debug=True automatically restarts the server when you change the code
    app.run(debug=True, port=5000)