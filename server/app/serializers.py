from rest_framework import serializers, status
from .models import Teacher, Student

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user', 'phone_number', 'teaching_class']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'parents_email', 'student_class', 'parents_phone_number']