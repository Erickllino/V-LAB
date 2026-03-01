from flask import Flask, request, jsonify
import profiles as pf
from services.student_service import create_user, get_user

app = Flask(__name__)

@app.route("/students", methods=["POST"])
def create_student():
    data = request.json
    
    user = create_user(data)
    
    return jsonify(user), 201


@app.route("/students/<user_id>", methods=["GET"])
def get_student(user_id):
    user = get_user(user_id)
    
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)