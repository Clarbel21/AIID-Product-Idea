const crypto = require("node:crypto");

const FASHN = "https://api.fashn.ai/v1";
const MAX_REQUEST_CHARS = 4 * 1024 * 1024;
const MAX_OUTPUT_BYTES = 3 * 1024 * 1024;
const CATEGORY_PROMPTS = {
  top: "upper-body top",
  outerwear: "outerwear garment",
  bottom: "lower-body garment",
  dress: "one-piece dress",
  shoes: "shoes",
  bag: "bag",
  accessory: "accessory"
};

function reply(res, status, body) {
  res.status(status).json(body);
}

function origins() {
  return (process.env.MATCHBUY_ALLOWED_ORIGINS || "")
    .split(",")
    .map((value) => value.trim().replace(/\/$/, ""))
    .filter(Boolean);
}

function secureEqual(a, b) {
  const left = Buffer.from(String(a || ""));
  const right = Buffer.from(String(b || ""));
  return left.length === right.length && left.length > 0 && crypto.timingSafeEqual(left, right);
}

function authorize(req, res) {
  const allow = origins();
  if (!process.env.MATCHBUY_TRYON_ACCESS_CODE || !process.env.FASHN_API_KEY || allow.length === 0) {
    reply(res, 503, { error: "The private try-on service is not configured yet." });
    return false;
  }
  const origin = String(req.headers.origin || "").replace(/\/$/, "");
  if (origin && !allow.includes(origin)) {
    reply(res, 403, { error: "This website is not allowed to use the try-on service." });
    return false;
  }
  if (origin) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-MatchBuy-Access");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  }
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return false;
  }
  if (!secureEqual(req.headers["x-matchbuy-access"], process.env.MATCHBUY_TRYON_ACCESS_CODE)) {
    reply(res, 401, { error: "The private demo access code is incorrect." });
    return false;
  }
  return true;
}

function parseBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") return JSON.parse(req.body);
  return {};
}

function validProductUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" &&
      origins().includes(url.origin) &&
      /\/assets\/[A-Za-z0-9._-]+$/.test(url.pathname);
  } catch (_) {
    return false;
  }
}

async function startPrediction(req, res) {
  const body = parseBody(req);
  const personImage = body.personImage;
  const productImage = body.productImage;
  const category = body.category;
  const name = String(body.productName || "selected garment").replace(/[\r\n]/g, " ").slice(0, 120);

  if (typeof personImage !== "string" ||
      !/^data:image\/jpeg;base64,[A-Za-z0-9+/]+=*$/.test(personImage) ||
      personImage.length > MAX_REQUEST_CHARS) {
    return reply(res, 400, { error: "Choose a valid photo. It is compressed in your browser before sending." });
  }
  if (!validProductUrl(productImage)) {
    return reply(res, 400, { error: "The catalog image must be a product image hosted by this approved site." });
  }
  if (!CATEGORY_PROMPTS[category]) {
    return reply(res, 400, { error: "This product category is not supported for try-on." });
  }

  const prompt = "Replace only the " + CATEGORY_PROMPTS[category] + " with the provided product, " +
    "which is named " + name + ". Preserve the person's identity, face, hair, body shape, pose, " +
    "lighting, and background. Keep all other clothing, shoes, and accessories unchanged. " +
    "Render natural fabric drape and realistic garment placement. Do not add items or alter the person.";

  let response;
  try {
    response = await fetch(FASHN + "/run", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + process.env.FASHN_API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model_name: "tryon-max",
        inputs: {
          model_image: personImage,
          product_image: productImage,
          prompt,
          resolution: "1k",
          generation_mode: "balanced",
          num_images: 1,
          output_format: "jpeg",
          return_base64: true
        }
      })
    });
  } catch (_) {
    return reply(res, 502, { error: "Could not reach the try-on provider. Please try again later." });
  }

  let result = {};
  try { result = await response.json(); } catch (_) {}
  if (!response.ok || !result.id) {
    return reply(res, response.status === 401 ? 502 : 502, {
      error: response.status === 401
        ? "The try-on provider rejected its server key. Check the private FASHN_API_KEY setting."
        : "The try-on provider could not start this request. Check the photo and try again."
    });
  }
  return reply(res, 200, { id: result.id });
}

async function normalizeOutput(output) {
  const item = Array.isArray(output) ? output[0] : output;
  if (typeof item !== "string") return null;
  if (/^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/]+=*$/.test(item)) return item;

  let url;
  try { url = new URL(item); } catch (_) { return null; }
  if (url.protocol !== "https:" || !["cdn.fashn.ai", "media.fashn.ai"].includes(url.hostname)) return null;
  const response = await fetch(url.href);
  if (!response.ok) return null;
  const type = response.headers.get("content-type") || "";
  if (!type.startsWith("image/")) return null;
  const bytes = Buffer.from(await response.arrayBuffer());
  if (bytes.length === 0 || bytes.length > MAX_OUTPUT_BYTES) return null;
  return "data:" + type.split(";")[0] + ";base64," + bytes.toString("base64");
}

async function checkPrediction(req, res) {
  const id = typeof req.query?.id === "string" ? req.query.id : "";
  if (!/^[A-Za-z0-9_-]{12,100}$/.test(id)) {
    return reply(res, 400, { error: "Invalid try-on request ID." });
  }
  let response;
  try {
    response = await fetch(FASHN + "/status/" + encodeURIComponent(id), {
      headers: { "Authorization": "Bearer " + process.env.FASHN_API_KEY }
    });
  } catch (_) {
    return reply(res, 502, { error: "Could not check try-on progress. Please retry." });
  }
  let result = {};
  try { result = await response.json(); } catch (_) {}
  if (!response.ok) return reply(res, 502, { error: "Could not check try-on progress. Please retry." });
  if (result.status === "failed") {
    return reply(res, 200, { status: "failed", error: "The model could not process these images. Try a clear, full-body photo and a straight-on product photo." });
  }
  if (result.status === "completed") {
    let image = null;
    try { image = await normalizeOutput(result.output); } catch (_) {}
    if (!image) return reply(res, 502, { error: "The model finished, but its image could not be retrieved." });
    return reply(res, 200, { status: "completed", image });
  }
  return reply(res, 200, { status: result.status || "processing" });
}

module.exports = async function handler(req, res) {
  if (!authorize(req, res)) return;
  if (req.method === "POST") return startPrediction(req, res);
  if (req.method === "GET") return checkPrediction(req, res);
  res.setHeader("Allow", "GET, POST, OPTIONS");
  return reply(res, 405, { error: "Method not allowed." });
};
