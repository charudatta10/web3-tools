class UniversityDAO:
    def __init__(self):
        self.course_count = 0
        self.courses = {}
        self.certificates = {}

    def create_course(self, name, instructor):
        self.course_count += 1
        self.courses[self.course_count] = {"name": name, "instructor": instructor, "students": []}
        return f"Course {name} created with ID {self.course_count}."

    def enroll_student(self, course_id, student):
        if course_id in self.courses:
            self.courses[course_id]["students"].append(student)
            return f"Student {student} enrolled in course ID {course_id}."
        else:
            return "Invalid course ID."

    def issue_certificate(self, course_id, student):
        if course_id in self.courses and student in self.courses[course_id]["students"]:
            if course_id not in self.certificates:
                self.certificates[course_id] = {}
            self.certificates[course_id][student] = True
            return f"Certificate issued to student {student} for course ID {course_id}."
        else:
            return "Student not enrolled in course."

    def verify_certificate(self, course_id, student):
        if course_id in self.certificates and self.certificates[course_id].get(student, False):
            return f"Certificate for student {student} in course ID {course_id} is valid."
        else:
            return f"Certificate for student {student} in course ID {course_id} is not valid."
