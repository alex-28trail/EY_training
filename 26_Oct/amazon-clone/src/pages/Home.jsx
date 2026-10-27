
import { useState } from "react";

const products = [
  {
    id: 1,
    name: "Laptop",
    price: 55000,
    image: "https://placehold.co/300x200?text=Laptop"
  },
  {
    id: 2,
    name: "Smartphone",
    price: 20000,
    image: "https://placehold.co/300x200?text=Smartphone"
  },
  {
    id: 3,
    name: "Headphones",
    price: 2000,
    image: "https://placehold.co/300x200?text=Headphones"
  },
  {
    id: 4,
    name: "Smart Watch",
    price: 5000,
    image: "https://placehold.co/300x200?text=Smart+Watch"
  },
  {
    id: 5,
    name: "Keyboard",
    price: 1500,
    image: "https://placehold.co/300x200?text=Keyboard"
  },
  {
    id: 6,
    name: "Mouse",
    price: 800,
    image: "https://placehold.co/300x200?text=Mouse"
  }
];

function Home({ addToCart }) {
  const [search, setSearch] = useState("");

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <h1>Welcome to Amazon Clone</h1>

      <input
        type="text"
        placeholder="Search products..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search"
      />

      <h2>Products</h2>

      <div className="products">
        {filteredProducts.map((product) => (
          <div className="product" key={product.id}>
            <img src={product.image} alt={product.name} />

            <h3>{product.name}</h3>
            <p>₹{product.price.toLocaleString("en-IN")}</p>

            <button onClick={() => addToCart(product)}>
              Add to Cart
            </button>
          </div>
        ))}
      </div>

      {filteredProducts.length === 0 && <p>No products found.</p>}
    </div>
  );
}

export default Home;
