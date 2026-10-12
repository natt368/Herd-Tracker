# Herd
Herd record keeping

**Rangebook** — a single-file cow/calf herd ledger (`index.html`). Open it in a browser; data is stored locally (`localStorage`) or synced to Google Drive via an Apps Script web app (see Settings → Manage Data in the app).

**Live app:** https://natt368.github.io/Herd-Tracker/

**Shared data for a crew on Google Workspace:** open the app's Settings → Manage Data → *Copy Workspace script*, paste it at script.new, and deploy as a Web app (Execute as **Me**, access **Anyone within your organization**). The Web app URL serves Rangebook inside your Workspace, with everyone signing in with their own Google account and sharing one data file in the deployer's Drive. The deployer can pick which Drive folder holds that file, and dated backups go to a *Rangebook Backups* folder next to it — every minute while the app is open (when something changed), or on demand with *Back up now*.

Hosted with GitHub Pages: on every push to `main`, the Pages workflow runs `build.py`, which publishes `index.html` with the app script packed so Google's HtmlService can't alter it. Anything merged into `main` goes live within a minute or two.
