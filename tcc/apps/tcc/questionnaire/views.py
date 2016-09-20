from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .models import Answer, Questionnaire, update_score
from .forms import AnswerForm, QuestionnaireForm


def generic_questionnaire_view(request, initial, template, url, questionnaire_form=QuestionnaireForm):
    questionnaire = Questionnaire()
    AnswerFormSet = inlineformset_factory(
        Questionnaire,
        Answer,
        form=AnswerForm,
        can_delete=False,
        extra=len(initial)
    )
    if request.method == 'POST':
        form = questionnaire_form(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            formset = AnswerFormSet(request.POST, instance=questionnaire, initial=initial)
            if formset.is_valid():
                questionnaire.save()
                form.save_m2m()
                formset.save()
                messages.add_message(request, messages.SUCCESS, _("Thank you for your feedback!"))
                update_score(questionnaire)
                return redirect(reverse(url))
        else:
            formset = AnswerFormSet(request.POST, instance=questionnaire, initial=initial)
    else:
        formset = AnswerFormSet(instance=questionnaire, initial=initial)
        form = questionnaire_form()


    return render(request, template, {
        'form': form,
        'answer_formset': formset,
        'questions': initial
    })
