from django.shortcuts import render, HttpResponseRedirect, Http404,redirect
from dashboard.models import Student,Teacher,Users,Department,Course,Attendence,Timetable,TimetableDetails,Announcements,Assignments,AssignmentDetails,Quiz,QuizDetails,QuestionAnswer,Answer,MCQANSWERS
from django.contrib.auth.models import User, auth
from .forms import CourseForm,DepartmentForm,AnnouncementForm,AssignmentForm
from collections import Counter
import numpy as np
import datetime
# Create your views here.



def Home(request):

    context = locals()
    return render(request,'dashboard.html',context)

def StudentDashboard(request):

    now = datetime.datetime.now()
    Today = now.strftime("%A") 
    now1 = str(now)
    now2 = now1.split(" ")[1]
    print(now2)

    user1 = request.user
    std = Student.objects.filter(id=user1.id).first()
    TD = TimetableDetails.objects.all()

    for cs1 in std.Courses.all():
        for t in TD:
            if cs1 == t.Course and t.Time=="8:30 - 9:20" and t.Day==Today:
                print(str(cs1) + " class at "+str(t.Time))
            elif cs1 == t.Course and t.Time=="9:20 - 10:10" and t.Day==Today:
                print(str(cs1) + " class at "+str(t.Time))
            elif cs1 == t.Course and t.Time=="10:10 - 11:00" and t.Day==Today:
                print(str(cs1) + " class at "+str(t.Time))


    context = {'std':std,"TD":TD,"Today":Today}

    return render(request,'SDashboard.html',context)

def TeacherDashboard(request):

    now = datetime.datetime.now()
    Today = now.strftime("%A") 
    now1 = str(now)
    now2 = now1.split(" ")[1]
    print(now2)

    user1 = request.user
    std = Teacher.objects.filter(id=user1.id).first()
    TD = TimetableDetails.objects.all()

    for cs1 in std.Courses.all():
        for t in TD:
            if cs1 == t.Course and t.Time=="8:30 - 9:20" and t.Day==Today:
                print(str(cs1) + " class at "+str(t.Time))
            elif cs1 == t.Course and t.Time=="9:20 - 10:10" and t.Day==Today:
                print(str(cs1) + " class at "+str(t.Time))
            elif cs1 == t.Course and t.Time=="10:10 - 11:00" and t.Day==Today:
                print(str(cs1) + " class at "+str(t.Time))


    context = {'std':std,"TD":TD,"Today":Today}

    return render(request,'Tdashboard.html',context)


def LoginPage(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            if user.user_type == 1:
                print('Student Login')
                return redirect('StudentDashboard')

            if user.user_type == 2:
                print('Teacher Login')
                return redirect('TeacherDashboard')

            if user.is_superuser:
                print('Admin Login')
                return redirect('Dashboard')

        else:
            return redirect('login')

    else:

        context = locals()

        return render(request,'registration/login.html',context)


def Logout(request):

    auth.logout(request)
    return redirect('login')

# TIMETABLE

def CreateTimetable(request):

    crs = Course.objects.all()
    Teach  = Teacher.objects.all()

    TT = Timetable.objects.all()
    TD = TimetableDetails.objects.all()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std':crs,'base_template':base_template,'t':Teach,'TT':TT,'TD':TD}
    return render(request,'admin_tools/create_timetable.html',context)

def AddCoursesToTimetable(request):

    crs = Course.objects.all()
    Teach  = Teacher.objects.all()
    course_value = request.POST.get('change1')
    
    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'all_c':crs,'base_template':base_template,'t':Teach,'cv':course_value}
    return render(request,'admin_tools/addCourse_timetable.html',context)


def AddCoursesToTimetable1(request,pk,pk1):

    my_t = Teacher.objects.all()

    day = pk.split(" ")[0]
    print(day)
    times = pk.split(" ")[1:4]
    time1 = ' '.join(str(e) for e in times)
    print(time1)

    courses = pk.split(" ")[4:5]

    t1 = ' '.join(str(e) for e in courses)

    c1 = str(t1) + " " + str(pk1)
    print("pk1 is --> " + str(c1))

    tch = []
    cc = []
    for tchrs in my_t:
        for tc in tchrs.Courses.all():
            if tc.Course_Name == c1:
                print(tchrs.Name)
                print(tc.Course_Name)
                tch.append(tchrs.Name)

    my_c1 = Course.objects.filter(Course_Name=c1).first()
    my_t1 = Teacher.objects.filter(Name=tch[0]).first()

    if Timetable.objects.filter(Day=day):
        print("Yes this day is in timetable")
        
        tt1 = Timetable.objects.get(Day=day)

        if TimetableDetails.objects.filter(Time=time1,Day=day):
            tt2 = TimetableDetails.objects.get(Time=time1,Day=day)
            tt2.Course = my_c1
            tt2.teacher = my_t1
            tt2.save()
            tt1.Details.add(tt2)
            print("Yes this time is added in Timetable")

        else:
            tt3 = TimetableDetails.objects.create(Time=time1,Course = my_c1,teacher=my_t1,Day=day)
            tt1.Details.add(tt3)
            print("Yes this time is added in Timetable")

    else:
        tt1 = Timetable.objects.create(Day=day)
        print("Yes this day is added in Timetable")

        if TimetableDetails.objects.filter(Time=time1,Day=day):
            tt2 = TimetableDetails.objects.get(Time=time1,Day=day)
            tt2.Course = my_c1
            tt2.teacher = my_t1
            tt2.save()

            tt1.Details.add(tt2)
            print("Yes this time is added in Timetable")

        else:
            tt2 = TimetableDetails.objects.create(Time=time1,Course = my_c1,teacher=my_t1,Day=day)
            tt1.Details.add(tt2)
        print("Yes this time is added in Timetable")


    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    return redirect('createtimetable')


def ViewTimetable(request):

    crs = Course.objects.all()
    Teach  = Teacher.objects.all()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std':crs,'base_template':base_template,'t':Teach}
    return render(request,'admin_tools/timetable.html',context)


# STUDENT ACCOUNT

def ViewStudentCourses(request,pk):

    std = Student.objects.filter(id=pk).first()
    t  = Teacher.objects.all()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std':std,'base_template':base_template,'t':t}
    return render(request,'students/student_courses.html',context)

def ViewStudentCoursesDetails(request,pk,pk1):

    std = Student.objects.filter(id=pk).first()
    crs = Course.objects.filter(id=pk1).first()
    t  = Teacher.objects.all()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std':std,'cs':crs,'base_template':base_template,'t':t}
    return render(request,'students/student_courseDetails.html',context)

# TEACHER ACCOUNT

def ViewTeacherCoursesDetails(request,pk):

    user1 = request.user
    tch = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    std = Student.objects.all()

    sec_array = []

    for st in std:
        for sc in st.Courses.all():
            for tc in tch.Courses.all():
                if sc == tc:
                    sec_array.append(st.Section)

    print(list(set(sec_array)))
    my_sec = list(set(sec_array))

    context = {'tch':tch,'cs':crs,'sec':my_sec,'base_template':base_template}
    return render(request,'teachers/teacher_courseDetails.html',context)

def CourseGrades(request,pk,pk1):

    user1 = request.user

    tch = Student.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    qs1 = QuizDetails.objects.filter(student=tch).all()
    ass1 = AssignmentDetails.objects.filter(student=tch).all()

    for q in qs1:
        print(q.student)
        print(q.Scored)


    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std':tch,'cs':crs,'sec':pk1,'q1':qs1,'base_template':base_template}
    return render(request,'students/CourseGrades.html',context)

def Coursepeoples(request,pk,pk1):

    user1 = request.user

    tch = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    stds = Student.objects.all() 

    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'tch':tch,'std':stds,'cs':crs,'sec':pk1,'base_template':base_template}
    return render(request,'teachers/CoursePeoples.html',context)


def CreateAnnouncements(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    print("Section is --> " + str(pk1))

    AnnounceForm = AnnouncementForm(request.POST)

    if AnnounceForm.is_valid():
        obj = AnnounceForm.save(commit=False)
        obj.teacher = t
        obj.Course = crs
        obj.Section = pk1
        obj.save()

        return  redirect('CreateAnnouncements',pk,pk1)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'t':t,'form':AnnounceForm,'s':pk1}
    return render(request,'teachers/TeacherAnnouncements.html',context)

def SeePeoples(request,pk):

    user1 = request.user

    tch = Student.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    stds = Student.objects.all() 

    p = []
    for s in stds:
        for cs in s.Courses.all():
            if cs == crs and s.Section == tch.Section:
                print(s.name)
                p.append(s)

    print("Section is --> " + str(tch.Section))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'tch':tch,'p':p,'sec':tch.Section,'base_template':base_template}
    return render(request,'students/SeeCoursePeoples.html',context)

def SeeAnnouncements(request,pk,pk1):

    user1 = request.user
    t  = Student.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    tch = Teacher.objects.all()

    teach = []

    for tc in tch:
        for c in tc.Courses.all():
            if c == crs:
                teach.append(tc)

    print(teach[0])
    t1 = teach[0]
    print("Section is --> " + str(pk1))

    Announce = Announcements.objects.filter(teacher=t1,Course=crs,Section=pk1)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'s':pk1,'teacher':t1,'Announce':Announce}
    return render(request,'students/StdAnnouncements.html',context)

def viewtimetable(request):

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = locals()
    return render(request,'admin_tools/timetable.html',context)


def SeeAttendence(request,pk):

    user1 = request.user
    t  = Student.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    tch = Teacher.objects.all()

    teach = []
    for tc in tch:
        for c in tc.Courses.all():
            if c == crs:
                teach.append(tc)

    print(teach[0])
    t1 = teach[0]

    now = datetime.datetime.now()
    Today = now.strftime("%A") 
    now1 = str(now)
    now2 = now1.split(" ")[1]
    date_today = now1.split(" ")[0]

    print(now2)
    print(now1)
    print(Today)
    print(date_today)

    attnd = Attendence.objects.filter(Course=crs,student=t,teacher=t1,Date=date_today)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'student':t,'teacher':t1,'Attnd':attnd}
    return render(request,'students/StdAttnd.html',context)

def TeacherAllAssignments(request,pk,pk1):

    user1 = request.user
    st  = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    tch = Teacher.objects.all()
    print(pk1)

    ass1 = Assignments.objects.filter(teacher=st,Course=crs,Section=pk1)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'student':st,'ass':ass1,'s':pk1}
    return render(request,'teachers/TeacherSeeAssign.html',context)

def TeacherAssigDetail(request,pk):

    user1 = request.user
    st  = Teacher.objects.filter(id=user1.id).first()
    ass1 = Assignments.objects.filter(id=pk).first()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'teacher':st,'ass':ass1}
    return render(request,'teachers/TeacherAssigDetail.html',context)

def SeeAssignment(request,pk,pk1):

    user1 = request.user
    st  = Student.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    tch = Teacher.objects.all()
    print(pk1)

    teach = []
    for tc in tch:
        for c in tc.Courses.all():
            if c == crs:
                teach.append(tc)

    print(teach[0])
    t1 = teach[0]

    ass1 = Assignments.objects.filter(teacher=t1,Course=crs,Section=pk1)
    ass2 = Assignments.objects.filter(teacher=t1,Course=crs,Section=pk1).first()
    

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'student':st,'ass':ass1}
    return render(request,'students/SeeAssign.html',context)

def ViewStdAssign(request,pk):

    user1 = request.user
    tch = Teacher.objects.filter(id=user1.id).first()
    assdetail = AssignmentDetails.objects.filter(id=pk).first()

    mymarks = request.POST.get('marks',None)
    myRemarks = request.POST.get('Remarks',None)
    print(mymarks)
    print(myRemarks)

    if mymarks == None and myRemarks == None:
        print("Nothing performed..!")
    else:
        assdetail = AssignmentDetails.objects.filter(id=pk).update(Remarks=myRemarks,Scored=mymarks)
        assdetail = AssignmentDetails.objects.filter(id=pk).first()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'teacher':tch,'ass':assdetail}
    return render(request,'teachers/ViewStdAssign.html',context)


def SeeAssignmentDetail(request,pk):

    user1 = request.user
    st  = Student.objects.filter(id=user1.id).first()
    ass1 = Assignments.objects.filter(id=pk).first()

    mysubDet = request.POST.get('description')
    myfiles = request.FILES.get('myfile')

    print(mysubDet)
    print(myfiles)

    assdetail1 = ""
    if mysubDet == None and myfiles == None:
        print("Nothing performed..!")    

    elif AssignmentDetails.objects.filter(Assignment=ass1,student=st).first():
        assdetail1 = AssignmentDetails.objects.filter(Assignment=ass1,student=st).first()
        assdetail1.Sub_Details = mysubDet
        assdetail1.Submission = myfiles
        assdetail1.save()
        print("Modefification Done...!!")

    elif ass1.DoesNotExist:
        assdetail = AssignmentDetails.objects.create(Assignment=ass1,student=st,Submission=myfiles,Sub_Details=mysubDet,status="Submitted")
        ass1.AssignDetails.add(assdetail)
        print("Created...!!")

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    if AssignmentDetails.objects.filter(Assignment=ass1,student=st).first():
        context = {'base_template':base_template,'ass':ass1,'ass1':assdetail1}
    else:
        context = {'base_template':base_template,'ass':ass1}
        
    return render(request,'students/SeeAssignDetails.html',context)

def UpdateStdAssignment(request,pk):

    user1 = request.user
    st  = Student.objects.filter(id=user1.id).first()
    ass1 = AssignmentDetails.objects.filter(id=pk).first()

    mysubDet1 =  ass1.Sub_Details
    myfiles1 = ass1.Submission
    print(mysubDet1)

    mysubDet = request.POST.get('description',mysubDet1)
    myfiles = request.FILES.get('myfile',myfiles1)

    # myid =0
    # for asg in ass2:
    #     if asg.AssignDetails == ass1:
    #         print("Yes Found it")
    #         myid = asg.id

    myid = ass1.Assignment.id
    print(myid)

    assdetail = AssignmentDetails.objects.update(student=st,Submission=myfiles,Sub_Details=mysubDet,status="Submitted")
    
    print(mysubDet)
    print(myfiles)
    print(myid)

    ass1.Submission = myfiles
    ass1.Sub_Details = mysubDet
    print("Created...!!")

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'
        
    return redirect('SeeAssignmentDetail',myid)

def TchQuiz(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    q1 = Quiz.objects.filter(teacher=t,Course=crs)

    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'t':t,'s':pk1,"q":q1}
    return render(request,'teachers/TchQuiz.html',context)

def ViewStdQuiz(request,pk,pk1):

    user1 = request.user
    t  = Student.objects.filter(id=user1.id).first()
    cs = Course.objects.filter(id=pk).first()
    q1 = Quiz.objects.filter(Course=cs,Section=t.Section)

    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,'s':pk1,"q":q1,"cs":cs}
    return render(request,'students/ViewStdQuiz.html',context)

def StartQuiz(request,pk):

    user1 = request.user
    t  = Student.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()
    nextBtn = 1
    myAns = request.POST.get('opt',None)

    num = 0
    for qs in q1.QuestionAns.all():
        print(qs.question)
        num += 1

    print("You checked " + str(myAns))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,"q":q1,"nextBtn":nextBtn,'lent':num}
    return render(request,'students/StartQuiz.html',context)

def NextQuestion(request,pk,pk1):

    user1 = request.user
    t  = Student.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()
    nextBtn = int(pk1)
    print(pk1)
    myAns = request.POST.get('opt',None)

    num = 0
    for qs in q1.QuestionAns.all():
        print(qs.question)
        num += 1

    print("You checked " + str(myAns) )

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,"q":q1,"nextBtn":nextBtn,'lent':num}
    return render(request,'students/StartQuiz.html',context)

def AnsTheQuestion(request,pk,pk1,pk2):

    user1 = request.user
    t  = Student.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()
    qa1 = QuestionAnswer.objects.filter(id=pk2).first()
    myAns = request.POST.get('opt',None)
    print("You checked " + str(myAns))

    num = 0
    for qs in q1.QuestionAns.all():
        print(qs.question)
        num += 1

    if QuizDetails.objects.filter(Quiz=q1,student=t):
        qs1 = QuizDetails.objects.filter(Quiz=q1,student=t).first()
        print("Already Created..!!")
    else:
        qs1 = QuizDetails.objects.create(Quiz=q1,student=t)
        q1.QuizDetail.add(qs1)
        print("Object Created..!!")

    if Answer.objects.filter(quizDetail=qs1,Question=qa1):
        ans1 = Answer.objects.filter(quizDetail=qs1,Question=qa1).first()
        ans1.Answers=myAns
        qs1.Ans.add(ans1)
        print("Modefied..with " + str(ans1.Answers))
    else:
        ans1 = Answer.objects.create(quizDetail=qs1,Answers=myAns,Question=qa1)
        print("Answer Created..!!")

    nextBtn = int(pk1) + 1
    print(nextBtn)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    if nextBtn <= num:
        context = {'base_template':base_template,'t':t,"q":q1,"nextBtn":nextBtn,'lent':num}
        return render(request,'students/StartQuiz.html',context)
    elif nextBtn > num:
        qs1.status = "Submitted"
        qs1.save()
        return redirect('ViewStdQuiz',q1.Course.id,q1.Section)

def OpenReviewToQuiz(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()

    print("Section is --> " + str(pk1))

    q1.Review = "Open"
    q1.save()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    return redirect('ViewTchQuiz',q1.id,q1.Section)


def ViewTchQuiz(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()

    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,'s':pk1,"q":q1}
    return render(request,'teachers/ViewTchQuiz.html',context)

def ShowStdQuiz(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()
    std = Student.objects.filter(id=pk1).first()
    qz = QuizDetails.objects.filter(Quiz=q1,student=std).first()
    ans = Answer.objects.filter(quizDetail=qz)
    score = 0
    for qs in q1.QuestionAns.all():

        for a in ans.all():

            if a.Question == qs:
                print("New Question")

                for qs1 in qs.MCQAns.all():

                    if qs1.Correct_Ans == "Yes" and a.Answers == qs1.Answers:
                        print("You Ans was Correct " + str(a.Answers))
                        score += qs.Marks
                    elif a.Answers == qs1.Answers:
                        print("Your Wrong Ans were " + str(a.Answers))
                    elif qs1.Correct_Ans == "Yes":
                        print("Correct Ans were " + str(qs1.Answers))
                    else:
                        print("Normal Ans were " + str(qs1.Answers))

    qz.Scored = score
    qz.save()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,"q":q1,'std':std,'qd':qz,'ans':ans,'score':score}
    return render(request,'teachers/ShowStdQuiz.html',context)

def UploadQuiz(request,pk,pk1):

    user1 = request.user
    t = Teacher.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()
    q1.upload = "Yes"
    q1.save()

    print("This is upload -- > " + str(q1.upload))
    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    return redirect('ViewTchQuiz',q1.id,pk1)

def AddQuestToQuiz(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    q1 = Quiz.objects.filter(id=pk).first()

    myquest = request.POST.get('question',None)
    Mymarks = request.POST.get('marks',None)

    if myquest == None:
        print("Nothing Performed..!!!")
    else:
        qs = QuestionAnswer.objects.create(Quiz=q1,question=myquest,Marks=Mymarks)
        q1.QuestionAns.add(qs)

    print("Section is --> " + str(pk1))

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,'s':pk1,"q":q1}
    return render(request,'teachers/AddQuestToQuiz.html',context)

def AddMCQToQuiz(request,pk):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    q1 = QuestionAnswer.objects.filter(id=pk).first()

    myOpt = request.POST.get('Opt',None)
    myOpt1 = request.POST.get('Opt1',None)
    print("My Option is = "+str(myOpt))
    print("My Option is = "+str(myOpt1))

    if myOpt == None:
        print("Nothing Performed..!!!")
    else:
        qs = MCQANSWERS.objects.create(QuesAns=q1,Answers=myOpt,Correct_Ans=myOpt1)
        q1.MCQAns.add(qs)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'base_template':base_template,'t':t,"q":q1}
    return render(request,'teachers/AddMCQToQuiz.html',context)

def CreateQuiz(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    print("Section is --> " + str(pk1))

    if request.method == "POST":

        Description = request.POST.get('desc', False)
        mytitle = request.POST.get('title', False)
        myfiles = request.FILES.get('myfiles')
        myDate = request.POST.get('lastDate', "1111-11-11")
        myTime = request.POST.get('EndTime', "11:00 PM")
        mymarks = request.POST.get('marks', False)

        print(Description)
        print(myDate)

        if mytitle is False:
            pass
        else:
            quiz1 = Quiz.objects.create(teacher=t,Course=crs,Section=pk1,description=Description,title=mytitle,end_Date=myDate,end_Time=myTime,Total_Marks=mymarks,upload='No')

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'t':t,'s':pk1}
    return render(request,'teachers/CreateQuiz.html',context)


def CreateAssignments(request,pk,pk1):

    user1 = request.user
    t  = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    print("Section is --> " + str(pk1))

    if request.method == "POST":

        ass = request.POST.get('Assignment', False)
        mytitle = request.POST.get('title', False)
        myfiles = request.FILES.get('myfiles')
        myDate = request.POST.get('lastDate', "1111-11-11")
        myTime = request.POST.get('EndTime', "11:00 PM")
        mymarks = request.POST.get('marks', False)

        print(ass)
        print(myDate)

        if ass is False:
            pass
        else:
            ass1 = Assignments.objects.create(teacher=t,Course=crs,Section=pk1,description=ass,title=mytitle,files=myfiles,end_Date=str(myDate),end_Time=str(myTime),Total_Marks=mymarks)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'cs':crs,'base_template':base_template,'t':t,'s':pk1}
    return render(request,'teachers/TeacherAssignments.html',context)


def StudentAttendencePre(request,pk,pk1):

    stds = Student.objects.filter(id=pk).first()

    p_url = request.META['HTTP_REFERER']
    print(str(p_url) + " Url is this")
    list2 = p_url[-15:-13]
    print(str(list2) + " these are course id")

    p_url1 = p_url.split('/')[1]
    print(p_url1)

    Secs = p_url[-12:-11]
    print(str(Secs) + " these are Section")

    cr = Course.objects.filter(id=list2).first()
    c_N = cr.Course_Name
    
#    m = request.POST.get('sections')
    print("STudent  is present --> " + str(stds))
    print("LIST2--->" + str(list2))
    print('Sections are ' + str(pk1))
    print('Course is ' + str(c_N))
#    print('Pk1 = ' + str(pk1))

    add_array = []
    
    std = Student.objects.all()

    for s in std:
        if s.Section == Secs:
            for cs in s.Courses.all():
                if cs == cr:
                #    print(str(s.name) + 'is enrolled in ' + str(cs.Course_Name))
                    add_array.append(s)

    Att = Attendence.objects.filter(Course=cr).first()

    for stnd in Attendence.objects.filter(Course=cr):
        stnd.student.add(stds)
        print("Added")
    
    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    return redirect('TeachersStudentList1',list2,Secs)


def StudentAttendenceAbs(request,pk,pk1):

    stds = Student.objects.filter(id=pk).first()

    p_url = request.META['HTTP_REFERER']
    print(str(p_url) + " Url is this")
    list2 = p_url[-15:-13]
    print(str(list2) + " these are course id")
    
    Secs = p_url[-13:-12]
    print(str(Secs) + " these are Section")

    cr = Course.objects.filter(id=list2).first()
    print(cr.Course_Name)
    c_N = cr.Course_Name
    
    print("STudent  is present --> " + str(stds))
    print("LIST2--->" + str(list2))
    print('Sections are ' + str(pk1))
    print('Course is ' + str(c_N))


    add_array = []
    
    std = Student.objects.all()

    for s in std:
        if s.Section == Secs:
            for cs in s.Courses.all():
                if cs == cr:
                    add_array.append(s)

    Att = Attendence.objects.filter(Course=cr).first()

    for stnd in Attendence.objects.filter(Course=cr):
        stnd.student.remove(stds)
        print("Removed")

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    return redirect('TeachersStudentList1',list2,Secs)


def CreateAttendence(request,pk,pk1):

    add_array = []

    crs = Course.objects.filter(id=pk).first()
    Att = Attendence.objects.filter(Course=crs).first()

    print('Section is this ->' + str(pk1))

    std = Student.objects.all()

    for s in std:
        if s.Section == pk1:
            for cs in s.Courses.all():
                if cs == crs:
                    add_array.append(s)

    for stds in add_array:
        print(stds.name)

    now = datetime.datetime.now()
    Today = now.strftime("%A") 
    now1 = str(now)
    now2 = now1.split(" ")[1]
    # print(now2)

    # print(datetime.date.today())
    dt = datetime.date.today()
    Today1 = now.strftime("%I:%M%p")
    # print(Today1)

    user1 = request.user
    mytch = Teacher.objects.filter(id=user1.id).first()
    TD = TimetableDetails.objects.all()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std_all':add_array,'base_template':base_template,'Att':Att,'mytch':mytch,"TD":TD,'Tnow':Today1,"Today":Today,'s':pk1,'dates':dt}
    return render(request,'teachers/CreateAttendence.html',context)


def TeachersStudentList1(request,pk,pk1,pk2):

    add_array = []

    user1 = request.user
    mytch = Teacher.objects.filter(id=user1.id).first()
    crs = Course.objects.filter(id=pk).first()
    Att = Attendence.objects.filter(Course=crs).first()
    TD = TimetableDetails.objects.all()
    print(str(pk) + " Actual course id")

    urls = request.get_full_path()
    print(urls)
    list2 = urls[-15:-13]
    print(str(list2) + " these are course id")


    now = datetime.datetime.now()
    Today = now.strftime("%A") 
    now1 = str(now)
    now2 = now1.split(" ")[1]
    print(now2)
    print('Class time is this ->' + str(pk2))
    
    p1 = pk2.split('-')[0]
    p2 = pk2.split('-')[1]
    print(p1)
    print(p2)

    if len(p1) == 3:
        tp = p1[:1] + ':' + p1[1:] + ':' + '00'
    elif len(p1) == 4:
        tp = p1[:2] + ':' + p1[1:] + ':' + '00'

    print(tp)

#    print(datetime.date.today())
    dt = datetime.date.today()

    if Attendence.objects.filter(Course=crs,Time=tp,teacher=mytch,Section=pk1,Day=Today,Date=dt).exists():
        print("Already exists")
    else:
        Attnd = Attendence.objects.create(Course=crs,Time=tp,Day=Today,Section=pk1,Date=dt)
        print("Attendence Object Created..!!!!")
        std = Student.objects.all()

        Attnd.teacher.add(mytch)

        for s in std:
            if s.Section == pk1:
                for cs in s.Courses.all():
                    if cs == crs:
                        Attnd.student.add(s)

    print('Section is this ->' + str(pk1))

    std = Student.objects.all()

    for s in std:
        if s.Section == pk1:
            for cs in s.Courses.all():
                if cs == crs:
                    add_array.append(s)

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std_all':add_array,'base_template':base_template,'Att':Att,'mytch':mytch,"TD":TD,"Today":Today}
    return render(request,'teachers/teachers_students_list1.html',context)


def TeachersStudentList(request,pk,pk1=""):

    add_array = []

    crs = Course.objects.filter(id=pk).first()
    m = request.POST.get('sections')

    # p_url = request.META.get('HTTP_REFERER')
    # if "StudentAttendencePre" in p_url:
    #     pk1 = 
    # print(p_url)

    print('Pk2 is ->' + str(pk1))

    std = Student.objects.all()

    for s in std:
        if s.Section == m:
            for cs in s.Courses.all():
                if cs == crs:
                # print(str(s.name) + 'is enrolled in ' + str(cs.Course_Name))
                    add_array.append(s)

    
    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std_all':add_array,'base_template':base_template}
    return render(request,'teachers/teachers_students_list.html',context)


def TeacherCourses(request,pk):

    t = Teacher.objects.filter(id=pk).first()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    std = Student.objects.all()

    sec_array = []

    for st in std:
        for sc in st.Courses.all():
            for tc in t.Courses.all():
                if sc == tc:
                    sec_array.append(st.Section)

    print(list(set(sec_array)))
    my_sec = list(set(sec_array))

    context = {'base_template':base_template,'t':t,'sec':my_sec}

    return render(request,'teachers/teacher_courses.html',context)


# ADMIN ACCOUNT


# FUNCTIONS FOR STUDENT


def AddStudent(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        Name = request.POST['Name']
        Photo = request.FILES['photo']
        DOB = request.POST['Date_of_birth']
        guardianMobile = request.POST['guardian_Mobile']
        MobileNo = request.POST['mobileNo']
        RegNo = request.POST['RegNo']

        if password == password1:

            if Student.objects.filter(username=username).exists():
                return redirect('addstd')

            elif Student.objects.filter(email=email).exists():
                return redirect('addstd')

            user1 = Student.objects.create_user(username=username,email=email,
                    password=password,name=Name,photo=Photo,date_of_birth=DOB,RegistrationNo=RegNo,
                    mobile=MobileNo,guardian_mobile=guardianMobile,user_type = 1)

            user1.save()

            return redirect('Dashboard')

        else:
            return redirect('addstd')

    else:

        context = locals()

        return render(request,'students/addstudent.html',context)

def StudentList(request):

    std = Student.objects.all()
    
    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    for s in std:
        print(s)

    context = {'std_all':std,'base_template':base_template}
    return render(request,'students/students_list.html',context)

def ViewStudent(request,pk):

    std = Student.objects.filter(id=pk).first()
    t  = Teacher.objects.all()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'std':std,'t':t,'base_template':base_template}
    return render(request,'students/student_details.html',context)


def StudentResult(request):

    context = locals()
    return render(request,'students/result_in_detail.html',context)

def AddDepStd(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    dList = Department.objects.all()
    StdList = Student.objects.filter(id=list2).first()

    print(list2)

    f_array = []
    add_array = []

    for d in dList:
        if d == StdList.Department:
            f_array.append(d)


    for d in dList:
        add_array.append(d)

    odd_word = list((Counter(add_array) - Counter(f_array)).elements())

    dep = Department.objects.all()
    context = {'departments':dep,'p_url':list2,'add_dep':odd_word,'rem_dep':f_array}

    return render(request,'admin_tools/addDepStd.html',context)


def AssignDepStd(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    dep = Department.objects.filter(id=pk).first()

    StdList = Student.objects.filter(id=list2).first()

    StdList.Department = dep
    StdList.save()

    return redirect('AddDepStd',list2)

def ShowCourseStd(request,pk):

    courseList = Student.objects.filter(id=pk).first()
    print(courseList.id)

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    urls_id = request.get_full_path

    t  = Teacher.objects.all()
    cLists = Course.objects.all()

    for t1 in t:
        for c1 in t1.Courses.all():
            for cl in cLists:
                if c1 == cl:
                    print(str(t1) + ' teaches ' + str(c1.Course_Name))

    c = courseList.Courses
    courses1 = Course.objects.all()
    arry = []
    arry1 = []

    for items in courses1:
        arry1.append(items)

    for c2 in courses1:
        for c1 in c.all():
            if c1 != c2:
                arry.append(c1)
            else:
                pass

    mycourses = list(dict.fromkeys(arry))

    odd_word = list((Counter(arry1) - Counter(mycourses)).elements())

    context = {'t_course':courseList,'add_courses':odd_word,'p_url':list2,'t':t}

    return render(request,'course/course_assign_to_student_list.html',context)


def RemoveStdCourses(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    c = Course.objects.filter(id=pk).first()
    std = Student.objects.filter(id=list2).first()

    if Student.objects.filter(id=list2,Courses=c).exists():
        std.Courses.remove(c)
    else:
        pass

    return redirect('ShowCourseStd',list2)

def AssignCourseStd(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    c = Course.objects.filter(id=pk).first()
    std = Student.objects.filter(id=list2).first()

    if Student.objects.filter(id=list2,Courses=c).exists():
        print('FACULTY ALREADY EXISTS')
    else:
        std.Courses.add(c)

    return redirect('ShowCourseStd',list2)



# FUNCTIONS FOR TEACHER 


def AddTeacher(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        name = request.POST['Name']
        Photo = request.FILES['photo']
        DOB = request.POST['Date_of_birth']
        Designation = request.POST['Designation']
        MobileNo = request.POST['mobileNo']


        if password == password1:

            if Teacher.objects.filter(username=username).exists():
                return redirect('Add_Teacher')

            elif Teacher.objects.filter(email=email).exists():
                return redirect('Add_Teacher')

            user1 = Teacher.objects.create_user(username=username,email=email,
                    password=password,Name=name,photo=Photo,Date_of_birth=DOB,Designation=Designation,
                    mobileNo=MobileNo,user_type = 2)

            user1.save()

            return redirect('Dashboard')

        else:
            return redirect('Add_Teacher')

    else:

        context = locals()
        return render(request,'teachers/add_teacher.html',context)

def AllTeachers(request):

    allTeacher = Teacher.objects.all()

    context = {'teachers':allTeacher}

    return render(request,'teachers/teacher_list.html',context)


def DetailTeacher(request,pk):

    teachers = Teacher.objects.filter(id=pk).first()

    if request.user.user_type == 1:
        base_template = 'SDashboard.html'

    elif request.user.user_type == 2:
        base_template = 'TDashboard.html'

    elif request.user.is_superuser:
        base_template = 'dashboard.html'

    context = {'teacher':teachers, 'base_template':base_template}

    return render(request,'teachers/teacher_detail.html',context)


def CreateTeacherDesignation(request):

    context = locals()
    return render(request,'teachers/designation_create.html',context)


def CourseList(request):

    courseList = Course.objects.all()
    context = {'all_course':courseList}

    return render(request,'course/course_list.html',context)


def ShowCourses(request):

    courseList = Course.objects.all()
    context = {'all_course':courseList}

    return render(request,'course/show_course_list.html',context)


def Add_Course(request):

    courseForm = CourseForm(request.POST)

    if courseForm.is_valid():
        courseForm.save()
        cID = courseForm.cleaned_data['Course_Id']
        c1 = Course.objects.filter(Course_Id=cID).first()
        print("Course id is --> " + str(cID))
        return  redirect('courseList')

    context = {'form':courseForm}

    return render(request,'course/add_course.html',context)

def AddCourseDep(request,pk):

    cor = Course.objects.filter(id=pk).first()
    dep = Department.objects.all()

    add_c = []
    rem_c = []

    for d in dep:
        if cor.Department == d:
            print(d.Dept_Name)
            rem_c.append(d)

    for d in dep:
        add_c.append(d)

    odd_word = list((Counter(add_c) - Counter(rem_c)).elements())

    context = {'dep':dep,'rem_dep':rem_c,'add_dep':odd_word}

    return render(request,'admin_tools/addCourseDep.html',context)


def SelectCourseDep(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    dep = Department.objects.filter(id=pk).first()
    cor = Course.objects.filter(id=list2).first()

    cor.Department = dep
    cor.save()

    return redirect('AddCourseDep',list2)


def courseSection(request):

    context = locals()
    return render(request,'course/add_section.html',context)

def courseAttendence(request):

    context = locals()
    return render(request,'course/add_course_attendance.html',context)

def ShowCourseTeach(request,pk):

    courseList = Teacher.objects.filter(id=pk).first()
    print(courseList.id)

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    urls_id = request.get_full_path

    c = courseList.Courses
    courses1 = Course.objects.all()
    arry = []
    arry1 = []

    for items in courses1:
        arry1.append(items)

    for c2 in courses1:
        for c1 in c.all():
            if c1 != c2:
                arry.append(c1)
            else:
                pass

    mycourses = list(dict.fromkeys(arry))

    odd_word = list((Counter(arry1) - Counter(mycourses)).elements())

    context = {'t_course':courseList,'add_courses':odd_word,'p_url':list2}

    return render(request,'course/course_assign_to_teacher_list.html',context)


def RemoveAssignedCourseTeach(request,pk):

    courseList1 = Course.objects.filter(id=pk).first()
    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    courseList = Teacher.objects.filter(id=list2).first()

#    atts = Attendence.objects.create(Course=courseList1,teacher=courseList)
    if Attendence.objects.filter(Course=courseList1,teacher=courseList):
        Attendence.objects.filter(Course=courseList1,teacher=courseList).delete()
#        atts.teacher.remove(courseList)
    else:
        pass

    for c in courseList.Courses.all():
        if c == courseList1:
            courseList.Courses.remove(courseList1)
            print('THIS IS COURSE IS DELETED')
        else:
            pass

    return redirect('showCourseTeach',list2)


def AssignDepTeach(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    depList1 = Department.objects.filter(id=pk).first()
    TList = Teacher.objects.filter(id=list2).first()

    TList.Department = depList1
    TList.save()

    return redirect('AddDepTeach',list2)


def AddDepTeach(request,pk):

    depList1 = Department.objects.filter(id=pk).first()
    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    dList = Department.objects.all()
    TList = Teacher.objects.filter(id=list2).first()

    f_array = []
    add_array = []

    for d in dList:
        if d == TList.Department:
            f_array.append(d)

    for d in dList:
        add_array.append(d)

    odd_word = list((Counter(add_array) - Counter(f_array)).elements())

    dep = Department.objects.all()
    context = {'departments':dep,'p_url':list2,'add_dep':odd_word,'rem_dep':f_array}

    return render(request,'admin_tools/addDepTeach.html',context)


def AssignCourseTeach(request,pk):

    courseList1 = Course.objects.filter(id=pk).first()
    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    courseList = Teacher.objects.filter(id=list2).first()
    Stdns = Student.objects.all()

    if Attendence.objects.filter(Course=courseList1,teacher=courseList):
        print("Attendence Object Exists")
    else:
        atts = Attendence.objects.create(Course=courseList1)
        atts.teacher.add(courseList)
        print("Attendence Object Created..!!!")

    for sts in Stdns:
        for sts1 in sts.Courses.all():
            if sts1 == courseList1:
                atndnce = Attendence.objects.filter(Course=courseList1,teacher=courseList).first()
                atndnce.student.add(sts)
                print('STUDENT added to this attendence')
            else:
                pass

    if Teacher.objects.filter(id=list2,Courses=courseList1).exists():
        print('THIS IS COURSE ALREADY EXISTS')
        pass
    else:
        courseList.Courses.add(courseList1)
        print('THIS IS COURSE IS ADDED')

    return redirect('showCourseTeach',list2)

def Departments(request):

    dep = Department.objects.all()
    context = {'departments':dep}

    return render(request,'admin_tools/departments.html',context)

def ChangeDepartment(request):

    dep = Department.objects.all()
    context = {'departments':dep}

    return render(request,'admin_tools/Changedepartments.html',context)


def ChangeDepFaculty(request,pk):

    dep = Department.objects.filter(id=pk).first()
    hod = Teacher.objects.all()

    f_array = []
    add_array = []

    for t in hod:
        for d in dep.Faculty.all():
            if d == t:
                f_array.append(d)

    for t in hod:
        add_array.append(t)

    odd_word = list((Counter(add_array) - Counter(f_array)).elements())

    for items in odd_word:
        print(items)

    context = {'dep':dep,'add_f':odd_word,'remove_f':f_array}

    return render(request,'admin_tools/Faculty_list.html',context)

def RemoveFaculty(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    faculty = Teacher.objects.filter(id=pk).first()
    dep = Department.objects.filter(id=list2).first()

    if Department.objects.filter(id=list2,Faculty=faculty).exists():
        dep.Faculty.remove(faculty)
    else:
        pass

    return redirect('ChangeDepFaculty',list2)

def SelectDepFaculty(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    faculty = Teacher.objects.filter(id=pk).first()
    dep = Department.objects.filter(id=list2).first()

    if Department.objects.filter(id=list2,Faculty=faculty).exists():
        print('FACULTY ALREADY EXISTS')
    else:
        dep.Faculty.add(faculty)

    return redirect('ChangeDepFaculty',list2)


def ChangeDepHOD(request,pk):

    dep = Department.objects.filter(id=pk).first()
    hod = Teacher.objects.all()

    add_c = []
    rem_c = []
    d = dep.HOD
    for t in hod:
        if d == t:
            print(d.Name)
            rem_c.append(d)

    for t in hod:
        add_c.append(t)

    odd_word = list((Counter(add_c) - Counter(rem_c)).elements())

    context = {'dep':dep,'teachers':rem_c,'add_hod':odd_word}

    return render(request,'admin_tools/HOD_list.html',context)


def SelectDepHOD(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    hod = Teacher.objects.filter(id=pk).first()
    dep = Department.objects.filter(id=list2).first()

    dep.HOD = hod
    dep.save()

    return redirect('ChangeDepHOD',list2)


def ChangeDepCourses(request,pk):

    dep = Department.objects.filter(id=pk).first()
    c = Course.objects.all()

    add_c = []
    rem_c = []

    for courses in c:
        for d in dep.courses.all():
            if d == courses:
                print(d.Course_Name)
                rem_c.append(d)

    for courses in c:
        add_c.append(courses)

    odd_word = list((Counter(add_c) - Counter(rem_c)).elements())

    context = {'dep':dep,'courses':rem_c,'add_c':odd_word}

    return render(request,'admin_tools/DepCourse_list.html',context)

def SelectDepCourses(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    c = Course.objects.filter(id=pk).first()
    dep = Department.objects.filter(id=list2).first()

    if Department.objects.filter(id=list2,courses=c).exists():
        pass
    else:
        dep.courses.add(c)

    return redirect('ChangeDepCourses',list2)

def RemoveDepCourses(request,pk):

    p_url = request.META.get('HTTP_REFERER')
    list2 = p_url[-2:]

    c = Course.objects.filter(id=pk).first()
    dep = Department.objects.filter(id=list2).first()

    if Department.objects.filter(id=list2,courses=c).exists():
        dep.courses.remove(c)
    else:
        pass

    return redirect('ChangeDepCourses',list2)

def AddDepartments(request):

    DeptForm = DepartmentForm(request.POST)

    if DeptForm.is_valid():
        DeptForm.save()
        return  redirect('Departments')

    context = {'form':DeptForm}
    
    return render(request,'admin_tools/addDepartments.html',context)

def Academic_Session(request):

    context = locals()
    return render(request,'admin_tools/academic_sessions.html',context)

def AllSemester(request):

    context = locals()
    return render(request,'admin_tools/all_semester.html',context)
