
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Student, Professor, FieldProject
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        role = data.get('role') 

        if role == 'student':
            user = Student.objects.filter(
            full_name=username,
            password=password
            ).first()
            
        elif role == 'professor':
            user = Professor.objects.filter(
            full_name=username,
            password=password
            ).first()
            
        else:
            return JsonResponse({"error": "Invalid role selected"}, status=400)

        if user:
            # login(request, user)
            return JsonResponse({
                "status": "success",
                "username": user.full_name,
                "role": role
            })
        else:
            return JsonResponse({"error": f"User is not registered as a {role}"}, status=403)

    return JsonResponse({"error": "Invalid credentials"}, status=401)

@csrf_exempt
def profile_view(request):

    role = request.GET.get('role')
    username = request.GET.get('username')

    try:
        if role == 'student':
            profile = Student.objects.get(full_name=username)
            data = {
                # "image" : profile.image,
                "name": profile.full_name,
                "subject": profile.course_name,
                "roll_number" : profile.roll_number,
                "year": profile.year
            }
        elif role == 'professor':
            profile = Professor.objects.get(full_name=username)
            data = {
                # "image" :profile.image,
                "name": profile.full_name,
                "subject": profile.sub,
            }
        
        return JsonResponse(data)
    except (Student.DoesNotExist, Professor.DoesNotExist):
        return JsonResponse({"error": "Profile not found"}, status=404)

@csrf_exempt
def project_list(request):
    role = request.GET.get("role")
    username = request.GET.get("username")

    if role == "professor":
        projects = FieldProject.objects.select_related('student').all()

        data = []
        for project in projects:
            data.append({
                "id": project.id,
                "title": project.title,
                "student_name": project.student.full_name,
                "roll_number": project.student.roll_number,
                "submitted_at": project.submitted_at,
                "is_checked": project.is_checked,
                "marks": project.marks
            })

        return JsonResponse(data, safe=False)

    elif role == "student":
        try:
            student = Student.objects.get(full_name=username)
            project = FieldProject.objects.get(student=student)

            data = {
                "id": project.id,
                "title": project.title,
                "submitted_at": project.submitted_at,
                "is_checked": project.is_checked,
                "marks": project.marks
            }

            return JsonResponse(data)

        except:
            return JsonResponse({"message": "No project submitted"})

    return JsonResponse({"error": "Invalid role"}, status=400)

@csrf_exempt
def update_project(request, id):
    if request.method == "POST":
        body = json.loads(request.body)

        project = FieldProject.objects.get(id=id)
        project.is_checked = body.get("is_checked")
        project.marks = body.get("marks")
        project.save()

        return JsonResponse({"message": "Updated successfully"})

@csrf_exempt
def submit_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        username = request.POST.get("username")
        file = request.FILES.get("project_file")

        student = Student.objects.get(full_name=username)

        FieldProject.objects.create(
            title=title,
            student=student,
            project_file=file
        )

        return JsonResponse({"message": "Project submitted successfully"})