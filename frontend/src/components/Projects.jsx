// Projects.jsx: sección "Proyectos".
// Muestra tarjetas con la imagen, descripción, tecnologías y enlaces.
import Icon from './icons.jsx'

export default function Projects({ projects }) {
  return (
    <section id="proyectos" className="section section--dark">
      <div className="container">
        <p className="section-eyebrow">Proyectos</p>
        <h2 className="section-title">Mi trabajo</h2>

        <div className="projects-grid">
          {projects.map((project) => (
            <article key={project.id} className="project-card">
              {/* Imagen del proyecto (si existe) */}
              {project.image ? (
                <div className="project-image-wrap">
                  <img
                    src={project.image}
                    alt={`Captura de ${project.title}`}
                    className="project-image"
                    loading="lazy"
                  />
                </div>
              ) : (
                <div className="project-image-placeholder">Sin imagen</div>
              )}

              <div className="project-body">
                <h3 className="project-title">{project.title}</h3>
                <p className="project-description">{project.description}</p>

                {/* Tecnologías como etiquetas */}
                <div className="project-tech">
                  {project.technologies.map((tech) => (
                    <span key={tech} className="tech-tag">
                      {tech}
                    </span>
                  ))}
                </div>

                {/* Enlaces a GitHub y demo */}
                <div className="project-links">
                  {project.url_github && (
                    <a
                      href={project.url_github}
                      target="_blank"
                      rel="noreferrer"
                      className="btn btn--small btn--dark"
                    >
                      <Icon name="github" />
                      Código
                    </a>
                  )}
                  {project.url_demo && (
                    <a
                      href={project.url_demo}
                      target="_blank"
                      rel="noreferrer"
                      className="btn btn--small btn--primary"
                    >
                      <Icon name="external" />
                      Demo
                    </a>
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
