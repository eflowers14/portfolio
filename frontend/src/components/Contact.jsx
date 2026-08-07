// Contact.jsx: sección "Contacto".
// Muestra el email en un botón y las redes sociales como iconos.
import Icon from './icons.jsx'

export default function Contact({ profile, socialLinks }) {
  return (
    <section id="contacto" className="section section--contact">
      <div className="container">
        <p className="section-eyebrow">Contacto</p>
        <h2 className="section-title">Hablemos</h2>

        <p className="contact-lead">
          ¿Tienes una idea, un proyecto o simplemente quieres saludar?
          Escríbeme, respondo con gusto.
        </p>

        {/* Botón de email: mailto: abre el programa de correo */}
        <a href={`mailto:${profile.email}`} className="btn btn--primary btn--big">
          <Icon name="email" />
          {profile.email}
        </a>

        {/* Redes sociales */}
        <div className="social-links">
          {socialLinks.map((link) => (
            <a
              key={link.url}
              href={link.url}
              target="_blank"
              rel="noreferrer"
              className="social-link"
              aria-label={link.label}
              title={link.label}
            >
              <Icon name={link.icon} />
              <span className="social-label">{link.label}</span>
            </a>
          ))}
        </div>
      </div>
    </section>
  )
}
