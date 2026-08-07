// App.jsx: componente principal de la aplicación.
// 1) Pide los datos a la API de Django (fetch('/api/')).
// 2) Mientras carga, enseña un estado de carga.
// 3) Cuando llegan, pinta las secciones con esos datos.
import { useEffect, useState } from 'react'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import About from './components/About.jsx'
import Projects from './components/Projects.jsx'
import Contact from './components/Contact.jsx'
import Footer from './components/Footer.jsx'

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

export default function App() {
  // Estado de la aplicación:
  //   data    -> los datos que devuelve la API (o null si aún no hay)
  //   loading -> true mientras esperamos la respuesta
  //   error   -> mensaje si la petición falla
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // useEffect: se ejecuta UNA vez al montar el componente.
  useEffect(() => {
    // fetch es el navegador pidiendo una URL. En desarrollo, el proxy
    // de Vite reenvía '/api/' a Django (http://localhost:8000/api/).
    fetch(`${API_BASE_URL}/api/`)
      .then((response) => {
        // Si la respuesta no es correcta (ej: 404), lanzamos error
        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`)
        }
        return response.json()
      })
      .then((json) => {
        setData(json)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, []) // Los corchetes vacíos [] = solo se ejecuta una vez

  // ---------- Estado de carga ----------
  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" aria-hidden="true" />
        <p>Cargando portfolio ...</p>
      </div>
    )
  }

  // ---------- Estado de error ----------
  if (error) {
    return (
      <div className="loading">
        <p className="error">
          No se pudo conectar con la API. ¿Está corriendo Django en el puerto
          8000? <br />
          <small>Detalle: {error}</small>
        </p>
      </div>
    )
  }

  // ---------- Vista normal: toda la página ----------
  return (
    <>
      <Navbar />
      <main>
        <Hero profile={data.profile} />
        <About profile={data.profile} skills={data.skills} />
        <Projects projects={data.projects} />
        <Contact profile={data.profile} socialLinks={data.social_links} />
      </main>
      <Footer />
    </>
  )
}
