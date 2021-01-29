from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone

class Users(AbstractUser):

    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
      (3, 'admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


class Student(Users):

    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='static')
    date_of_birth = models.DateField(blank=True, null=True)
    RegistrationNo = models.CharField(max_length=16, unique=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    guardian_mobile = models.CharField(max_length=11, blank=True, null=True)
    Department = models.ForeignKey("Department",on_delete=models.CASCADE,related_name="StudentDep",null=True)
    Semester = models.ForeignKey("Semester",on_delete=models.CASCADE,related_name="StudentSem",null=True)
    Courses = models.ManyToManyField("Course",related_name='StdCourses')
    Section = models.CharField(max_length=16)
    Attendence = models.ManyToManyField("Attendence",related_name="StdAtt",null=True)


    class Meta:
        verbose_name = "Student"


class Teacher(Users):

    Name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='static')
    Date_of_birth = models.DateField(blank=True, null=True)
    Designation = models.CharField(max_length=150)
    Department = models.ForeignKey("Department",on_delete=models.CASCADE,related_name="TeacherDep",null=True)
    Courses = models.ManyToManyField("Course")
    Semester = models.ForeignKey("Semester",on_delete=models.CASCADE,null=True,related_name="TeacherSem")
    mobileNo = models.CharField(max_length=11, blank=True, null=True)
    Email = models.CharField(max_length=255, blank=True, null=True)
    joining_date = models.DateField(auto_now=True)
    Attendence = models.ManyToManyField("Attendence",related_name="TeacherAtt",null=True)

    class Meta:
        verbose_name = "Teacher"

    def __str__(self):
        return self.Name

class Department(models.Model):

    Dept_Name = models.CharField(max_length=150)
    HOD = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="HOD",null=True)
    Faculty = models.ManyToManyField(Teacher)
    courses = models.ManyToManyField("Course")

    class Meta:
        verbose_name = "Department"

    def __str__(self):
        return self.Dept_Name

class Course(models.Model):

    Course_Name = models.CharField(max_length=150,unique=True)
    Course_Id = models.CharField(max_length=150,unique=True)
    Department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="CourseDep",null=True)
    credit_hours = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Course"

    def __str__(self):
        return self.Course_Name


class Semester(models.Model):

    Semester = models.PositiveIntegerField(null=True)
    Department = models.ForeignKey("Department",on_delete=models.CASCADE,related_name="SemesterDep",null=True)
    Course = models.ManyToManyField("Course")

    def __int__(self):
        return self.Semester

    class Meta:
        verbose_name = "Semester"

class Attendence(models.Model):

    week_days = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
    )

    Attendence_status = (
      ('Absent','Absent'),
      ('Present','Present'),
    )

    Course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="CAttendence",null=True)
    Section = models.CharField(max_length=20,null=True)
    Date = models.DateField(auto_now_add=False, null=True)
    student = models.ManyToManyField(Student,related_name="StdAtt",null=True)
    teacher = models.ManyToManyField(Teacher,related_name="TeaAtt",null=True)
    Time = models.TimeField(auto_now_add=False,null=True)
    Day = models.CharField(choices=week_days,max_length=20, null=True)
    status = models.CharField(choices=Attendence_status,max_length=20,null=True)
    

    def __str__(self):
        return str(self.Course.Course_Name)

    class Meta:
        verbose_name = "Attendence"

class Timetable(models.Model):

    week_days = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
    )

    Date = models.DateField(auto_now_add=True, null=True)
    Day = models.CharField(choices=week_days,max_length=20, null=True)
    Details = models.ManyToManyField("TimetableDetails")

    def __str__(self):
        return self.Day

    class Meta:
        verbose_name = "Timetable"


class TimetableDetails(models.Model):

    class_Timings = (
        ("8:30 - 9:20","8:30 - 9:20"),
        ("9:20 - 10:10","9:20 - 10:10"),
        ("10:10 - 11:00","10:10 - 11:00"),
        ("11:00 - 11:50","11:00 - 11:50"),
        ("11:50 - 12:40","11:50 - 12:40"),
        ("12:40 - 1:30","12:40 - 1:30"),
    )

    week_days = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
    )

    Time = models.CharField(choices=class_Timings,max_length=20,null=True)
    Course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="CTimetable",null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="TeaTimetable",null=True)
    Day = models.CharField(choices=week_days,max_length=20, null=True)

    def __str__(self):
        return self.Time

    class Meta:
        verbose_name = "TimetableDetail"

class Announcements(models.Model):

    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="TeaAnnouncement",null=True)
    Course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="CAnnouncement",null=True)
    Section = models.CharField(max_length=10,null=True)
    texts = models.CharField(max_length=1000,null=True)
    start_Date = models.DateField(auto_now_add=True, null=True)
    start_Time = models.TimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Announcement"

    def __str__(self):
        return str(self.Course.Course_Name) +" --- " + str(self.teacher.Name) +" --- Sec " + str(self.Section)


class Assignments(models.Model):

    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="TeaAssignments",null=True)
    Course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="CAssignments",null=True)
    Section = models.CharField(max_length=10,null=True)
    AssignDetails = models.ManyToManyField("AssignmentDetails")
    title = models.CharField(max_length=100,null=True) 
    description = models.CharField(max_length=1000,null=True)
    files = models.FileField(upload_to='static')
    Total_Marks = models.PositiveIntegerField(null=True)
    start_Date = models.DateField(auto_now_add=True, null=True)
    start_Time = models.TimeField(auto_now_add=True,null=True)
    end_Date = models.DateField(default="1111-11-11",null=True,blank=True)
    end_Time = models.TimeField(null=True,blank=True)

    class Meta:
        verbose_name = "Assignments"

    def __str__(self):
        return str(self.Course.Course_Name) +" --- " + str(self.teacher.Name) +" --- Sec " + str(self.Section)

class AssignmentDetails(models.Model):

    Assignment =  models.ForeignKey(Assignments,on_delete=models.CASCADE,related_name="StdAssigns",null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name="StdSubmission",null=True)
    Submission = models.FileField(upload_to='static')
    Sub_Details =  models.CharField(max_length=1000,null=True)
    status = models.CharField(max_length=1000,default="No Submission Yet",null=True)
    Remarks =  models.CharField(max_length=1000,null=True)
    Scored = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name = "AssignmentDetail"

    def __str__(self):
        return str(self.student.name) + " --- Sec " + str(self.student.Section) + "--" + str(self.Assignment.title)

class Quiz(models.Model):

    upload_opt = (
        ('Yes','Yes'),
        ('No','No'),
    )

    review_opt = (
        ('Open','Open'),
        ('Closed','Closed'),
    )
    
    title = models.CharField(max_length=100,null=True) 
    description = models.CharField(max_length=1000,null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="TeaQuiz",null=True)
    Course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="CAQuiz",null=True)
    QuizDetail = models.ManyToManyField("QuizDetails")
    QuestionAns = models.ManyToManyField("QuestionAnswer")
    Section = models.CharField(max_length=10,null=True)
    files = models.FileField(upload_to='static')
    Total_Marks = models.PositiveIntegerField(null=True)
    start_Date = models.DateField(auto_now_add=True, null=True)
    start_Time = models.TimeField(auto_now_add=True,null=True)
    end_Date = models.DateField(default="1111-11-11",null=True,blank=True)
    end_Time = models.TimeField(null=True,blank=True)
    upload = models.CharField(choices=upload_opt,max_length=10,null=True,blank=True)
    Review = models.CharField(choices=review_opt,max_length=10,null=True,blank=True)

    class Meta:
        verbose_name = "Quiz"

    def __str__(self):
        return str(self.Course.Course_Name) +" --- " + str(self.teacher.Name) +" --- Sec " + str(self.Section)

class QuizDetails(models.Model):

    Quiz =  models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="MyQuiz1",null=True) 
    Ans = models.ManyToManyField("Answer")
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name="StdQuiz",null=True)
    Sub_Details =  models.CharField(max_length=1000,null=True)
    status = models.CharField(max_length=1000,default="No Answered Yet",null=True)
    Remarks =  models.CharField(max_length=1000,null=True)
    Scored = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name = "QuizDetails"

class QuestionAnswer(models.Model):

    Quiz =  models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="MyQuiz2",null=True)
    question = models.CharField(max_length=10,null=True)
    MCQAns =  models.ManyToManyField("MCQANSWERS")
    Answers = models.CharField(max_length=1000,null=True)
    Marks = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name = "QuestionAnswer"

class Answer(models.Model):

    quizDetail = models.ForeignKey(QuizDetails,on_delete=models.CASCADE,related_name="MyAns",null=True)
    Question = models.ForeignKey(QuestionAnswer,on_delete=models.CASCADE,related_name="AnsQs",null=True)
    Submission = models.FileField(upload_to='static')
    Answers = models.CharField(max_length=1000,null=True)

    class Meta:
        verbose_name = "Answer"


class MCQANSWERS(models.Model):

    correct_opt = (
        ('Yes','Yes'),
        ('No','No'),
    )

    QuesAns =  models.ForeignKey(QuestionAnswer,on_delete=models.CASCADE,related_name="MyQuizAns",null=True)
    Answers = models.CharField(max_length=1000)
    Correct_Ans = models.CharField(max_length=100,choices=correct_opt)


class GRADE(models.Model):

    correct_opt = (
        ('Yes','Yes'),
        ('No','No'),
    )

    Quizes = models.ManyToManyField("Quiz")
    Assignments =  models.ManyToManyField("Assignments")
    Grade = models.CharField(max_length=100,choices=correct_opt)

