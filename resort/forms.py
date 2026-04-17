from django import forms


class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'your@email.com'
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': '+1 234 567 8900'
    }))
    country = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Country'
    }))
    adults = forms.IntegerField(min_value=1, max_value=10, initial=2, widget=forms.NumberInput(attrs={
        'class': 'form-input', 'min': '1', 'max': '10'
    }))
    children = forms.IntegerField(min_value=0, max_value=10, initial=0, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'max': '10'})
    )
    special_requests = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-input', 'rows': 4, 'placeholder': 'Dietary requirements, late check-in, etc.'
    }))
    agree_terms = forms.BooleanField(required=True, error_messages={
        'required': 'You must agree to the Terms & Conditions to proceed.'
    })

    def clean(self):
        cleaned = super().clean()
        adults = cleaned.get('adults', 1)
        children = cleaned.get('children', 0) or 0
        if adults + children > 10:
            raise forms.ValidationError('Total guests cannot exceed 10.')
        return cleaned


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Your full name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'your@email.com'
    }))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': '+1 234 567 8900 (optional)'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-input', 'rows': 6, 'placeholder': 'How can we help you?'
    }))
