# Herd
Herd record keeping

**Rangebook** — a cow/calf herd ledger that runs in the browser (`index.html`). Records are saved on each computer in the browser's IndexedDB, and backed up to a Google Drive folder you choose.

**Live app:** https://natt368.github.io/Herd-Tracker/

## Google Drive backup and sync

- Backs up one minute after the last change, loads the newest backup when the app opens, and keeps one dated copy per day (the last 14 by default).
- Several computers and phones can share one folder (a shared drive works too). Changes made on two computers are combined record by record, so nothing entered on either is lost, and deletions stay deleted.
- Before every upload, Range Book reads what is in Google Drive and merges it in first. It refuses an upload that would drop a record without a recorded delete, and checks the file reads back before sending it. Time stamps follow Google Drive's clock, so a computer with a wrong clock doesn't win or lose by mistake. Tabs on one computer take turns syncing and share each other's changes.
- Settings → Manage Data → **Change log**: every record added, changed or deleted, and every restore, with when, which computer and which Google account. Searchable, and downloads as CSV.
- Works without internet once the app has been opened online (`sw.js`). Changes back up by themselves when the internet returns.
- The badge in the top bar always says whether the data is safe. Tap it for details, *Back up now* and *Download backup file*.
- Settings → Manage Data: connect Google Drive, choose the folder, the backup options, *Restore from Google Drive…*, and download or restore a backup file.

Backups are gzip JSON files: `Range Book backup - <name>.json.gz`, plus `Range Book backup - <name> - YYYY-MM-DD.json.gz` for each day.

### One-time set-up: the Google Client ID

Whoever looks after the site creates an OAuth Client ID once:

1. In [Google Cloud](https://console.cloud.google.com/projectcreate), create a project (e.g. "Range Book").
2. APIs & Services → Library → **Google Drive API** → Enable.
3. OAuth consent screen: **External**, app name "Range Book", your email. Add everyone who will use it under **Test users**. (Everyone in one Google Workspace? Choose **Internal** instead.)
4. Credentials → Create credentials → **OAuth client ID** → **Web application**. Authorized JavaScript origin: `https://natt368.github.io`.
5. Put the Client ID in `config.js` (`googleClientId`) so every computer gets it, or paste it in Settings → Manage Data on each computer.

The first sign-in shows Google's "unverified app" warning; choose **Continue**.

**Coming from the older Apps Script sync?** Each computer keeps the herd it already had. Connect Google Drive and choose a folder: the first computer backs up its records there, and the others combine theirs with it. The old `rangebook-herd-data.json` file can also be loaded with *Restore backup file*.

## Hosting

GitHub Pages: on every push to `main`, the Pages workflow runs `build.py`, which copies `index.html`, `config.js`, `sw.js` and the icons into the site. Anything merged into `main` goes live within a minute or two.
