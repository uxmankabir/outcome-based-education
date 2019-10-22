from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Plo(models.Model):
    plo_code = models.CharField(max_length=10)
    description = models.TextField(max_length=1500)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    batch = models.CharField(max_length=4, default=2015)

    def __str__(self):
        return '%s - %s - %s' % (self.plo_code, self.program.name, self.description)


class Slo(models.Model):
    slo_code = models.CharField(max_length=10)
    description = models.TextField(max_length=1500)
    plo = models.ForeignKey(Plo, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.slo_code, self.description)


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    course_code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return '%s - %s' % (self.course_code, self.name)


class Clo(models.Model):
    clo_code = models.CharField(max_length=10)
    description = models.TextField(max_length=1500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slo = models.ForeignKey(Slo, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.clo_code, self.description)


class Role(models.Model):
    title = models.CharField(max_length=30, unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title


class Student(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    batch = models.CharField(max_length=4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'user: %s, program: %s, batch: %s' % (self.user.username, self.program.name, self.batch)


class Semester(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    section_name = models.CharField(max_length=1)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return 'section: %s, semester: %s, instructor: %s, coursed: %s' % (self.section_name, self.semester.title, self.instructor.username, self.course.name)


class AssessmentTool(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    clo = models.ForeignKey(Clo, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_tool = models.ForeignKey(AssessmentTool, on_delete=models.CASCADE)
    assessment_count = models.IntegerField()
    question_no = models.IntegerField()
    obtained_marks = models.DecimalField(max_digits=3, decimal_places=2)
    total_marks = models.DecimalField(max_digits=3, decimal_places=2)
