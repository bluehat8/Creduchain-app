from .models import Student

## Student functions

def create_student(student_name, student_last_name, student_id, city, program, horary_zone, graduation_date):
    student = Student.objects.create(
        student_name=student_name,
        student_last_name=student_last_name,
        student_id=student_id,
        city=city,
        program=program,
        horary_zone=horary_zone,
        graduation_date=graduation_date
    )
    return student


def del_student(student_id):
    student = Student.objects.get(student_id=student_id)
    student.delete()
    return student


def get_student(student_id):
    student = Student.objects.get(student_id=student_id)
    return student


def get_students():
    students = Student.objects.all()
    return students


def update_student(student_id, student_name, student_last_name, city, program, horary_zone, graduation_date):
    student = Student.objects.get(student_id=student_id)
    student.student_name = student_name
    student.student_last_name = student_last_name
    student.city = city
    student.program = program
    student.horary_zone = horary_zone
    student.graduation_date = graduation_date
    student.save()
    return student
