// main.jsx: punto de entrada de la aplicación React.
// Se encarga de montar (mostrar) el componente <App /> dentro de la
// etiqueta <div id="root"> que está en index.html.
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// createRoot busca el elemento <div id="root"> y lo "monta"
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
