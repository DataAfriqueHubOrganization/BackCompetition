# serializers.py
import json
from rest_framework import serializers, exceptions
from django.db import transaction
from .models import Dataset, DatasetFile

# --- Serializer pour LIRE et afficher un fichier (INCHANGÉ) ---
class DatasetFileSerializer(serializers.ModelSerializer):
    file_path = serializers.CharField(source='file.name', read_only=True)
    class Meta:
        model = DatasetFile
        fields = ['id', 'file_path', 'file_type', 'description', 'original_filename', 'created_at', 'updated_at']
        read_only_fields = fields

# --- Serializer dédié à la VALIDATION/CRÉATION imbriquée ---
#     (Utilisé UNIQUEMENT comme 'write_only' dans DatasetSerializer)
class DatasetFileCreateNestedSerializer(serializers.ModelSerializer):
    # Ce serializer définit les champs attendus pour CHAQUE fichier initial
    # Le champ 'file' sera géré par DRF pour l'upload multipart
    # file = serializers.FileField(required=True, use_url=False) # Déjà défini par ModelSerializer
    file_type = serializers.ChoiceField(choices=DatasetFile.FileType.choices, required=True)
    description = serializers.CharField(required=False, allow_blank=True, style={'base_template': 'textarea.html'})

    class Meta:
        model = DatasetFile
        # Champs nécessaires pour créer un DatasetFile (sauf 'dataset' qui sera ajouté dans create)
        fields = ['file', 'file_type', 'description']


# --- Serializers pour Update/Create d'un fichier via les actions (INCHANGÉS) ---
class DatasetFileCreateSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, use_url=False)
    file_type = serializers.ChoiceField(choices=DatasetFile.FileType.choices, required=True)
    description = serializers.CharField(required=False, allow_blank=True, style={'base_template': 'textarea.html'})

class DatasetFileUpdateSerializer(serializers.ModelSerializer):
    file = serializers.CharField(source='file.name', read_only=True)
    original_filename = serializers.CharField(read_only=True)
    class Meta:
        model = DatasetFile
        fields = ['id', 'file', 'file_type', 'description', 'original_filename', 'created_at', 'updated_at']
        read_only_fields = ['id', 'file', 'original_filename', 'created_at', 'updated_at']


# --- Serializer principal pour Dataset (Modifié) ---
class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializer pour Dataset.
    - Gère la création initiale avec fichiers via 'initial_files' (nested ModelSerializer write_only).
    - Affiche les fichiers via 'files' (read_only).
    - Ignore 'initial_files' lors des mises à jour.
    """
    # Champ pour LIRE les fichiers associés (utilise le serializer de lecture)
    files = DatasetFileSerializer(many=True, read_only=True)

    # Champ pour RECEVOIR les fichiers initiaux lors de la CREATION (write_only)
    # Utilise le serializer imbriqué dédié à la création
    initial_files = DatasetFileCreateNestedSerializer(
        many=True,
        write_only=True,
        required=False # Optionnel à la création
    )

    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'description',
            'files',          # Lecture seule
            'initial_files',  # Ecriture seule (pour création)
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


    @transaction.atomic
    def create(self, validated_data):
        # Si DRF gère correctement le NestedSerializer, initial_files_data
        # devrait être une liste de dictionnaires validés.
        initial_files_data = validated_data.pop('initial_files', [])
        print("Données reçues pour initial_files:", initial_files_data) # DEBUG

        # Créer l'instance Dataset principale
        dataset_instance = Dataset.objects.create(**validated_data)

        # Traiter les fichiers initiaux
        files_created = []
        for file_data in initial_files_data:
            print("Traitement fichier initial data:", file_data) # DEBUG
            if not file_data: # Vérifier si le dict n'est pas vide
                 print("Skipping empty file data dict.")
                 continue

            # Extraire le fichier uploadé et les autres métadonnées
            # Le nom de la clé pour le fichier est 'file' (défini dans DatasetFileCreateNestedSerializer)
            uploaded_file = file_data.get('file')
            file_type = file_data.get('file_type')
            description = file_data.get('description')

            if not uploaded_file:
                print(f"Fichier manquant dans les données: {file_data}")
                # Idéalement, lever une erreur ici si le fichier est requis
                # raise serializers.ValidationError("Missing 'file' in initial_files data.")
                continue

            # Créer le DatasetFile
            df = DatasetFile.objects.create(
                dataset=dataset_instance,
                file=uploaded_file, # Passer l'objet fichier uploadé
                file_type=file_type,
                description=description
            )
            files_created.append(df)

        print(f"Fichiers créés pour le dataset {dataset_instance.id}: {len(files_created)}")
        # dataset_instance.refresh_from_db()
        return dataset_instance

    def update(self, instance, validated_data):
        # Ignorer 'initial_files' explicitement lors de la mise à jour
        validated_data.pop('initial_files', None)

        # Mettre à jour les champs simples
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance