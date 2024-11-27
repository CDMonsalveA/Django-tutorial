from django.db.models import F
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Without using generic views

# # Without using shortcut
# # from django.template import loader
# # def index(request):
# #     latest_question_list = Question.objects.order_by("-pub_date")[:5]
# #     template = loader.get_template("polls/index.html")
# #     context = {"latest_question_list": latest_question_list}
# #     return HttpResponse(template.render(context, request))

# # Using shortcut
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# # Without using get_object_or_404 shortcut
# # def detail(request, question_id):
# #   try:
# #       question = Question.objects.get(pk=question_id)
# #   except Question.DoesNotExist:
# #       raise Http404("Question does not exist.")
# #   return render(request, "polls/detail.html", {"question": question})

# # Using get_object_or_404 shortcut
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

# # Basic results view
# # def results(request, question_id):
# #     response = "You're looking at the results of question %s."
# #     return HttpResponse(response % question_id)

# # Usefull results view
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# # Dummy vote view
# # def vote(request, question_id):
# #     return HttpResponse("You're voting on question %s." % question_id)

# Using generic views

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# Usefull vote view
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))