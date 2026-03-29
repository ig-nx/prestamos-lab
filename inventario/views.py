from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin 
from django.urls import reverse_lazy 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView 
from django.shortcuts import redirect, render
 
from .forms import NotebookForm 
from .models import Notebook 
 
 
class NotebookListView(ListView): 
    model = Notebook 
    template_name = 'notebook_list.html' 
    context_object_name = 'notebooks' 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        visitas = self.request.session.get('visitas_inicio', 0) 
        self.request.session['visitas_inicio'] = visitas + 1 
        context['visitas'] = self.request.session['visitas_inicio'] 
        return context 
 
 
class NotebookCreateView(CreateView): 
    model = Notebook 
    form_class = NotebookForm 
    template_name = 'notebook_form.html' 
    success_url = reverse_lazy('notebook_list') 
 
    def form_valid(self, form): 
        messages.success(self.request, 'Notebook creado correctamente.') 
        return super().form_valid(form) 
 
 
class NotebookUpdateView(UpdateView): 
    model = Notebook 
    form_class = NotebookForm 
    template_name = 'notebook_form.html' 
    success_url = reverse_lazy('notebook_list') 
 
    def form_valid(self, form): 
        messages.success(self.request, 'Notebook actualizado correctamente.') 
        return super().form_valid(form) 
 
 
class NotebookDeleteView(DeleteView): 
    model = Notebook 
    template_name = 'notebook_confirm_delete.html' 
    success_url = reverse_lazy('notebook_list') 
 
    def form_valid(self, form): 
        messages.success(self.request, 'Notebook eliminado correctamente.') 
        return super().form_valid(form) 
 
 # Solo los usuarios en el grupo "Encargados" pueden ver el reporte interno
class SoloEncargadosMixin(LoginRequiredMixin, UserPassesTestMixin): 
    login_url = 'login'  # Redirige a la página de login si no está autenticado
    def test_func(self): 
        return self.request.user.groups.filter(name='Encargados').exists() 
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return redirect('access_denied')  # Redirige a una pagina de acceso denegado si el usuario no tiene el permiso necesario
class AccessDeniedView(TemplateView): 
    template_name = 'access_denied.html'

    


# Vista para el reporte interno, accesible solo por encargados con permiso específico
class ReporteInternoView(SoloEncargadosMixin, PermissionRequiredMixin, TemplateView): 
    template_name = 'reporte_interno.html' 
    permission_required = 'inventario.puede_ver_reporte_interno' 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['total'] = Notebook.objects.count() 
        context['disponibles'] = Notebook.objects.filter(disponible=True).count() 
        context['mantencion'] = Notebook.objects.filter(estado='mantencion').count() 
        return context


