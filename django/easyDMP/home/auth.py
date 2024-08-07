from allauth.account.forms import SignupForm

class UserRegistrationForm(SignupForm):

    def save(self,request):
        user = super(UserRegistrationForm, self).save(request)
        return user