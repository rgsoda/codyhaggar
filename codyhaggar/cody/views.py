#!/usr/bin/env python
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list
from cody.models import Challenge, Solution, Lurk
from django import forms

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        exclude = ('created_by',)

class SolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        exclude = ('created_by', 'challenge')


def index(request):
    extra_context = {
            'solutions': Solution.objects.all().order_by('-id')[:50],
            }
    challenges_list = {
            'request': request,
            'queryset': Challenge.objects.all().order_by('-id'),
            'paginate_by': 1,
            'template_name': 'index.html',
            'extra_context': extra_context,
            }
    return object_list(**challenges_list)


def challenge(request, challenge_id=None):
    if request.method == 'GET':
        if challenge_id is not None:
            ch = get_object_or_404(Challenge, \
                    created_by = request.user, \
                    pk = challenge_id)
            form = ChallengeForm(instance=ch)
        else:
            form = ChallengeForm()
    else:
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_by = request.user
            challenge.save()
            return HttpResponseRedirect(reverse('index'))

    data = {
            'form': form,
            }
    return render_to_response("add.html", \
            data, \
            context_instance=RequestContext(request), \
            )

def display_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    solutions = Solution.objects.filter(challenge=challenge)
    data = {
            'challenge': challenge,
            'solutions': solutions
            }
    return render_to_response("display.html", \
            data, \
            context_instance=RequestContext(request), \
            )

def lurk(request, challenge_id):
    try:
        lurk = Lurk.objects.get(challenge__pk=challenge_id, \
                user = request.user)
    except Lurk.DoesNotExist:
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        lurk = Lurk()
        lurk.user = request.user
        lurk.challenge = challenge
        lurk.save()
    finally:
        return HttpResponseRedirect(reverse("display-challenge", \
            args=(challenge_id,)))


def solve(request, challenge_id):
    challenge = None
    if challenge_id is not None:
        challenge = Challenge.objects.get(id=challenge_id)
        if challenge.was_lurked_by(request.user):
            raise Http404()

    if request.method == 'GET':
        form = SolutionForm()
    else:
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.created_by = request.user
            solution.challenge = challenge
            solution.save()
            return HttpResponseRedirect(reverse("index"))

    data = {
            'form': form,
            'challenge_id': challenge_id,
            'challenge' : challenge,
            }
    return render_to_response("solve.html", \
            data, \
            context_instance=RequestContext(request), \
            )

