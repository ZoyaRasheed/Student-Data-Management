from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import *
import jwt # type: ignore
import datetime
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from .enums import *
from middleware.authorization import *
from .helper import *
import json
from bson import ObjectId # type: ignore

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

    def get(self, request):
        type = request.GET.get('type')
        if type == 'self_identification':
            return self.self_identification(request)
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

    @login_required
    def self_identification(self, request):
        user_payload = getattr(request, 'user_payload', None)
        if user_payload:
            return Response({
                "success": True,
                "message": "User identified successfully",
                "response": user_payload
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "User information not available"
            }, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class teacher_services(APIView):
    def post(self, request):
        request_type = request.GET.get('type')
        if request_type == 'add_marks':
            return self.add_marks(request)
        elif request_type == 'update_student_marks':
            return self.update_student_marks(request)
        else:
            return Response({"success": False, "message": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        request_type = request.GET.get('type')
        if request_type == 'get_student_marks':
            return self.get_student_marks(request)
        else:
            return Response({"success": False, "message": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)
    
    @login_required
    def add_marks(self, request):
        user_payload = getattr(request, 'user_payload', None)
        
        if not user_payload or user_payload['role'].get('role_name') != Role.TEACHER.value:
            return Response({"success": False, "message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)

        student_id = request.data.get('student_id')
        subjects_marks = request.data.get('subjects_marks')  
        exam_name = request.data.get('exam_name')
        total_marks_per_subject = request.data.get('total_marks')

        if not all([student_id, subjects_marks, exam_name, total_marks_per_subject]):
            return Response({"success": False, "message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        existing_record = mark_collection.find_one({"student_id": student_id, "exam_name": exam_name})
        if existing_record:
            return Response({"success": False, "message": "Marks already exist for this student in this exam"}, status=status.HTTP_409_CONFLICT)


        student = user_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            return Response({"success": False, "message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        teacher_class_id = user_payload['class'][str('class_id')]
        teacher_subjects = set(user_payload['class']['subjects'])

        student_class_id = str(student['class_id'])

        if teacher_class_id != student_class_id:
            return Response({"success": False, "message": "Teacher and student are not in the same class"}, status=status.HTTP_403_FORBIDDEN)
        
        student_class = class_collection.find_one({"_id": ObjectId(student_class_id)})
        if not student_class:
            return Response({"success": False, "message": "Class not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        student_subjects = set(student_class['subjects'])

        input_subjects = set(subjects_marks.keys())
        if not input_subjects.issubset(teacher_subjects) or not input_subjects.issubset(student_subjects):
            return Response({"success": False, "message": "Invalid subjects provided"}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(total_marks_per_subject, dict):
         
            for subject, marks in subjects_marks.items():
                if subject not in total_marks_per_subject:
                    return Response({"success": False, "message": f"Total marks not specified for {subject}"}, status=status.HTTP_400_BAD_REQUEST)
                if marks > total_marks_per_subject[subject]:
                    return Response({"success": False, "message": f"Marks for {subject} exceed the allowed total"}, status=status.HTTP_400_BAD_REQUEST)
            total_marks = sum(total_marks_per_subject.values())
        else:
           
            total_marks = total_marks_per_subject
           
            for subject, marks in subjects_marks.items():
                if marks > total_marks:
                    return Response({"success": False, "message": f"Marks for {subject} exceed the allowed total"}, status=status.HTTP_400_BAD_REQUEST)

        obtained_marks = sum(subjects_marks.values())
        percentage = (obtained_marks / total_marks) * 100
        grade = calculate_grade(percentage)

      
        final_data = {
            "student_id": student.get("user_id", str(student["_id"])), 
            "student_name": student["name"],
            "teacher_id": user_payload["user_id"],
            "teacher_name": user_payload["name"],
            "class_id": teacher_class_id,
            "exam_name": exam_name,
            "date": datetime.datetime.utcnow(),
            "subjects_marks": subjects_marks,
            "total_obtained_marks": obtained_marks,
            "total_marks": total_marks,
            "percentage": round(percentage, 2),
            "grade": grade
        }

        mark_collection.insert_one(final_data)

        return Response(
            {
                "success": True,
                "message": "Marks added successfully"
            },
            status=status.HTTP_201_CREATED
        )
    
    @login_required
    def get_student_marks(self, request):
        user_payload = getattr(request, 'user_payload', None)
        
        if not user_payload or user_payload['role'].get('role_name') != Role.TEACHER.value:
            return Response({"success": False, "message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        teacher_class_id = user_payload['class'][str('class_id')]

        students_marks = list(mark_collection.find({"class_id": teacher_class_id}))

        for mark in students_marks:
            mark["_id"] = str(mark["_id"])  

        return Response(
            {
                "success": True,
                "message": "Student Marks",
                "response": students_marks
            },
            status=status.HTTP_201_CREATED
        )
    
    @login_required
    def update_student_marks(self, request):
        user_payload = getattr(request, 'user_payload', None)
        
        if not user_payload or user_payload['role'].get('role_name') != Role.TEACHER.value:
            return Response({"success": False, "message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        marks_id = request.data.get('marks_id')
        updated_subjects_marks = request.data.get('subjects_marks')
        
        if not all([marks_id, updated_subjects_marks]):
            return Response({"success": False, "message": "Marks ID and subjects marks are required"}, 
                        status=status.HTTP_400_BAD_REQUEST)
  
        existing_record = mark_collection.find_one({"_id": ObjectId(marks_id)})
        if not existing_record:
            return Response({"success": False, "message": "Marks record not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
        
        teacher_id = user_payload["user_id"]
        teacher_class_id = user_payload['class'][str('class_id')]
        teacher_subjects = set(user_payload['class']['subjects'])
        
        if existing_record["teacher_id"] != teacher_id:
            return Response({"success": False, "message": "Not authorized to update these marks"}, 
                        status=status.HTTP_403_FORBIDDEN)
        
        if existing_record["class_id"] != teacher_class_id:
            return Response({"success": False, "message": "Cannot update marks for a different class"}, 
                        status=status.HTTP_403_FORBIDDEN)
        
        input_subjects = set(updated_subjects_marks.keys())
        if not input_subjects.issubset(teacher_subjects):
            return Response({"success": False, "message": "Invalid subjects provided"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        for subject in updated_subjects_marks:
            if subject not in existing_record["subjects_marks"]:
                return Response({"success": False, "message": f"Subject {subject} does not exist in the original record"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        total_marks = existing_record["total_marks"]
        for subject, marks in updated_subjects_marks.items():
            if marks > total_marks:
                return Response({"success": False, "message": f"Marks for {subject} exceed the allowed total"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        subjects_marks = existing_record["subjects_marks"].copy()
        subjects_marks.update(updated_subjects_marks)
        
        obtained_marks = sum(subjects_marks.values())
        percentage = (obtained_marks / total_marks) * 100
        grade = calculate_grade(percentage)
        
        update_data = {
            "subjects_marks": subjects_marks,
            "total_obtained_marks": obtained_marks,
            "percentage": round(percentage, 2),
            "grade": grade,
            "date": datetime.datetime.utcnow() 
        }
        
        mark_collection.update_one(
            {"_id": ObjectId(marks_id)},
            {"$set": update_data}
        )
        
        updated_record = mark_collection.find_one({"_id": ObjectId(marks_id)})
        updated_record["_id"] = str(updated_record["_id"])
        
        return Response(
            {
                "success": True,
                "message": "Marks updated successfully",
                "response": updated_record
            },
            status=status.HTTP_200_OK
        )
        