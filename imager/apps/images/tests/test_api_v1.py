import os

from django.conf import settings
from django.urls import reverse
from django_webtest import WebTest

from imager.apps.images.models import (
    Image,
    Label,
    LabelId,
    Surface,
)


class ImageAPITest(WebTest):
    csrf_checks = False
    maxDiff = None

    def test_image_api(self):
        self.assertEqual(0, Image.objects.all().count())
        self.assertEqual(0, Label.objects.all().count())

        file = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'python-logo@2x.png')

        # test image upload
        create_url = reverse('image-create-api-v1')

        resp = self.app.post(create_url, upload_files=[('image', file)])
        self.assertEqual(201, resp.status_code)
        self.assertEqual(1, Image.objects.all().count())

        file_id = resp.json['id']
        image = Image.objects.all()[0]

        self.assertEqual(str(image.pk), file_id)
        self.assertTrue(os.path.exists(image.image.file.name))

        # test retrieving image URL
        get_url = reverse('image-url-api-v1', kwargs={'pk': file_id})

        resp = self.app.get(get_url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json['url'], image.image.url)

        # test adding annotation
        upd_url = reverse('image-retrieve-update-api-v1', kwargs={'pk': file_id})

        data = {
            'labels': [
                {
                    'meta': {
                        'confirmed': False,
                        'confidence_percent': 0.99,
                    },
                    'class_id': str(LabelId.TOOTH),
                    'surface': [str(Surface.B), str(Surface.O), str(Surface.L)],
                    'shape': {
                        'endX': 983,
                        'endY': 1399,
                        'startY': 605,
                        'startX': 44,
                    },
                },
            ],
        }

        resp = self.app.put_json(url=upd_url, params=data)

        self.assertEqual(200, resp.status_code)
        resp_json = resp.json
        label_id = resp_json['labels'][0]['id']
        data['labels'][0]['id'] = label_id
        self.assertEqual(data, resp_json)

        data['labels'][0]['shape']['endX'] = 12

        resp = self.app.put_json(url=upd_url, params=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(data['labels']), len(resp.json['labels']))
        label_id = resp.json['labels'][0]['id']
        data['labels'][0]['id'] = label_id
        self.assertEqual(data, resp.json)

        resp = self.app.get(url=upd_url, expect_errors=True)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, len(resp.json['labels']))

        resp = self.app.get(url=upd_url, params={'format': 'internal'})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(data['labels']), len(resp.json['labels']))
        self.assertEqual(data, resp.json)

        data['labels'].append({
            'meta': {
                'confirmed': True,
                'confidence_percent': 1.2,
            },
            'class_id': str(LabelId.STOPPING),
            'surface': [str(Surface.B), str(Surface.L)],
            'shape': {
                'endX': 123,
                'endY': 199,
                'startY': 905,
                'startX': 444,
            },
        })

        resp = self.app.put_json(url=upd_url, params=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(data['labels']), len(resp.json['labels']))
        resp_json = resp.json
        del resp_json['labels'][0]['id']
        del resp_json['labels'][1]['id']
        del data['labels'][0]['id']
        self.assertEqual(data, resp_json)

        resp = self.app.get(url=upd_url)
        self.assertEqual(1, len(resp.json['labels']))
        self.assertNotIn('meta', resp.json['labels'][0])

        resp = self.app.get(url=upd_url, params={'format': 'export'})
        self.assertEqual(1, len(resp.json['labels']))

        resp = self.app.get(url=upd_url, params={'format': 'internal'})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(data['labels']), len(resp.json['labels']))
        resp_json = resp.json
        del resp_json['labels'][0]['id']
        del resp_json['labels'][1]['id']
        self.assertEqual(data, resp_json)
