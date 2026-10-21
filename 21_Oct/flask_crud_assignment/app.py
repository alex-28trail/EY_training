from flask import Flask, request
from flask import jsonify

app = Flask(__name__)
students = [
    {"id": 1, "name": "Rhea Kapoor", "course": "Python", "score": 82},
    {"id": 2, "name": "Zain Malik", "course": "SQL", "score": 76},
    {"id": 3, "name": "Devika Rao", "course": "Cloud", "score": 91},

]
@app.route("/students")
def get_student():
    return jsonify(students)


@app.route("/students/<int:student_id>")
def get_students(student_id):
    students = [
        {"id": 1,"name": "Rhea Kapoor","course": "Python","score": 82},
        {"id": 2,"name": "Zain Malik","course": "SQL","score": 76},
        {"id": 3,"name": "Devika Rao","course": "Cloud","score": 91},

    ]

    for student in students:
        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({"message": "student not found"}), 404

@app.route("/students",methods=["POST"])
def post_student():
    data = request.get_json()
    if not data:
        return jsonify({"message": "no data"}), 400


    if any(student["id"] == data['id'] for student in students):
        return jsonify({"message": "Student ID already exists"}), 409

    students.append(data)
    return jsonify({"message": "student added successfully"}), 201


@app.route("/students/<int:student_id>",methods=["PUT"])
def put_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "no data"}), 400
    if any(student["id"] == data['id'] for student in students):
        return jsonify({"message": "Student ID already exists"}), 409
    students.append(data)
    return jsonify({"message": "student added successfully"}), 201


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            return jsonify({
                "message": "Student deleted successfully"
            }), 200

    return jsonify({
        "message": "Student not found"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)