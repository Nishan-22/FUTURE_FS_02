from django.shortcuts import render, redirect, get_object_or_404

from .models import Lead, Note
from .forms import LeadForm, NoteForm

def dashboard(request):
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'leads': leads})


def create_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = LeadForm()

    return render(request, 'create_lead.html', {'form': form})


def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    notes = lead.notes.all().order_by('-created_at')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.lead = lead
            note.save()
            return redirect('lead_detail', pk=pk)
    else:
        form = NoteForm()

    return render(request, 'lead_detail.html', {
        'lead': lead,
        'notes': notes,
        'form': form
    })

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    lead_id = note.lead.id
    note.delete()
    return redirect('lead_detail', pk=lead_id)

def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_detail', pk=lead.id)
    else:
        form = LeadForm(instance=lead)

    return render(request, 'leads/edit_lead.html', {'form': form})
