// Navbar.jsx: barra de navegación FIJA en la parte superior.
// En móvil se colapsa en un botón "hamburguesa".
import { useState } from 'react'

// Lista de secciones. 'href' es el ancla (#id) de cada sección.
const links = [
  { label: 'Inicio', href: '#inicio' },
  { label: 'Sobre mí', href: '#sobre-mi' },
  { label: 'Proyectos', href: '#proyectos' },
  { label: 'Contacto', href: '#contacto' },
]

export default function Navbar() {
  // 'open' controla si el menú móvil está desplegado o no
  const [open, setOpen] = useState(false)

  return (
    <header className="navbar">
      <nav className="nav-container">
        {/* Logo / marca: lleva al inicio */}
        <a href="#inicio" className="nav-logo" onClick={() => setOpen(false)}>
          <img className="nav-logo-badge" src="profileHide.jpg"></img>
          <span className="nav-logo-text">Enrique Flores</span>
        </a>

        {/* Enlaces (versión escritorio) */}
        <ul className={`nav-links ${open ? 'nav-links--open' : ''}`}>
          {links.map((link) => (
            <li key={link.href}>
              <a href={link.href} onClick={() => setOpen(false)}>
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Botón hamburguesa (solo visible en móvil) */}
        <button
          className="nav-toggle"
          aria-label="Abrir menú"
          aria-expanded={open}
          onClick={() => setOpen(!open)}
        >
          {/* Convertimos las 3 rayas del botón en una X cuando está abierto */}
          <span className={open ? 'bar bar--x1' : 'bar'} />
          <span className={open ? 'bar bar--x2' : 'bar'} />
          <span className={open ? 'bar bar--x3' : 'bar'} />
        </button>
      </nav>
    </header>
  )
}
