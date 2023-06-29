# API-запросы в приложении shoppapp
___

## POST-запрос
___
POST /api/api_products/products/
```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "pk": 7,
    "name": "White Desktop",
    "description": "Greatful Desktop",
    "price": "3999.00",
    "discount": 3,
    "created_at": "2023-06-29T16:21:43.297824Z",
    "archived": false,
    "preview": null
}
```

## OPTION-запрос
___
OPTIONS /api/api_products/products/
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "name": "Product List",
    "description": "Набор представлений для действий над Product.\nПолный CRUD для сущностей товара.",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "pk": {
                "type": "integer",
                "required": false,
                "read_only": true,
                "label": "ID"
            },
            "name": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Name",
                "max_length": 100
            },
            "description": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Description"
            },
            "price": {
                "type": "decimal",
                "required": false,
                "read_only": false,
                "label": "Price"
            },
            "discount": {
                "type": "integer",
                "required": false,
                "read_only": false,
                "label": "Discount"
            },
            "created_at": {
                "type": "datetime",
                "required": false,
                "read_only": true,
                "label": "Created at"
            },
            "archived": {
                "type": "boolean",
                "required": false,
                "read_only": false,
                "label": "Archived"
            },
            "preview": {
                "type": "image upload",
                "required": false,
                "read_only": false,
                "label": "Preview",
                "max_length": 100
            }
        }
    }
}
```
## GET-запрос
___
GET /api/api_products/products/
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 7,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": 1,
            "name": "Laptop",
            "description": "Super Laptop!",
            "price": "999.00",
            "discount": 3,
            "created_at": "2023-06-02T17:35:34.034840Z",
            "archived": false,
            "preview": "http://127.0.0.1:8000/media/products/product_1/preview/toshiba.png"
        },
        {
            "pk": 2,
            "name": "Desktop",
            "description": "",
            "price": "0.00",
            "discount": 0,
            "created_at": "2023-04-09T09:15:26.248005Z",
            "archived": false,
            "preview": null
        },
        {
            "pk": 3,
            "name": "Smartphone",
            "description": "Too many text. Too many text. Too many text. Too many text. Too many text. Too many text. Too many text. Too many text. Too many text.",
            "price": "0.00",
            "discount": 0,
            "created_at": "2023-04-30T12:07:57.765650Z",
            "archived": true,
            "preview": null
        },
        {
            "pk": 4,
            "name": "New Tablet",
            "description": "Great Tablet ever!",
            "price": "1199.00",
            "discount": 1,
            "created_at": "2023-04-11T17:33:56.538766Z",
            "archived": false,
            "preview": null
        },
        {
            "pk": 5,
            "name": "Phone 10",
            "description": "great Phone!",
            "price": "1299.00",
            "discount": 3,
            "created_at": "2023-04-11T18:15:20.357886Z",
            "archived": false,
            "preview": null
        },
        {
            "pk": 6,
            "name": "Headphones",
            "description": "Great headphones!",
            "price": "199.00",
            "discount": 3,
            "created_at": "2023-04-22T08:14:09.173522Z",
            "archived": false,
            "preview": null
        },
        {
            "pk": 7,
            "name": "White Desktop",
            "description": "Greatful Desktop",
            "price": "3999.00",
            "discount": 3,
            "created_at": "2023-06-29T16:21:43.297824Z",
            "archived": false,
            "preview": null
        }
    ]
}
```