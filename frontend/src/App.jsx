import { useAppData } from './appData.jsx'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import About from './components/About.jsx'
import Projects from './components/Projects.jsx'
import Contact from './components/Contact.jsx'
import Footer from './components/Footer.jsx'

export default function App({ initialData, year = new Date().getFullYear() }) {
  const { data, loading, error } = useAppData(initialData)

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" aria-hidden="true" />
        <p>Cargando portfolio ...</p>
      </div>
    )
  }

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
  return (
    <>
      <Navbar />
      <main>
        <Hero profile={data.profile} />
        <About profile={data.profile} skills={data.skills} />
        <Projects projects={data.projects} />
        <Contact profile={data.profile} socialLinks={data.social_links} />
      </main>
      <Footer year={year} />
    </>
  )
}
