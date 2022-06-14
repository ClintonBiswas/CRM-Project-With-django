import random
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.urls import reverse
from agents.forms import AgentForm
from .mixins import OrganisoAndLoginRequiredMixin


class AgentListView(OrganisoAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agentlist.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

class AgentCreateView(OrganisoAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentForm

    def get_success_url(self) -> str:
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject = "You are invited to be an agent",
            message = "You were added as an agent on DJCRM. Please come login to start working",
            from_email = "admin@test.com",
            recipient_list = [user.email],
        )
        return super(self, AgentCreateView).form_valid(form)

class AgentDetailsView(OrganisoAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentForm
    context_object_name = 'agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        print(organization)
        queryset = Agent.objects.filter(organization=organization)
        return queryset

    def get_success_url(self) -> str:
        return reverse('agents:agent-list')

class AgentDeleteView(OrganisoAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    def get_success_url(self) -> str:
        return reverse('agents:agent-list')

