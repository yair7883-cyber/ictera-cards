# Free and Code-Only AI Avatar Video Pipeline (as of Nov 2026, USD)

Research limits: fal.ai, ai.google.dev, invideo, markaicode, gpuperhour and similar hosts were NOT fetchable from this session (network allowlist). All prices below come from WebSearch result summaries and secondary sources, not from the vendors' live pages. Every price is "verify before budgeting".

## 1. What is free or open-source, and where does it run (free host vs paid GPU)?

### Takeaway
Free tiers (Colab, Kaggle, HF ZeroGPU) are good for demos, TTS, Whisper captions and small image models, but not for dependable 14B-class video or lip-sync generation. Open-source talking-avatar models exist (InfiniteTalk, Wan 2.2 S2V, LTX-2.3 audio-to-video), but practical use needs quantized builds or a rented GPU. No reliable Hebrew-quality open-source TTS was found.

### Cited Findings
- InfiniteTalk (MeiGen-AI, built on Wan 2.1) is open source, supports unlimited-length audio-driven talking video, has a low-VRAM mode and 720P output, and is integrated into Wan2GP (low-VRAM tool) — [MeiGen-AI/InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk)
- A community one-click Colab notebook for InfiniteTalk exists; README warns about Colab session timeouts and pins torch 2.4.1 with flash_attn — [InfiniteTalk-Google-Collab](https://github.com/sruckh/InfiniteTalk-Google-Collab)
- Wan 2.2 S2V-14B (speech-to-video) is available with ComfyUI workflows including Q4 GGUF quantized versions for low VRAM; no VRAM figures found — [aistudynow guide](https://aistudynow.com/wan-2-2-s2v-14b-speech-to-video-comfyui-workflow-gguf-ready/)
- LTX-2.3 audio-to-video avatar workflow in ComfyUI with GGUF/low-VRAM variant is claimed; the source is a Patreon/affiliate-style post, treat as unverified — [Patreon post](https://www.patreon.com/TheLocalLab/posts/animate-any-free-153297616)
- Colab free does not publish limits; one guide estimates 15-30 GPU-hours/week on T4-class with 12h sessions (estimate only) — [gpuperhour](https://gpuperhour.com/blog/free-cloud-gpus-and-credits); Colab FAQ confirms limits are unpublished/variable — [Colab FAQ](https://research.google.com/colaboratory/faq.html)
- Kaggle: 12h session limit documented; the "30 h/week" figure is widely cited but not confirmed in docs; a staff announcement reportedly retired the P100 option on Sept 15, 2026, T4 x2 (16 GB each) remain — [aimultiple](https://aimultiple.com/free-cloud-gpu), [gpuperhour](https://gpuperhour.com/blog/free-cloud-gpus-and-credits)
- HF ZeroGPU free quota: documented as about 5 GPU-minutes/day for free accounts (a conflicting guide says 25 min for PRO) — [HF forum](https://discuss.huggingface.co/t/what-is-the-free-zerogpu-quota-for-1-space/178610)
- Paid GPU (RunPod, billed per second; prices vary by snapshot): RTX 4090 about $0.34-1.15/h, A100 about $1.39-1.79/h, H100 about $2.89-4.39/h — [RunPod pricing](https://www.runpod.io/gpu-pricing), [Thunder Compute comparison](https://www.thundercompute.com/blog/Runpod-pricing-vs-thunder-compute)
- Not researched/verified (no source retrieved): SadTalker, Wav2Lip, LatentSync, HunyuanVideo, Flux.2 Kontext open weights, Qwen-Image-Edit, LoRA training specifics, Remotion/HyperFrames/MoviePy details.

### Inferences
- An A100 at about $1.5-1.8/h is likely the sweet spot for self-hosting InfiniteTalk/Wan S2V, but a 30s talking-head clip probably takes many minutes of GPU time (not measured here); per-reel self-hosted cost is plausibly under $1-2 but uncertain.
- For a solo creator, free Colab for video is fragile (timeouts, quotas, dependency pins); use it only for experiments.

### Gaps
- Real VRAM/runtime numbers for InfiniteTalk, Wan 2.2 S2V, LTX-2.3 on a T4/A100; open-model licenses; Kontext/Qwen-Image-Edit/LoRA free-host feasibility.

## 2. Hebrew TTS and captions

### Takeaway
Best-evidenced Hebrew TTS options are cloud (Edge/Azure he-IL Avri and Hila, Gemini TTS, ElevenLabs v3, MiniMax). Open-source Hebrew TTS is niche. Gemini TTS is extremely cheap per reel.

### Cited Findings
- Hebrew TTS comparison (snapshot 22 Mar 2025, out of date): MiniMax best; Edge TTS (Avri, Hila), Gemini (Puck, Zephyr), ElevenLabs good; Chatterbox and Resemble poor; ElevenLabs needs v3 with Hebrew code, multilingual v2 was unintelligible — [Hebrew-TTS-Providers](https://github.com/danielrosehill/Hebrew-TTS-Providers)
- Open-source Hebrew: Phonikud (G2P front-end, Interspeech 2026, works with Piper) — [phonikud](https://phonikud.github.io/); LightBlue (MIT, CPU real-time, self-reported quality) — [LightBlue](https://huggingface.co/niobures/LightBlue/blob/main/README.md); Kokoro-Hebrew SASPEECH (commercial use restricted) — [avris/kokoro-hebrew-saspeech](https://huggingface.co/avris/kokoro-hebrew-saspeech); pitput (private research only) — [pitput](https://huggingface.co/useless-ai/pitput)
- Gemini 2.5 Flash TTS: $0.50/1M input tokens, $10/1M audio output tokens; audio = 25 tokens/second; newer preview TTS models have different rates — [Google Cloud TTS pricing](https://cloud.google.com/text-to-speech/pricing). Hebrew support not confirmed in sources found (the 2025 comparison above says Gemini works for Hebrew).
- Azure neural TTS free tier: 0.5M characters/month; paid price masked in results ("$-") — [Azure Speech pricing](https://azure.microsoft.com/en-us/pricing/details/speech/)
- ElevenLabs Free: 10,000 credits/month (about 10 min), NO commercial license; Starter (about $5-6/mo, 30,000 credits) is cheapest commercial tier — [dupple summary](https://dupple.com/learn/is-elevenlabs-free), [bigvu](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) (third-party)

### Inferences
- 30-60s of Gemini TTS = 750-1500 audio tokens = about $0.008-0.015 (computed from cited rates). Effectively free; Azure free tier also covers it.
- Whisper (open-source, local or free Colab) for word-level captions is standard, but Hebrew accuracy of base Whisper is mediocre; ivrit.ai fine-tunes exist (listed in the Hebrew-TTS-Providers repo as a Hebrew speech resource; not verified here).

### Gaps
- Azure paid per-1M-char price; Gemini TTS Hebrew confirmation in 2026 docs; current Hebrew quality ranking (the only benchmark is Mar 2025).

## 3. API prices (video, image) and cost estimate

### Takeaway
Cheapest credible API video: Veo 3.1 Lite (about $0.05-0.08/s) and Wan 2.5 (about $0.05/s), then Kling 2.5 Turbo (about $0.07/s), Veo 3.1 Fast ($0.10-0.12/s). A 30s, 8-shot reel costs roughly $1.5-4 in video plus under $1 for images/TTS before retries; real cost is typically 2-3x with re-rolls.

### Cited Findings
- Google Gemini API: Veo 3.1 standard $0.40/s (720p/1080p), $0.60/s 4K; Veo 3.1 Fast cut Apr 7 to $0.10/s 720p, $0.12/s 1080p, $0.30/s 4K; Veo 3.1 Lite $0.05/s 720p, $0.08/s 1080p; model IDs listed as preview; a forum thread flags confusing Lite pricing display — [The Decoder](https://the-decoder.com/googles-veo-3-1-lite-cuts-video-generation-costs-by-more-than-half/), [Wavespeed](https://wavespeed.ai/blog/cost-and-billing/google-veo-3-pricing/), [Google forum](https://discuss.ai.google.dev/t/the-documentation-for-veo-3-1-using-table-is-incostient-with-what-is-shown-on-the-generative-ai-page/145253)
- fal.ai (via search summary, sources disagree): Veo 3.1 $0.20/s no audio, $0.40/s with audio (Fast from $0.10/s); Kling 2.5 Turbo Pro $0.35 for 5s then $0.07/extra s; Kling 3.0 Pro 5s clip $0.56 no audio / $0.84 audio; Seedance 2.0 Fast $0.2419/s 720p, Standard $0.3024/s (audio included); Seedance 2.5 listed $0.47/s 720p; Wan 2.5 $0.05/s (480p only confirmed) — [fal image-to-video pages](https://fal.ai/explore/image-to-video-apis), [omr.com](https://omr.com/en/reviews/product/fal/pricing), [invideo pricing roundup Aug 2026](https://invideo.io/blog/ai-video-model-pricing)
- Images: FLUX.1 Kontext [pro] on fal about $0.04/image (billed per megapixel, rounded up; checked 23 Sep 2026) — [markaicode fal pricing](https://markaicode.com/pricing/fal-ai-pricing/); Gemini 2.5 Flash Image about $0.039/image (1,290 tokens x $30/M, older snapshot); newer Gemini 3.x image models roughly $0.045-0.134 depending on resolution/variant, conflicting — [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), [Vertex pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- fal exposes a pricing API (api.fal.ai/v1/models/pricing) and bills video per second or per video — [fal docs](https://fal.ai/docs/model-apis/pricing)
- No price found for fal InfiniteTalk / Kling avatar / nano-banana-2 / nano-banana-pro.

### Inferences (computed)
- Reel A (30s, 8 shots of about 3.75s; premium-ish): Veo 3.1 Fast 1080p on Gemini API 30 s x $0.12 = $3.60; if each shot is rounded up to 4s (32s) = $3.84. Images 8 keyframes + 4 rerolls x $0.04-0.07 = $0.5-0.85. TTS about $0.01. Total about $4.1-4.7; with 2x video re-rolls about $8-9. (Veo native audio would also give ambient/speech, but Hebrew lip-sync fidelity is unverified.)
- Reel B (cheap): Veo 3.1 Lite 720p $0.05 x 32 s = $1.60 (or Wan 2.5 at $0.05/s = $1.60; Kling 2.5 Turbo 8 x 5s clips = 8 x $0.35 = $2.80). Images with Gemini 2.5 Flash Image or Kontext about $0.4-0.5, TTS about $0.01, ffmpeg/Whisper free. Total about $2-3.3; with 2x re-rolls about $4-6.
- Premium reference: Seedance 2.0 Fast 30 s x $0.2419 = $7.26 before re-rolls.
- 60s reels roughly double the video component.
- Free-credit routes: Gemini API free tier, fal signup credits, Colab/Kaggle — not verified for video in this session; assume none covers Veo video.

### Gaps
- Official live fal/Gemini pages not fetched; Wan 2.5 price at 720p/1080p; Veo Lite quirk (per-video vs per-second); audio surcharge on Gemini Veo; free credits amounts.

## 4. Can it be orchestrated purely with code? Architecture, caveats, ToS

### Takeaway
Yes. A Python script can do script -> TTS -> keyframes -> i2v clips -> Whisper captions -> ffmpeg/Remotion/HyperFrames compose, with no GUI. Main risks are character consistency, Hebrew lip-sync/TTS quality, preview-model price/availability changes and Instagram AI labeling.

### Cited Findings
- Instagram: creators must label photorealistic video or realistic synthetic audio made with AI; Meta also auto-applies "AI info" labels — [Instagram Help](https://help.instagram.com/761121959519495)
- Since late Aug 2026 Instagram applies an account-level "AI-generated profile" label; undisclosed synthetic-person profiles lose non-follower reach (Reels, Explore); adding the label carries no reach penalty; appeals possible; creators merely using AI tools need not label the account — [TechCrunch 2026-08-31](https://techcrunch.com/2026/08/31/instagram-puts-new-limits-on-undisclosed-ai-profiles/), [Gadget Review](https://www.gadgetreview.com/instagram-is-done-letting-ai-influencers-hide-in-plain-sight), [TechRepublic](https://techrepublic.com/article/news-instagram-ai-generated-profile-label-recommendations/), [Engadget](https://engadget.com/2246914/instagram-will-demote-ai-generated-influencers-if-they-dont-clearly-label-their-account/)
- ElevenLabs free tier forbids commercial use (see section 2); Kokoro-Hebrew SASPEECH restricts commercial use.
- fal.ai reportedly has a "2-request limit" for new/free accounts (title of a Nov 2026 pricing article; details not read) — [markaicode](https://markaicode.com/pricing/fal-ai-pricing/)

### Inferences (proposed architecture)
1. Script/storyboard JSON via LLM (8 shots, Hebrew VO text).
2. TTS: Gemini TTS or Azure he-IL (Avri/Hila) -> WAV; measure duration to set shot lengths.
3. Character keyframes: one reference image (+ optional LoRA) -> Flux Kontext or Gemini image edit per shot, passing the reference each call for consistency.
4. Image-to-video per shot (Veo 3.1 Lite/Fast, Kling 2.5 Turbo, or Wan 2.5) via REST/SDK; poll async jobs; retry failures.
5. Optional talking-head shots only: InfiniteTalk/S2V on rented A100 or a hosted API; use B-roll/voiceover for the rest to cut cost and avoid Hebrew lip-sync artifacts.
6. Whisper (local) word timestamps -> SRT/ASS (Hebrew RTL rendering needs a font and bidi check in ffmpeg/libass).
7. Compose: ffmpeg concat + audio mix + burned captions, or Remotion/HyperFrames for animated captions; export 1080x1920, H.264/AAC, 30 fps.
Caveats: consistency drifts across independent i2v clips (mitigate with first-frame conditioning from the same reference and short clips); i2v clips are about 4-8s so 8 shots suits 30s; async queues and rate limits (fal new-account limits, Gemini quota); preview model IDs/prices may change; save every intermediate for idempotent re-runs; budget 2-3x for re-rolls; label content as AI per Instagram rules.

### Gaps
- No primary-source verification of Meta ToS text, provider rate limits, Remotion/HyperFrames capabilities, or measured consistency quality.
