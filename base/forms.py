from django import forms
from .models import Proposal

class ProposalForm(forms.ModelForm):
    YES = 'Si'
    CHOICES = [(YES, 'Si')]
    terms_service = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=True, label="Acepta los términos de la política de tratamiento de datos personales",)

    class Meta:
        model = Proposal
        fields = '__all__'
        exclude = ['approved']
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'contact_charge': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'contact_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'group'}),
            'locality': forms.Select(attrs={'class': 'form-select', 'placeholder': 'group'}),
            'impact_sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px', 'placeholder': 'group', 'size': '40'}),
            'problematic': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px', 'placeholder': 'group'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px', 'placeholder': 'group'}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px', 'placeholder': 'group'}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control',}),
            'annex': forms.FileInput(attrs={'class': 'form-control',}),
            'url_video': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'group'}),
            'terms_service': forms.RadioSelect(attrs={"required": "required"}),
        }
