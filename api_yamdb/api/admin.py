from django.contrib import admin

from users.models import User
from cgt.models import Categorie, Genre, Title


admin.site.register(User)
admin.site.register(Categorie)
admin.site.register(Genre)
admin.site.register(Title)
