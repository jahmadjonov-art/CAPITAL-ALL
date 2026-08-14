// Minimal service worker: enough to make the app installable and to survive a
// dead zone, without the classic PWA failure where users get pinned to a stale
// build forever.
//
//  - Navigations are network-first, so a fresh deploy is picked up immediately
//    and the cached shell is only used when the network actually fails.
//  - Vite's hashed assets are cache-first, since their filenames change on
//    every build and can never go stale.
//  - Anything cross-origin (every Supabase call) is left alone entirely, so
//    your data is never served from a cache.

const VERSION = 'cam-v1'
const SHELL = new URL('./', self.location).pathname

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(VERSION).then((cache) => cache.add(SHELL)))
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return

  const url = new URL(request.url)
  if (url.origin !== self.location.origin) return

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone()
          caches.open(VERSION).then((cache) => cache.put(SHELL, copy))
          return response
        })
        .catch(() => caches.match(SHELL))
    )
    return
  }

  event.respondWith(
    caches.match(request).then(
      (hit) =>
        hit ||
        fetch(request).then((response) => {
          if (response.ok) {
            const copy = response.clone()
            caches.open(VERSION).then((cache) => cache.put(request, copy))
          }
          return response
        })
    )
  )
})
