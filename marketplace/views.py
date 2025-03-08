from django.shortcuts import render


# Main Page
def main(request):
    return render(request, 'marketplace/index.html')
