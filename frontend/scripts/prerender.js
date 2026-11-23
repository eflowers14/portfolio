import { readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import React from 'react'
import { renderToString } from 'react-dom/server'
import { createServer, loadEnv } from 'vite'
import { validatePortfolioData } from '../src/portfolioData.js'

const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const distIndexPath = path.join(frontendRoot, 'dist', 'index.html')
const apiBaseUrl =
  process.env.VITE_API_URL ||
  loadEnv('production', frontendRoot, '').VITE_API_URL ||
  'http://localhost:8000'

function serializeSafely(value) {
  return JSON.stringify(value)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029')
}

async function main() {
  let vite
  try {
    const apiUrl = `${apiBaseUrl.replace(/\/+$/, '')}/api/`
    let response
    try {
      response = await fetch(apiUrl)
    } catch (error) {
      throw new Error(`No se pudo consultar la API en ${apiUrl}: ${error.message}`, {
        cause: error,
      })
    }
    if (!response.ok) {
      throw new Error(`La API respondió HTTP ${response.status} en ${apiUrl}`)
    }

    let data
    try {
      data = validatePortfolioData(await response.json())
    } catch (error) {
      throw new Error(`Respuesta inválida de ${apiUrl}: ${error.message}`, {
        cause: error,
      })
    }

    vite = await createServer({
      configFile: path.join(frontendRoot, 'vite.config.js'),
      root: frontendRoot,
      appType: 'custom',
      server: { middlewareMode: true },
      logLevel: 'error',
    })

    const { default: App } = await vite.ssrLoadModule('/src/App.jsx')
    const year = new Date().getFullYear()
    const markup = renderToString(
      React.createElement(App, { initialData: data, year }),
    )
    const payload = serializeSafely({ data, year })
    let html = await readFile(distIndexPath, 'utf8')
    const rootPlaceholder = '<div id="root"></div>'

    if (!html.includes(rootPlaceholder)) {
      throw new Error(`No se encontró ${rootPlaceholder} en dist/index.html.`)
    }

    html = html.replace(rootPlaceholder, `<div id="root">${markup}</div>`)
    html = html.replace(
      '</body>',
      `<script id="__PORTFOLIO_DATA__" type="application/json">${payload}</script>\n  </body>`,
    )
    await writeFile(distIndexPath, html)
    console.log(`Prerender completado con datos de ${apiUrl}`)
  } catch (error) {
    console.error(`Error al prerenderizar el portfolio: ${error.message}`)
    process.exitCode = 1
  } finally {
    if (vite) await vite.close()
  }
}

await main()
