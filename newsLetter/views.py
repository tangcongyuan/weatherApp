from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignupForm
from .models import Subscriber

# Create your views here.
def default(request):
    context = None
    return render(request, 'newsLetter/index.html', context)

def signup(request):
    context = {
        "cities": ["Anchorage, AK", "Austin, TX", "Boston, MA", "Seattle, WA", "Washington, DC"],
        "form" : None,
        "error" : None,
    }

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # process the data in form.cleaned_data as required
            sub = Subscriber(email_address = data['email_address'], location = data['location'])
            try:
                if not data['location'] == "Default":
                    sub.save()
                    # redirect to a new URL:
                    return HttpResponseRedirect('/thanks')
                else:
                    context['error'] = "Please select your city."
            except:
                context['error'] = "Error occurred. This ususally means you already subscribed using this email."
            context['form'] = form
            return render(request, 'newsLetter/signup.html', context)
        else:
            # context['error'] = "Something bad happened."
            context['form'] = form
            return render(request, 'newsLetter/signup.html', context)
    else:
        form = SignupForm()
        context['form'] = form
        return render(request, 'newsLetter/signup.html', context)

def thanks(request):
    return render(request, 'newsLetter/thanks.html')
