from distutils.log import Log
from django.urls import reverse
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import render, redirect
from leads.models import Lead, Category
from leads.forms import LeadCategoryUpdateForm, LeadForm, CustomUserCreationForm, AssignAgentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from agents.mixins import OrganisoAndLoginRequiredMixin

# Register View

class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')

def Landing_page(request):
    return render(request, 'landing.html')


# @login_required
# def Leads_List(request):
#     #return HttpResponse("Hello world")
#     lead = Lead.objects.all()
#     dict = {'leads': lead}
#     return render(request,"leads/lead.html", context=dict)
# class Based Lead List View

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context

class AssignAgentView(LoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        print(form.data)
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


# def Lead_details(request, pk):
#     lead = Lead.objects.get(id=pk)
#     dict = {'leads': lead}
#     return render(request, "leads/lead_details.html", context=dict)

#class Based Lead Details

class LeadDetailView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_details.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset




def Lead_create(request):
    form = LeadForm()
    if request.method =="POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    dict = {"form": form}
    return render(request, 'leads/lead_create.html', context=dict)

# class LeadCreate(generic.CreateView):
#     template_name = 'leads/lead_create.html'
#     form_class = LeadForm

#     def get_success_url(self) -> str:
#         return reverse('leads:create')
    
#     def form_valid(self, form):
#         send_mail(
#             subject="A new lead has been created",
#             message= "Go to the site to see the new lead",
#             from_email="test@test.com",
#             recipient_list=["test1@test.com"]
#         )
#         return super(LeadCreate, self).form_valid(form)


# def Lead_Update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm(instance=lead)
#     if request.method == "POST":
#         form = LeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
#     dict = {"form": form, "leads": lead}
#     return render(request, 'leads/lead_update.html', context=dict)

# Class Base Lead Update

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    context_object_name = "leads"
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset
    def get_success_url(self) -> str:
        return reverse('leads:lead-list')

# def Lead_Delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect('/leads')

#class Based Lead Delete

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset
    def get_success_url(self) -> str:
        return reverse('leads:lead-list')
    

# Category Crud class Based View

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
        context.update({
            "Unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
            
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = Lead.objects.filter(category=self.get_object())
        # leads = self.get_object().leads.all()
        context.update({
            "leads": leads
        })
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
            
        return queryset


class leadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    context_object_name = "leads"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset
    def get_success_url(self) -> str:
        return reverse('leads:lead-list')















