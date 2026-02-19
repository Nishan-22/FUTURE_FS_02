from django import forms
from .models import Lead, Note

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'source', 'status', 'assigned_to']



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
