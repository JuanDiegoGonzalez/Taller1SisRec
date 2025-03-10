from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.model.forms import CreateForm
from apps.model.process import predict

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import time, json

#-------------------------------------
# Nuevo endpoint
#-------------------------------------
@method_decorator(csrf_exempt, name="dispatch")
class ModelView(View):
    template_name = "movies/movie_list.html"

    def get(self, request):
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    def post(self, request):
        try:
            data = json.loads(request.body)  # Get JSON data from request
            modelo = data.get('modelo')
            tipo = data.get('tipo')
            k = data.get('k')

            if not modelo or not tipo or k is None:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Start processing
            start_time = time.time()
            # TODO
            print(modelo, tipo, k, int(data.get('user').get('username')))
            predicciones = predict(modelo, tipo, k, int(data.get('user').get('username')))
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.4f} seconds")

            # Convert predictions to JSON format
            predicciones_json = predicciones.to_dict(orient='records')

            return JsonResponse(predicciones_json, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

#-------------------------------------
# Anteriores endpoints
#-------------------------------------
class ModelOldCreateView(LoginRequiredMixin, CreateView):
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
        
        model = form.save(commit=False)
        model.owner = request.user

        start_time = time.time()  # Start timer
        # TODO
        predicciones = predict(model.modelo, model.tipo, model.k, int(model.owner.username))
        end_time = time.time()  # End timer
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.4f} seconds")

        predicciones_json = predicciones.to_dict(orient='records')

        request.session['predicciones'] = predicciones_json
        return redirect(self.success_url)

class ModelOldResultView(View):
    template_name = "model/model_result.html"

    def get(self, request) :
        context = {'predicciones' : request.session['predicciones']}
        return render(request, self.template_name, context)
    