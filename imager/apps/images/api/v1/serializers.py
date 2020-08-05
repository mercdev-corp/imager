from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    Field,
    MultipleChoiceField,
    SerializerMethodField
)
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from imager.apps.images.models import (
    Image,
    Label
)


class MetaField(Field):
    def to_internal_value(self, data):
        return Label.get_meta(data)

    def get_attribute(self, instance):
        # pass object itself to `to_representation`
        return instance

    def to_representation(self, value):
        return value.meta


class MultiselectField(MultipleChoiceField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            return data

        return ','.join(data)

    def to_representation(self, value):
        return value.split(',')


class LabelExportSerializer(ModelSerializer):
    surface = SerializerMethodField()

    class Meta:
        model = Label
        fields = [
            'id',
            'class_id',
            'shape',
            'surface',
        ]

    def get_surface(self, obj):
        return obj.surface.replace(',', '')


class LabelSerializer(ModelSerializer):
    surface = MultiselectField(choices=Label.SURFACES)
    meta = MetaField()

    class Meta:
        model = Label
        fields = [
            'id',
            'class_id',
            'meta',
            'surface',
            'shape',
        ]


class LabelManageSerializer(LabelSerializer):
    class Meta:
        model = Label
        fields = [
            'id',
            'class_id',
            'image',
            'meta',
            'surface',
            'shape',
        ]


class ImageExportSerializer(ModelSerializer):
    labels = SerializerMethodField()

    class Meta:
        model = Image
        fields = ['labels']

    def get_labels(self, obj):
        return LabelExportSerializer(
            instance=obj.labels.filter(meta_confirmed=True),
            many=True,
        ).data


class ImageCreateSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image'
        ]


class ImageSerializer(ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = Image
        fields = ['labels']

    def update(self, instance, validated_data):
        if 'labels' not in validated_data:
            return instance

        instance.labels.all().delete()

        for label in validated_data['labels']:
            label['image'] = str(instance.pk)
            _label = LabelManageSerializer(data=label)

            if _label.is_valid():
                _label.save()

        return instance


class ImageUrlSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = Label
        fields = [
            'url',
        ]

    def get_url(self, obj):
        return obj.image.url
