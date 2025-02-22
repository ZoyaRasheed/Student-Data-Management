from django.contrib import admin
from .models import User, Teacher, Student

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name')
    list_filter = ('user_type', 'is_staff', 'is_active')

# Register Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'teaching_class')
    search_fields = ('user__email', 'user__first_name', 'phone_number')
    list_filter = ('teaching_class',)

# Register Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'full_name', 'student_class', 'parents_email')
    search_fields = ('user__email', 'full_name', 'student_id')
    list_filter = ('student_class',)
