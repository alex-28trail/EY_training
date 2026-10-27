
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Enable CORS for React/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
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


# PostgreSQL connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="product_store",
        user="postgres",
        password="YOUR_PASSWORD"
    )


# Home endpoint
@app.get("/")
def home():
    return {"message": "Product API is running"}


# GET all products
@app.get("/products")
def get_products():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, price, image
                FROM products
                ORDER BY id
            """)
            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "image": row[3]
            }
            for row in rows
        ]
    finally:
        conn.close()


# GET product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, price, image
                FROM products
                WHERE id = %s
            """, (product_id,))

            row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return {
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "image": row[3]
        }
    finally:
        conn.close()


# POST - Add product
@app.post("/products", status_code=201)
def add_product(product: Product):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO products (id, name, price, image)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, price, image
            """, (
                product.id,
                product.name,
                product.price,
                product.image
            ))

            row = cursor.fetchone()

        conn.commit()

        return {
            "message": "Product added successfully",
            "product": {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "image": row[3]
            }
        }

    except psycopg2.IntegrityError as exc:
        conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product ID already exists"
        ) from exc
    finally:
        conn.close()


# PUT - Update product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE products
                SET name = %s,
                    price = %s,
                    image = %s
                WHERE id = %s
                RETURNING id, name, price, image
            """, (
                updated_product.name,
                updated_product.price,
                updated_product.image,
                product_id
            ))

            row = cursor.fetchone()

        if row is None:
            conn.rollback()
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        conn.commit()

        return {
            "message": "Product updated successfully",
            "product": {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "image": row[3]
            }
        }
    finally:
        conn.close()


# DELETE - Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM products
                WHERE id = %s
                RETURNING id, name, price, image
            """, (product_id,))

            row = cursor.fetchone()

        if row is None:
            conn.rollback()
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        conn.commit()

        return {
            "message": "Product deleted successfully",
            "product": {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "image": row[3]
            }
        }
    finally:
        conn.close()
