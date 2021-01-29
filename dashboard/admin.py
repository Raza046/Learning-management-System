from django.contrib import admin
from dashboard.models import Student,Users,Teacher,Department,Course,Semester,Attendence,Timetable,TimetableDetails,Announcements,Assignments,Quiz,AssignmentDetails,Quiz,QuestionAnswer,QuizDetails,Answer,MCQANSWERS


admin.site.register(Users)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Attendence)
admin.site.register(Timetable)
admin.site.register(TimetableDetails)
admin.site.register(Announcements)
admin.site.register(Assignments)
admin.site.register(Quiz)
admin.site.register(AssignmentDetails)
admin.site.register(QuizDetails)
admin.site.register(QuestionAnswer)
admin.site.register(Answer)
admin.site.register(MCQANSWERS)

