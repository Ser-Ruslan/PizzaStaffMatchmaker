from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings

from .models import (
    UserProfile, Resume, Vacancy, Application, 
    Interview, ApplicationComment, UserRole
)

# User registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
        return user

# User profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'photo', 'about', 'desired_position', 'experience', 'education']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'education': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields not required for non-candidates
        if self.instance and self.instance.role != UserRole.CANDIDATE:
            self.fields['desired_position'].required = False
            self.fields['experience'].required = False
            self.fields['education'].required = False

# Resume upload form
class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].validators.append(
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])
        )
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size
            if file.size > settings.MAX_RESUME_SIZE:
                raise forms.ValidationError("File size cannot exceed 5MB.")
            
            # Check file type
            content_type = file.content_type
            if content_type not in settings.ALLOWED_RESUME_TYPES:
                raise forms.ValidationError("Only PDF and Word documents are allowed.")
        
        return file

# Vacancy form
class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'title', 'position_type', 'restaurants', 
            'description', 'requirements', 'responsibilities', 
            'conditions', 'salary_min', 'salary_max', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'conditions': forms.Textarea(attrs={'rows': 4}),
        }

# Application form
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Only show active resumes for the current user
            self.fields['resume'].queryset = Resume.objects.filter(
                user=user, is_active=True
            )

# Application status form
class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']

# Application comment form
class ApplicationCommentForm(forms.ModelForm):
    class Meta:
        model = ApplicationComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

# Interview form
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interviewer', 'restaurant', 'date_time', 'location', 'is_online', 'meeting_link', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        application = kwargs.pop('application', None)
        super().__init__(*args, **kwargs)
        
        if application:
            # Only show restaurants related to the vacancy
            self.fields['restaurant'].queryset = application.vacancy.restaurants.all()
            
            # Only show restaurant managers or HR managers as interviewers
            self.fields['interviewer'].queryset = User.objects.filter(
                profile__role__in=[UserRole.HR_MANAGER, UserRole.RESTAURANT_MANAGER]
            )
