from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ContactForm, ProposalForm
from base.models import KeyConcepts, Partner, Phase, Proposal, Inscription, Category, Locality, Settings, SocialMedia, Testimony, Tool

def home(request):

    configuracion = Settings.objects.all()[0]
    last_proposals = Proposal.objects.filter(approved=True)[:5]
    phases = Phase.objects.all()
    conceptos = KeyConcepts.objects.all()
    herramientas = Tool.objects.all()
    convocatorias = Inscription.objects.all()[:5]
    testimonios = Testimony.objects.all()[:3]
    form = ProposalForm()
    redes = SocialMedia.objects.all()
    alianzas = Partner.objects.all()
    contactForm = ContactForm()

    context = {
        'configuracion': configuracion,
        'last_proposals': last_proposals,
        'conceptos': conceptos,
        'phases': phases,
        'herramientas': herramientas,
        'convocatorias': convocatorias,
        'testimonios': testimonios,
        'form': form,
        'redes': redes,
        'alianzas': alianzas,
        'contactForm': contactForm
    }

    """
    Handle Multiple <form></form> elements
    """
    if request.method == 'POST':
        if 'formOne' in request.POST:
            form = ProposalForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Se ha enviado su propuesta con éxito! Se visualizara cuando sea aprobada.')
                return redirect('/#formulario')
            else:
                context['form'] = form
                request.path = '/#formulario'
                return render(request, 'base/home.html', context)
        if 'formTwo' in request.POST:
            contactForm = ContactForm(request.POST)
            if contactForm.is_valid():
                contactForm.save()
                messages.success(request, '¡Se ha enviado su mensaje con éxito!')
                return redirect('/#contacto')

    return render(request, 'base/home.html', context)

def proposals(request):
    category_q = request.GET.get('category') if request.GET.get('category') != None else 0
    locality_q = request.GET.get('locality') if request.GET.get('locality') != None else 0
    text_q = request.GET.get('q') if request.GET.get('q') != None else ''

    q = {}
    if category_q != 0:
        q.update({'category__id': category_q})

    if locality_q != 0:
        q.update({'locality__id': locality_q})

    proposals = Proposal.objects.filter(approved=True).filter(**q).filter(
        Q(name__icontains=text_q) |
        Q(group_name__icontains=text_q) |
        Q(contact_name__icontains=text_q)
    ) 

    paginator = Paginator(proposals, 16)
    page_number = request.GET.get('page')
    page_proposals = paginator.get_page(page_number)

    categories = Category.objects.all()
    localities = Locality.objects.all()

    configuracion = Settings.objects.all()[0]

    context = {'configuracion': configuracion, 'proposals': page_proposals, 'categories': categories, 'localities': localities, 'category_q': int(category_q), 'locality_q': int(locality_q), 'text_q': text_q}
    return render(request, 'base/lista-iniciativas.html', context)

def proposal(request, pk):
    configuracion = Settings.objects.all()[0]
    proposal = Proposal.objects.get(id=pk)
    context = {'configuracion': configuracion, 'proposal': proposal}
    return render(request, 'base/iniciativa.html', context)
