from django import forms
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'face_id',
            'name',
            'address',
            'job',
            'phone',
            'email',
            'bio',
            'image',
        ]
        widgets = {
            'face_id': forms.TextInput(attrs={'placeholder': 'Your Face ID', 'class': 'custom-css-class'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
            'address': forms.TextInput(attrs={'placeholder': 'Your Address', 'class': 'custom-css-class'}),
            'job': forms.TextInput(attrs={'placeholder': 'Your Job'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Your Bio'}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'})
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['face_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['job'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'accept': 'image/*'})