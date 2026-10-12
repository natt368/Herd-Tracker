"""Build the published copy of Rangebook into _site/.

The Google Workspace edition serves this page through Apps Script's
HtmlService, which rewrites inline scripts on the way through and can break
the app's code. To keep it intact, the main app script is published as a
base64 string that a tiny loader decodes and runs in the browser.
index.html in the repo stays readable; only the published copy is packed.
"""
import base64, os, re, shutil, sys

SRC = 'index.html'
OUT = sys.argv[1] if len(sys.argv) > 1 else '_site'

LOADER = ('<script>(function(){var b=atob("%s"),u=new Uint8Array(b.length);'
          'for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);'
          'var s=document.createElement("script");s.text=new TextDecoder().decode(u);'
          '(document.body||document.documentElement).appendChild(s);})();</script>')

html = open(SRC, encoding='utf-8').read()
# The main app script is the inline <script> that starts with the STATE banner comment.
m = re.search(r'<script>\n(/\* =+\s*\n?\s*STATE.*?)</script>', html, re.S)
if not m:
    m = re.search(r'<script>(\s*/\*\s*=+[\s\S]*?)</script>', html)
if not m:
    sys.exit('build.py: could not find the main app script')
packed = LOADER % base64.b64encode(m.group(1).encode('utf-8')).decode('ascii')
html = html[:m.start()] + packed + html[m.end():]

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
for f in ('README.md', '.nojekyll'):
    if os.path.exists(f):
        shutil.copy(f, OUT)
print('built %s/index.html (app script packed, %d bytes)' % (OUT, len(m.group(1))))
