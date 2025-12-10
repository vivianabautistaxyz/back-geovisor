from django.urls import path
from .views import *

urlpatterns = [
    path("form/<int:pk>/", FormView.as_view()),
    path("form/<str:search>/", FormView.as_view()),
    path("form/", FormView.as_view()),
    

    path("form/<int:form_id>/section/<int:section_id>/", FormSectionView.as_view(), name='form-section'),
   
    path("section/<int:pk>/", SectionView.as_view()),
    path("section/<str:search>/", SectionView.as_view()),
    path("section/", SectionView.as_view()),

    path("question/<str:search>/", QuestionView.as_view()),
    path("question/", QuestionView.as_view()),
    path("question-type/", QuestionTypeView.as_view()),

    path("section/<int:section_id>/question/<int:question_id>/", SectionQuestionView.as_view(), name='section-question')
]
