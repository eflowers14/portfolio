// main.jsx: punto de entrada de la aplicación React.
// Se encarga de montar (mostrar) el componente <App /> dentro de la
// etiqueta <div id="root"> que está en index.html.
import { StrictMode } from 'react'
import { createRoot, hydrateRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

const rootElement = document.getElementById('root')
const dataElement = document.getElementById('__PORTFOLIO_DATA__')

if (dataElement) {
  let payload
  try {
    payload = JSON.parse(dataElement.textContent)
  } catch (error) {
    throw new Error('No se pudieron leer los datos prerenderizados.', {
      cause: error,
    })
  }

  dataElement.remove()
  hydrateRoot(
    rootElement,
    <StrictMode>
      <App initialData={payload.data} year={payload.year} />
    </StrictMode>,
  )
} else {
  createRoot(rootElement).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}
