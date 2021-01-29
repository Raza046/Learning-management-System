from django import forms
from dashboard.models import Teacher,Student,Course,Department,Announcements,Assignments
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (Layout, Field,
                                 ButtonHolder, Submit)

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course

        fields = [
            'Course_Name',
            'Course_Id',
            'credit_hours'
        ]

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignments

        fields = [
            'files',
            'end_Date',
            'end_Time'
        ]

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department

        fields = [
            'Dept_Name',
        ]

class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcements

        fields = [
            'texts',
        ]

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher

        fields = [
            'Department',
        ]

