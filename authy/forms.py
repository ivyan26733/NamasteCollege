from django import forms
from authy.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



from django import forms
from .models import Profile

class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), required=True)
    # bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)
    # url = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'URL'}), required=True)
    # location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}), required=True)
    FACULTY_CHOICES = [
        ('Engineering', 'Faculty of Engineering'),
        ('Science', 'Faculty of Science'),
        ('Arts', 'Faculty of Arts'),
        ('Arch', 'Faculty of Architecture'),
        ('Comm', 'Faculty of Commerce'),
        ('Ayush', 'Faculty of Integrated Alternative Medicine (AYUSH)'),
        ('SocialS', 'Faculty of Social Science'),
        ('Edu', 'Faculty of Education'),
        ('TC', 'Technical College'),

    ]
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, widget=forms.Select(attrs={'class': 'select'}), required=False)
    COURSE_CHOICES = [
        ('B.Tech', 'B.Tech'),
        ('B.Sc', 'B.Sc'),
        ('B.A', 'B.A'),
        ('M.Tech', 'M.Tech'),
    ]
    course = forms.ChoiceField(choices=COURSE_CHOICES, widget=forms.Select(attrs={'class': 'select'}), required=False)

    BRANCH_CHOICES = [
        ('ME', 'ME'),
        ('EE', 'EE'),
        ('physics', 'Physics'),
        ('English', 'English'),
    ]
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, widget=forms.Select(attrs={'class': 'select'}), required=False)

    YEAR_CHOICES = [
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
    ]
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'select'}), required=False)

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'bio', 'url', 'location', 'faculty', 'course', 'branch', 'year']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.faculty:  # Check if faculty is already set
            self.fields['faculty'].widget.attrs['disabled'] = True  # Disable the faculty field

    def clean_faculty(self):
        """
        Ensure that the faculty field remains unchanged once set.
        """
        if self.instance and self.instance.faculty:
            return self.instance.faculty
        else:
            return self.cleaned_data['faculty']




class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'prompt srch_explore'}), max_length=50, required=True)
    # username = forms.EmailInput(widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=50, required=True)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



