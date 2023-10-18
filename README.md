# Inventory API

This is a small showcase django application implementing an API for creating/reading Products records and 
placing/viewing Orders 


## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Future Work](#future-work)
- [License](#license)


## Features

- **Authentication**: Using credentials (username, password) user gets an Authentication Token
- **Create Product Listings**: Post new products into the database
- **View Paginated Product List**: Fetch existing products in the inventory using pagination
- **Place new Order**: Place order asking for N amount of a Product
- **Order History**: View order history
- **Swagger Integration**: Project has Swagger implemented giving a UI to test the API

## Prerequisites

- [Python](https://www.python.org/downloads/)
- Additional libraries and dependencies (refer to the `requirements.txt`).
- Docker

## Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:StefosGeo/InventoryAPI.git
   ```

2. Build the Docker image:
   ```bash
    docker build -t inventory_api .
    ```
   
3. Run the Docker container:
   ```bash
    docker run -p 8000:8000 -it inventory_api
    ```
   

## Usage

Docker image by default creates a superuser with `username = admin` and `password = admin`

1. Get you authentication token using this call
```
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "admin",
    "password": "admin"
}' localhost:8000/api-token-auth/
```

2. Set access token
```
export ACCESS_TOKEN="your_access_token_here"
```

3. Create a product
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $ACCESS_TOKEN" -d '{
    "name": "Product Name",
    "price": 10.99,
    "quantity_in_stock": 100
}' localhost:8000/api/products/
```

4. List Products

```
curl -X GET -H "Authorization: Token $ACCESS_TOKEN" localhost:8000/api/products/
```

5. Place Order (remember to replace product_id)
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $ACCESS_TOKEN" -d '{
    "product": {product_id},  # Replace with the actual product ID
    "quantity_ordered": 5
}' localhost:8000/api/orders/

```

6. View Order History
```
curl -X GET -H "Authorization: Token $ACCESS_TOKEN" localhost:8000/api/orders/
```


## Tests

Run the tests using the following command:
```bash
python manage.py test
```


## Future Work
- [ ] Add more tests and better structure of tests
- [ ] Build a proper deployment script
- [ ] Search for edge cases and proper handling exceptions


## License

#### MIT License