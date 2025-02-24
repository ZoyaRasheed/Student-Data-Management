from config.db import *

class_collection = db['Class']
roles_collection = db['Roles']

# Roles Seeder
def seed_roles():
    roles = [
        {"name": "ADMIN", "permissions": ["view", "create", "delete", "update"]},
        {"name": "TEACHER", "permissions": ["view", "create", "delete", "update"]},
        {"name": "STUDENT", "permissions": ["view"]}
    ]
    for role in roles:
        if not roles_collection.find_one({"name": role["name"]}):
            roles_collection.insert_one(role)
    print("Roles seeded")

# Class Seeder
def seed_classes():
    subjects_1_to_5 = ["Math", "Science", "English", "History", "Geography"]
    subjects_6_to_10 = ["Math", "English", "Biology", "Physics", "Chemistry"]
    for i in range(1, 11):
        if not class_collection.find_one({"name": f"Class {i}"}):
            subjects = subjects_1_to_5 if i <= 5 else subjects_6_to_10
            class_collection.insert_one({"name": f"Class {i}", "subjects": subjects})
    print("Classes seeded")

if __name__ == "__main__":
    seed_roles()
    seed_classes()

    print("Seeding complete")