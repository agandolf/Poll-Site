from rest_framework import serializers

from .models import Question, Choice


class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    choice_text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)


class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200, required=False)
    pub_date = serializers.DateTimeField()
    was_published_recently = serializers.BooleanField(read_only=True) # Serializer is smart enough to understand that was_published_recently is a method on Question
    choices = ChoiceSerializer(many=True, write_only=True)
    if len(str(question_text)) == 0:
        raise ValidationError({
                "questionError": "Question is required."
        })

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        if len(choices) <= 1:
            raise serializers.ValidationError({
                "choiceError": "Error: At least two choices are required."
            })
        question = Question.objects.create(**validated_data)
        for choice_dict in choices:
            choice_dict['question'] = question
            Choice.objects.create(**choice_dict)
        return question


class MultipleQuestionsCreateSerializer(serializers.Serializer):
    questions = QuestionListPageSerializer(write_only=True)


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionResultPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)
    max_voted_choice = ChoiceSerializerWithVotes(read_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(required=False)