from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post

def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # get the username
            messages.success(request, f'Your account has been created! you are now able to login in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Store original values to detect changes
        original_username = request.user.username
        original_email = request.user.email
        original_image = request.user.profile.image
        
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            # Check what has changed
            username_changed = u_form.cleaned_data.get('username') != original_username
            email_changed = u_form.cleaned_data.get('email') != original_email
            password_changed = bool(u_form.cleaned_data.get('new_password1'))
            image_changed = bool(request.FILES.get('image'))
            
            # Check if anything actually changed
            changes_made = username_changed or email_changed or password_changed or image_changed
            
            if not changes_made:
                messages.info(request, 'Your information is saved as it is.')
                return redirect('blog-home')
            
            # Save changes
            user = u_form.save()
            p_form.save()
            
            # If password was changed, update the session to keep user logged in
            if password_changed:
                update_session_auth_hash(request, user)
                messages.success(request, 'Your profile and password have been updated successfully!')
            else:
                messages.success(request, 'Your profile has been updated successfully!')
            
            return redirect('blog-home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Get user's posts
    user_posts = request.user.post_set.all().order_by('-date_posted')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_posts': user_posts
    }
    return render(request,'users/profile.html', context)