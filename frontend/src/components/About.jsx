// About.jsx: sección "Sobre mí".
// Muestra el resumen del perfil y las habilidades agrupadas por categoría.
export default function About({ profile, skills }) {
  return (
    <section id="sobre-mi" className="section">
      <div className="container">
        {/* Cabecera de la sección */}
        <p className="section-eyebrow">Sobre mí</p>
        <h2 className="section-title">Perfil</h2>

        <div className="about-grid">
          {/* Columna izquierda: resumen personal */}
          <div className="about-summary">
            <p>{profile.summary}</p>
          </div>

          {/* Columna derecha: habilidades por categoría */}
          <div className="about-skills">
            {skills.map((group) => (
              <div key={group.category} className="skill-group">
                <h3 className="skill-category">{group.category}</h3>
                <div className="skill-tags">
                  {group.items.map((skill) => (
                    <span key={skill} className="skill-tag">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
