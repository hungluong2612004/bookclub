
from django.contrib import admin
from django.urls import path, include

#enable image uploading
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('my-books/', include('shelf.urls')),
    path('account/', include('account.urls')),
    path('review/', include('review.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)