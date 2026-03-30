---
description: Diagnose deployment issues (stale config, connect failures, missing add-in)
---

# Debug a Claude Office deployment

You are helping an enterprise admin diagnose why the deployed add-in isn't
working right. Start by asking **what's wrong**, then route.

## Triage

Ask the admin to describe the symptom. Route by answer:

| Symptom | Section |
|---|---|
| Updated the manifest but users still see old config | [Stale config after update](#stale-config-after-update) |
| Add-in shows "Connection failed" | [Read the error paste](#read-the-error-paste) |
| Add-in doesn't appear in Excel/PowerPoint at all | [Add-in not visible](#add-in-not-visible) |
| Sign-in popup fails or loops | [Admin consent](#admin-consent) |

If they have an error paste from the add-in (the **Copy error details** button
on the connect-failed screen), always start there. It carries everything.

---

## Read the error paste

Paste structure:

```
Claude for Office connection failed (<Provider>)
Build: <sha>

<friendly message>

Request:
  <key>: <value actually sent>
  ...

Manifest params:
  <key>: <value the deployed manifest carries>
  ...

Raw error:
<SDK/HTTP error>
```

**What to check:**

- `Request:` vs `Manifest params:` delta. Keys are the same snake_case names
  in both blocks, so diff directly. If they differ, the user typed override
  values into the form. If they match, the manifest values went through
  unchanged.
- `Manifest params:` `m` key is the version tag (e.g. `unified-1.0.0.11`). If
  it's below what you last uploaded, the user is on a stale manifest. Go to
  [Stale config](#stale-config-after-update).
- `Raw error:` is the ground truth. Common patterns:
  - `invalid_client` (401, Google) → wrong `google_client_secret` for that
    `google_client_id`. Verify in GCP Console → Credentials.
  - `Load failed (<host>)` → network blocked at the WebView layer. Firewall
    needs to allow that host.
  - `STS AssumeRoleWithWebIdentity failed` → AWS IAM OIDC provider
    misconfigured or role trust policy wrong.
  - `HTTP 401/403` (gateway) → bad token or gateway rejected the key.

---

## Stale config after update

Two caches, two clocks:

| Layer | Who holds it | TTL | How to clear |
|---|---|---|---|
| Service | M365 Admin Center → Exchange Online → client | Up to **72h** for updates (24h for fresh deploys) | Wait, or redeploy with a fresh `<Id>` |
| Client | Office app's Wef folder on each machine | Until app restart, sometimes longer | Delete the folder |

Microsoft's own FAQ:
> It can take up to 72 hours for add-in updates, changes from turn on or turn off to reflect for users.
> https://learn.microsoft.com/en-us/microsoft-365/admin/manage/centralized-deployment-faq

### Confirm what Admin Center is serving

Admin Center silently ignores re-uploads with the same `<Version>`. If you
uploaded a fix without bumping the fourth segment, it never took. Open M365
Admin Center → Integrated apps → your add-in → check the listed version.

### Force a client-side refresh

Quit Excel/PowerPoint first, then:

**macOS:**
```bash
rm -rf ~/Library/Containers/com.microsoft.Excel/Data/Library/Caches/
rm -rf ~/Library/Containers/com.microsoft.Powerpoint/Data/Library/Caches/
rm -rf ~/Library/Containers/com.microsoft.Excel/Data/Documents/wef
rm -rf ~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/wef
```

**Windows:**
```cmd
rd /s /q "%LOCALAPPDATA%\Microsoft\Office\16.0\Wef"
```

Relaunch. If still stale, the service-side cache hasn't caught up. Wait, or
use a fresh `<Id>` (below).

Microsoft's cache-clear doc: https://learn.microsoft.com/en-us/office/dev/add-ins/testing/clear-cache

### Nuclear option: redeploy with a fresh Id

If 72h is unacceptable, a fresh `<Id>` UUID forces Admin Center and every
client to treat it as a brand-new add-in (24h fresh-deploy SLA, usually much
faster). Edit `manifest.xml`, replace the text inside `<Id>` with a new UUID
(`uuidgen` on mac/linux, `[guid]::NewGuid()` in PowerShell), re-upload.

---

## Add-in not visible

- **Not in the ribbon:** Check M365 Admin Center → Integrated apps → your
  add-in → Users tab. Is the user (or their group) assigned? Nested groups
  aren't supported.
- **Shows "My Add-ins" but not the ribbon button:** The manifest's `<Hosts>`
  may not include this app. Check both `<Hosts>` lists (top-level and under
  `<VersionOverrides>`).
- **Fresh deploy, been <24h:** Normal. Microsoft's SLA is 24h for first-time
  deployment visibility.

---

## Admin consent

If the user sees a sign-in popup that closes immediately or loops, the tenant
hasn't granted admin consent to the Claude app. Run
[`:consent`](consent.md) to generate the consent URL for a Global Admin to
approve. The symptom in error pastes: `user_canceled` in the raw error (the
broker maps any unclassifiable close to that).
