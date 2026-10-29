/* Range Book offline support. Network first, so a new version shows up straight away;
   if the network is slow (about 4 seconds) or offline, the copy saved last time opens instead.
   Google sign-in and Drive calls are never cached. */
const CACHE = 'rangebook-v1';
const SHELL = ['./', './index.html', './config.js', './favicon.svg', './favicon.png', './apple-touch-icon.png'];
const CDN_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com'];

self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=> Promise.all(SHELL.map(u=> c.add(u).catch(()=>{})))));
  self.skipWaiting();
});
self.addEventListener('activate', e=>{
  e.waitUntil(caches.keys()
    .then(keys=> Promise.all(keys.filter(k=> k!==CACHE).map(k=> caches.delete(k))))
    .then(()=> self.clients.claim()));
});
self.addEventListener('fetch', e=>{
  const req = e.request;
  if(req.method!=='GET') return;
  const url = new URL(req.url);
  if(url.origin!==self.location.origin && !CDN_HOSTS.includes(url.hostname)) return;
  e.respondWith(networkFirst(req));
});
async function networkFirst(req){
  const cache = await caches.open(CACHE);
  const net = fetch(req).then(res=>{
    if(res && (res.ok || res.type==='opaque')) cache.put(req, res.clone()).catch(()=>{});
    return res;
  });
  net.catch(()=>{});
  try{
    const res = await Promise.race([net, new Promise(r=> setTimeout(()=> r(null), 4000))]);
    if(res) return res;
  }catch(e){}
  const hit = await cache.match(req, { ignoreSearch: req.mode==='navigate' })
    || (req.mode==='navigate' ? await cache.match('./index.html') || await cache.match('./') : null);
  return hit || net;
}
