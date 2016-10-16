from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSet
from .models import Answer, Questionnaire, update_score
from .forms import AnswerForm, QuestionnaireFormMixin, AnswersInline

class GenericQuestionnaireView(CreateWithInlinesView):
    model = Questionnaire
    inlines = [AnswersInline]

    def get_form_kwargs(self):
        kwargs = super(GenericQuestionnaireView, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def forms_valid(self, form, inlines):
        response = super(GenericQuestionnaireView, self).forms_valid(form, inlines)
        messages.add_message(self.request, messages.SUCCESS, _("Thank you for your feedback!"))
        update_score(self.request, form.instance)
        return response

    def construct_inlines(self):
        inline_formsets = super(GenericQuestionnaireView, self).construct_inlines()
        questions = self.questions()
        inline_formsets[0].initial = questions
        inline_formsets[0].extra = len(questions)
        return inline_formsets

    def get_success_url(self):
        return "/"


def generic_questionnaire_view(request, initial, template, url, extra_inlines,
    questionnaire_form=QuestionnaireFormMixin, questionnaire_initial=[],
    questionnaire=Questionnaire()):

    AnswerFormSet = inlineformset_factory(
        Questionnaire,
        Answer,
        form=AnswerForm,
        can_delete=False,
        extra=len(initial)
    )
    if request.method == 'POST':
        form = questionnaire_form(request.user, request.POST,
            initial=questionnaire_initial)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            formset = AnswerFormSet(request.POST, instance=questionnaire, initial=initial)
            if formset.is_valid():
                questionnaire.save()
                form.save_m2m()
                formset.save()
                messages.add_message(request, messages.SUCCESS, _("Thank you for your feedback!"))
                update_score(request, questionnaire)
                return redirect(reverse(url))
        else:
            formset = AnswerFormSet(request.POST, instance=questionnaire, initial=initial)
    else:
        formset = AnswerFormSet(instance=questionnaire, initial=initial)
        form = questionnaire_form(request.user, initial=questionnaire_initial)


    return render(request, template, {
        'form': form,
        'answer_formset': formset,
        'questions': initial
    })
