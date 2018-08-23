from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from keystroke import views as keystroke_views
from face import views as face_views
from student import views as student_views
from quiz import views as quiz_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^students$', student_views.StudentAPIView.as_view()),
    url(r'^students/(?P<pk>\d+)/$', student_views.StudentRudView.as_view()),
    url(r'^keystroke/test/(?P<pk>\d+)/$', keystroke_views.KeystrokeTestTypeAPIView.as_view()),
    url(r'^keystroke/session/(?P<pk>\d+)/$', keystroke_views.KeystrokeTestSessionAPIView.as_view()),
    url(r'^keystroke/distance$', keystroke_views.KeystrokeTestDistanceAPIView.as_view()),
    url(r'^face/distance$', face_views.FaceDistanceAPIView.as_view()),
    url(r'^quiz/(?P<pk>\d+)/$', quiz_views.QuizInfoAPIView.as_view())
]

url = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
