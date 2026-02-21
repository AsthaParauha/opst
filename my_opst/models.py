from django.db import models

# Create your models here.
class Professor(models.Model):
    image = models.ImageField(upload_to='professor_images/', blank=True, null=True)
    full_name = models.CharField(max_length=100)
    sub = models.CharField(max_length=100)
    password = models.CharField(max_length=20) 
    def __str__(self):
        return self.full_name

class Student(models.Model):
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    full_name = models.CharField(max_length=100)
    year= models.CharField(max_length=20)
    course_name = models.CharField(max_length=30)
    roll_number = models.CharField(max_length=7 , unique=True)
    password = models.CharField(max_length=20) 

    def __str__(self):
        return self.full_name

class FieldProject(models.Model):
    # title
    title = models.CharField(max_length=60)
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at=models.DateTimeField(auto_now_add=True)
    #  project .pptx or .ppt file
    project_file=models.FileField(upload_to='fild_projects')
    # is_checked
    is_checked = models.BooleanField(default=False) 
    # marks 
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
