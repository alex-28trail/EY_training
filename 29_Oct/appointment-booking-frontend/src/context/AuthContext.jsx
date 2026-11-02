import { createContext, useContext, useState } from "react"

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  )

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user")
    return savedUser ? JSON.parse(savedUser) : null
  })

  function login(accessToken, userData) {
    localStorage.setItem("access_token", accessToken)
    localStorage.setItem("user", JSON.stringify(userData))

    setToken(accessToken)
    setUser(userData)
  }

  function logout() {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user")

    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated: !!token,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}