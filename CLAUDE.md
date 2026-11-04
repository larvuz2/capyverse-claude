# Capyverse × Claude — media workroom

This repo is where Claude writes prompts and makes media for **Capyverse Odyssey** with **Gus Garza**
(gus@phattyacid.studio / gus@metazooie.com, Phatty Acid Studio × Metazooie).
Read this file first, then the docs it points to, before answering any media request.

## The project in one paragraph

Capyverse Odyssey is a real **Unreal Engine game**. The four playable heroes fly with **side-mounted belt
jetpacks** and each carries a signature back-mounted weapon: **Cappy** (capybara, popcorn gatling),
**Moody** (pink pygmy hippo, disco-ball cannon), **Axie** (purple axolotl, wooden ballista), **Jim**
(bulldog, trumpet). The villain side is **Ophelia** (giant white cat with gold crown and red eyes) and
her wasteland crew. Current work is **Steam store marketing art** built from in-engine renders: capsules,
key art, logo placement. All generation happens in **Shot Forge** (Gus's Lovable app), project
"Capyverse Odyssey" (`fe0ee570-4f89-4a43-903a-4993b932a83a`).

## Read before working

| File | What it gives you |
|---|---|
| `docs/gus-prompt-style.md` | **How Gus writes prompts.** Structure, vocabulary, iteration habits. Match it. |
| `docs/cast-and-assets.md` | Every `@tag` in the project, what it looks like, when to use it. |
| `docs/latest-50-study.md` | What Gus made in his latest 50 generations, what worked, what failed. |
| `docs/reference/prompting-rulebook.md` | Gus's own rulebook for cinematic **video** sequences. Follow it for video. |
| `prompts/templates/` | Ready-to-fill templates in Gus's style. |
| `prompts/archive/` | The 32 unique prompts behind the latest 50 generations, verbatim. |

## How to handle a request

1. **Read the ask the way Gus writes it.** His raw requests are short, fast, typo-prone, and end in `!`
   ("Add @Axie_flying Small on the left. Keep characters as is. Keep center empty as is!").
   Take the intent; don't ask about typos.
2. **Expand it into his structured prompt style** (see style guide): opening task sentence →
   `SECTION — VERY IMPORTANT:` blocks → `CRITICAL COMPOSITION RULES` bullets → priority chain for big
   compositions. Use `@tags` for every project asset, never re-describe a tagged asset's look.
3. **Name the inputs.** Source image (what's being edited), reference images (`@tags` + any one-off
   image, cited as "the second image attached"), model, aspect ratio (default **16:9**).
4. **Recommend a model** (see style guide → Models). Default edit model today: `nano-banana-pro`;
   run `gpt-image-2-5` side by side when the brief is a full re-composition.
5. **Save it.** Write each request to `prompts/requests/YYYY-MM-DD_short-slug.md` (prompt, inputs,
   model, and later the result links + Gus's verdict). Commit and push.
6. **Iterate like Gus does:** change one thing per round, keep everything else word-for-word.
   When the model ignores something, escalate it: plain line → `VERY IMPORTANT` heading → caps → a
   repeated bullet in the rules list → a number (e.g. "2–3% of the image width").

## Generating media

- **Shot Forge MCP server** can generate images/video directly
  (`https://zvuqjqilmokxcnhorrsa.supabase.co/functions/v1/mcp-server`, Bearer `shotforge_pat_...`).
  It is **not connected** in this repo yet. Until Gus adds it, deliver prompts + inputs ready to paste
  into Shot Forge. Never ask Gus to paste a token into chat; it belongs in the MCP/connector config.
- The Lovable connector can **read** the Shot Forge database (`query_database` on Lovable project
  `5af0d6c3-8277-46bd-912c-921d27109932`). Use it only for `SELECT`s, to pull new generations and
  results. **Never write to that database**: it is production for the whole team.
- Media URLs on `zvuqjqilmokxcnhorrsa.supabase.co/storage/v1/object/public/...` are public and stable;
  `curl` them directly.

## Repo layout

```
media/library/          Original reference images for every @tag (characters, logos, props, environments)
media/latest50/         Gus's latest 50 outputs (JPEG previews, 2560px) + the 2 unique source images
data/all_media_manifest.json   All 3,804 project generations (every author): id, date, author, model, image/video URLs
data/raw/               Raw DB exports: latest 50 scenes (full prompts) + latest 60 generation events
prompts/archive/        Verbatim prompt history   prompts/templates/  Templates   prompts/requests/  New work
scripts/                Helpers (fetch media from the manifest)
```

## House rules

- Characters are **locked game assets**: never let a prompt redesign, beautify, or add detail to them.
- Keep the "raw in-engine Unreal" look; ban concept-art / AI-art polish unless Gus asks for it.
- Gus's priority is readability at **Steam thumbnail size**.
- Don't put model identifiers in commit messages or files outside this repo's docs.
