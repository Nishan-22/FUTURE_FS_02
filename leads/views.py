from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Lead, Note
from .forms import LeadForm, NoteForm
from .serializers import LeadSerializer

class LeadCaptureView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [AllowAny] # Allow website forms to post without auth

@login_required
def dashboard(request):
    # EVERYONE can see EVERY lead
    leads = Lead.objects.all().order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        leads = leads.filter(name__icontains=query) | leads.filter(email__icontains=query)
    
    # Filter functionality
    status_filter = request.GET.get('status')
    if status_filter:
        leads = leads.filter(status=status_filter)
    
    # Global Analytics
    stats = {
        'total': Lead.objects.count(),
        'new': Lead.objects.filter(status='new').count(),
        'converted': Lead.objects.filter(status='converted').count(),
    }
    
    return render(request, 'dashboard.html', {
        'leads': leads, 
        'stats': stats,
        'query': query,
        'status_filter': status_filter
    })

@login_required
def create_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            if not lead.assigned_to:
                lead.assigned_to = request.user
            lead.save()
            return redirect('dashboard')
    else:
        form = LeadForm()

    return render(request, 'create_lead.html', {'form': form})

@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    # NO permission check for viewing detail (everyone can see)
    
    notes = lead.notes.all().order_by('-created_at')

    if request.method == 'POST':
        # STRICT permission check for ADDING notes
        if lead.assigned_to and lead.assigned_to != request.user and not request.user.is_staff:
            raise PermissionDenied
            
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

@login_required
def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    
    # STRICT permission check for EDITING
    if lead.assigned_to and lead.assigned_to != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_detail', pk=lead.id)
    else:
        form = LeadForm(instance=lead)

    return render(request, 'edit_lead.html', {'form': form, 'lead': lead})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    # Only owner or admin can delete notes
    if note.lead.assigned_to and note.lead.assigned_to != request.user and not request.user.is_staff:
        raise PermissionDenied
        
    lead_id = note.lead.id
    note.delete()
    return redirect('lead_detail', pk=lead_id)

@login_required
def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'dashboard.html', {'leads': leads})
