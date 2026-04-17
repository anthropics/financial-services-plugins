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
| Foundry | `azure_resource_name` `azure_api_key` |
| Gateway | `gateway_url` `gateway_token` `gateway_auth_header` `gateway_api_format` |
| Gateway (`gateway_api_format=vertex`) | also `gcp_project_id` `gcp_region` |

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

## MCP servers

`mcp_servers` is a JSON array of customer-hosted MCP servers the add-in
connects to directly. Each entry is `{url, label, headers?, discover?}` —
`headers` present means static auth; absent triggers OAuth discovery. Values
interpolate other config keys via `{{gateway_url}}`-style templates.

Setting it here applies one list org-wide; per-user lists belong in
[bootstrap](bootstrap.md#mcp_servers), which also has the full schema. The
value is JSON inside a shell arg — single-quote it:

```bash
mcp_servers='[{"url":"{{gateway_url}}/deepwiki/mcp","label":"DeepWiki","headers":{"Authorization":"Bearer {{gateway_token}}"}}]'
```

## Telemetry

`otlp_endpoint` routes the add-in's OpenTelemetry traces to a collector you
operate. Set it to the collector's base HTTPS URL — the add-in appends
`/v1/traces` and posts OTLP/HTTP. gRPC isn't supported (the add-in runs in a
browser WebView). Leave it unset and no custom collector is configured.

`otlp_headers` supplies authentication headers for that collector, in the same
`key1=value1,key2=value2` format as the standard
`OTEL_EXPORTER_OTLP_HEADERS` variable. URL-encode the value in the manifest.

Setting these here applies one collector org-wide; per-user routing belongs in
[bootstrap](bootstrap.md#telemetry) or extension attrs.

## Inference headers

`inference_headers` is a JSON object of extra HTTP headers the add-in attaches
to every request it sends to your gateway (`gateway_url`). Use it for
accounting or cost-allocation tags your gateway expects — e.g., an internal
application ID — so you don't need a header-injecting proxy in front of it.
Applies only when using a gateway; direct cloud connections ignore it.

```bash
inference_headers='{"x-application-id":"app123"}'
```

The add-in treats the values as opaque. `Authorization`, `x-api-key`,
`Content-Type`, `Host`, `Content-Length`, `User-Agent`, `Cookie`, and any
`anthropic-*` / `x-amz-*` / `x-goog-*` header are reserved and silently dropped
— they carry the add-in's own auth and protocol negotiation.

Setting it here applies one header set org-wide; per-user values belong in
[bootstrap](bootstrap.md#inference_headers).

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
