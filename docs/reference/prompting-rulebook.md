# Cinematic Animation Sequence Prompting — Rulebook

Owner: Gus Garza / Larvuz · Version 1.1 — September 2026
Scope: AI video story sequences of 10, 15, 20 and 30 seconds (Seedance 2.5 / Dreamina, Magnific, Kling, Veo, Runway, fal pipelines).

> Movie Maker's Story mode (`src/lib/movie-maker/story-director.ts`) writes every block prompt
> with this rulebook: `CINEMA_RULES` condenses it for the screenplay director, and `compileBlock`
> emits the fixed prompt anatomy of section 1. Edit both when the rulebook changes.

**Thesis:** One prompt = one complete story beat, told with real film grammar, built on a locked reference package (character + voice + props + location), directed like a live-action scene.

## 0. Non-Negotiables
- **Cinematic is the objective.** Every prompt is a scene from a film. If the shot could not exist in a real movie, restage it.
- **One prompt = one story.** Setup → turn → payoff. Never two ideas in one prompt.
- **References before prompts.** No story prompt is written until the reference package exists: character sheet, voice reference, prop sheets, location plates. Every recurring element is an object with a tag.
- **Characters are references, not descriptions.** Identity by @name, voice by @name_voice. Always. Every prompt.
- **Establish first.** The sequence opens on geography (establishing wide or declared @frame continuation) before coverage.
- **Timeline is explicit.** Every beat has a time range, a shot label, one action, one endpoint. Camera, action, dialogue and reaction are described together inside the same time range.
- **Direct the performance.** Small expressions, believable pauses, breaths, glances, physical weight. Dialogue sounds spontaneous. Leave time to breathe.
- **Continuity is written, not assumed.** Axis, screen direction, wardrobe, props, lighting direction, geometry.
- **Art style is a lock, not a mood.** Any style; declared once, held everywhere.
- **Sound is a timing layer.** Diegetic per beat. NO MUSIC unless music is the point.
- **Effects are grounded.** Magic, VFX and explosions interact with the scene's light and space and support the performance; they never replace it.
- **No generic adjectives.** "Epic, stunning, 8K, award-winning" are banned. Staging replaces adjectives.
- **Hard cuts only.** No transitions. No UI. No text. Unless explicitly requested.

## 1. Prompt Anatomy (fixed block order)
```
[HEADER]                 duration · aspect · mode · cut rule · art style lock
[REFERENCE ROLE MAP]     every @tag: what it defines + what it must NOT contribute
[CHARACTER PROFILES]     identity lock · voice lock · wardrobe · props · acting register
[SCENE PROMISE]          one sentence: what the audience sees happen
[STAGING + PERFORMANCE]  location, positions, intentions, acting style, effect rules
[SPACE + LIGHTING]       geometry, axis, light sources with direction
[TIMELINE]               time ranges: camera + action + dialogue + reaction together
[AUDIO]                  ambience, SFX, dialogue delivery, lip-sync rule
[CONTINUITY LOCKS]       what must not change
[NEGATIVE]               what must not appear
```
Word budget: 15s ≈ 350–450 words · 20s ≈ 450–550 · 30s ≈ 600–750. Over budget means adjectives, not information.

## 2. Reference Package (built before any story prompt)
A story sequence is only as consistent as its reference package. Build the package once per project, tag it once, reuse forever.

### 2.1 What the package contains
| Sheet | Tag pattern | Minimum content | Generated how |
| --- | --- | --- | --- |
| Character identity sheet | @name | Front, 3/4, profile on neutral grey; full body + face close-up; base wardrobe; T-pose or relaxed stand | Image gen, one sheet, same seed/style |
| Character expression sheet | @name_expr | 6–9 faces: neutral, small smile, doubt, fear, anger, surprise, tired, listening, caught | Same identity ref as input |
| Wardrobe variants | @name_v2, @name_armor | Same body, declared alternate costume, front + back | Input @name + costume description |
| Voice reference | @name_voice | 10–20 s clean speech in the character's language, neutral + one emotional line, no music, no room echo | TTS/voice clone or recorded, saved as audio ref |
| Prop sheet | @prop_name | Object on neutral grey: front, side, top, scale next to a hand, and one shot in-hand or in-use; material and wear stated | Image gen, single sheet |
| Location plate — wide | @loc_name | The master establishing view with time of day and the key light source visible | Image gen or 3D render / Unreal / splat |
| Location plate — coverage angles | @loc_name_a, @loc_name_b | The two reverse angles used for OTS coverage, same lighting | Same as above |
| Frame plates | @frame_N | First frame or last frame of a prompt, used to chain prompts | Exported from previous generation |
| Style plate | @style_name | One image that defines palette, grain, brush, render look, with no story content | Image gen |
| Motion ref | @Video N / @move_name | 5–10 s clip that defines camera rhythm or choreography only | Any owned/licensed clip |

Rules:
- Prop sheets are mandatory for any object that changes hands, matters to the story, or appears in more than one shot. A prop described in words drifts. A prop with a sheet holds.
- Location plates are shot from the actual coverage angles the prompt will use. If the prompt has OTS A / OTS B, the location package has both reverse plates.
- Everything on neutral grey except location plates. Backgrounds leak.
- The style plate is generated once and added to every prompt as @style_x defines palette, texture and render look only. Do not use its content.

### 2.2 Prompts for generating the sheets (templates)
**Character identity sheet:** Character reference sheet on flat neutral grey background, [art style lock]. [Name]: [age, build, face shape, eye color, hair length/texture/color, skin, distinguishing marks]. Base wardrobe: [items, colors, materials, wear]. Layout: full body front view, full body 3/4 view, full body profile, face close-up front, face close-up 3/4. Same lighting on all views: soft overcast key from front-left, no shadows on background. No text, no labels, no props, no other characters.

**Prop sheet:** Prop reference sheet on flat neutral grey background, [art style lock]. [Prop]: [exact size in cm], [material], [color], [wear/scratches/patina], [any moving parts]. Layout: front view, side view, top view, the prop held in an adult hand for scale, the prop resting on a wooden table. Consistent soft key from front-left. No text, no labels.

**Location plate (wide + reverses):** Location plate, [art style lock]. [Place]: [architecture, materials, dimensions, notable fixtures], [time of day], [weather]. Key light: [source, direction, color]. Fill: [source, direction, color]. View 1: establishing wide from the [door/entrance] looking toward [landmark], camera at 1.6 m. No people, no text. Then two more with: View 2: from [position A] looking toward [position B], 35mm, same lighting. and the reverse.

**Voice reference:** [Name]'s voice: [age], [pitch], [texture], [accent / language], [pace]. Record 15 seconds: one neutral line, one quiet emotional line, one short exclamation. Dry, no music, no reverb, no room noise.

### 2.3 Tag syntax
| Platform | Syntax | Example |
| --- | --- | --- |
| Magnific / fal / general | @tag lowercase, no spaces | @malacha, @mansion2, @frame11 |
| Seedance 2.5 / Dreamina official | @Image 1, @Video 1, @Audio 1 | @Image 1 defines Malacha's face… |

Never rename a tag mid-project. Never mix the two syntaxes in one prompt. Every tag in the prompt has a line in the Role Map. Unmapped tag = leak. Never say "respectively". One line per asset.

### 2.4 Role map grammar
*what it defines + what it must NOT contribute.*
- @malacha defines Malacha's face, hair, skin texture, body proportions and default wardrobe. Do not use its background or lighting.
- @malacha_voice defines Malacha's voice: timbre, accent, cadence. Do not use its room noise.
- @prop_key defines the brass key: shape, size (9 cm), worn brass finish, red thread on the bow. Do not use the hand or table in the sheet.
- @mansion2 defines the ballroom layout, columns, staircase frame-right of the door, materials. Do not use any people.
- @mansion2_a defines the angle from the door toward the staircase. @mansion2_b defines the reverse.
- @style_film defines palette, grain and render look only. Do not use its content.
- @frame11 is the first frame. It defines opening composition and positions.
- Multiple views of one subject: @malacha, @malacha_expr define one same character. Keep exactly one Malacha throughout.
- Environment refs: say the layer inherited (layout / materials / lighting).

### 2.5 Voice locking (every speaking character)
- @name_voice attached in the role map even for one word.
- Dialogue written as: Malacha (@malacha_voice), quiet, almost to herself: {No debería estar aquí.}
- Declare language once: Dialogue language: natural Mexican Spanish.
- Delivery is an instruction (quiet / dry / half-laugh / under her breath), not an adjective.
- Add accurate lip sync and finish all dialogue before [physical action] when the line and an action are close together.
- If no audio slot exists: the voice description text is identical in every prompt. Consistency is repetition.

## 3. Character Profiles and Performance Direction
### 3.1 Profile block (paste verbatim in every prompt)
```
[Character: Malacha]
Identity: @malacha / @malacha_expr — single strict visual reference. Lock face, jawline, eye color, hair length and texture, skin, body proportions, posture.
Voice: @malacha_voice — low, dry, unhurried, slight rasp. Mexican Spanish native.
Wardrobe (this scene): black wool coat, grey scarf, no hat. Exactly as @malacha unless stated.
Props: @prop_key (brass key) — owned by Malacha, in her right hand until placed on the table.
Acting register: understated, watchful, holds eye contact a beat too long, speaks after a breath.
Do not use: any other character's wardrobe; no hats; no glasses.
```
- Max 3 recurring characters per prompt.
- Prop ownership is explicit: who holds it, when it changes hands, where it ends.
- Scale explicit for non-humans: "knee-height to the human guard, not minion-size, not tiny."
- Count locked: Keep exactly one Malacha and exactly one Guard throughout.

### 3.2 Performance direction rules
Direct the actor, not the "vibe".
- **Visible actions only.** What the character looks at, touches, does, reacts to. "She glances down at her empty left palm" beats "she feels hungry."
- **Micro-beats.** Exhale before a line. Glance away then back. Weight shifts. A half-smile that fades. Hands doing something real.
- **Pauses are written.** "Beat of silence." "She holds the look for two seconds." "He does not answer immediately."
- **Dialogue is spontaneous.** Short lines, contractions, interruptions. Max 2–3 lines in 15s, 4 in 30s. Lines are timed inside the range; action after the line is stated.
- **Reactions get their own time.** A reveal without a reaction shot is half a beat.
- **Intention per character per beat.** "Malacha wants him to take the key. The Guard wants her to leave without it."
- **Restraint.** No exaggerated expressions unless the style is cartoon comedy and it is declared.
- **Effects support the performance.** Magic/VFX are small, timed, cast light on skin and surfaces, and the character's eyes follow them.

## 4. Duration Playbooks
### 4.1 Shot budgets
| Duration | Max shots | Ideal | Avg shot | Story shape |
| --- | --- | --- | --- | --- |
| 5s | 1 | 1 | 5s | One action, one endpoint |
| 10s | 3 | 2 | 4–5s | Setup → payoff |
| 15s | 4 | 3 | 4–5s | Setup → action/reveal → reaction |
| 20s | 5 | 4 | 4–5s | Establish → build → turn → payoff |
| 30s | 7 | 5–6 | 4–6s | Three stages 0–10 / 10–20 / 20–30 |

- No shot under 2s. No shot over 8s unless a declared continuous take.
- Consecutive, non-overlapping ranges: 0–4s, 4–9s, 9–15s.
- Last beat always resolves. No new idea in the final 3 seconds.
- Continuous single-take is allowed at any duration; then use named movements instead of cuts and keep the camera physically plausible (stationary phone, handheld operator, tethered follow).

### 4.2 15s — setup / action or reveal / reaction
```
0–4s   ESTABLISH — wide (or declared continuous frame). Geography, key light visible, intention readable.
4–8s   COVERAGE A — OTS or medium on A. One line or one action.
8–12s  COVERAGE B — reverse OTS on B. Reply or reveal.
12–15s REACTION / TURN — insert, push-in, or return to wide. Hold the reaction to the end.
```
Line is set in the establishing shot. OTS pairs mirror. End on a face if emotional, on the object/space if physical.

### 4.3 20s — action or discovery
```
0–4s    ESTABLISH — wide or slow reveal.
4–9s    APPROACH — tracking/follow. Screen direction set.
9–14s   CONTACT — medium/close. Physical cause → effect.
14–18s  CONSEQUENCE — reaction or wide. World responds.
18–20s  BUTTON — held frame or micro-move.
```

### 4.4 30s — three-stage story
```
[0–10s] STAGE 1 — SETUP: initial state → one event → visible end state.
[10–20s] STAGE 2 — ESCALATION: inherit locks in one line → one event → end state.
[20–30s] STAGE 3 — PAYOFF: closing action → final composition, hold 1–2s.
```
Two shots max per stage.

### 4.5 Timing syntax
- Range `0–6s` — pacing allocation.
- Exact point `At 12s the lantern flares amber.` — max 1–2 per prompt.
- Relative `Two seconds after the door slams, the dog barks.` — causal.
- Never frame-accurate. Never two major actions in one range.

## 5. Shot Grammar
### 5.1 Order for a story beat
Establishing → Master → Coverage (OTS / medium / close) → Insert → Resolution. Skip levels, never invert without reason.

### 5.2 Vocabulary
**Sizes:** extreme wide / establishing · wide · medium wide (cowboy) · medium · medium close-up · close-up · extreme close-up / insert.
**Setups:** over-the-shoulder (always say whose shoulder, which side of frame) · two-shot · low angle · high angle · POV (only when physically plausible) · dutch (only when motivated).
**Movement — always relational:** "Locked frame, no camera move." · "Slow dolly-in from medium to close-up over 4s." · "Camera tracks backward 1.5 m ahead of the subject, matching her pace." · "Lateral track left-to-right at walking speed, subject frame-center." · "Quarter orbit clockwise, 90°, subject centered." · "Camera rises 3 m revealing the courtyard." · "Subtle handheld, breathing sway, no whip pans." · "Rack focus from foreground key to background face."
Rules: one move per shot; give size + angle + move + position relative to subject + speed; lens feel allowed ("85mm compression, soft background").

### 5.3 Over-the-shoulder conversation set
- Establish the two-shot/wide first (sets the line).
- OTS on A: A's shoulder foreground-left, B's face frame-right looking left.
- OTS on B: B's shoulder foreground-right, A's face frame-left looking right.
- Eye-lines match. Same lens, same height, same distance both sides.
- Key light stays on the same physical side of both faces.
- Never cross the line. If you must, insert a neutral shot between.

### 5.4 Axis and screen direction
- Declare in the establishing shot: "Malacha frame-left, Guard frame-right; keep this axis for the whole sequence."
- One direction of travel per prompt. Exit frame-right → enter frame-left next shot.
- Reversals only with a visible turn or a neutral shot.

### 5.5 Continuity across shots and prompts
- Each cut inherits the end state of the previous shot: position, prop, light, expression. Write it: "Continuing from the key on the table…"
- No time jumps unless declared: "Hard cut, 10 minutes later, same room, dusk."
- Chaining prompts: end frame of prompt N becomes @frame_N in prompt N+1; paste the character profiles verbatim; carry axis and lighting in the header.

## 6. Lighting Language
Format: **source → direction → quality → color → effect on subject.**
- "Single practical: candelabra on the table, warm 2700K, soft falloff, key from frame-left on both faces. Moonlight fill from the window behind, cool blue, low."
- "Overcast daylight through tall windows, soft, low contrast, no crushed blacks, faces readable."
- "Sodium street lamp overhead, hard top-light, amber, deep but not black shadows, wet asphalt reflections."

Rules: name the key and its side; keep it across reverses. Default look: low contrast, soft shadows, not too dark, shadows keep detail. Lighting changes are timed events, once. Time of day explicit. Mixed sources when motivated ("moonlight mixed with candlelight"). Never write "cinematic lighting" — write the lamp.

| Mood | Recipe |
| --- | --- |
| Intimate drama | one warm practical + cool window fill, low contrast |
| Gothic / fantasy | moonlight key above-behind, candle fill front, haze for depth |
| Tension | single hard side source, negative fill, shadows keep detail |
| Hopeful / open | soft overcast or bounced daylight, wide range, pastel sky |
| Action exterior | direct sun, long shadows, dust catching light |
| Sci-fi interior | cool panel practicals + one warm accent, clean reflections |
| Backstage / vlog | mixed practical set lights blurred behind, soft front from a bounce, believable skin |

## 7. Art Style Lock
Format: medium + technique/era + palette + texture + edge behaviour + what stays realistic.
- "Photoreal, 35mm film grain, muted teal-amber grade, soft halation on practicals."
- "Painterly 2D, gouache texture, visible brush edges, 6-color palette, backgrounds like painted plates, characters on 2s."
- "Stylized 3D, Pixar-adjacent proportions, matte materials, grounded physics."
- "90s cel anime, hard shadow shapes, held frames, painted backgrounds."
- "Stop-motion, felt and clay, fingerprints, slight frame jitter, miniature DOF."

Rules: declared once in the header, repeated in locks, applies to everything ("all elements share one medium"), physics stays grounded, no media mixing unless the mix is the story. Attach @style_x plate when available.

## 8. Story Rules for a Single Prompt
Scene promise in one sentence with a change in it. Setup / turn / payoff. One protagonist; others react. One location unless the move is the action. One emotional arc. Irreversible endpoint. Sparse dialogue; pauses and breaths are beats. Last 2–3s are a hold.

## 9. Sound Rules
- Per beat, chronological, matching the visible events.
- Diegetic by default. NO MUSIC explicit. If score: functional description + entry time.
- Dialogue format with voice tag, delivery, language. Accurate lip sync. Finish all dialogue before [action].
- Silence is a tool.
- Seedance channels: ( music ), < sfx >, { dialogue }, 【 subtitle 】. Say No subtitles.

## 10. Continuity Locks (paste block)
```
[CONTINUITY LOCKS]
Identity: @malacha and @guard exactly as reference in every shot; exactly one of each.
Wardrobe: unchanged.
Props: @prop_key — Malacha's right hand → table at 13s → stays.
Space: @mansion2 layout; staircase frame-right of the door.
Axis: Malacha left / Guard right; never crossed.
Screen direction: left-to-right.
Lighting: candelabra key frame-left, moonlight fill behind; constant.
Camera: same lens height for all OTS; one move per shot.
Style: @style_film; [style line].
Time: continuous, no ellipsis.
```

## 11. Negative Constraints (paste block)
```
[NEGATIVE]
No music (unless specified). No subtitles, UI, text, logos, watermarks, branding.
No transitions, dissolves, fades, speed ramps, slow motion. Hard cuts only.
No extra characters or background people unless established.
No wardrobe, hair or face drift. No new or duplicated props.
No camera moves not listed. No whip pans, no dutch angles.
No crushed blacks, no blown highlights, not too dark.
No lens flares or anamorphic streaks unless in the style lock.
No exaggerated expressions. No large effects that overpower the performance.
```

## 12. Pre-Send QA
- ☐ Reference package exists: character sheet, voice, prop sheets, location plates, style plate.
- ☐ Header: duration, aspect, cut rule, style lock.
- ☐ Every @tag mapped with job + exclusion.
- ☐ Every character: identity + voice + wardrobe + props + acting register.
- ☐ Scene promise = one sentence with a change.
- ☐ Staging block: positions, intentions, acting style, effect rule.
- ☐ Opens on geography or declared @frame.
- ☐ Ranges consecutive, within shot budget; each range = camera + action + dialogue + reaction.
- ☐ OTS pairs mirrored; axis and direction stated.
- ☐ Lighting: named source, side, quality.
- ☐ Sound per beat; NO MUSIC stated; lip sync + dialogue-before-action stated.
- ☐ Locks + negative present. Last beat holds. No banned adjectives. Word budget.

## 13. Repair Table
One variable per retry. Two same failures → restructure.

| Symptom | Fix |
| --- | --- |
| Face drifts | Repeat identity tag inside each beat; reduce to 2 characters; add @name_expr. |
| Voice changes | @name_voice on every line; identical delivery words. |
| Prop drifts / multiplies | Add a prop sheet; lock count and ownership per stage. |
| Cuts blend | "HARD CUT" at each boundary; fewer shots. |
| Axis flips | Restate axis per beat; neutral insert between reverses. |
| Camera chaos | One move per shot; height, distance, direction, speed. |
| Lighting jumps | Name key source and side in header + locks. |
| Too dark | "Low contrast, shadows keep detail, faces readable." |
| Overacting | "Understated, small expressions, believable pauses." |
| Effect swallows the scene | Size it ("very subtle, translucent"), time it, tie it to light on skin. |
| Style wobbles | Attach @style_x; "all elements share one medium." |
| Too long | Delete adjectives, then merge adjacent beats. |

## 14. Examples
The owner's full production examples (A — "The Key", 15s OTS dialogue, photoreal gothic; B — "Gate Breaker", 20s action, stylized 3D; C — "Two Loaves", 30s three-stage, painterly 2D; D — "Cupcake", 15s continuous vlog) are the reference for tone and density. Example A's prompt, the canonical shape Story mode emits:

```
[HEADER]
Duration 15s. 21:9. Image+audio-to-video. Hard cuts only, no transitions.
Style lock: @style_gothic — photoreal, 35mm grain, low contrast, soft shadows, muted amber-blue grade, soft halation on candle flames. NO MUSIC. No text, no UI.

[REFERENCE ROLE MAP]
@malacha and @malacha_expr define one same character: Malacha's face, scar on left brow, hair, skin, proportions, black wool coat and grey scarf. Do not use their grey background.
@malacha_voice defines Malacha's voice: timbre, accent, cadence. Do not use its room noise.
@guard defines the Guard's face, grey beard, height, dark wool uniform with brass buttons. Do not use its background.
@guard_voice defines the Guard's voice.
@prop_key defines the brass key: 9 cm, worn brass, red thread on the bow. Do not use the hand or table from the sheet.
@mansion2 defines the ballroom layout, columns, staircase frame-right of the door, marble, windows and candelabra position. @mansion2_a defines the angle toward the staircase; @mansion2_b the reverse toward the door. Do not use any people.
@style_gothic defines palette, grain and render look only.

[CHARACTER PROFILES]
Malacha (@malacha / @malacha_voice): black wool coat buttoned, grey scarf, hood down, @prop_key in her right hand, thumb over the bow. Acting register: guarded, still, speaks after a breath, holds eye contact a beat too long. Exactly one.
Guard (@guard / @guard_voice): dark uniform, hands clasped behind his back the whole scene until the last shot. Acting register: tired authority, does not raise his voice, looks at the key before he looks at her. Exactly one.
Dialogue language: natural Mexican Spanish.

[SCENE PROMISE]
Malacha returns the stolen key; the Guard refuses to take it, and she sets it down anyway.

[STAGING + PERFORMANCE]
Night interior, @mansion2. Malacha stands frame-left near the candelabra side table; the Guard frame-right at the foot of the staircase, 3 m apart. Malacha wants him to take the key and end it. The Guard wants her to leave without making him decide. Both understated. Her only big movement is lowering the key. His only movement is a slow head shake. No one else in the room.

[SPACE + LIGHTING]
Key: candelabra on the side table frame-left, warm 2700K, soft, falls on the left side of both faces. Fill: moonlight through the tall windows behind them, cool blue, low. Constant in all shots. Low contrast, shadows keep detail, faces readable, not too dark. Axis: Malacha left / Guard right for the whole sequence.

[TIMELINE]
0–4s  ESTABLISHING WIDE from @mansion2, locked frame, camera at 1.6 m. Both figures small in the hall, candle glow left, moonlit windows behind. Malacha takes two slow steps toward the Guard, left-to-right, and stops. The key catches the candlelight in her right hand. The Guard does not move. She exhales.
4–8s  HARD CUT. OTS over Malacha's left shoulder (her shoulder foreground-left, soft), Guard's face frame-right looking left, medium close-up, 85mm feel, angle from @mansion2_a. Slow dolly-in 20 cm over the shot. The Guard's eyes go to the key first, then to her face. Malacha (@malacha_voice), quiet, after a breath: {Lo traje de vuelta.}
8–12s HARD CUT. Reverse OTS over the Guard's right shoulder (foreground-right), Malacha's face frame-left looking right, same lens, same height, same distance, angle from @mansion2_b. She raises the key slightly toward him, wrist only. The Guard gives one slow head shake. Guard (@guard_voice), low, steady: {Ya no sirve.} Beat of silence, one second. Her jaw tightens; she does not look away.
12–15s HARD CUT. Insert, extreme close-up, locked: her right hand lowers @prop_key onto the marble side table beside the candelabra, thread trailing. The candle flame flutters from the air movement and light shifts across the brass. Her hand withdraws frame-left. Hold on the key alone for the final 1.5s.

[AUDIO]
<large stone-hall room tone, faint wind at the windows, two footsteps on marble at 0–4s, cloth movement of the wool coat>. Dialogue as written, natural conversational delivery, accurate lip sync, lines finished before each cut. <brass key set on marble at 13s: small clear click, candle flame flutter>. NO MUSIC. No subtitles.

[CONTINUITY LOCKS]
Identity exactly as @malacha and @guard, one of each, all shots. Wardrobe unchanged. @prop_key: Malacha's right hand → table at 13s → stays. Axis Malacha left / Guard right, never crossed. Screen direction left-to-right. Candelabra key frame-left on both faces in every shot. Same lens height and distance for both OTS. Style line unchanged.

[NEGATIVE]
No music, no subtitles, no UI, no text, no transitions, no extra characters, no camera moves beyond those listed, no crushed blacks, no lens flares, no wardrobe or hair change, no face morphing, no second key, no exaggerated expressions.
```

## 15. Quick Reference Card
```
PACKAGE    Character sheet + expr sheet + voice + prop sheets + location plates (wide + 2 reverses) + style plate
ORDER      Header → Refs → Characters → Promise → Staging+Performance → Space+Light → Timeline → Audio → Locks → Negative
BUDGET     15s = 3 shots · 20s = 4 · 30s = 5–6 (3 stages) · min 2s · max 8s
OPEN       Establishing wide first (or declared @frame continuation)
CONVO      Wide → OTS A → OTS B (mirrored) → insert/turn. Same lens, height, key side.
AXIS       Declare left/right once. Never cross. Neutral insert if you must.
DIRECTION  One direction of travel per prompt.
CAMERA     One move per shot; size + angle + move + position + speed.
ACTING     Visible actions, breaths, glances, pauses. Intention per beat. Understated.
EFFECTS    Small, timed, cast light on skin, eyes follow them.
LIGHT      Source → direction → quality → color. Low contrast, shadows keep detail.
VOICE      @name_voice on every line. Language declared. Delivery as instruction. Lip sync. Line before action.
SOUND      Per beat, chronological, diegetic. NO MUSIC unless asked.
STYLE      Declared once in header, repeated in locks, style plate attached.
END        Last 2–3s hold. Irreversible endpoint. No new idea.
FIX        One variable per retry. Adjectives never fix staging.
```
