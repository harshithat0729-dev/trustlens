# Competitor scan  (Day 1 deliverable)

**Why we do this:** so we (a) never overclaim ("world's first"), (b) sharpen our real
differentiation, and (c) hand judges a comparison table that proves we did our homework.

## Comparison table

| Tool | What it is | Inputs | Languages | Strengths | Gap vs TrustLens | Link |
|---|---|---|---|---|---|---|
| **Cyberwall** (Kerala Police) | Free public AI digital-safety assistant; WhatsApp / Telegram chatbot | 9+ types: text, screenshot, link, QR, APK, phone no., email, bank details, IP, voice note | English + Malayalam | Govt-backed trust; 35-40+ checks; Trust Score /100; clear "do this next" guidance; ~90k queries in first 4 weeks | No Telugu / Tinglish; chatbot-first (not our simple mobile flow); says "scam / not scam" more than showing a combined evidence report | cyberwall.keralapolice.gov.in |
| **SafeMeAI** | Free prototype web + Android app; "scam / looks genuine / not sure" | Message, link, UPI ID, phone number, website, document text | English + Hindi | Plain-language verdict + next steps; scam-word + fake-site + bad-number checks; on-device option; "not sure" state | No Telugu / Tinglish; no multimodal media (image/video) evidence report; narrower "trust" framing | safemeai.in |
| **Sanchar Saathi - Chakshu** (DoT, Govt of India) | Official **reporting** portal for suspected fraud calls/SMS/WhatsApp | Report form (call, SMS, WhatsApp) | English + Hindi | Authoritative; can trigger action on the sender (disconnect/FIR) | Not an analysis tool - it reports, it doesn't explain risk; we can *link* to it | sancharsaathi.gov.in/sfc |
| **AI4TRUST** (EU Horizon) | Research platform: human+AI disinformation detection for media/fact-checkers | Text, audio, visual, multimodal at platform scale | 8 EU languages | Deepfake video/audio detection, verdict generation, real-time platform monitoring | Not a consumer mobile app; built for professionals; EU-focused; no Indian language | cordis.europa.eu/project/id/101070190 |
| **Google SynthID** | Watermark + detector for AI-generated content | Image, video, audio, text | (tool UI) English | Detects Google/partner AI content; watermark survives edits; SynthID Detector portal | Only finds *its own* watermarks - **not a universal fake detector**; no message/link/claim checking | deepmind.google/models/synthid |

## What this means for us

1. **We are NOT first.** Cyberwall (Kerala Police) and SafeMeAI already do "check a suspicious
   thing, get a risk read-out". Never claim "world's first".
2. **The real gap we can own** is narrow and honest:
   - **Telugu / Tinglish-first** explanation (Cyberwall = Malayalam, SafeMeAI = Hindi).
   - **One simple mobile flow** that combines link + message + image/video + claim (not a chatbot,
     not a professional research platform).
   - **A combined evidence report** with sources + limitations + uncertainty - not just a score.
   - **Honest "Inconclusive"** as a first-class result, matching how Cyberwall itself admits
     "no automated system is 100% accurate".
3. **Free, credible data points to cite** for judges: Cyberwall's 90k queries/4 weeks shows the
   demand is real; SafeMeAI's "not sure" state validates our uncertainty-first design.
4. **SynthID is a complement, not a competitor** - where available it can be *one signal* in our
   media module (and we must state its limit: it only detects its own watermarks).

## Sources

- Cyberwall (Kerala Police): https://cyberwall.keralapolice.gov.in/  and /faq
- Cyberwall usage (news): https://www.newindianexpress.com/states/kerala/2026/Sep/20/over-90000-queries-in-four-weeks-kerala-polices-cyberwall-is-a-big-hit
- SafeMeAI: https://safemeai.in/  and Play Store listing
- Sanchar Saathi / Chakshu: https://www.sancharsaathi.gov.in/sfc/
- AI4TRUST: https://cordis.europa.eu/project/id/101070190
- Google SynthID: https://deepmind.google/models/synthid/  and SynthID Detector blog
