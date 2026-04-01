---
description: Generate the add-in manifest XML with your cloud config baked in
---

# Generate add-in manifest

The script fetches the canonical manifest from `pivot.claude.ai/manifest.xml`
and appends your config as URL query parameters. The add-in reads them at
startup.

## Keys by cloud

Prompt only for the keys their cloud path needs. Don't ask for all eight.

| Cloud | Keys |
|---|---|
| Vertex | `gcp_project_id` `gcp_region` `google_client_id` `google_client_secret` |
| Bedrock | `aws_role_arn` `aws_region` |
| Gateway | `gateway_url` `gateway_token` `gateway_auth_header` |

## Entra SSO

`entra_sso=1` makes the add-in acquire an Entra ID token at startup. Set it
when your deployment needs the user's Microsoft identity — Bedrock uses it as
the STS web identity, the bootstrap endpoint uses it as Bearer auth, and
per-user attrs ([update-user-attrs](update-user-attrs.md)) ride inside it as
`extn.*` claims.

**Admin consent is a prerequisite.** Without it, every user hits a Microsoft
consent dialog on first open. Run [consent](consent.md) first so
`entra_sso=1` is silent for your users.

If you don't need Entra — static gateway config, Vertex with Google OAuth —
leave it off. Users won't see a Microsoft prompt for a setup that doesn't
involve Microsoft.

## Bootstrap endpoint

`bootstrap_url` points to an HTTPS endpoint you host. At startup the add-in
fetches per-user JSON from it — provider keys, `mcp_servers`, `skills` — and
the response overrides manifest values for that user. The URL itself is
[interpolated](bootstrap.md#template-interpolation) against manifest + attrs
before the fetch, so one endpoint can branch on a query param.

See [bootstrap](bootstrap.md) for the request/response contract, JWT
validation, and handler scaffolding.

## Auto-connect

Default: when all fields for a provider are set, users skip the connection form
and land straight in chat. Ask: should they instead see the form first
(prefilled, one click)? Yes → `auto_connect=0`.

## Version

M365 Admin Center caches by `<Id>` + `<Version>` — re-upload with the same
version is silently ignored. After the script writes `manifest.xml`, ask whether
this replaces an existing deployment; if yes, edit `<Version>` to bump the
fourth segment past their last deployed value. First deploy can leave the
template's version as-is.

## Run

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/build-manifest.mjs" manifest.xml \
  gcp_project_id=<value> \
  gcp_region=<value> \
  auto_connect=0 \
  ...
```

The script validates key names (unknown keys fail hard) and shape-hints values
(warns but doesn't block — their infra may look different).

## Validate

```bash
npx --yes office-addin-manifest validate manifest.xml
```

If validation passes but M365 Admin Center still rejects or ignores the upload,
match the symptom below. Edit `manifest.xml` directly, then re-validate.

| Symptom | Fix |
|---|---|
| "An add-in with this ID already exists" | Replace the text inside `<Id>` with a fresh UUID. The template carries the marketplace install's ID. |
| Re-upload accepted but nothing changes | M365 caches by ID + version. Edit `<Version>` to a higher fourth segment (e.g. `1.0.0.9` → `1.0.0.10`) and re-validate. |
| Only want Excel (not PowerPoint) | Remove `<Host>` elements for `Presentation`. **Two parallel lists:** the top-level `<Hosts>` uses `Name="Presentation"`, the one under `<VersionOverrides>` uses `xsi:type="Presentation"` — both must go or the manifest is inconsistent. The `xsi:type` block is multi-line, delete the whole `<Host xsi:type="Presentation">...</Host>`. |
