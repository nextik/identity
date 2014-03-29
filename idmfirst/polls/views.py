from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from polls.models import Choice, Poll
from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_poll_list'

  def get_queryset(self):
    """Return the last five published polls."""
    return Poll.objects.order_by('-pub_date')[:5]
    
#def index(request):
#  latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#  output = ', '.join([p.question for p in latest_poll_list])
#  template = loader.get_template('polls/index.html')
#  context = RequestContext(request, {
#        'latest_poll_list': latest_poll_list,
#  })
#  return render(request, 'polls/index.html', {'latest_poll_list': latest_poll_list})
  
class DetailView(generic.DetailView):
  model = Poll
  template_name = 'polls/detail.html'
  
#def detail(request, poll_id):
#  poll = get_object_or_404(Poll, pk=poll_id)
#  return render(request, 'polls/detail.html', {'poll' : poll})

class ResultsView(generic.DetailView):
  model = Poll
  template_name = 'polls/results.html'
  
#def results(request, poll_id):
#  poll = get_object_or_404(Poll, pk=poll_id)
#  return render(request, 'polls/results.html', {'poll' : poll})

def vote(request, poll_id):
  p = get_object_or_404(Poll, pk=poll_id)
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
    return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))