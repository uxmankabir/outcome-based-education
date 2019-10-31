from rest_framework.serializers import ModelSerializer
from my_admin.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    user = UserSerializer()
    program = ProgramSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class SloSerializer(ModelSerializer):
    class Meta:
        model = Slo
        fields = '__all__'


class PloSerializer(ModelSerializer):
    class Meta:
        model = Plo
        fields = '__all__'
