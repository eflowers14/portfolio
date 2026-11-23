function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0
}

export function validatePortfolioData(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    throw new Error('La API debe devolver un objeto JSON.')
  }

  const { profile, skills, projects, social_links: socialLinks } = data
  if (
    !profile ||
    !isNonEmptyString(profile.name) ||
    !isNonEmptyString(profile.summary) ||
    !isNonEmptyString(profile.email)
  ) {
    throw new Error('La API no incluye los datos obligatorios del perfil.')
  }

  if (
    !Array.isArray(skills) ||
    skills.length === 0 ||
    !skills.every(
      (group) =>
        isNonEmptyString(group?.category) &&
        Array.isArray(group.items) &&
        group.items.length > 0 &&
        group.items.every(isNonEmptyString),
    )
  ) {
    throw new Error('La API no incluye una lista válida de habilidades.')
  }

  if (
    !Array.isArray(projects) ||
    projects.length === 0 ||
    !projects.every(
      (project) =>
        (typeof project?.id === 'number' || isNonEmptyString(project?.id)) &&
        isNonEmptyString(project.title) &&
        typeof project.description === 'string' &&
        Array.isArray(project.technologies) &&
        project.technologies.every(isNonEmptyString) &&
        (project.url_github == null || typeof project.url_github === 'string') &&
        (project.url_demo == null || typeof project.url_demo === 'string') &&
        (project.image == null || typeof project.image === 'string'),
    )
  ) {
    throw new Error('La API no incluye una lista válida de proyectos.')
  }

  if (
    !Array.isArray(socialLinks) ||
    socialLinks.length === 0 ||
    !socialLinks.every(
      (link) =>
        isNonEmptyString(link?.label) &&
        isNonEmptyString(link.url) &&
        isNonEmptyString(link.icon),
    )
  ) {
    throw new Error('La API no incluye una lista válida de redes sociales.')
  }

  return data
}
