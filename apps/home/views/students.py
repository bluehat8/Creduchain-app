from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.home.utils import get_students, create_student
from ..forms import StudentForm
import json


@login_required
def students_management(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if(form.is_valid()):
            student = form.save()
            return render(request, 'home/createstudent.html', {
                'form': StudentForm(),
                'students': get_students()
            })
    else:
        form = StudentForm()
    students = get_students()
    return render(request, 'home/createstudent.html', {
        'students': students,
        'form': form
        })
