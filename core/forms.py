from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group



class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

class SignupForm(UserCreationForm):

    group_map = {
        'add' : 'Add',
        'edit' : 'Edit',
        'delete' : 'Delete'
    }

    is_superuser = False

    add = forms.BooleanField(required=False, label=_("Can add"))
    edit = forms.BooleanField(required=False, label=_("Can edit"))
    delete = forms.BooleanField(required=False, label=_("Can delete"))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        self.is_superuser = kwargs.pop('is_superuser', False)
        user_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if not self.is_superuser:
            for field, group_name in self.group_map.items():
                self.fields.pop(field)

        elif user_instance:
            for field, group_name in self.group_map.items():
                self.fields[field].initial = self.instance.groups.filter(name=group_name).exists()


    def save(self, commit=True):
        user = super().save(commit=False)


        if commit:
            user.save()
            
        if self.is_superuser: 
            for field, group_name in self.group_map.items():
                group_check, dummy = Group.objects.get_or_create(name=group_name)
                if self.cleaned_data[field]:
                    user.groups.add(group_check)
                else:
                    user.groups.remove(group_check)
        return user

