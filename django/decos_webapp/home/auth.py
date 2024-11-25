from allauth.account.forms import SignupForm, LoginForm
from PRP_CDM_app.models import Users
from django.core.exceptions import ObjectDoesNotExist

class UserRegistrationForm(SignupForm):

    def save(self,request):
        user = super(UserRegistrationForm, self).save(request)
        return user
    
class UserLoginForm(LoginForm):
    
    def login(self, *args, **kwargs):
        
        try:
            if Users.objects.get(pk=self.user.username) is not None:
                Users.objects.get(pk=self.user.username)
        except ObjectDoesNotExist as e:
            user = Users(user_id = self.user.username, email=self.user.email) # TODO add other data
            user.save()
        # Add your own processing here.
        # You must return the original result.
        return super(UserLoginForm, self).login(*args, **kwargs)