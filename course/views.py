# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView

from student.models import Student
from .models import Course
from quiz.models import Quiz
from keystroke.models import KeystrokeTestSession

from .forms import CourseForm

# Create your views here.
class CourseStudentStatusView(View):

  def get(self, request, *args, **kwargs):

    student_id = self.kwargs['student_id']

    if not Student.objects.filter(moodle_username = student_id).exists():
      return JsonResponse({
        "has_record": False,
        "has_picture": False
      })
    else:
      student = Student.objects.filter(moodle_username = student_id)[0]
      course_id = self.kwargs['course_id']
      course = Course.objects.filter(id = course_id)[0]
      test_type = course.keystroke_test_type

      return JsonResponse({
        "has_record": KeystrokeTestSession.objects.filter(student = student, test_type = test_type).exists(),
        "has_picture": True
      })

class DashCourse(LoginRequiredMixin, TemplateView):
  template_name = "course_index.html"


class DashCourseList(LoginRequiredMixin, TemplateView):
  template_name = "course_list.html"

  def get_context_data(self, **kwargs):
    context = super(DashCourseList, self).get_context_data(**kwargs)
    context["courses"] = Course.objects.filter(owner = self.request.user)
    return context


class DashCourseDetails(LoginRequiredMixin, TemplateView):
  template_name = "course_details.html"

  def get_context_data(self, **kwargs):
    context = super(DashCourseDetails, self).get_context_data(**kwargs)
    context["course_id"] = self.kwargs["pk"]
    context["quizzes"] = Quiz.objects.filter(course = self.kwargs["pk"])
    return context


class DashCourseAdd(LoginRequiredMixin, FormMixin, TemplateView):
  model = Course
  template_name = "course_add.html"
  form_class = CourseForm

  def get_form_kwargs(self):
    kwargs = super(DashCourseAdd, self).get_form_kwargs()
    kwargs.update({'owner': self.request.user})
    return kwargs

  def post(self , request , *args , **kwargs):
    form = self.get_form()
    if form.is_valid():
      instance = form.save(commit=False)
      instance.owner = self.request.user
      instance.save()
      return HttpResponseRedirect("/dash/course/list")
    else:
      return self.form_invalid(form)
