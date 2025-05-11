# admin.py
from django.contrib import admin
from .models import Dataset, DatasetFile

class DatasetFileInline(admin.TabularInline): # Ou StackedInline pour plus d'espace
    model = DatasetFile
    fields = ('file', 'file_type', 'description', 'original_filename', 'created_at', 'updated_at')
    readonly_fields = ('original_filename', 'created_at', 'updated_at')
    extra = 1 # Nombre de formulaires vides à afficher pour ajouter des fichiers
    # Attention avec FileField dans les inlines, peut être lourd si beaucoup de fichiers.

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [DatasetFileInline] # Intégrer la gestion des fichiers directement

# Optionnel: enregistrer DatasetFile séparément aussi pour une vue dédiée
@admin.register(DatasetFile)
class DatasetFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataset', 'file_type', 'original_filename', 'created_at')
    list_filter = ('file_type', 'dataset')
    search_fields = ('original_filename', 'description', 'dataset__name')
    readonly_fields = ('id', 'original_filename', 'created_at', 'updated_at')