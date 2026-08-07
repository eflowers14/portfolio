// Hero.jsx: sección "Inicio". Es lo primero que ve el visitante.
// Muestra el nombre, el título y dos botones de acción (CTA).
export default function Hero({ profile }) {
  return (
    <section id="inicio" className="hero">
      <div className="hero-grid" aria-hidden="true" />
      <div className="container hero-content">
        {/* Pequeña etiqueta sobre el nombre */}
        <p className="hero-eyebrow">Ingeniero Informático</p>

        {/* Nombre grande */}
        <h1 className="hero-name">{profile.name}</h1>

        {/* Título destacado con acento azul */}
        <p className="hero-title">
          Construyo software claro, honesto y con los datos{' '}
          <span className="accent">protegidos</span>.
        </p>

        {/* Botones de acción (Call To Action) */}
        <div className="hero-actions">
          <a href="#proyectos" className="btn btn--primary">
            Ver proyectos
          </a>
          <a href="#contacto" className="btn btn--ghost">
            Contáctame
          </a>
        </div>
      </div>
    </section>
  )
}
