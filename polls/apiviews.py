import subprocess, datetime
from datetime import timezone
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Question, Choice
from .serializers import QuestionListPageSerializer, QuestionDetailPageSerializer, ChoiceSerializer, VoteSerializer, QuestionResultPageSerializer


@api_view(['GET', 'POST'])
def questions_view(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def multiple_questions_view(request):
    serializer = QuestionListPageSerializer(many=True, data=request.data)
    if serializer.is_valid():
        questions = serializer.save()
        return Response(QuestionDetailPageSerializer(questions, many=True).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def vote_view(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
            choice.votes += 1
            choice.save()
            return Response("Voted")
    except:
        raise serializer.ValidationError({
                "voteError": "No choice exists at provided id"
            })


@api_view(['GET'])
def question_result_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)

@api_view(['GET'])
def uptime_view(request):
    output = subprocess.check_output(['sh', '/app/time.sh'])
    output = output.split()
    dates = output[0].decode().split('-')
    times = output[1].decode().split(':')
    year = int(dates[0])
    month = int(dates[1])
    day = int(dates[2])
    hour = int(times[0])
    mins = int(times[1])
    sec = int(times[2])
    d = datetime.datetime(year, month, day, hour, mins, sec)
    day = int(output[3].decode()) * 24
    hour = int(output[5].decode()) + day
    mins = int(output[7].decode())
    output = "PT"+str(hour)+":"+str(mins)
    return Response({"started": d.now(timezone.utc).astimezone().isoformat(),
        "runtime": output}, status=status.HTTP_200_OK)