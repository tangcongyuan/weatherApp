from django import forms

class SignupForm(forms.Form):
    OPTIONS = (
                ("Default", "Where do you live?"),
                ("Anchorage, AK", "Anchorage, AK"),
                ("Austin, TX", "Austin, TX"),
                ("Boston, MA", "Boston, MA"),
                ("Seattle, WA", "Seattle, WA"),
                ("Washington, DC", "Washington, DC"),
              )
    email_address = forms.EmailField(label='Email address', max_length=100)
    location = forms.ChoiceField(label='Location', choices = OPTIONS)
