---
description: Setup wizard — provision Vertex/Bedrock/gateway, admin consent, generate manifest
---

# Claude in Office — Direct Cloud Setup

You are walking an enterprise admin through configuring the Claude Office add-in
to call their own cloud instead of Anthropic's API. The output is a customized
`manifest.xml` they deploy via M365 Admin Center.

**Before anything else:** the setup log lives at
`~/Desktop/claude-in-office-setup.md` (resolve `~` for their platform). If it
exists, read it first — you may be resuming a prior run and can skip completed
steps. Start a new `## Run — <timestamp>` section and append each command and
its captured output (IDs, URLs) as you go.

**Check for Node.js** — Steps 4 and 6 shell out to `node` and `npx`. Run
`node --version`. If it's missing, **ask before installing** — it's their
machine. If they say yes, `brew install node` (mac) / `winget install OpenJS.NodeJS`
(win) / whatever their package manager is. If no, stop here.

**When capturing values from the admin** (IDs, URLs, secrets pasted back from a
console) — don't use AskUserQuestion. That's a choice picker; they're holding a
string. Just say "paste the Client ID when you have it" and read it from their
next message. Use AskUserQuestion only for the actual branch points (gateway vs
vertex, per-user vs org-wide).

## Step 1 — How does the add-in reach Claude?

Ask this first, because it's the thing admins get wrong: **do you already run
an LLM gateway (LiteLLM, Portkey, Kong, etc.)?**

- **Yes → `gateway`.** Even if the gateway routes to Vertex or Bedrock under
  the hood — the add-in talks to *your gateway*, not to Google or AWS. You
  just need the gateway URL.
- **No → `vertex` or `bedrock`.** The add-in authenticates directly to the
  cloud provider. Pick where your infra lives.

| Path | What it means | Provisioning | Manifest keys |
|---|---|---|---|
| `gateway` | Add-in → your gateway → (whatever) | None | `gateway_url` |
| `vertex` | Add-in → Google Vertex AI, directly | Google OAuth client | `gcp_project_id`, `gcp_region`, `google_client_id`, `google_client_secret` |
| `bedrock` | Add-in → AWS Bedrock, directly | IAM OIDC provider + role | `aws_role_arn`, `aws_region` |

Bedrock and per-user config (bootstrap endpoint or extension attrs) need
`entra_sso=1` — the add-in acquires the user's Entra ID token to authenticate
those flows. See the Entra SSO section in [manifest](manifest.md).

Branch to the matching section below.

---

## Vertex AI

### 1a. Prerequisites

Confirm with the admin:
- GCP project ID (they should know this)
- Region with Claude model quota (typically `us-east5`)

### 1b. Create the OAuth client

No `gcloud` command exists for this. Open the console link (substitute their
project ID), walk them through, they paste back the client ID and secret.

> Open: `https://console.cloud.google.com/apis/credentials?project=<PROJECT_ID>`
> → **Create Credentials** → **OAuth client ID**
> - Application type: **Web application**
> - Name: `Claude for Office`
> - Authorized redirect URI: `https://pivot.claude.ai/auth/callback`
> → **Create** → copy the **Client ID** and **Client Secret**

Enable the Vertex API while they're there:

```bash
gcloud services enable aiplatform.googleapis.com --project=<PROJECT_ID>
```

Capture: `gcp_project_id`, `gcp_region`, `google_client_id`, `google_client_secret`.

Continue to [Step 3](#step-3--decide-whats-org-wide-vs-per-user). Vertex uses
Google OAuth, not Entra, so admin consent isn't needed unless you also opt into
per-user config (in which case come back to Step 2 after deciding in Step 3).

---

## Bedrock

### 1a. Prerequisites

Confirm with the admin:
- AWS account ID and a region with Claude model access (usually `us-east-1`)
- Their Azure tenant ID (from Entra admin center, or `az account show --query tenantId`)
- `aws` CLI configured against the target account

### 1b. Create OIDC provider + role

Three `aws iam` calls. The trust policy's `aud` condition is the security
boundary — only tokens Azure minted for the Claude add-in can assume this role.

Substitute their tenant ID and region:

```bash
TENANT_ID="<their-azure-tenant-guid>"
CLAUDE_APP_ID="c2995f31-11e7-4882-b7a7-ef9def0a0266"
AWS_REGION="us-east-1"
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
ISSUER="login.microsoftonline.com/${TENANT_ID}/v2.0"

# OIDC identity provider. Thumbprint is required by the API; AWS validates
# major IdPs via its own trust store, but the param can't be omitted.
THUMBPRINT=$(openssl s_client -servername login.microsoftonline.com \
  -connect login.microsoftonline.com:443 </dev/null 2>/dev/null \
  | openssl x509 -fingerprint -sha1 -noout | cut -d= -f2 | tr -d ':')

aws iam create-open-id-connect-provider \
  --url "https://${ISSUER}" \
  --client-id-list "${CLAUDE_APP_ID}" \
  --thumbprint-list "${THUMBPRINT}"

PROVIDER_ARN="arn:aws:iam::${ACCOUNT}:oidc-provider/${ISSUER}"

# Role with trust policy gated on aud.
aws iam create-role --role-name ClaudeBedrockAccess \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Federated": "'"${PROVIDER_ARN}"'"},
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {"'"${ISSUER}"':aud": "'"${CLAUDE_APP_ID}"'"}
      }
    }]
  }'

# Bedrock invoke permissions.
aws iam put-role-policy --role-name ClaudeBedrockAccess \
  --policy-name BedrockInvoke \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.*",
        "arn:aws:bedrock:*:'"${ACCOUNT}"':inference-profile/us.anthropic.*"
      ]
    }]
  }'

echo "aws_role_arn: arn:aws:iam::${ACCOUNT}:role/ClaudeBedrockAccess"
```

If `create-open-id-connect-provider` errors with `EntityAlreadyExists`, a
provider for that issuer already exists — that's fine, the role will trust it.
The ARN is deterministic (`arn:aws:iam::<account>:oidc-provider/<issuer>`).

Capture: `aws_role_arn`, `aws_region`. Add `entra_sso=1` when generating the
manifest — Bedrock needs the Entra ID token as the STS web identity.

Continue to [Step 2](#step-2--azure-admin-consent).

---

## Gateway

No provisioning. Ask for the gateway base URL (LiteLLM, Portkey, etc) and the
token. If the token varies per user, it goes in [Step 5](#step-5--per-user-config)
instead of the manifest.

Capture: `gateway_url`, `gateway_token`.

**Auth header scheme.** The add-in sends the token as `x-api-key: <token>` by
default — this is what LiteLLM, Portkey, and Kong accept out of the box. If
your gateway expects `Authorization: Bearer <token>` instead (common for
custom/enterprise gateways), set `gateway_auth_header=authorization`. The
value is case-sensitive lowercase; anything else silently falls back to
`x-api-key`. If you're unsure, run the Step 6 smoke test with `x-api-key`
first — a 401 with "no Authorization header" in your gateway logs means you
need `authorization`.

Continue to [Step 3](#step-3--decide-whats-org-wide-vs-per-user). Gateway auth
is token-based, not Entra, so admin consent isn't needed unless you also opt
into per-user config (in which case come back to Step 2 after deciding in Step 3).

---

## Step 2 — Azure admin consent

**Only required when `entra_sso=1`** — that is, Bedrock (the Entra token is the
STS web identity) or per-user config via extension attrs/bootstrap. If neither
applies, skip to Step 3.

Read `${CLAUDE_PLUGIN_ROOT}/commands/consent.md` and follow it.

## Step 3 — Decide what's org-wide vs. per-user

The add-in reads per-user extension attributes first, falls back to manifest
params. Any key can live at either layer. So the question is: **of the values
captured in Step 1, do any vary per user?**

Ask concretely — don't make them map it themselves:
- Gateway: is it one URL for everyone? One token, or a token per user?
- Vertex: same project for everyone? Same region, or do some users need a
  different one for data residency?
- Bedrock: same role for everyone, or team-specific roles?

| Answer | Split |
|---|---|
| Nothing varies | Everything → manifest. Skip Step 5. |
| Unique per user (e.g. gateway token) | Unique key → Step 5, rest → manifest. |

Write the split into the setup log so Step 4 and Step 5 each know their subset.

## Step 4 — Generate the manifest

Read `${CLAUDE_PLUGIN_ROOT}/commands/manifest.md` and follow it with the
**org-wide** values from Step 3. The command wraps:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/build-manifest.mjs" manifest.xml <key>=<value> ...
```

Then validate:

```bash
npx -y office-addin-manifest validate manifest.xml
```

## Step 5 — Per-user config

Skip unless Step 3 routed something here. Otherwise pick a mechanism by what
you're carrying:

| Carrying | Use | Read |
|---|---|---|
| A string or two — token, region | Extension attrs | `${CLAUDE_PLUGIN_ROOT}/commands/update-user-attrs.md` |
| `mcp_servers`, `skills`, anything structured | Bootstrap endpoint | `${CLAUDE_PLUGIN_ROOT}/commands/bootstrap.md` |

Attrs are an `az rest PATCH` per user — less work, but flat strings ≤256 chars
only. Bootstrap is an HTTPS service you build — more work, no shape limits.

## Step 6 — Verify a model is reachable

Before they deploy, confirm at least one of **Claude Sonnet 4.5** or
**Claude Opus 4.5** (or newer) actually answers. A manifest that points at an
unenabled model deploys fine and then fails silently at first user message.

**Gateway:** probe with a 1-token request. 200 means it works. 404 means the
gateway doesn't route that model name — try the other, or ask them to check
their gateway config. 429 means auth works but no quota on that model — try
the other. 401/403 means the token is wrong, which is a Step 1 problem.

```bash
# Windows: swap /dev/null for NUL
# If gateway_auth_header=authorization, swap the -H line for:
#   -H 'authorization: Bearer <token>'
curl -s -o /dev/null -w '%{http_code}\n' "<gateway_url>/v1/messages" \
  -H 'content-type: application/json' -H 'x-api-key: <token>' \
  -d '{"model":"claude-sonnet-4-5","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'
```

**Vertex:** model enablement is click-ops — the EULA accept has no API. Open
the Model Garden page, confirm at least one model shows **Enabled** (not
"Request access") for their region:

> `https://console.cloud.google.com/vertex-ai/publishers/anthropic?project=<PROJECT_ID>`

If it says "Request access", they click through, accept terms, wait for
enable. No API call until they confirm.

**Bedrock:** same constraint — model access grant has no API. Open the model
access page, confirm at least one Claude 4.5+ model shows **Access granted**
(not "Available to request"):

> `https://console.aws.amazon.com/bedrock/home?region=<aws_region>#/modelaccess`

If it says "Available to request", they request, accept terms, wait for grant
(usually minutes, sometimes longer).

Log the verified model name to the setup log. Don't proceed until you have a
200, a confirmed "Enabled", or a confirmed "Access granted" — whichever
matches their path.

## Step 7 — Deploy

Walk them through the upload — there are a few screens, and the user-assignment
one is a real decision.

> Open: `https://admin.cloud.microsoft/?#/Settings/IntegratedApps`
> → **Upload custom apps**
> - App type: **Office Add-in**
> - Choose how: **Upload manifest file (.xml) from device** → select `manifest.xml`
> - It validates on upload. If it errors here, Step 4's `npx office-addin-manifest validate` should have caught it — re-run that.

**Users screen** — the decision point:
- If Step 5 was skipped (nothing varies per user) → **Entire organization** is fine.
- If Step 5 wrote per-user attrs → assign to **Specific users/groups** matching
  exactly who got PATCHed. Everyone else would open the add-in with no config.
- First deploy? Start with **Just me** or a pilot group, confirm it works, then
  widen. You can change assignment later without redeploying.

> → **Accept permissions** → **Finish deployment**

Propagation to users takes up to 24 hours (usually much faster). The add-in
appears under **Home → Add-ins** in Excel/Word/PowerPoint once it lands.

Append the final manifest path and the assignment scope to the setup log. Done.
