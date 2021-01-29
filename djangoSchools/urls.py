"""djangoSchools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Dashboard', views.Home, name='Dashboard'),
    path('StudentDashboard', views.StudentDashboard, name='StudentDashboard'),
    path('TeacherDashboard', views.TeacherDashboard, name='TeacherDashboard'),
    path('login', views.LoginPage, name='login'),
    path('Logout', views.Logout, name='Logout'),
    path('addstd', views.AddStudent, name='addstd'),
    path('AddCoursesToTimetable', views.AddCoursesToTimetable, name='AddCoursesToTimetable'),
    path('AddCoursesToTimetable1 <str:pk> <str:pk1>', views.AddCoursesToTimetable1, name='AddCoursesToTimetable1'),
    path('viewStudent <str:pk>', views.ViewStudent, name='viewStudent'),
    path('ViewStudentCourses <str:pk>', views.ViewStudentCourses, name='ViewStudentCourses'),
    path('ViewStudentCoursesDetails <str:pk> <str:pk1>', views.ViewStudentCoursesDetails, name='ViewStudentCoursesDetails'),
    path('CreateAttendence <str:pk> <str:pk1>', views.CreateAttendence, name='CreateAttendence'),
    path('TeachersStudentList <str:pk>', views.TeachersStudentList, name='TeachersStudentList'),
    path('UpdateStdAssignment <str:pk>', views.UpdateStdAssignment, name='UpdateStdAssignment'),
    path('ViewStdAssign <str:pk>', views.ViewStdAssign, name='ViewStdAssign'),
    path('TeachersStudentList1 <str:pk> <str:pk1>/<str:pk2>', views.TeachersStudentList1, name='TeachersStudentList1'),
    path('StudentAttendencePre <str:pk> <str:pk1>', views.StudentAttendencePre, name='StudentAttendencePre'),
    path('StudentAttendenceAbs <str:pk> <str:pk1>', views.StudentAttendenceAbs, name='StudentAttendenceAbs'),
    path('ViewStdQuiz <str:pk> <str:pk1>', views.ViewStdQuiz, name='ViewStdQuiz'),
    path('AnsTheQuestion <str:pk> <str:pk1> <str:pk2>', views.AnsTheQuestion, name='AnsTheQuestion'),
    path('NextQuestion <str:pk> <str:pk1>', views.NextQuestion, name='NextQuestion'),
    path('StartQuiz <str:pk>', views.StartQuiz, name='StartQuiz'),
    path('TchQuiz <str:pk> <str:pk1>', views.TchQuiz, name='TchQuiz'),
    path('UploadQuiz <str:pk> <str:pk1>', views.UploadQuiz, name='UploadQuiz'),
    path('CreateQuiz <str:pk> <str:pk1>', views.CreateQuiz, name='CreateQuiz'),
    path('ViewTchQuiz <str:pk> <str:pk1>', views.ViewTchQuiz, name='ViewTchQuiz'),
    path('ShowStdQuiz <str:pk> <str:pk1>', views.ShowStdQuiz, name='ShowStdQuiz'),
    path('AddQuestToQuiz <str:pk> <str:pk1>', views.AddQuestToQuiz, name='AddQuestToQuiz'),
    path('AddMCQToQuiz <str:pk>', views.AddMCQToQuiz, name='AddMCQToQuiz'),
    path('OpenReviewToQuiz <str:pk> <str:pk1>', views.OpenReviewToQuiz, name='OpenReviewToQuiz'),
    path('CourseGrades <str:pk> <str:pk1>', views.CourseGrades, name='CourseGrades'),
    path('createtimetable', views.CreateTimetable, name='createtimetable'),
    path('viewtimetable', views.viewtimetable, name='viewtimetable'),
    path('all_student', views.StudentList, name='all_student'),
    path('std_result', views.StudentResult, name='std_result'),
    path('AddDepStd <str:pk>', views.AddDepStd, name='AddDepStd'),
    path('AssignDepStd <str:pk>', views.AssignDepStd, name='AssignDepStd'),
    path('ShowCourseStd <str:pk>', views.ShowCourseStd, name='ShowCourseStd'),
    path('RemoveStdCourses <str:pk>', views.RemoveStdCourses, name='RemoveStdCourses'),
    path('assignCourseStd <str:pk>', views.AssignCourseStd, name='assignCourseStd'),
    path('Add_Teacher', views.AddTeacher, name='Add_Teacher'),
    path('TeacherCourses <str:pk>', views.TeacherCourses, name='TeacherCourses'),
    path('ViewTeacherCoursesDetails <str:pk>', views.ViewTeacherCoursesDetails, name='ViewTeacherCoursesDetails'),
    path('detailTeacher <str:pk>', views.DetailTeacher, name='detailTeacher'),
    path('Coursepeoples <str:pk> <str:pk1>', views.Coursepeoples, name='Coursepeoples'),
    path('CreateAnnouncements <str:pk> <str:pk1>', views.CreateAnnouncements, name='CreateAnnouncements'),
    path('CreateAssignments <str:pk> <str:pk1>', views.CreateAssignments, name='CreateAssignments'),
    path('SeeAnnouncements <str:pk> <str:pk1>', views.SeeAnnouncements, name='SeeAnnouncements'),
    path('SeeAssignment <str:pk> <str:pk1>', views.SeeAssignment, name='SeeAssignment'),
    path('TeacherAllAssignments <str:pk> <str:pk1>', views.TeacherAllAssignments, name='TeacherAllAssignments'),
    path('SeeAssignmentDetail <str:pk>', views.SeeAssignmentDetail, name='SeeAssignmentDetail'),
    path('TeacherAssigDetail <str:pk>', views.TeacherAssigDetail, name='TeacherAssigDetail'),
    path('SeeAttendence <str:pk>', views.SeeAttendence, name='SeeAttendence'),
    path('SeePeoples <str:pk>', views.SeePeoples, name='SeePeoples'),
    path('all_teachers', views.AllTeachers,name='all_teachers'),
    path('AddTeacherDesig', views.CreateTeacherDesignation, name='AddTeacherDesig'),
    path('courseList', views.CourseList,name='courseList'),
    path('ShowCourses', views.ShowCourses,name='ShowCourses'),
    path('AddCourseDep <str:pk>', views.AddCourseDep, name='AddCourseDep'),
    path('SelectCourseDep <str:pk>', views.SelectCourseDep, name='SelectCourseDep'),
    path('add_Course', views.Add_Course,name='add_Course'),
    path('courseSection', views.courseSection, name='courseSection'),
    path('courseAttendence', views.courseAttendence, name='courseAttendence'),
    path('showCourseTeach <str:pk>', views.ShowCourseTeach, name='showCourseTeach'),
    path('RemoveAssigCourseTeach <str:pk>', views.RemoveAssignedCourseTeach, name='RemoveAssigCourseTeach'),
    path('assignCourseTeach <str:pk>', views.AssignCourseTeach, name='assignCourseTeach'),
    path('AddDepTeach <str:pk>', views.AddDepTeach, name='AddDepTeach'),
    path('AssignDepTeach <str:pk>', views.AssignDepTeach, name='AssignDepTeach'),
    path('ChangeDepartment', views.ChangeDepartment, name='ChangeDepartment'),
    path('ChangeDepFaculty <str:pk>', views.ChangeDepFaculty, name='ChangeDepFaculty'),
    path('SelectDepFaculty <str:pk>', views.SelectDepFaculty, name='SelectDepFaculty'),
    path('RemoveFaculty <str:pk>', views.RemoveFaculty, name='RemoveFaculty'),
    path('ChangeDepHOD <str:pk>', views.ChangeDepHOD, name='ChangeDepHOD'),
    path('SelectDepHOD <str:pk>', views.SelectDepHOD, name='SelectDepHOD'),
    path('ChangeDepCourses <str:pk>', views.ChangeDepCourses, name='ChangeDepCourses'),
    path('SelectDepCourses <str:pk>', views.SelectDepCourses, name='SelectDepCourses'),
    path('RemoveDepCourses <str:pk>', views.RemoveDepCourses, name='RemoveDepCourses'),
    path('AssignCourseStd', views.AssignCourseStd, name='AssignCourseStd'),
    path('Departments', views.Departments, name='Departments'),
    path('addDepartments', views.AddDepartments, name='addDepartments'),
    path('academic_Session', views.Academic_Session, name='academic_Session'),
    path('AllSemester', views.AllSemester, name='AllSemester'),


]
