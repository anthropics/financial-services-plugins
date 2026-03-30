#!/usr/bin/env node
// Fetches the canonical add-in manifest and writes a customized copy with your
// org's config baked into the taskpane URL as query parameters.
//
// Usage: node build-manifest.mjs <out.xml> key=value [key=value ...]
// Example: node build-manifest.mjs acme.xml gcp_project_id=acme gcp_region=us-east5

import { writeFileSync } from "node:fs";

const MANIFEST_URL = process.env.MANIFEST_URL || "https://pivot.claude.ai/manifest.xml";

// The manifest has two URL slots Office reads from; both must carry the same params.
const URL_SLOTS = [/(<SourceLocation\s+DefaultValue=")([^"]+)(")/, /(id="Taskpane\.Url"\s+DefaultValue=")([^"]+)(")/];

// Recognized config keys. `pattern` is a shape hint — mismatches warn but don't block
// (your infra may look different). `secret` keys warn louder: the manifest is an
// org-wide file and its URL can land in deploy logs; per-user secrets typically go
// in Azure extension attributes instead.
const KEYS = {
  gcp_project_id: { pattern: /^[a-z][a-z0-9-]{4,28}[a-z0-9]$/, hint: "GCP project ID" },
  gcp_region: { pattern: /./, hint: "GCP region, e.g. us-east5 or global" },
  google_client_id: { pattern: /\.apps\.googleusercontent\.com$/, hint: "OAuth 2.0 client ID" },
  google_client_secret: { pattern: /^GOCSPX-/, hint: "OAuth 2.0 client secret" },
  aws_role_arn: {
    pattern: /^arn:aws:iam::\d{12}:role\//,
    hint: "e.g. arn:aws:iam::123456789012:role/ClaudeBedrockAccess",
  },
  aws_region: { pattern: /^[a-z]{2}-[a-z]+-\d+$/, hint: "e.g. us-east-1" },
  gateway_url: { pattern: /^https:\/\//, hint: "HTTPS base URL" },
  gateway_token: { pattern: /./, hint: "gateway API key", secret: true },
  gateway_auth_header: { pattern: /^(x-api-key|authorization)$/, hint: "auth header scheme (default: x-api-key)" },
  bootstrap_url: { pattern: /^https:\/\//, hint: "HTTPS endpoint returning per-user config" },
  auto_connect: { pattern: /^[01]$/, hint: "0 shows form, 1 (or omit) auto-connects" },
  entra_sso: { pattern: /^[01]$/, hint: "1 enables Entra SSO (required for aws_role_arn)" },
  allow_1p: {
    pattern: /^[01]$/,
    hint: "1 allows Claude.ai OAuth alongside 3P (default: locked when other keys present)",
  },
};

const NEEDS_ENTRA = ["aws_role_arn"];

async function main() {
  const [out, ...pairs] = process.argv.slice(2);
  if (!out || pairs.length === 0) {
    console.error("Usage: node build-manifest.mjs <out.xml> key=value [key=value ...]");
    console.error(`Keys: ${Object.keys(KEYS).join(", ")}`);
    process.exit(1);
  }

  const params = new URLSearchParams();
  for (const p of pairs) {
    const eq = p.indexOf("=");
    if (eq < 1) throw new Error(`bad arg: ${p} (expected key=value)`);
    const [k, v] = [p.slice(0, eq).trim(), p.slice(eq + 1).trim()];

    const spec = KEYS[k];
    if (!spec) throw new Error(`unknown key: ${k}\n  valid: ${Object.keys(KEYS).join(", ")}`);
    if (!v) throw new Error(`empty value for ${k}`);
    if (!spec.pattern.test(v)) console.warn(`warn: ${k}=${v} — expected ${spec.hint}`);
    if (spec.secret) {
      console.warn(
        `note: ${k} in the manifest applies to every user. If it varies per user, set it via update-user-attrs instead.`,
      );
    }
    params.set(k, v);
  }

  const needsEntra = NEEDS_ENTRA.find((k) => params.has(k));
  if (needsEntra && params.get("entra_sso") !== "1") {
    throw new Error(`${needsEntra} requires entra_sso=1 (the add-in needs an Entra ID token to use it)`);
  }

  // URLSearchParams joins with `&`; XML attribute values need it escaped.
  const qs = params.toString().replaceAll("&", "&amp;");

  const res = await fetch(MANIFEST_URL);
  if (!res.ok) throw new Error(`fetch ${MANIFEST_URL}: ${res.status} ${res.statusText}`);
  let xml = await res.text();

  for (const slot of URL_SLOTS) {
    if (!slot.test(xml)) throw new Error(`manifest missing expected URL slot: ${slot.source}`);
    // The template URL already carries ?m=<tag> — append with & not a second ?
    xml = xml.replace(slot, (_, pre, url, post) => pre + url + (url.includes("?") ? "&amp;" : "?") + qs + post);
  }

  writeFileSync(out, xml);
  console.log(`Wrote ${out}  (params: ${params})`);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
