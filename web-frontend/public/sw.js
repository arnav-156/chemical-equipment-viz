const CACHE_NAME = 'chemviz-v1.0.0';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico'
];

// Install - cache resources
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .catch((err) => console.error('[SW] Cache failed:', err))
  );
  self.skipWaiting();
});

// Activate - clean old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch - offline-first strategy
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle static assets
  event.respondWith(
    caches.match(request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(request)
          .then((response) => {
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => cache.put(request, responseToCache));
            return response;
          })
          .catch(() => {
            if (request.mode === 'navigate') {
              return caches.match('/');
            }
          });
      })
  );
});

// Handle API requests with offline support
async function handleApiRequest(request) {
  const url = new URL(request.url);
  const cacheKey = `api-${url.pathname}`;

  try {
    const networkResponse = await fetch(request.clone());
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(cacheKey, networkResponse.clone());
      broadcastOnlineStatus(true);
      return networkResponse;
    }
  } catch (error) {
    console.log('[SW] Network failed, trying cache');
  }

  const cachedResponse = await caches.match(cacheKey);
  if (cachedResponse) {
    broadcastOnlineStatus(false);
    return cachedResponse;
  }

  broadcastOnlineStatus(false);
  return new Response(
    JSON.stringify({ error: 'Offline - No cached data', offline: true }),
    { status: 503, headers: { 'Content-Type': 'application/json' } }
  );
}

function broadcastOnlineStatus(isOnline) {
  self.clients.matchAll().then((clients) => {
    clients.forEach((client) => {
      client.postMessage({ type: 'ONLINE_STATUS', isOnline });
    });
  });
}
