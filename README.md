# Imager

Core service to store images and annotations for it. Meta information for labels stored directly to avoid unnecessary SQL JOINs and speed up SELECT by this meta information. Shape data stored in JSON field with same purposes. It is assumed that we will not make SQL requests by shape data but will show this info via API.

## Details

Tehere also configured `celery` module which is not used actually. But can be easily enabled if required (just my bootstrap script generates django project with celery by default).  

`docker-compose.yml` contains full set of containers to setup working instance. For development you can omit to execute `daphne` and `nginx` containers, then project can use your additional settings from `imager/saettings_local.py` if it exists. Can be useful in development.

## Endpoints

### `/api/v1/images/` 

#### `POST`

upload image to this endpoint in `image` field

### `/api/v1/images/<UUID>/`

#### `PUT` 

Set/update annotations for target image. New set completely replaces old one

Example (will add 2 annotations to image):

```json
{
   "labels":[
      {
         "id":"753ed1c8-205a-4cde-8dd7-019e69aaebfc",
         "class_id":"tooth",
         "meta":{
            "confirmed":false,
            "confidence_percent":0.99
         },
         "surface":[
            "B",
            "O",
            "L"
         ],
         "shape":{
            "endX":983,
            "endY":1399,
            "startX":44,
            "startY":605
         }
      },
      {
         "id":"51756b58-062c-4ade-ad98-09faa3687f25",
         "class_id":"stopping",
         "meta":{
            "confirmed":true,
            "confidence_percent":1.12
         },
         "surface":[
            "B",
            "O"
         ],
         "shape":{
            "endX":12,
            "endY":1432,
            "startX":2,
            "startY":455
         }
      }
   ]
}
```

#### `GET`

Return annotations for target image. Use `?fmt=json` if you try to check it in browser

Able to return internal or export formatted result. Export-formatted resuld does not include `meta` information, `surface` returned as string and includes only `meta.confirmed` equals to `true`. By default results reurned in `export` format. To get `internal` format use `format=internal` query params.

### `/api/v1/images/<UUID>/url/`

#### `GET`

Return URL of target image
