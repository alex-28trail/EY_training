from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for React/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Product model
class Product(BaseModel):
    id: int
    name: str
    price: float
    image: str


# In-memory product data
products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "price": 4500,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "price": 7000,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
    },
    {
        "id": 3,
        "name": "Laptop",
        "price": 65000,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
    }
]


# HOME - Check API status
@app.get("/")
def home():
    return {"message": "Product API is running"}


# GET - All products
@app.get("/products")
def get_products():
    return products


# GET - Product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# POST - Add a new product
@app.post("/products", status_code=201)
def add_product(product: Product):
    for existing_product in products:
        if existing_product["id"] == product.id:
            raise HTTPException(
                status_code=400,
                detail="Product ID already exists"
            )

    new_product = product.model_dump()
    products.append(new_product)

    return {
        "message": "Product added successfully",
        "product": new_product
    }


# PUT - Update an existing product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:

            # Ensure the product ID remains unchanged
            if updated_product.id != product_id:
                raise HTTPException(
                    status_code=400,
                    detail="Product ID in the URL must match the product ID in the body"
                )

            products[index] = updated_product.model_dump()

            return {
                "message": "Product updated successfully",
                "product": products[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# DELETE - Remove a product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(index)

            return {
                "message": "Product deleted successfully",
                "product": deleted_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )