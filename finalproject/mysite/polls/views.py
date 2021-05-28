from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader
from .models import Question, Choice, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class IndexView(View):
    def get(self, request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list':
        latest_question_list,
            'user': request.user,
        }
        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(template.render(context, request))
    def post(self, request):
        if request.POST:
            if 'inputUsername' in request.POST.keys():
                user = authenticate(username=request.POST['inputUsername'],
                    password=request.POST['inputPassword'])
                if user is not None:
                    login(request,user)
                else:
                    pass
            elif 'logout' in request.POST.keys():
                logout(request)
        loggedIn = request.user.is_authenticated

        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list': latest_question_list,
            'loggedIn': loggedIn,
            'user': request.user,
        }

        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(template.render(context, request))
        # can treat the def post differently - coming from a form - welcome message, check if user is logged in


class DetailView(View):
    def get(self, request):
        return HttpResponse("Your're looking at question %s." % question_id)

class ResultsView(View):
    def get(self, request):
        response = "Your're looking at the results of question %s."
        return HttpResponse(response % question_id)

class VotingView(View):
    def get(self, request):
        question = get_object_or_404(Question, pk = question_id)
        try:
            selected_choice = question.choice_set.get(pk = request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls / index.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
                'user': request.user,
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args =(question.id, )))
