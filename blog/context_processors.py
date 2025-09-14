from django.db.models import Count
from .models import Post
from django.contrib.auth.models import User

def sidebar_context(request):
    """Context processor to provide sidebar data to all templates"""
    
    # Latest posts (5 most recent)
    latest_posts = Post.objects.all().order_by('-date_posted')[:5]
    
    # Popular categories (categories with post counts)
    categories_with_counts = []
    category_choices = Post.CATEGORY_CHOICES
    
    for category_code, category_name in category_choices:
        if category_code == 'other':
            # Handle custom categories
            custom_posts = Post.objects.filter(category='other').exclude(custom_category__isnull=True).exclude(custom_category='')
            custom_categories = custom_posts.values('custom_category').annotate(count=Count('custom_category'))
            for custom_cat in custom_categories:
                categories_with_counts.append({
                    'name': custom_cat['custom_category'],
                    'count': custom_cat['count']
                })
        else:
            count = Post.objects.filter(category=category_code).count()
            if count > 0:
                categories_with_counts.append({
                    'name': category_name,
                    'count': count
                })
    
    # Sort by count (most popular first)
    categories_with_counts = sorted(categories_with_counts, key=lambda x: x['count'], reverse=True)[:5]
    
    # Blog statistics
    total_posts = Post.objects.count()
    total_users = User.objects.filter(post__isnull=False).distinct().count()
    total_categories = len([cat for cat in categories_with_counts if cat['count'] > 0])
    
    return {
        'latest_posts': latest_posts,
        'popular_categories': categories_with_counts,
        'total_posts': total_posts,
        'total_users': total_users,
        'total_categories': total_categories,
    }