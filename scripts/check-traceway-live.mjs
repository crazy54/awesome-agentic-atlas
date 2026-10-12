#!/usr/bin/env node
// Live Traceway check: loads each URL in headless Chrome and passes only when the
// page fetched its Traceway configuration (HTTP 200) and the SDK delivered at least
// one report to traceway.jeremyfhall.com/api/report (HTTP 200).
//
//   node check-traceway-live.mjs https://blog.jeremyfhall.com/ [more URLs]
//
// No dependencies: it drives Chrome over the DevTools protocol with Node's built-in
// WebSocket (Node 22+). Set CHROME_PATH if Chrome is not in a standard location,
// TRACEWAY_CHECK_TIMEOUT (seconds per attempt, default 60) to wait longer for the first
// report, and TRACEWAY_CHECK_ATTEMPTS (default 1) to retry a failing URL 30 seconds
// later, which covers a deploy that is still propagating.
import { spawn } from 'node:child_process'
import { existsSync, mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import path from 'node:path'

const urls = process.argv.slice(2)
if (!urls.length) {
  console.error('usage: node check-traceway-live.mjs <url> [url...]')
  process.exit(2)
}
if (typeof WebSocket === 'undefined') {
  console.error('Node 22 or newer is required (global WebSocket).')
  process.exit(2)
}
const timeoutMs = Number(process.env.TRACEWAY_CHECK_TIMEOUT || 60) * 1000
const attempts = Math.max(1, Number(process.env.TRACEWAY_CHECK_ATTEMPTS || 1))
const configPath = '/api/telemetry-config'
const reportUrl = 'https://traceway.jeremyfhall.com/api/report'

function findChrome() {
  const candidates = [
    process.env.CHROME_PATH,
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  ].filter(Boolean)
  const found = candidates.find((candidate) => existsSync(candidate))
  if (!found) throw new Error('Chrome not found; set CHROME_PATH')
  return found
}

async function launch() {
  const profile = mkdtempSync(path.join(tmpdir(), 'traceway-check-'))
  const chrome = spawn(findChrome(), [
    '--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--no-sandbox', 'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] })
  const endpoint = await new Promise((resolve, reject) => {
    let log = ''
    const timer = setTimeout(() => reject(new Error(`Chrome did not start:\n${log}`)), 20000)
    chrome.stderr.on('data', (chunk) => {
      log += chunk
      const match = /DevTools listening on (ws:\/\/\S+)/.exec(log)
      if (match) { clearTimeout(timer); resolve(match[1]) }
    })
    chrome.on('exit', (code) => reject(new Error(`Chrome exited (${code}):\n${log}`)))
  })
  const socket = new WebSocket(endpoint)
  await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject })
  let nextId = 0
  const pending = new Map()
  const listeners = new Set()
  socket.onmessage = ({ data }) => {
    const message = JSON.parse(data)
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id)
      pending.delete(message.id)
      message.error ? reject(new Error(message.error.message)) : resolve(message.result)
    } else for (const listener of listeners) listener(message)
  }
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const id = ++nextId
    pending.set(id, { resolve, reject })
    socket.send(JSON.stringify({ id, method, params, sessionId }))
  })
  const close = () => {
    try { socket.close() } catch {}
    chrome.kill()
    try { rmSync(profile, { recursive: true, force: true }) } catch {}
  }
  return { send, listeners, close }
}

async function check(browser, url) {
  const { targetId } = await browser.send('Target.createTarget', { url: 'about:blank' })
  const { sessionId } = await browser.send('Target.attachToTarget', { targetId, flatten: true })
  const requests = new Map()
  const result = { config: null, reports: [], failures: [], exceptions: [] }
  const done = new Promise((resolve) => {
    const listener = ({ method, params, sessionId: from }) => {
      if (from !== sessionId) return
      if (method === 'Network.requestWillBeSent') requests.set(params.requestId, params.request)
      if (method === 'Network.responseReceived') {
        const request = requests.get(params.requestId)
        if (!request) return
        if (request.url.includes(configPath)) result.config = params.response.status
        if (request.url.startsWith(reportUrl) && request.method === 'POST') result.reports.push(params.response.status)
      }
      if (method === 'Network.loadingFailed') {
        const request = requests.get(params.requestId)
        if (request && (request.url.includes(configPath) || request.url.startsWith(reportUrl))) {
          result.failures.push(`${request.method} ${request.url}: ${params.errorText}${params.corsErrorStatus ? ` (CORS ${params.corsErrorStatus.corsError})` : ''}`)
        }
      }
      if (method === 'Runtime.exceptionThrown') result.exceptions.push(params.exceptionDetails.exception?.description || params.exceptionDetails.text)
      if (result.config === 200 && result.reports.includes(200)) { browser.listeners.delete(listener); resolve() }
    }
    browser.listeners.add(listener)
    setTimeout(() => { browser.listeners.delete(listener); resolve() }, timeoutMs)
  })
  await browser.send('Network.enable', {}, sessionId)
  await browser.send('Runtime.enable', {}, sessionId)
  await browser.send('Page.enable', {}, sessionId)
  await browser.send('Page.navigate', { url }, sessionId)
  await done
  await browser.send('Target.closeTarget', { targetId })
  return result
}

const browser = await launch()
let failed = false
try {
  for (const url of urls) {
    let result, ok = false
    for (let attempt = 1; attempt <= attempts && !ok; attempt++) {
      if (attempt > 1) {
        console.log(`  retrying in 30s (attempt ${attempt} of ${attempts})`)
        await new Promise((resolve) => setTimeout(resolve, 30000))
      }
      result = await check(browser, url)
      ok = result.config === 200 && result.reports.includes(200)
    }
    failed ||= !ok
    console.log(`${ok ? 'PASS' : 'FAIL'} ${url}`)
    console.log(`  telemetry config: ${result.config ?? 'no response'}`)
    console.log(`  reports to Traceway: ${result.reports.length ? result.reports.join(', ') : 'none'}`)
    for (const failure of result.failures) console.log(`  failed request: ${failure}`)
    for (const exception of result.exceptions.slice(0, 5)) console.log(`  page exception: ${exception.split('\n')[0]}`)
  }
} finally {
  browser.close()
}
process.exit(failed ? 1 : 0)
