from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import *
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .enums import *

SECRET_KEY = "Q!E2R3S4"

@method_decorator(csrf_exempt, name='dispatch')
class serviceInfo(APIView):
    def get(self, request):
        return Response({"success": True, "message": "Welcome to our API service."}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class auth(APIView):
    def post(self, request):
        request_type = request.GET.get('type')
        if request_type == 'signup_teacher':
            return self.sign_up_teacher(request)
        elif request_type == 'signup_student':
            return self.sign_up_student(request)
        elif request_type == 'teacher_login':
            return self.teacher_login(request)
        elif request_type == 'student_login':
            return self.student_login(request)
        else:
            return Response({"success": False, "message": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

    def sign_up_teacher(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        teaching_class = request.data.get('teaching_class')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')

        if not all([name, email, teaching_class, password, phone_number]):
            return Response({"success": False, "message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = generate_password_hash(password)

        role = roles_collection.find_one({"name": Role.TEACHER.value})
        if not role:
            return Response({"success": False, "message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        user_class = class_collection.find_one({"name": ClassEnum[teaching_class].value})
        if not user_class:
            return Response({"success": False, "message": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        user_collection.insert_one({
            "role_id": role["_id"],
            "role": Role.TEACHER.value,
            "name": name,
            "email": email,
            "class_id": user_class["_id"],
            "class": ClassEnum[teaching_class].value,
            "phone_number": phone_number,
            "password": hashed_password
        })

        return Response({"success": True, "message": "Teacher signed up successfully"}, status=status.HTTP_201_CREATED)

    def sign_up_student(self, request):
        name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        student_class = request.data.get('student_class')
        parents_email = request.data.get('parents_email')
        parents_phone_number = request.data.get('parents_phone_number')

        if not all([name, email, password, student_class, parents_email, parents_phone_number]):
            return Response({"success": False, "message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = generate_password_hash(password)

        role = roles_collection.find_one({"name": Role.STUDENT.value})
        if not role:
            return Response({"success": False, "message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        user_class = class_collection.find_one({"name": ClassEnum[student_class].value})
        if not user_class:
            return Response({"success": False, "message": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        user_collection.insert_one({
            "role_id": role["_id"],
            "role": Role.STUDENT.value,
            "name": name,
            "email": email,
            "class_id": user_class["_id"],
            "class": ClassEnum[student_class].value,
            "parents_email": parents_email,
            "parents_phone_number": parents_phone_number,
            "password": hashed_password
        })

        return Response({"success": True, "message": "Student signed up successfully"}, status=status.HTTP_201_CREATED)

    def teacher_login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = user_collection.find_one({"email": email, "role": Role.TEACHER.value})
        if not user or not check_password_hash(user['password'], password):
            return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "user_id": str(user['_id']),
            "role": user['role'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return Response({"success": True, "message": "Login successful", "token": token}, status=status.HTTP_200_OK)

    def student_login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = user_collection.find_one({"email": email, "role": Role.STUDENT.value})
        if not user or not check_password_hash(user['password'], password):
            return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "user_id": str(user['_id']),
            "role": user['role'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return Response({"success": True, "message": "Login successful", "token": token}, status=status.HTTP_200_OK)
