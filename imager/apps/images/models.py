import uuid

from django.db import models


class LabelId(models.TextChoices):
    CARIES = 'caries'
    STOPPING = 'stopping'
    TOOTH = 'tooth'


class Surface(models.TextChoices):
    B = 'B'
    L = 'L'
    O = 'O'


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='annotated_images')


class Label(models.Model):
    CLASS_IDS = LabelId.choices
    SURFACES = Surface.choices

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(to=Image, on_delete=models.CASCADE,
                              related_name='labels')
    shape = models.JSONField()
    class_id = models.CharField(max_length=24, choices=CLASS_IDS)
    surface = models.CharField(max_length=64, choices=SURFACES)
    meta_confirmed = models.BooleanField(default=False, db_index=True)
    meta_confidence_percent = models.FloatField(db_index=True)

    class Meta:
        ordering = ['meta_confirmed']

    @property
    def meta(self):
        return {
            'confirmed': self.meta_confirmed,
            'confidence_percent': self.meta_confidence_percent,
        }

    @classmethod
    def get_meta(cls, meta):
        if not isinstance(meta, dict):
            raise ValueError('`meta` attribute should be dict')

        _meta = {}

        if 'confirmed' in meta:
            _meta['confirmed'] = meta['confirmed']

        if 'confidence_percent' in meta:
            _meta['confidence_percent'] = meta['confidence_percent']

        return _meta

    @meta.setter
    def meta(self, meta):
        if not isinstance(meta, dict):
            raise ValueError('`meta` attribute should be dict')

        if 'confirmed' in meta:
            self.meta_confirmed = meta['confirmed']

        if 'confidence_percent' in meta:
            self.meta_confidence_percent = meta['confidence_percent']
