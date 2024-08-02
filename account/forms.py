from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Authentication successful
            return JsonResponse({'authenticated': True, 'username': user.username})
        else:
            # Authentication failed
            return JsonResponse({'authenticated': False}, status=401)

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Method not allowed'}, status=405)