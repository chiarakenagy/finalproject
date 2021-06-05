from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader
from .models import Question, Choice, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# view for index.html
class IndexView(View):
    def get(self, request):
        # get view - not coming from a form
        latest_question_list = Question.objects.order_by('-pub_date')[:5] #order by date pub
        template = loader.get_template('polls/index.html') #load template
        context = {
            'latest_question_list':
        latest_question_list,
            'user': request.user,
        }
        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(template.render(context, request))
    def post(self, request):
         # view from submitted form
         # set up different response wether user is logged in or not
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

        # set up system for saving questions
        if "question" in request.POST.keys():
            question = Question(
                question_text = request.POST["question"],
                pub_date = timezone.now(),
            )
            question.save()
            choice1 = Choice(
                question = question,
                choice_text = request.POST["choice1"],
            )
            choice2 = Choice(
                question = question,
                choice_text = request.POST["choice2"],
            )
            choice1.save()
            choice2.save()

        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list': latest_question_list,
            'loggedIn': loggedIn,
            'user': request.user,
        }

        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(template.render(context, request))



# class DetailView(View):
#     def get(self, request, question_id):
#         return HttpResponse("Your're looking at question %s." % question_id)

class ResultsView(View):
    def get(self, request, question_id):
        response = "Your're looking at the results of question %s."
        return HttpResponse(response % question_id)

class DetailView(View):
    #view questions and vote on them view
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk = question_id)
        try:
            choices = question.choice_set.filter(question=question)
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
                'user': request.user,
            })
        else:
            #selected_choice.votes += 1
            #selected_choice.save()
            pass

        context= { 'question': question,
                'choices': choices,


        }
        print(context)
        return render(request, "polls/detail.html", context)
    def post(self, request, question_id):
        if "pollChoices" in request.POST:
            choice = Choice.objects.get(id=int(request.POST['pollChoices']))
            question = choice.question
            choice.votes += 1
            choice.save()

            choices = Choice.objects.filter(question=question)

            context = {'choices': choices,
                        'question': question,
                        }
        return render(request, 'polls/results.html', context)
