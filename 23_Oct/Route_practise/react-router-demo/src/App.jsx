
// import {
//   BrowserRouter,
//   Routes,
//   Route,
//   Link,
//   useParams,
//   useNavigate
// } from "react-router-dom"

// import { useEffect, useState } from "react"

// const API_URL = "http://127.0.0.1:8000/products"

// // Home Page
// function Home() {
//   const navigate = useNavigate()

//   return (
//     <div>
//       <h1>Home</h1>
//       <p>Welcome to the Product Store</p>

//       <button onClick={() => navigate("/products")}>
//         View Products
//       </button>
//     </div>
//   )
// }

// // Products Page
// function Products() {
//   const [products, setProducts] = useState([])
//   const [error, setError] = useState("")

//   useEffect(() => {
//     fetch(`${API_URL}/products`)
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Failed to load products")
//         }
//         return response.json()
//       })
//       .then((data) => {
//         setProducts(data)
//       })
//       .catch((error) => {
//         console.error("Error fetching products:", error)
//         setError("Could not load products. Check FastAPI.")
//       })
//   }, [])

//   return (
//     <div>
//       <h1>Product Store</h1>

//       {error && <p>{error}</p>}

//       {products.map((product) => (
//         <div key={product.id}>
//           <img
//             src={product.image}
//             alt={product.name}
//             width="180"
//           />

//           <h2>{product.name}</h2>
//           <p>Product ID: {product.id}</p>
//           <p>Price: ₹{product.price}</p>

//           <Link to={`/products/${product.id}`}>
//             View Details
//           </Link>

//           <hr />
//         </div>
//       ))}
//     </div>
//   )
// }

// // Product Details Page
// function ProductDetails() {
//   const { id } = useParams()
//   const navigate = useNavigate()

//   const [product, setProduct] = useState(null)
//   const [error, setError] = useState("")

//   useEffect(() => {
//     fetch(`${API_URL}/products/${id}`)
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Product not found")
//         }
//         return response.json()
//       })
//       .then((data) => {
//         setProduct(data)
//       })
//       .catch((error) => {
//         console.error("Error fetching product:", error)
//         setError("Product not found")
//       })
//   }, [id])

//   return (
//     <div>
//       <h1>Product Details</h1>

//       {error && <p>{error}</p>}

//       {product && (
//         <div>
//           <img
//             src={product.image}
//             alt={product.name}
//             width="200"
//           />

//           <h2>{product.name}</h2>
//           <p>Product ID: {product.id}</p>
//           <p>Price: ₹{product.price}</p>
//         </div>
//       )}

//       <button onClick={() => navigate("/products")}>
//         Back to Products
//       </button>
//     </div>
//   )
// }

// // Add Product Page
// function AddProduct() {
//   const navigate = useNavigate()

//   const [id, setId] = useState("")
//   const [name, setName] = useState("")
//   const [price, setPrice] = useState("")
//   const [image, setImage] = useState("")
//   const [message, setMessage] = useState("")

//   function saveProduct(event) {
//     event.preventDefault()
//     setMessage("")

//     const product = {
//       id: Number(id),
//       name: name,
//       price: Number(price),
//       image: image
//     }

//     fetch(`${API_URL}/products`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify(product)
//     })
//       .then(async (response) => {
//         const data = await response.json()

//         if (!response.ok) {
//           throw new Error(
//             data.detail || "Failed to add product"
//           )
//         }

//         return data
//       })
//       .then(() => {
//         alert("Product added successfully!")

//         setId("")
//         setName("")
//         setPrice("")
//         setImage("")

//         navigate("/products")
//       })
//       .catch((error) => {
//         console.error("Error adding product:", error)
//         setMessage(error.message)
//       })
//   }

//   return (
//     <div>
//       <h1>Add Product</h1>

//       <form onSubmit={saveProduct}>
//         <input
//           type="number"
//           placeholder="Product ID"
//           value={id}
//           onChange={(e) => setId(e.target.value)}
//           required
//         />

//         <br /><br />

//         <input
//           type="text"
//           placeholder="Product Name"
//           value={name}
//           onChange={(e) => setName(e.target.value)}
//           required
//         />

//         <br /><br />

//         <input
//           type="number"
//           placeholder="Price"
//           value={price}
//           onChange={(e) => setPrice(e.target.value)}
//           required
//           min="0"
//           step="0.01"
//         />

//         <br /><br />

//         <input
//           type="url"
//           placeholder="Image URL"
//           value={image}
//           onChange={(e) => setImage(e.target.value)}
//           required
//         />

//         <br /><br />

//         <button type="submit">
//           Save Product
//         </button>
//       </form>

//       {message && <p>{message}</p>}
//     </div>
//   )
// }

// // About Page
// function About() {
//   return (
//     <div>
//       <h1>About</h1>
//       <p>Simple React Product Store connected to FastAPI.</p>
//     </div>
//   )
// }

// // Main App
// function App() {
//   return (
//     <BrowserRouter>
//       <nav>
//         <Link to="/">Home</Link>
//         {" | "}
//         <Link to="/products">Products</Link>
//         {" | "}
//         <Link to="/about">About</Link>
//         {" | "}
//         <Link to="/addproducts">Add Products</Link>
//       </nav>

//       <hr />

//       <Routes>
//         <Route path="/" element={<Home />} />

//         <Route
//           path="/products"
//           element={<Products />}
//         />

//         <Route
//           path="/products/:id"
//           element={<ProductDetails />}
//         />

//         <Route
//           path="/about"
//           element={<About />}
//         />

//         <Route
//           path="/addproducts"
//           element={<AddProduct />}
//         />
//       </Routes>
//     </BrowserRouter>
//   )
// }

// export default App





// // import {
// //   BrowserRouter,
// //   Routes,
// //   Route,
// //   Link,
// //   useParams,
// //   useNavigate
// // } from "react-router-dom"
// // import { useEffect, useState } from "react"
// // function Home() {
// //   const navigate = useNavigate()

// //   return (
// //     <div>
// //       <h1>Home</h1>

// //       <button onClick={() => navigate("/products")}>
// //         View Products
// //       </button>
// //     </div>
// //   )
// // }

// // function Products() {
// //   const [products, setProducts] = useState([])

// //   useEffect(() => {
// //     fetch("http://127.0.0.1:8000/products")
// //       .then((response) => response.json())
// //       .then((data) => {
// //         setProducts(data)
// //       })
// //       .catch((error) => {
// //         console.error("Error fetching products:", error)
// //       })
// //   }, [])

// //   return (
// //     <div>
// //       <h1>Product Store</h1>

// //       {products.map((product) => (
// //         <div key={product.id}>
// //           <img
// //             src={product.image}
// //             alt={product.name}
// //             width="180"
// //           />

// //           <h2>{product.name}</h2>

// //           <p>Price: ₹{product.price}</p>

// //           <hr />
// //         </div>
// //       ))}
// //     </div>
// //   )
// // }

// // function ProductDetails() {
// //   const { id } = useParams()
// //   const navigate = useNavigate()

// //   return (
// //     <div>
// //       <h1>Product Details</h1>

// //       <p>Product ID: {id}</p>

// //       <button onClick={() => navigate("/products")}>
// //         Back to Products
// //       </button>
// //     </div>
// //   )
// // }

// // function AddProduct({ products, setProducts }) {
// //   const navigate = useNavigate()

// //   const [id, setId] = useState("")
// //   const [name, setName] = useState("")
// //   const [price, setPrice] = useState("")
// //   const [image, setImage] = useState("")

// //   function saveProduct(event) {
// //     event.preventDefault()

// //     const product = {
// //       id: Number(id),
// //       name: name,
// //       price: Number(price),
// //       image: image
// //     }

// //     setProducts([...products, product])

// //     navigate("/products")
// //   }

// //   return (
// //     <div>
// //       <h1>Add Product</h1>

// //       <form onSubmit={saveProduct}>
// //         <input
// //           type="number"
// //           placeholder="Product ID"
// //           value={id}
// //           onChange={(e) => setId(e.target.value)}
// //         />

// //         <br /><br />

// //         <input
// //           type="text"
// //           placeholder="Product Name"
// //           value={name}
// //           onChange={(e) => setName(e.target.value)}
// //         />

// //         <br /><br />

// //         <input
// //           type="number"
// //           placeholder="Price"
// //           value={price}
// //           onChange={(e) => setPrice(e.target.value)}
// //         />

// //         <br /><br />

// //         <input
// //           type="text"
// //           placeholder="Image URL"
// //           value={image}
// //           onChange={(e) => setImage(e.target.value)}
// //         />

// //         <br /><br />

// //         <button type="submit">
// //           Save Product
// //         </button>
// //       </form>
// //     </div>
// //   )
// // }


// // function About() {
// //   return <h1>About</h1>
// // }

// // function App() {
// //   return (
// //     <BrowserRouter>
// //       <nav>
// //         <Link to="/">Home</Link>
// //         {" | "}
// //         <Link to="/products">Products</Link>
// //         {" | "}
// //         <Link to="/about">About</Link>
// //         {"|"}
// //         <Link to="/addproducts">AddProducts</Link>
// //       </nav>

// //       <Routes>
// //         <Route path="/" element={<Home />} />
// //         <Route path="/products" element={<Products />} />
// //         <Route path="/products/:id" element={<ProductDetails />} />
// //         <Route path="/about" element={<About />} />
// //         <Route path="/addproducts" element={<AddProducts/>}/>
// //       </Routes>
// //     </BrowserRouter>
// //   )
// // }

// // export default App



// // import { useState } from "react"
// // import {
// //   BrowserRouter,
// //   Routes,
// //   Route,
// //   Link,
// //   useParams,
// //   useNavigate
// // } from "react-router-dom"


// // const initialProducts = [
// //   {
// //     id: 1,
// //     name: "Wireless Mouse",
// //     price: 1200,
// //     image: "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46"
// //   },
// //   {
// //     id: 2,
// //     name: "Mechanical Keyboard",
// //     price: 3500,
// //     image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3"
// //   },
// //   {
// //     id: 3,
// //     name: "Monitor",
// //     price: 12000,
// //     image: "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf"
// //   }
// // ]


// // function Home() {
// //   const navigate = useNavigate()

// //   return (
// //     <div>
// //       <h1>Home</h1>
// //       <p>Welcome to the Product Application</p>

// //       <button onClick={() => navigate("/products")}>
// //         View Products
// //       </button>
// //     </div>
// //   )
// // }


// // function Products({ products }) {
// //   return (
// //     <div>
// //       <h1>Products</h1>

// //       {products.map((product) => (
// //         <div key={product.id}>
// //           <img
// //             src={product.image}
// //             alt={product.name}
// //             width="150"
// //           />

// //           <h3>{product.name}</h3>

// //           <p>Price: ₹{product.price}</p>

// //           <Link to={`/products/${product.id}`}>
// //             View Details
// //           </Link>

// //           <hr />
// //         </div>
// //       ))}
// //     </div>
// //   )
// // }


// // function ProductDetails({ products }) {
// //   const { id } = useParams()
// //   const navigate = useNavigate()

// //   const product = products.find(
// //     (product) => product.id === Number(id)
// //   )

// //   if (!product) {
// //     return <p>Product not found</p>
// //   }

// //   return (
// //     <div>
// //       <h1>Product Details</h1>

// //       <img
// //         src={product.image}
// //         alt={product.name}
// //         width="200"
// //       />

// //       <h2>{product.name}</h2>

// //       <p>Product ID: {product.id}</p>

// //       <p>Price: ₹{product.price}</p>

// //       <button onClick={() => navigate("/products")}>
// //         Back to Products
// //       </button>
// //     </div>
// //   )
// // }


// // function AddProduct({ products, setProducts }) {
// //   const navigate = useNavigate()

// //   const [id, setId] = useState("")
// //   const [name, setName] = useState("")
// //   const [price, setPrice] = useState("")
// //   const [image, setImage] = useState("")

// //   function saveProduct(event) {
// //     event.preventDefault()

// //     const product = {
// //       id: Number(id),
// //       name: name,
// //       price: Number(price),
// //       image: image
// //     }

// //     setProducts([...products, product])

// //     navigate("/products")
// //   }

// //   return (
// //     <div>
// //       <h1>Add Product</h1>

// //       <form onSubmit={saveProduct}>
// //         <input
// //           type="number"
// //           placeholder="Product ID"
// //           value={id}
// //           onChange={(e) => setId(e.target.value)}
// //         />

// //         <br /><br />

// //         <input
// //           type="text"
// //           placeholder="Product Name"
// //           value={name}
// //           onChange={(e) => setName(e.target.value)}
// //         />

// //         <br /><br />

// //         <input
// //           type="number"
// //           placeholder="Price"
// //           value={price}
// //           onChange={(e) => setPrice(e.target.value)}
// //         />

// //         <br /><br />

// //         <input
// //           type="text"
// //           placeholder="Image URL"
// //           value={image}
// //           onChange={(e) => setImage(e.target.value)}
// //         />

// //         <br /><br />

// //         <button type="submit">
// //           Save Product
// //         </button>
// //       </form>
// //     </div>
// //   )
// // }


// // function About() {
// //   return (
// //     <div>
// //       <h1>About</h1>
// //       <p>Simple React Product Application</p>
// //     </div>
// //   )
// // }


// // function App() {
// //   const [products, setProducts] = useState(initialProducts)

// //   return (
// //     <BrowserRouter>

// //       <nav>
// //         <Link to="/">Home</Link>
// //         {" | "}
// //         <Link to="/products">Products</Link>
// //         {" | "}
// //         <Link to="/add-product">Add Product</Link>
// //         {" | "}
// //         <Link to="/about">About</Link>
// //       </nav>

// //       <hr />

// //       <Routes>

// //         <Route
// //           path="/"
// //           element={<Home />}
// //         />

// //         <Route
// //           path="/products"
// //           element={
// //             <Products products={products} />
// //           }
// //         />

// //         <Route
// //           path="/products/:id"
// //           element={
// //             <ProductDetails products={products} />
// //           }
// //         />

// //         <Route
// //           path="/add-product"
// //           element={
// //             <AddProduct
// //               products={products}
// //               setProducts={setProducts}
// //             />
// //           }
// //         />

// //         <Route
// //           path="/about"
// //           element={<About />}
// //         />

// //       </Routes>

// //     </BrowserRouter>
// //   )
// // }

// // export default App



import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useParams,
  useNavigate
} from "react-router-dom"

import { useEffect, useState } from "react"

const API_URL = "http://127.0.0.1:8000/products"

// Home Page
function Home() {
  const navigate = useNavigate()

  return (
    <div>
      <h1>Home</h1>
      <p>Welcome to the Product Store</p>

      <button onClick={() => navigate("/products")}>
        View Products
      </button>
    </div>
  )
}

// Products Page - GET, PUT and DELETE
function Products() {
  const [products, setProducts] = useState([])
  const [error, setError] = useState("")
  const [editingId, setEditingId] = useState(null)

  const [name, setName] = useState("")
  const [price, setPrice] = useState("")
  const [image, setImage] = useState("")

  async function loadProducts() {
    try {
      const response = await fetch(API_URL)

      if (!response.ok) {
        throw new Error("Failed to load products")
      }

      const data = await response.json()
      setProducts(data)
      setError("")
    } catch (err) {
      setError("Could not load products. Check FastAPI.")
    }
  }

  useEffect(() => {
    loadProducts()
  }, [])

  // Start editing a product
  function startEdit(product) {
    setEditingId(product.id)
    setName(product.name)
    setPrice(String(product.price))
    setImage(product.image)
    setError("")
  }

  // PUT - Update product
  async function updateProduct(event) {
    event.preventDefault()
    setError("")

    const updatedProduct = {
      id: editingId,
      name,
      price: Number(price),
      image
    }

    try {
      const response = await fetch(
        `${API_URL}/${editingId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(updatedProduct)
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Update failed")
      }

      setEditingId(null)
      await loadProducts()
      alert("Product updated successfully!")
    } catch (err) {
      setError(err.message)
    }
  }

  // DELETE - Remove product
  async function removeProduct(id) {
    if (!window.confirm("Are you sure you want to delete this product?")) {
      return
    }

    setError("")

    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Delete failed")
      }

      setProducts((current) =>
        current.filter((product) => product.id !== id)
      )

      if (editingId === id) {
        setEditingId(null)
      }

      alert("Product deleted successfully!")
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h1>Product Store</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {products.map((product) => (
        <div key={product.id}>
          <img
            src={product.image}
            alt={product.name}
            width="180"
          />

          <h2>{product.name}</h2>
          <p>Product ID: {product.id}</p>
          <p>Price: ₹{product.price}</p>

          <Link to={`/products/${product.id}`}>
            View Details
          </Link>

          {" "}

          <button onClick={() => startEdit(product)}>
            Edit
          </button>

          {" "}

          <button onClick={() => removeProduct(product.id)}>
            Delete
          </button>

          {editingId === product.id && (
            <form onSubmit={updateProduct}>
              <h3>Edit Product</h3>

              <input
                type="text"
                placeholder="Product Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />

              <br /><br />

              <input
                type="number"
                placeholder="Price"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                min="0"
                step="0.01"
                required
              />

              <br /><br />

              <input
                type="url"
                placeholder="Image URL"
                value={image}
                onChange={(e) => setImage(e.target.value)}
                required
              />

              <br /><br />

              <button type="submit">
                Save Changes
              </button>

              {" "}

              <button
                type="button"
                onClick={() => setEditingId(null)}
              >
                Cancel
              </button>
            </form>
          )}

          <hr />
        </div>
      ))}
    </div>
  )
}

// Product Details Page - GET by ID
function ProductDetails() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [product, setProduct] = useState(null)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchProduct() {
      try {
        const response = await fetch(`${API_URL}/${id}`)

        if (!response.ok) {
          throw new Error("Product not found")
        }

        const data = await response.json()
        setProduct(data)
      } catch (err) {
        setError(err.message)
      }
    }

    fetchProduct()
  }, [id])

  return (
    <div>
      <h1>Product Details</h1>

      {error && <p>{error}</p>}

      {product && (
        <div>
          <img
            src={product.image}
            alt={product.name}
            width="200"
          />

          <h2>{product.name}</h2>
          <p>Product ID: {product.id}</p>
          <p>Price: ₹{product.price}</p>
        </div>
      )}

      <button onClick={() => navigate("/products")}>
        Back to Products
      </button>
    </div>
  )
}

// Add Product Page - POST
function AddProduct() {
  const navigate = useNavigate()

  const [id, setId] = useState("")
  const [name, setName] = useState("")
  const [price, setPrice] = useState("")
  const [image, setImage] = useState("")
  const [message, setMessage] = useState("")

  async function saveProduct(event) {
    event.preventDefault()
    setMessage("")

    const product = {
      id: Number(id),
      name,
      price: Number(price),
      image
    }

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(product)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to add product")
      }

      alert("Product added successfully!")
      navigate("/products")
    } catch (err) {
      setMessage(err.message)
    }
  }

  return (
    <div>
      <h1>Add Product</h1>

      <form onSubmit={saveProduct}>
        <input
          type="number"
          placeholder="Product ID"
          value={id}
          onChange={(e) => setId(e.target.value)}
          required
          min="1"
        />

        <br /><br />

        <input
          type="text"
          placeholder="Product Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <br /><br />

        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
          min="0"
          step="0.01"
        />

        <br /><br />

        <input
          type="url"
          placeholder="Image URL"
          value={image}
          onChange={(e) => setImage(e.target.value)}
          required
        />

        <br /><br />

        <button type="submit">
          Save Product
        </button>
      </form>

      {message && (
        <p style={{ color: "red" }}>{message}</p>
      )}
    </div>
  )
}

// About Page
function About() {
  return (
    <div>
      <h1>About</h1>
      <p>Simple React Product Store connected to FastAPI.</p>
    </div>
  )
}

// Main App
function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        {" | "}
        <Link to="/products">Products</Link>
        {" | "}
        <Link to="/about">About</Link>
        {" | "}
        <Link to="/addproducts">Add Products</Link>
      </nav>

      <hr />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetails />} />
        <Route path="/about" element={<About />} />
        <Route path="/addproducts" element={<AddProduct />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
