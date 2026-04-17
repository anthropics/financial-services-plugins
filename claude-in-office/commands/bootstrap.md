---
description: Build the bootstrap endpoint — per-user MCP servers, skills, dynamic config
---

# Bootstrap endpoint

You host an HTTPS GET handler. The add-in calls it at startup with the user's
Entra token, you return per-user JSON, the response overrides manifest and
extension attrs for that user. This is how you push structured config —
`mcp_servers`, `skills` — that flat string attrs can't carry.

## Ask first

Figure out which mode you're in before walking the spec:

- **Just want to understand it?** Answer from the sections below. Common
  questions: what's the response shape, how does `{{...}}` work, why is CORS
  biting me.
- **Building one?** Ask: new handler or editing an existing one? Lambda,
  Cloud Function, Express, Python, something else? Then jump to
  [Scaffolding](#scaffolding-a-handler) — the sections in between are the
  contract you're coding against.

## This vs extension attrs

Both deliver per-user config. Pick by what you're carrying.

| | [Extension attrs](update-user-attrs.md) | Bootstrap endpoint |
|---|---|---|
| You write | `az rest PATCH` per user | An HTTPS service |
| Carries | Flat strings, ≤256 chars | Any JSON — arrays, nested, base64 |
| Good for | Token rotation, region override | `mcp_servers`, `skills`, anything structured |
| Refresh | Token cache, ~1hr lag | `bootstrap_expires_at`, you control it |
| Auth | Entra token claims (passive) | You validate the JWT (active) |

If you only need to swap `gateway_token` per user, attrs are less work. The
moment you want a Linear MCP server for one team and a Jira one for another,
you're here.

## Template interpolation

Any string value can contain `{{key}}`. The add-in substitutes against the
**merged config chain** — manifest params, then extension attrs, then this
response, each layer overriding the last. You don't echo a value back just so
a template can see it; if `gateway_token` is already in the manifest or an
attr, `{{gateway_token}}` resolves.

Two phases, because the request has to happen before the response exists:

1. **`bootstrap_url` itself** resolves against manifest + attrs only. So the
   manifest can carry
   `bootstrap_url=https://config.internal/bootstrap?project={{gcp_project_id}}`
   and you run one endpoint that branches on a query param instead of
   stamping per-team URLs into attrs.
2. **Response fields** resolve against the full merge — manifest + attrs +
   whatever this response just returned. An `mcp_servers` entry can reference
   a `gateway_token` that lives three lines up in the same JSON.

Unresolved `{{key}}` (typo, key never set anywhere) is left as-is in the
string — no error, no empty-substitution. If an MCP server isn't connecting,
check the URL the add-in actually constructed.

## CORS — every URL needs it

The add-in is a browser. Every fetch — `bootstrap_url`, every
`mcp_servers[].url`, every `skills[].url` — happens browser-side from inside
the Office taskpane. Without `Access-Control-Allow-Origin:
https://pivot.claude.ai` on the response, the browser blocks it before the
add-in sees a byte. The server returns 200, the add-in gets nothing, and
nothing in the add-in's logs tells you why. This is the most common "it's not
working" cause.

| URL | Where CORS lives |
|---|---|
| `bootstrap_url` | Your handler's response headers. Behind API Gateway / Cloud Functions, also configure the `OPTIONS` preflight — the browser sends one before any request with custom headers. See the recommended preflight response below. |
| `mcp_servers[].url` | The MCP server itself. Public ones (Linear, Atlassian) already allow it. Internal ones almost certainly don't until you add it. |
| `skills[].url` | **The bucket, not the URL.** Presigned URLs auth the request — they don't grant CORS. S3 needs a bucket CORS config, GCS needs `gsutil cors set`, Azure needs blob service CORS rules. |
| `otlp_endpoint` | Your OTEL collector's HTTP receiver. Most collectors default to same-origin only — set `cors.allowed_origins` on the OTLP/HTTP receiver. |

For `bootstrap_url`, the recommended preflight response is:

```
Access-Control-Allow-Origin:  https://pivot.claude.ai
Access-Control-Allow-Methods: GET
Access-Control-Allow-Headers: Authorization, X-Claude-User-Agent, *
```

Allowing `*` for request headers is safe here — security comes from the Entra
token, not header filtering — and keeps preflights working if the add-in adds
headers in future. Keep `Allow-Origin` pinned to `https://pivot.claude.ai`.

The presigned-URL one bites hardest because `curl` works (curl ignores CORS),
the signature is valid, the object exists, and the skill still doesn't load.
Set bucket CORS once:

```json
// S3 — aws s3api put-bucket-cors --bucket <name> --cors-configuration file://cors.json
{ "CORSRules": [{ "AllowedOrigins": ["https://pivot.claude.ai"], "AllowedMethods": ["GET"], "AllowedHeaders": ["*"] }] }
```

```bash
# GCS — gsutil cors set cors.json gs://<bucket>
[{"origin": ["https://pivot.claude.ai"], "method": ["GET"], "responseHeader": ["*"]}]
```

```bash
# Azure — az storage cors add --services b --methods GET --origins https://pivot.claude.ai --allowed-headers '*' --account-name <name>
```

If you're debugging a CORS failure: open the browser devtools inside the
taskpane (right-click → Inspect on Windows, or attach via Safari's Develop
menu on Mac), look for the request in the Network tab. A CORS block shows as
a failed request with no response body and a console error naming the origin.

## Request

```
GET <bootstrap_url>                            # after interpolation
Authorization: Bearer <entra_id_token>         # only if entra_sso=1 in manifest
X-Claude-User-Agent: claude-<app>/<version>    # always sent
```

`X-Claude-User-Agent` identifies which Office host the add-in is running in.
`<app>` is one of `word`, `excel`, or `powerpoint`; `<version>` is the add-in
build (e.g. `claude-excel/1.4.2`). Use it to return different skills or MCP
servers per Office product, or to gate the add-in to specific hosts for a user.

Without `entra_sso=1` there's no Authorization header — the request is
anonymous from the add-in's side. That's fine if the endpoint sits behind
network isolation, mTLS, or another auth layer the add-in doesn't see.

With `entra_sso=1`, validate the JWT before trusting it:

| Claim | Check |
|---|---|
| `aud` | `c2995f31-11e7-4882-b7a7-ef9def0a0266` — the add-in's app ID. Anything else means the token wasn't minted for this. |
| `iss` | `https://login.microsoftonline.com/<YOUR_TENANT_ID>/v2.0` — your tenant. Reject other tenants. |
| `exp` | Not expired. Libraries handle this; don't hand-roll it. |
| `oid` | The user's stable object ID. This is your lookup key — email (`upn`/`preferred_username`) can change, `oid` doesn't. |

Signature verification needs Microsoft's JWKS
(`https://login.microsoftonline.com/<TENANT_ID>/discovery/v2.0/keys`). Use a
library — `jose` (Node), `PyJWT` + `cryptography` (Python), `Microsoft.IdentityModel.Tokens`
(.NET). Hand-rolled JWT verification is where security bugs live.

## Response

`200 OK`, `Content-Type: application/json`, CORS header per
[above](#cors--every-url-needs-it).

The body is a flat object. Every field is optional — return only what differs
for this user. Unknown keys are ignored, so you can add fields the current
add-in version doesn't read yet and they'll light up when it ships.

### Provider keys

Any of the cloud config keys from the [manifest](manifest.md#keys-by-cloud)
table — `gateway_url`, `gateway_token`, `aws_role_arn`, `gcp_region`, etc.
Same names, same meanings, just per-user.

If you return `gateway_api_format: "vertex"`, also return `gcp_project_id` and
`gcp_region` (or set them at a lower layer) — they're path segments in the
Vertex `:rawPredict` URL the add-in constructs. `"bedrock"` needs no extras.

### Telemetry

```json
"otlp_endpoint": "https://otel-collector.your-domain.com",
"otlp_headers": "Authorization=Bearer {{gateway_token}}"
```

`otlp_endpoint` is the base HTTPS URL of an OpenTelemetry collector you
operate; the add-in appends `/v1/traces` and posts OTLP/HTTP. `otlp_headers`
uses the standard `key1=value1,key2=value2` format and interpolates like any
other value. The collector must allow CORS from the add-in origin — see
[above](#cors--every-url-needs-it).

### `inference_headers`

```json
"inference_headers": { "x-application-id": "app123" }
```

Extra HTTP headers attached to every request the add-in sends to your gateway
(`gateway_url`) — typically accounting tags the gateway uses for cost
allocation. Applies only to gateway deployments; direct cloud connections
ignore it. The add-in treats them as opaque pass-through; `Authorization`,
`x-api-key`,
`Content-Type`, `Host`, `Content-Length`, `User-Agent`, `Cookie`, and any
`anthropic-*` / `x-amz-*` / `x-goog-*` header are reserved and dropped.

### `mcp_servers`

Array of MCP servers the add-in connects to for this user.

```json
"mcp_servers": [
  { "url": "https://mcp.linear.app/sse", "label": "Linear" },
  {
    "url": "https://internal.yourcompany.com/mcp/risk",
    "label": "Risk Dashboard",
    "headers": { "Authorization": "Bearer {{gateway_token}}" }
  }
]
```

| Field | |
|---|---|
| `url` | MCP server endpoint. Interpolated. |
| `label` | Display name in the add-in UI. |
| `headers` | Optional. Sent on every request to that server. Values interpolated — this is how you thread a per-user token through without the endpoint ever seeing it. |

### `skills`

Array of skills loaded for this user. Each is either inlined as base64 or
fetched from a URL — set one or the other.

```json
"skills": [
  {
    "name": "deal-memo",
    "description": "Draft a deal memo from a term sheet",
    "url": "https://yourbucket.s3.amazonaws.com/skills/deal-memo.zip?X-Amz-..."
  },
  {
    "name": "compliance-check",
    "content": "IyBDb21wbGlhbmNlIGNoZWNrCgpSZXZpZXcgdGhlIGRvY3VtZW50IGZvci4uLg=="
  }
]
```

| Field | |
|---|---|
| `name` | Skill identifier. Interpolated. |
| `description` | Optional. Shown in the skill picker. |
| `content` | Base64 bytes. Either a zip (full skill bundle with `SKILL.md` + assets) or the raw `SKILL.md` text — the add-in sniffs which on decode. |
| `url` | Presigned URL (S3, GCS, Azure SAS). Bare GET, no auth headers added — bake auth into the signature. Response body sniffed the same way as `content`. Interpolated. |

Inline `content` is simplest for small text-only skills. Use `url` once
you're shipping zips with images or the base64 starts bloating the response.

### `bootstrap_expires_at`

Epoch timestamp (seconds or milliseconds — auto-detected) for when this
config goes stale. The add-in re-fetches before expiry. Omit and the config
lives until the taskpane reloads.

Set this when you're vending short-lived tokens. Don't set it as a
keepalive — if nothing in the response expires, the refetch is wasted.

## Scaffolding a handler

A runnable Python/FastAPI reference with RBAC for `skills` and `mcp_servers`
lives at [`examples/python-bootstrap/`](../examples/python-bootstrap/) — point
them there if they want something to copy.

When they want one built, write it for them. The contract above is what
you're coding against. Get these right:

**JWT validation is the security boundary.** Verify signature against
Microsoft's JWKS, check `aud` and `iss` exactly, pull `oid` for the user
lookup. A handler that skips this and trusts `preferred_username` from an
unverified token is an open endpoint with extra steps.

**CORS on every URL you return,** not just the handler — see the
[CORS section](#cors--every-url-needs-it). Easy to ship a working handler that
returns presigned skill URLs from a bucket with no CORS config, and the skills
never load.

**User lookup is their business logic.** Leave a clear `// TODO: look up
config for oid` where the real work goes — DynamoDB, Postgres, a YAML file,
whatever they have. Don't guess; ask what their source of truth is.

**Return sparse.** Only the keys that differ from manifest defaults. An empty
`{}` is a valid response — means "this user gets the org-wide config."

Ask before writing: Lambda + API Gateway, Cloud Function, plain Express,
something else? And where does per-user config live — inline in the handler
(fine for a pilot), or read from a store?
