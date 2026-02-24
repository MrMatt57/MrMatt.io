var CACHE_NAME = 'photo-upload-v1';
var ASSETS = [
    '/upload/',
    '/upload/style.css',
    '/upload/app.js'
];

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(ASSETS);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', function(e) {
    e.waitUntil(
        caches.keys().then(function(names) {
            return Promise.all(
                names.filter(function(n) { return n !== CACHE_NAME; })
                    .map(function(n) { return caches.delete(n); })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', function(e) {
    var url = new URL(e.request.url);

    // Handle share target POST
    if (e.request.method === 'POST' && url.pathname === '/upload/') {
        e.respondWith(Response.redirect('/upload/?share-target'));
        e.waitUntil(
            e.request.formData().then(function(formData) {
                var photo = formData.get('photo');
                var caption = formData.get('caption') || '';
                if (photo) {
                    return storeSharedFile(photo, caption);
                }
            })
        );
        return;
    }

    // Network-first for all other requests
    e.respondWith(
        fetch(e.request).catch(function() {
            return caches.match(e.request);
        })
    );
});

function storeSharedFile(file, caption) {
    return caches.open('shared-photos').then(function(cache) {
        var response = new Response(JSON.stringify({
            name: file.name,
            type: file.type,
            caption: caption
        }));
        return Promise.all([
            cache.put('shared-photo-meta', response),
            cache.put('shared-photo-file', new Response(file))
        ]);
    });
}
