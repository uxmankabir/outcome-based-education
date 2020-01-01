from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

from faculty.fusioncharts import FusionCharts
from .serializers import StudentSerializer, SloSerializer, PloSerializer
import datetime

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

    if request.method == 'POST':
        course = Course.objects.get(pk=request.POST['course_id'])
        clo = Clo.objects.get(pk=request.POST['clos_list'])
        assessment_tool = AssessmentTool.objects.get(pk=request.POST['assessment_tool'])

        assessment_no = request.POST['assessment_no']
        question_no = request.POST['question_no']
        total_marks = request.POST['total_marks']

        students = request.POST.getlist('student')
        marks = [request.POST['marks_{}'.format(std)] for std in students]

        i = 0
        for student in students:
            assessment = Assessment()
            assessment.assessment_count = assessment_no
            assessment.question_no = question_no
            assessment.obtained_marks = marks[i]
            assessment.total_marks = total_marks
            assessment.assessment_tool = assessment_tool
            assessment.clo = clo
            assessment.course = course
            assessment.student = User.objects.get(username=student)
            i = i + 1
            assessment.save()

    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    assessment_tools = AssessmentTool.objects.all()
    context = {
        'courses': courses,
        'assessment_tools': assessment_tools
    }

    return render(request, 'faculty/result_add.html', context)


@login_required(login_url='home')
def result_load(request, course_id):
    user = request.user
    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    sections = Section.objects.filter(instructor_id=user.id, course_id=course_id)
    clos = Clo.objects.filter(course_id=course_id)
    assessment_tools = AssessmentTool.objects.all()

    context = {
        'courses': courses,
        'sections': sections,
        'clos': clos,
        'assessment_tools': assessment_tools
    }

    return render(request, 'faculty/result_add.html', context)


@login_required(login_url='home')
def clo_detail(request):
    user = request.user
    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    return HttpResponseRedirect(reverse('clo_detail', args=(courses[0]['id'],)))


def clo_detail(request, course_id=0):
    user = request.user
    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    clos = Clo.objects.filter(course_id=course_id)
    context = {
        'courses': courses,
        'clos': clos
    }
    return render(request, 'faculty/clo_detail.html', context)


def clo_delete(request, clo_id):
    instance = Clo.objects.get(id=clo_id)
    instance.delete()
    return redirect(clo_detail)


@login_required(login_url='home')
def clo_add(request):
    user = request.user
    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    return HttpResponseRedirect(reverse('faculty/clo_add.html', args=(courses[0]['id'],)))


@login_required(login_url='home')
def clo_add(request, course_id=0):
    user = request.user
    if request.method == 'POST':
        course_id = Course.objects.get(pk=request.POST['course_id'])
        clo_code = request.POST['clo_code']
        clo_statement = request.POST['clo_statement']
        slo_id = Slo.objects.get(pk=request.POST['slo_list'])
        clo = Clo()
        clo.course = course_id
        clo.description = clo_statement
        clo.clo_code = clo_code
        clo.slo = slo_id

        clo.save()

    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    clos = Clo.objects.filter(course_id=course_id)
    context = {
        'courses': courses,
        'clos': clos
    }
    return render(request, 'faculty/clo_add.html', context)


def clo_load(request, course_id=0):
    user = request.user
    courses = Course.objects.filter(section__instructor_id=user.id).distinct()
    plos = Plo.objects.filter(program__student__section__course_id=course_id).distinct()

    context = {
        'courses': courses,
        'plos': plos
    }
    return render(request, 'faculty/clo_add.html', context)


@login_required(login_url='home')
def slo_detail(request):
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()

    return HttpResponseRedirect(reverse('slo_detail', args=(programs[0]['id'],)))


def slo_detail(request, program_id=0):
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    slos = Slo.objects.filter(plo__program_id=program_id)
    context = {
        'programs': programs,
        'slos': slos,
    }
    return render(request, 'faculty/slo_detail.html', context)


@login_required(login_url='home')
def plo_add(request):
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    now = datetime.datetime.now()
    return HttpResponseRedirect(reverse('plo_add', args=(programs[0]['id'],)))


def plo_add(request, program_id=0):
    now = datetime.datetime.now()
    if request.method == 'POST':
        plo = Plo()
        program = Program.objects.get(pk=request.POST['program_id'])
        plo.program = program
        plo.plo_code = request.POST['plo_code']
        plo.description = request.POST['plo_description']
        plo.batch = now.year
        plo.save()
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    context = {
        'programs': programs,
        'year': now.year
    }
    return render(request, 'faculty/plo_add.html', context)


@login_required(login_url='home')
def plo_detail(request):
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    return HttpResponseRedirect(reverse('plo_detail', args=(programs[0]['name'],)))


def plo_detail(request, program_id=0):
    user = request.user
    # plo_id = request.path.split('/')[3]

    role = Role.objects.filter(users=user.id).first()

    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    plos = Plo.objects.filter(program_id=program_id)
    context = {
        'programs': programs,
        'plos': plos,
        'role': role.title
    }
    return render(request, 'faculty/plo_detail.html', context)


def plo_delete(request, plo_id):
    instance = Plo.objects.get(id=plo_id)
    instance.delete()
    return redirect(plo_detail)


@login_required(login_url='home')
def outline_detail(request):
    context = {}
    return render(request, 'faculty/outline_detail.html', context)


@login_required(login_url='home')
def slo_add(request):
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()

    return HttpResponseRedirect(reverse('slo_add', args=(programs[0]['id'],)))


def slo_load(request, program_id):
    user = request.user
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    plos = Plo.objects.filter(program_id=program_id)
    context = {
        'programs': programs,
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
    programs = Program.objects.filter(student__section__instructor_id=user.id).distinct()
    plos = Plo.objects.filter(program_id=program_id)
    context = {
        'programs': programs,
        'plos': plos,
    }
    return render(request, 'faculty/slo_add.html', context)


def slo_delete(request, slo_id):
    instance = Slo.objects.get(id=slo_id)
    instance.delete()
    return redirect(slo_detail)


@login_required(login_url='home')
def outline_add(request):
    return render(request, 'faculty/outline_add.html', {})


@api_view(['POST'])
def all_students(request):
    user = request.user
    section = request.POST['section']
    course = request.POST['course_id']
    students = Student.objects.filter(section__section_name=section, section__instructor_id=user.id,
                                      section__course_id=course)
    serializer = StudentSerializer(students, many=True)
    return Response(
        data=serializer.data,
        status=200
    )


@api_view(['POST'])
def all_slos(request):
    plo = Plo.objects.get(pk=request.POST['plo_id'])
    slos = plo.slo_set.all()
    # print(slos)
    serializer = SloSerializer(slos, many=True)
    return Response(
        data=serializer.data,
        status=200
    )


@api_view(['POST'])
def validate_plo_code(request):
    plo_code = request.POST['plo_code']
    print(plo_code)
    program_id = Program.objects.get(pk=request.POST['program_id'])
    print(program_id)
    is_unique_plo = Plo.objects.filter(plo_code=plo_code, program_id=program_id)
    print(is_unique_plo)

    serializer = PloSerializer(is_unique_plo, many=True)
    return Response(
        data=serializer.data,
        status=200
    )


def show_report(request):
    # Create an object for the Multiseries column 2D charts using the FusionCharts class constructor
    mscol2D = FusionCharts("mscolumn2d", "ex1", "600", "400", "chart-1", "json",
                           # The data is passed as a string in the `dataSource` as parameter.
                           """{
                                   "chart": {
                                   "caption": "App Publishing Trend",
                                   "subCaption": "2012-2016",
                                   "xAxisName": "Years",
                                   "yAxisName" : "Total number of apps in store",
                                   "formatnumberscale": "1",
                                   "drawCrossLine":"1",
                                   "plotToolText" : "<b>$dataValue</b> apps on $seriesName in $label",
                                   "theme": "fusion"
                               },
                    
                               "categories": [{
                                   "category": [{
                                   "label": "2012"
                                   }, {
                                   "label": "2013"
                                   }, {
                                   "label": "2014"
                                   }, {
                                   "label": "2015"
                                   },{
                                   "label": "2016"
                                   }
                                   ]
                               }],
                               "dataset": [{
                                   "seriesname": "iOS App Store",
                                   "data": [{
                                   "value": "125000"
                                   }, {
                                   "value": "300000"
                                   }, {
                                   "value": "480000"
                                   }, {
                                   "value": "800000"
                                   }, {
                                   "value": "1100000"
                                   }]
                               }, {
                                   "seriesname": "Google Play Store",
                                   "data": [{
                                   "value": "70000"
                                   }, {
                                   "value": "150000"
                                   }, {
                                   "value": "350000"
                                   }, {
                                   "value": "600000"
                                   },{
                                   "value": "1400000"
                                   }]
                               }, {
                                   "seriesname": "Amazon AppStore",
                                   "data": [{
                                   "value": "10000"
                                   }, {
                                   "value": "100000"
                                   }, {
                                   "value": "300000"
                                   }, {
                                   "value": "600000"
                                   },{
                                   "value": "900000"
                                   }]
                               }]
                           }""")
    user = request.user
    courses = Course.objects.filter(section__instructor_id=user.id).distinct()

    context = {
        'courses': courses,
        'output': mscol2D.render(),
    }

    return render(request, 'faculty/show_report.html', context)
