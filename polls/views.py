from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

class FormSectionView(APIView):
    def post(self, request, form_id, section_id):
        """
        Add a section to a form
        """
        try:
            form = Form.objects.get(id=form_id)
            section = Section.objects.get(id=section_id)
            
            # Check if the section is already linked to the form
            if FormSection.objects.filter(form=form, section=section).exists():
                return Response({"error": "Section is already linked to this form"}, 
                              status=status.HTTP_200_OK)
            
            # Create the link between form and section
            form_section = FormSection.objects.create(form=form, section=section)
            return Response({"message": "Section added successfully"}, 
                          status=status.HTTP_201_CREATED)
            
        except Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, form_id, section_id):
        """
        Remove a section from a form
        """
        try:
            form = Form.objects.get(id=form_id)
            section = Section.objects.get(id=section_id)
            
            # Find and delete the link between form and section
            form_section = FormSection.objects.get(form=form, section=section)
            form_section.delete()
            return Response({"message": "Section removed successfully"}, 
                          status=status.HTTP_200_OK)
            
        except Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)
        except FormSection.DoesNotExist:
            return Response({"error": "Section is not linked to this form"}, 
                          status=status.HTTP_400_BAD_REQUEST)

class FormView(APIView):
    def get(self, request, pk=None, search=None):
        queryset = Form.objects.all()
        if pk:
            try:
                form = Form.objects.get(id=pk)
                serializer = FormSerializer(form)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Form.DoesNotExist:
                return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Prefetch related sections to optimize query performance
        queryset = queryset.prefetch_related('formsection_set__section')
        
        serializer = FormSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, search=None):
        data = request.data
        # Suponiendo que 'name' es el campo único para identificar el formulario
        form, created = Form.objects.update_or_create(
            name=data.get('name'),
            defaults=data
        )
        serializer = FormSerializer(form)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    def put(self, request, pk):
        data = request.data
        form = Form.objects.get(pk=pk)
        form.name = data.get('name')
        form.description = data.get('description')
        form.save()
        serializer = FormSerializer(form)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SectionView(APIView):
    def get(self, request, pk=None, search=None):
        if pk:
            try:
                section = Section.objects.get(id=pk)
                serializer = SectionDetailSerializer(section)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Section.DoesNotExist:
                return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if search:
            sections = Section.objects.filter(name__icontains=search)
        else:
            sections = Section.objects.all()
        serializer = SectionListSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, search=None):
        data = request.data
        # Suponiendo que 'name' es el campo único para identificar la sección
        section, created = Section.objects.update_or_create(
            name=data.get('name'),
            defaults=data
        )
        serializer = SectionListSerializer(section)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    def put(self, request, pk):
        try:
            section = Section.objects.get(id=pk)
            data = request.data
           
            # Actualizar los campos de la sección
            section.name = data.get('name', section.name)
            section.description = data.get('description', section.description)
            
            # Guardar los cambios
            section.save()
            
            # Serializar y retornar la sección actualizada
            serializer = SectionDetailSerializer(section)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class QuestionView(APIView):
    def get(self, request, search=None):
        if search:
            questions = Question.objects.filter(question__icontains=search)
        else:
            questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, search=None):
        data = request.data
        
        # Obtener el typeChoice del request
        type_choice_id = data.get('typeChoice')
        
        # Buscar el TypeChoice según el ID (número) o nombre (string)
        type_choice = None
        if type_choice_id:
            try:
                # Intentar buscar por ID (número)
                type_choice = TypeChoice.objects.get(id=type_choice_id)
            except (ValueError, TypeChoice.DoesNotExist):
                return Response(
                    {'error': 'TypeChoice no encontrado'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        
        # Crear o actualizar la pregunta
        question, created = Question.objects.update_or_create(
            question=data.get('question'),
            defaults={
                'question': data.get('question'),
                'options': data.get('options', ''),
                'typeChoice': type_choice
            }
        )
        
        serializer = QuestionSerializer(question)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
    

class SectionQuestionView(APIView):
    def get(self, request, section_id, question_id):
        try:
            section_question = SectionQuestion.objects.get(section_id=section_id, question_id=question_id)
            serializer = SectionQuestionSerializer(section_question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SectionQuestion.DoesNotExist:
            return Response({"error": "SectionQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, section_id, question_id):
        try:
            section = Section.objects.get(id=section_id)
            question = Question.objects.get(id=question_id)
            
            # Check if the association already exists
            if SectionQuestion.objects.filter(section=section, question=question).exists():
                return Response({"error": "This question is already associated with this section"}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Create the association
            section_question = SectionQuestion.objects.create(section=section, question=question)
            serializer = SectionQuestionSerializer(section_question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, section_id, question_id):
        try:
            section_question = SectionQuestion.objects.get(section_id=section_id, question_id=question_id)
            section_question.delete()
            return Response({"message": "Association removed successfully"}, status=status.HTTP_200_OK)
        except SectionQuestion.DoesNotExist:
            return Response({"error": "SectionQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

class QuestionTypeView(APIView):
    def get(self, request):
        question_types = TypeChoice.objects.all()
        serializer = TypeChoiceSerializer(question_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
