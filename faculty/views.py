from django.core.serializers import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict



# Create your views here.
from django.urls import reverse

from my_admin.models import *


@login_required(login_url='home')
def result_detail(request):
    courses = ['History', 'Data Structure', 'Computer Networks', 'Numerical Methods']
    context = {
        'courses': courses,
    }
    return render(request, 'faculty/result_detail.html', context)


@login_required(login_url='home')
def result_add(request):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    i = 0
    for course_id in courses_id:
        course = Course.objects.filter(id=course_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    context = {
        'courses': courses
        # 'clos': clos
    }

    return render(request, 'faculty/result_add.html', context)


@login_required(login_url='home')
def result_load(request, course_id):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    i = 0
    for c_id in courses_id:
        course = Course.objects.filter(id=c_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    sections = Section.objects.filter(instructor_id=user.id, course_id=course_id)

    clos = Clo.objects.filter(course_id=course_id)

    context = {
        'courses': courses,
        'sections': sections,
        'clos': clos
    }

    return render(request, 'faculty/result_add.html', context)


@login_required(login_url='home')
def clo_detail(request):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    print(courses_id)
    i = 0
    for course_id in courses_id:
        course = Course.objects.filter(id=course_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    return HttpResponseRedirect(reverse('clo_detail', args=(courses[0]['id'],)))


def clo_detail(request, course_id=0):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    i = 0
    for c_id in courses_id:
        course = Course.objects.filter(id=c_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    clos = Clo.objects.filter(course_id=course_id)
    context = {
        'courses': courses,
        'clos': clos
    }
    return render(request, 'faculty/clo_detail.html', context)


@login_required(login_url='home')
def clo_add(request):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    print(courses_id)
    i = 0
    for course_id in courses_id:
        course = Course.objects.filter(id=course_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    return HttpResponseRedirect(reverse('faculty/clo_add.html', args=(courses[0]['id'],)))


@login_required(login_url='home')
def clo_add(request, course_id=0):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    i = 0
    for c_id in courses_id:
        course = Course.objects.filter(id=c_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    clos = Clo.objects.filter(course_id=course_id)
    context = {
        'courses': courses,
        'clos': clos
    }
    return render(request, 'faculty/clo_add.html', context)


def clo_load(request, course_id=0):
    user = request.user
    current_semester = 'Fall2018'

    courses_id = Course.objects.filter(section__instructor_id=user.id).values('id').distinct()
    courses = []
    i = 0
    for c_id in courses_id:
        course = Course.objects.filter(id=c_id['id']).values('id', 'name')
        courses.append(course[0])
        i = i + 1

    context = {
        'courses': courses,
        # 'clos': clos
    }
    return render(request, 'faculty/clo_add.html', context)


@login_required(login_url='home')
def slo_detail(request):
    user = request.user
    current_semester = 'Fall2018'

    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1

    return HttpResponseRedirect(reverse('slo_detail', args=(program_name[0]['id'],)))


def slo_detail(request, program_id=0):
    user = request.user
    # current_semester = 'Fall2018'
    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1

    plos = Plo.objects.filter(program_id=program_id)

    slos = []

    for plo in plos:
        slos.append(Slo.objects.filter(plo_id=plo.id))

    context = {
        'program_names': program_name,
        'slos': slos,
        'plos': plos,
    }
    return render(request, 'faculty/slo_detail.html', context)


@login_required(login_url='home')
def plo_add(request):
    user = request.user
    current_semester = 'Fall2018'

    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1
    return HttpResponseRedirect(reverse('plo_add', args=(program_name[0]['id'],)))


def plo_add(request, program_id=0):
    if request.method == 'POST':
        plo = Plo()
        program = Program.objects.get(pk=request.POST['program_id'])
        plo.program = program
        plo.plo_code = request.POST['plo_code']
        plo.description = request.POST['plo_description']
        plo.batch = request.POST['plo_batch']
        plo.save()

    user = request.user
    # current_semester = 'Fall2018'
    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1
    context = {
        'program_names': program_name,
    }
    return render(request, 'faculty/plo_add.html', context)


@login_required(login_url='home')
def plo_detail(request):
    user = request.user
    current_semester = 'Fall2018'

    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1
    return HttpResponseRedirect(reverse('plo_detail', args=(program_name[0]['id'],)))


def plo_detail(request, program_id=0):
    user = request.user
    # current_semester = 'Fall2018'
    # plo_id = request.path.split('/')[3]
    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1


    plos = Plo.objects.filter(program_id=program_id)
    context = {
        'program_names': program_name,
        'plos': plos,
    }
    return render(request, 'faculty/plo_detail.html', context)


@login_required(login_url='home')
def outline_detail(request):
    context = {}
    return render(request, 'faculty/outline_detail.html', context)


@login_required(login_url='home')
def slo_add(request):
    user = request.user
    current_semester = 'Fall2018'

    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1

    return HttpResponseRedirect(reverse('slo_add', args=(program_name[0]['id'],)))


def slo_load(request, program_id):
    user = request.user
    # current_semester = 'Fall2018'
    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1

    plos = Plo.objects.filter(program_id=program_id)

    #print(plos)

    context = {
        'program_names': program_name,
        'plos': plos,
    }
    return render(request, 'faculty/slo_add.html', context)


@login_required(login_url='home')
def slo_add(request, program_id=0):

    if request.method == 'POST':
        slo = Slo()
        slo.slo_code = request.POST['slo_code']
        slo.description = request.POST['slo_description']
        slo.plo = Plo.objects.get(pk=request.POST['plo_list'])

        slo.save()


    user = request.user
    # current_semester = 'Fall2018'
    programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
    program_name = []
    i = 0
    for p in programs_id:
        programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
        program_name.append(programs[0])
        i = i + 1

    plos = Plo.objects.filter(program_id=program_id)

    context = {
        'program_names': program_name,
        'plos': plos,
    }
    return render(request, 'faculty/slo_add.html', context)

#
# def slo_add(request, program_id=0):
#     if request.method == 'POST':
#         plo = Plo()
#         program = Program.objects.get(pk=request.POST['program_id'])
#         plo.program = program
#         plo.plo_code = request.POST['plo_code']
#         plo.description = request.POST['plo_description']
#         plo.batch = request.POST['plo_batch']
#         plo.save()
#
#
#
#         user = request.user
#     current_semester = 'Fall2018'
#
#     programs_id = Student.objects.filter(section__instructor_id=user.id).values('program_id').distinct()
#     program_name = []
#     i = 0
#     for p in programs_id:
#         programs = Program.objects.filter(id=programs_id[i]['program_id']).values('id', 'name')
#         program_name.append(programs[0])
#         i = i + 1
#
#     context = {
#         "program_names": program_name
#     }
#
#     return render(request, 'faculty/slo_add.html', context)


@login_required(login_url='home')
def outline_add(request):
    return render(request, 'faculty/outline_add.html', {})


def all_students(request):
    user = request.user
    section = request.POST['section']
    course = request.POST['course_id']
    print(section)
    print(course)
    students = Student.objects.filter(section__section_name=section, section__instructor_id=user.id, section__course_id=course)
    print(students)

    context = {
        'students': students
    }

    return render(request, 'faculty/result_add.html', context)
    # return HttpResponse(json.simplejson.dumps(context), mimetype="application/json")
    # return JsonResponse(context)

    # return HttpResponse(json.dumps(context), content_type="application/json")
