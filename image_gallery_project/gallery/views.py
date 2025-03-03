from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
from .forms import ImageForm
from django.http import Http404, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import os
from django.conf import settings

# Public view: Display the image gallery.
def gallery_view(request):
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery/gallery.html', {'images': images})

# Public view: Optional detail view (if needed for separate page; here the lightbox is done in a modal)
def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'gallery/lightbox.html', {'image': image})

# Public view: Download functionality.
def download_image(request, image_id):
    image_obj = get_object_or_404(Image, id=image_id)
    image_path = image_obj.image.path
    if os.path.exists(image_path):
        response = FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'
        return response
    raise Http404

# Custom decorator to ensure only staff (admin) users access admin views.
def admin_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))

# Admin view: Custom login page.
def admin_login(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            msg = 'Invalid credentials or not authorized.'
    return render(request, 'gallery/login.html', {'message': msg})

# Admin view: Logout.
def admin_logout(request):
    logout(request)
    return redirect('gallery')

# Admin dashboard: List images with edit/delete options.
@admin_required
def dashboard(request):
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery/dashboard.html', {'images': images})

# Admin view: Upload a new image.
@admin_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ImageForm()
    return render(request, 'gallery/upload.html', {'form': form})

# Admin view: Edit an existing image.
@admin_required
def edit_image(request, image_id):
    image_obj = get_object_or_404(Image, id=image_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ImageForm(instance=image_obj)
    return render(request, 'gallery/edit_image.html', {'form': form, 'image': image_obj})

# Admin view: Delete an image (with confirmation).
@admin_required
def delete_image(request, image_id):
    image_obj = get_object_or_404(Image, id=image_id)
    if request.method == 'POST':
        image_obj.delete()
        return redirect('dashboard')
    return render(request, 'gallery/delete_image.html', {'image': image_obj})
