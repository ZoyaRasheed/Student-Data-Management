from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import jwt # type: ignore
from app.models import *
from bson import ObjectId # type: ignore

SECRET_KEY = "Q!E2R3S4"


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):
        # Get Token
        token = request.COOKIES.get('access_token') or \
                (request.headers.get('Authorization', '').split(' ')[1] 
                 if request.headers.get('Authorization', '').startswith('Bearer ') else None)

        if not token:
            return Response({"success": False, "message": "Please login to access the resource"},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode JWT Token
            decoded_jwt_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # Extract User ID from JWT
            user_id = decoded_jwt_payload.get('user_id')  # Ensure JWT contains 'user_id'
            if not user_id:
                return Response({"success": False, "message": "Invalid token payload"}, 
                                status=status.HTTP_401_UNAUTHORIZED)

            # Fetch User Details from MongoDB
            user = user_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return Response({"success": False, "message": "User not found"}, 
                                status=status.HTTP_404_NOT_FOUND)

            # Fetch Role Details
            role = roles_collection.find_one({"_id": ObjectId(user['role_id'])})
            if not role:
                return Response({"success": False, "message": "Role not found"}, 
                                status=status.HTTP_404_NOT_FOUND)

            # Fetch Class Details
            user_class = class_collection.find_one({"_id": ObjectId(user['class_id'])})
            if not user_class:
                return Response({"success": False, "message": "Class not found"}, 
                                status=status.HTTP_404_NOT_FOUND)

            # Save Combined Payload to request.user_payload
            request.user_payload = {
                "user_id": str(user['_id']),
                "name": user.get("name"),
                "email": user.get("email"),
                "phone_number": user.get("phone_number"),
                "role": {
                    "role_id": str(role['_id']),
                    "role_name": role.get("name", user.get("role")),
                    "permissions": role.get("permissions", [])  # Include permissions from role
                },
                "class": {
                    "class_id": str(user_class['_id']),
                    "class_name": user_class.get("name", user.get("class")),
                    "subjects": user_class.get("subjects", [])  # Include subjects from class
                }
            }

        except jwt.ExpiredSignatureError:
            return Response({"success": False, "message": "Token has expired"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"success": False, "message": "Invalid token"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False, "message": f"An error occurred: {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return view_func(view, request, *args, **kwargs)

    return _wrapped_view
