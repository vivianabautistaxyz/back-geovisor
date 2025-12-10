from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import *





class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            'options': {'required': False},
            'typeChoice': {'required': False, 'allow_null': True}

        }

class SectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        depth = 1


class SectionDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = '__all__'
        depth = 1

    def get_questions(self, obj):
        # Get questions through the SectionQuestion model
        section_questions = SectionQuestion.objects.filter(section=obj)
        questions = Question.objects.filter(sectionquestion__section=obj)
        return QuestionSerializer(questions, many=True).data

        
class SectionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionQuestion
        fields = ['id', 'section', 'question']


class TypeChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeChoice
        fields = '__all__'
        depth = 1


class FormSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()
    
    class Meta:
        model = Form
        fields = '__all__'
        depth = 1

    def get_sections(self, obj):
        sections = []
        form_sections = FormSection.objects.filter(form=obj)
        for form_section in form_sections:
            sections.append(SectionListSerializer(form_section.section).data)
        return sections
