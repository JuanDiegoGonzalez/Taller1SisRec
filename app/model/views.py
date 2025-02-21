from django.shortcuts import render
from django.views.generic.edit import CreateView

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from model.forms import CreateForm
from model.process import proceso

class ModelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'model/model_form.html'
    success_url = reverse_lazy('model:model_result')

    def get(self, request):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        # Loading icon

        model = form.save(commit=False)
        model.owner = request.user

        predicciones = proceso(model.modelo, model.tipo, model.k, int(model.owner.username))
        predicciones_json = predicciones.to_dict(orient='records')

        request.session['predicciones'] = predicciones_json
        return redirect(self.success_url)

class ModelResultView(View):
    template_name = "model/model_result.html"

    def get(self, request) :
        context = {'predicciones' : request.session['predicciones']}
        return render(request, self.template_name, context)

