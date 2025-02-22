from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Teacher, Student
from rest_framework.authentication import TokenAuthentication

@method_decorator(csrf_exempt, name='dispatch')
class AuthAPIView(APIView):
    permission_classes = [AllowAny]

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
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        teaching_class = request.data.get('teaching_class')

        if not all([name, email, password, phone_number, teaching_class]):
            return Response({"success": False, "message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"success": False, "message": "Teacher with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=name,
                user_type='teacher'
            )
            Teacher.objects.create(user=user, phone_number=phone_number, teaching_class=teaching_class)
            return Response({"success": True, "message": "Teacher registered successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def sign_up_student(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        student_class = request.data.get('student_class')
        parents_email = request.data.get('parents_email')
        parents_phone_number = request.data.get('parents_phone_number')

        if not all([full_name, email, password, student_class, parents_email, parents_phone_number]):
            return Response({"success": False, "message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"success": False, "message": "Student with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=full_name,
                user_type='student'
            )
            Student.objects.create(
                user=user,
                full_name=full_name,
                student_class=student_class,
                parents_email=parents_email,
                parents_phone_number=parents_phone_number
            )
            return Response({"success": True, "message": "Student registered successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def teacher_login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([email, password]):
            return Response({"success": False, "message": "Both email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(request, email=email, password=password)
            
            if user and user.user_type == 'teacher':
                token, _ = Token.objects.get_or_create(user=user)
                teacher = Teacher.objects.get(user=user)
                return Response({
                    "success": True,
                    "message": "Login successful",
                    "response": {
                        "user_type": user.user_type,
                        "email": user.email,
                        "name": user.first_name,
                        "teaching_class": teacher.teaching_class,
                        "token": token.key
                    }
                }, status=status.HTTP_200_OK)
            return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def student_login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([email, password]):
            return Response({"success": False, "message": "Both email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(request, email=email, password=password)
            
            if user and user.user_type == 'student':
                token, _ = Token.objects.get_or_create(user=user)
                student = Student.objects.get(user=user)
                return Response({
                    "success": True,
                    "message": "Login successful",
                    "response": {
                        "user_type": user.user_type,
                        "email": user.email,
                        "student_id": student.student_id,
                        "name": user.first_name,
                        "student_class": student.student_class,
                        "token": token.key
                    }
                }, status=status.HTTP_200_OK)
            return Response({"success": False, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_type = request.GET.get('type')
        if request_type == 'change_password':
            return self.change_password(request)
        else:
            return Response({"success": False, "message": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        request_type = request.GET.get('type')
        if request_type == 'get_teacher_details':
            return self.get_teacher_details(request)
        elif request_type == 'get_student_details':
            return self.get_student_details(request)
        elif request_type == 'logout':
            return self.logout(request)
        else:
            return Response({"success": False, "message": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not all([old_password, new_password]):
            return Response({"success": False, "message": "Both old and new passwords are required"}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            # Create new token after password change
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            return Response({
                "success": True, 
                "message": "Password changed successfully",
                "new_token": new_token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    def get_teacher_details(self, request):
        try:
            user = request.user
            teacher = Teacher.objects.filter(user=user).first()

            if not teacher:
                return Response({"success": False, "message": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

            data = {
                "name": teacher.user.first_name,
                "email": teacher.user.email,
                "phone_number": teacher.phone_number,
                "teaching_class": teacher.teaching_class
            }
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_student_details(self, request):
        try:
            user = request.user
            student = Student.objects.filter(user=user).first()

            if not student:
                return Response({"success": False, "message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

            data = {
                "student_id": student.student_id,
                "full_name": student.full_name,
                "email": student.user.email,
                "student_class": student.student_class,
                "parents_email": student.parents_email,
                "parents_phone_number": student.parents_phone_number
            }
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            return Response({"success": True, "message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)