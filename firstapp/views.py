from django.shortcuts import render,redirect
from .models import Photo , Category
from django.contrib import messages

# Create your views here.
def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name = category)
    categories = Category.objects.all()
    context = {'categories':categories, 'photos':photos}
    return render(request,'gallery.html', context)
def viewPhoto(request,pk):
    photo = Photo.objects.get(id = pk)
    context = {'photo':photo}
    return render(request,'photo.html', context)
def addPhoto(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = request.POST
            image = request.FILES.get('image')
            print(data, image)
            if data['category'] != 'none':
                category = Category.objects.get(id = data['category'])
            elif data['categoryname'] != '':
                category, created = Category.objects.get_or_create(name = data['categoryname'])
            else:
                category = None
            if data['description']:
                Photo.objects.create(
                    category = category,
                    description = data['description'],
                    image = image,
                )
            else:
                pass
            return redirect('gallery')
        else:
            messages.info(request , "You aren't administrator!")
    context = {'categories':categories}
    return render(request,'add.html', context)