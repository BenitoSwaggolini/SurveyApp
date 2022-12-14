from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Answer, Submission

class SurveyForm(forms.Form):
    question_1 = forms.ChoiceField(widget=forms.RadioSelect, choices=())

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        del self.fields["question_1"]
        for question in survey.question_set.all():
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            self.fields[f"question_{question.id}"] = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
            self.fields[f"question_{question.id}"].label = question.text

    def save(self):
        data = self.cleaned_data
        submission = Submission(survey=self.survey)
        submission.save()
        for question in self.survey.question_set.all():
            choice = Answer.objects.get(pk=data[f"question_{question.id}"])
            submission.answer.add(choice)

        submission.save()
        return submission


class SurveyCreateForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'



class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
