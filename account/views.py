from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Authentication successful
            return redirect("/")
        else:
            # Authentication failed
            return JsonResponse({'authenticated': False}, status=401)

    # Handle other HTTP methods if needed
    
    else:
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})

    # return JsonResponse({'error': 'Method not allowed'}, status=405)
