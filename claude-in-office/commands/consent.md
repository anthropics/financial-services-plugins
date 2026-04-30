---
description: Azure admin consent URL — one-time tenant approval for Entra SSO
---

# Azure admin consent

**Only needed when `entra_sso=1`** in the manifest. Gateway and Vertex setups
with org-wide config don't use Entra and can skip this. If you set
`graph_client_id` (your own Entra app), this page doesn't apply either — you
manage consent on your app directly.

One-time per tenant. A Global Admin opens this URL, clicks Accept, done. Until
they do, NAA sign-in inside the add-in fails for every user in the tenant.

## The URL

Same URL for every customer — `/organizations/` resolves the tenant from
whoever signs in. No substitution needed.

```
https://login.microsoftonline.com/organizations/adminconsent?client_id=c2995f31-11e7-4882-b7a7-ef9def0a0266&redirect_uri=https://pivot.claude.ai/auth/callback
```

Print it. Tell them: open in a browser where a **Global Admin** for their
tenant is signed in. They'll see a permissions screen listing what the add-in
reads (user profile, extension attributes). After they click **Accept**, they
land on a confirmation page — "Admin consent granted, you can close this tab."

## Verify

```bash
az ad sp show --id c2995f31-11e7-4882-b7a7-ef9def0a0266 --query appId -o tsv
```

If that returns the same GUID, the service principal exists in their tenant —
consent worked. If it errors with "does not exist", consent didn't complete.