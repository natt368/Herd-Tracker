"""Build the published copy of Range Book into _site/ (GitHub Pages).

The app is index.html plus a few small files: config.js (site settings such as
the Google Client ID for Drive backup), sw.js (offline support) and the icons.
"""
import os, shutil, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else '_site'
FILES = ('index.html', 'config.js', 'sw.js', 'README.md', '.nojekyll',
         'favicon.svg', 'favicon.png', 'apple-touch-icon.png')

if not os.path.exists('index.html'):
    sys.exit('build.py: index.html not found')
os.makedirs(OUT, exist_ok=True)
for f in FILES:
    if os.path.exists(f):
        shutil.copy(f, OUT)
print('built %s/ (%d bytes of index.html)' % (OUT, os.path.getsize('index.html')))
