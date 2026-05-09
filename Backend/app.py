from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db
from config import ALLOWED_ORIGINS

# ─── Import Controllers ────────────────────────────────────
from controllers.auth_controller       import auth_bp
from controllers.line_controller       import line_bp
from controllers.assignment_controller import assignment_bp
from controllers.user_task_controller import user_task_bp


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=ALLOWED_ORIGINS)

app.register_blueprint(auth_bp)
app.register_blueprint(line_bp)
app.register_blueprint(assignment_bp)
app.register_blueprint(user_task_bp)



@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)