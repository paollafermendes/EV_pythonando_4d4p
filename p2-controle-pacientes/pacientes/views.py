from django.shortcuts import render

# Create your views here.
def pacientes(request):
    if request.method == "GET": # Rodar no navegador o arquivo pacientes.html
      return render (request, 'pacientes.html')
    
