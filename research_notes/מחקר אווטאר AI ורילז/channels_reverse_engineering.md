# Reverse-engineering @shaxx.ai and @daniel.moldawsky AI-animated reels (as of 2026-11-24)

Access notes: instagram.com is login-walled; beacons.ai, apps.apple.com, ai2people.com and mwm.ai did NOT resolve from this sandbox (not in the allowed network list), so the beacons.ai/shaxx tutorial and App Store pages could not be opened directly. Instagram data below comes from a HasData scraper (public profile/comments JSON), App Store data only via search-engine snippets. No video frames or audio were analyzed, so all tooling/pipeline statements about the actual videos are INFERRED unless marked verified.

## Q1. What is the Pixmo app, pricing, models, free tier?

### Takeaway
The app named in the shaxx.ai bio ("Pixmo", tagged @pixmoai) most plausibly corresponds to the App Store app "PixMo - AI Video Generator" by PixMo Development LLC (a photo-to-video / template-effect app with credits and subscriptions), but the match is by name only; nothing public confirms the underlying models, and a separate web product "Pixmo" (getpixmo.com, faceless YouTube Shorts) also exists.

### Cited Findings
- App Store listing "PixMo - AI Video Generator", developer PixMo Development LLC; iPhone photo-to-video app focused on "scene-specific AI personalization"; listed features include body-curve adjustment, one-tap outfit change, classic scene adaptation; free download with in-app purchases; rating 3.7/5 from 59 ratings — [App Store (via search summary)](https://apps.apple.com/app/id6752974574)
- In-app purchases include credit packs (e.g. 600 credits $7.99) and "PixMo Monthly Pro $12.99"; weekly/monthly/yearly Pro plans range roughly $7.99-$89.99 — [App Store (via search summaries)](https://apps.apple.com/app/id6752974574)
- Store text promotes "new templates added daily that follow social media trends"; one aggregator says the app may no longer be on the App Store (3.71/5, 62 ratings), mixed reviews (some say output looks nothing like the source image) — [MWM aggregator snippet](https://mwm.ai/apps/pixmo-ai-video-generator/6752974574), [AppBrain](https://www.appbrain.com/appstore/pixmo-ai-video-generator/ios-6752974574)
- Independent reviewer: adds natural motion to hair, clothes, background from a photo; works best without pushing sliders far — [ai2people review (snippet only)](https://ai2people.com/pixmo-ai-video-app-review/)
- A different, similarly named listing "AI Video Generator Labs: PIXMO" / "AI Dream Video Generator PIXMO" (id6741569114) exists, and "AI Art Generator - PixMo" (id6757395118, different developer, Jan 2026) — [App Store](https://apps.apple.com/np/app/ai-video-generator-labs-pixmo/id6741569114), [AppGoblin](https://appgoblin.info/apps/6757395118)
- Separate web product "Pixmo — Create Faceless YouTube Shorts with AI" (getpixmo.com): rebuilds an uploaded viral video shot-by-shot with your own characters, or videos starring you from one selfie — [getpixmo.com](https://getpixmo.com/)
- No page found naming the underlying models (Kling/Veo/etc.) for PixMo; Kling/Veo mentions in search belong to other apps — search results above.
- Verified from Instagram scrape (Nov 2026): shaxx.ai bio "I use Pixmo App to make my videos 👀 / How I make my Videos ⬇️", link http://beacons.ai/shaxx, email team@shaxmanagement.com (suggests a management/agency entity "Shax Management"); 151,607 followers, follows 0, verified — [HasData profile scrape](https://api.hasdata.com/scrape/instagram/profile/?handle=shaxx.ai)
- Verified: captions Oct-Nov 2026 tag @pixmoai ("I used @pixmoai to make this video (Peep the link for free step by step tutorial) 🤫 #ai #animation", Oct 20 2026) and from Nov 22-24 repeatedly say "I used Pixmo app to make this video you're watching 😭 #pixmo", "This video was made using pixmo", "Pixmo app made this video too", "I cooked up this video using Pixmo too", i.e. ~9 of the 11 newest posts name Pixmo; others are bare story captions ("Based on true story 🔥", "She dumped me 😭", "He thought he'd win 😭") — same source.
- Verified: the Nov 22-24 burst is ~10 reels in 3 days (high-volume daily posting) — same source.

### Inferences
- INFERRED: "PixMo - AI Video Generator" (PixMo Development LLC) is the promoted app because it is the top App Store hit, is a photo-to-video app with trend templates, and matches the credit/subscription paywall ("is it free or subscription" comments). The handle @pixmoai is not confirmed to belong to that developer.
- INFERRED: Underlying engine is a third-party image-to-video model behind a template/effect layer (typical of such apps); exact model unknown.
- INFERRED: shaxx.ai is a paid/affiliate or partnered promo channel for the app (self-labelled "How I make my videos", tags the brand, repeated "made using Pixmo" captions, management email); the channel's own content (memes) is a vehicle for installs.

### Gaps
- Could not open App Store page directly, so exact free-tier limits, current price list, release date and developer website are unverified.
- No confirmation of underlying models or whether the app is still listed in the US store.
- Whether @pixmoai belongs to PixMo Development LLC: unverified.

## Q2. Public tutorials ("free step by step tutorial") for the shaxx.ai style

### Takeaway
No public tutorial (YouTube/TikTok/Reddit/Medium) was found; the tutorial lives behind the beacons.ai/shaxx link, which was unreachable from this sandbox.

### Cited Findings
- Searches for shaxx.ai + Pixmo tutorial returned only generic image-to-video guides (Pixlr, Picsart) and an unrelated product "Pixo" (pixo.video) with a text-to-multi-scene tutorial — [Pixo tutorial](https://pixo.video/blog/getting-started-pixo), [Pixlr](https://pixlr.com/blog/how-to-create-animated-drawings-with-pixlr/). These are NOT shown to be related to Pixmo.
- Generic reviewer description of the PixMo workflow: upload a single photo, pick a trending template or add a text prompt, export — [ai2people snippet](https://ai2people.com/pixmo-ai-video-app-review/) (snippet-level, not a full tutorial)
- beacons.ai/shaxx: fetch failed (host not resolvable in sandbox) — [beacons.ai/shaxx](https://beacons.ai/shaxx)

### Inferences
- INFERRED from the app category and captions: pipeline is (1) generate/choose a still (character/meme frame), (2) apply a Pixmo trend template/preset or prompt to animate it, (3) add caption text overlay and sound in-app or CapCut. Meme "scenes" (short 5-15 s stories: "He thought he'd win", "I got rewarded for crashing his Lambo") suggest template-driven single-clip animations, not multi-scene storyboards. Unverified without watching the videos.
- INFERRED: the "free tutorial" link is most likely the app's download/affiliate link or a short how-to page (a conversion step), consistent with the promo-funnel model.

### Gaps
- Actual content of beacons.ai/shaxx; any YouTube/TikTok/Reddit tutorial: not found. Needs network allow-listing of beacons.ai or manual check.

## Q3. How @daniel.moldawsky's Hebrew animated cartoon reels are likely made

### Takeaway
Nothing public documents his toolchain. Verified facts are the content/funnel; the cartoon style and tools are inferred, and Hebrew voice via ElevenLabs/HeyGen-type TTS plus a general image/video model is the plausible stack but unconfirmed.

### Cited Findings
- Profile: Daniel Moldawsky, 96,767 followers, verified, owner of @tanaor.jewelry.il; bio claims his brands brought in 53M NIS in 2025, "teaching for free how to build a brand from 0"; bio links to a YouTube channel (free e-commerce courses) and a bit.ly landing page (bit.ly/dmabiolp1) — [HasData profile scrape](https://api.hasdata.com/scrape/instagram/profile/?handle=daniel.moldawsky)
- Reel Df40X3lA9sv (Nov 18 2026), alt text "cartoon", 1080x1920, 106 s long, original audio, 1,498 likes, 226 comments (scraper count), caption: "Based on my story... after building one of the biggest online brands in the country, I decided to teach from 0 how anyone can build their own brand with AI. Want the guide? Comment 'מותג' below" with #איקומרס #תנאור #יזמות #כסף #שופיפיי — [HasData comments scrape](https://api.hasdata.com/scrape/instagram/comments?url=https%3A%2F%2Fwww.instagram.com%2Fp%2FDf40X3lA9sv%2F)
- Reel Df654VUg4Ys (Nov 19 2026), alt text "cartoon of bus", caption "פחות בקטע של ציונים טובים ;)" with #איקומרס #דרופשיפינג #יזמות #כסף #שופיפיי — [HasData profile scrape](https://api.hasdata.com/scrape/instagram/profile/?handle=daniel.moldawsky)
- The cartoon reels are a Nov 2026 shift: previous posts are photos/carousels/lifestyle; an Aug 2026 repost (@yuval_tsarfati) used the same "comment 'מיליונים' to get the episode" mechanic — same profile scrape.
- Hebrew TTS options exist: Fliki (4 Hebrew voices), HeyGen (Hebrew library), Kapwing, Podcastle, VEED (preset voices only) — [Fliki](https://fliki.ai/voices/hebrew), [HeyGen](https://www.heygen.com/text-to-speech/hebrew), [Podcastle](https://podcastle.ai/ai-voices/hebrew-text-to-speech)
- Veo 3 (Google AI Pro) launched in Israel; marketed with lip-synced dialogue and ambient audio (vendor claim); Hebrew quality not verified — [Mako](https://www.mako.co.il/nexter-news/Article-7922bf3beefc791027.htm), [VEED Veo 3](https://www.veed.io/he-IL/ai-models/video-models/veo-3)
- No Israeli creator tutorial or tool attribution for Hebrew AI cartoon reels found.

### Inferences
- INFERRED: A 106 s "story" cartoon is a multi-scene, edited sequence (likely many 5-10 s image-to-video clips from a consistent character sheet, plus voiceover). Likely candidates: still images from Midjourney/Nano Banana/GPT-image style generators for consistent style, animated via Kling/Veo/Seedance/Higgsfield, voice by ElevenLabs or similar (Hebrew supported), stitched in CapCut. None verified.
- INFERRED: "Original audio" under his name means the final edit was exported as one file (voice and music baked in), not a trending sound.
- INFERRED: The cartoon format is a hook-and-storytelling wrapper for an info-product/lead funnel; production is likely semi-automated by an editor/agency (not checked).

### Gaps
- Exact tools, voice (cloned vs stock), lip-sync and consistency method: unknown; requires watching the video (not possible here) or asking the creator.
- Per-reel play counts were not retrievable (scraper returned likes/comments only for the one reel).

## Q4. Comment-to-get-guide automation mechanics

### Takeaway
The "comment the word" funnel is standard ManyChat-style Instagram comment-to-DM automation via Meta's official API; Daniel's comments are visibly single-word keyword replies ("מותג", "מדריך"), consistent with such a trigger (tool itself not identified).

### Cited Findings
- ManyChat flow: Automations > New Automation > "Auto-DM links from comments"; trigger on a specific keyword or any comment, limit to one reel; sends private DM with the link; can post rotating public replies (4-5 variants) to avoid repetition flags; running across all posts needs paid Pro — [ManyChat blog](https://manychat.com/blog/how-to-automate-your-comments-with-manychat/), [ManyChat guide](https://manychat.com/blog/the-ultimate-guide-for-instagram-comment-automation/)
- Add misspellings as keywords; also match the same keyword in DMs; test with a second account — [Chatimize](https://chatimize.com/instagram-comments/)
- Compliance: official Meta-partner tools operate through the API; aggressive keyword triggers/high DM volume can still be restricted — same sources.
- Verified comments on Df40X3lA9sv (Nov 21-24): "מותג" (x7+), "מדריך", plus emoji/"King" comments; the single keyword in caption equals the dominant comment — [HasData comments scrape](https://api.hasdata.com/scrape/instagram/comments?url=https%3A%2F%2Fwww.instagram.com%2Fp%2FDf40X3lA9sv%2F)
- Hebrew keyword support in ManyChat: no source found (English examples only).

### Inferences
- INFERRED: A DM with the guide link then leads to the bit.ly landing page / course funnel (not verified); the commenting also boosts algorithmic engagement (comments count 226 on this reel; user stated 600-1000 on others).
- INFERRED: Same mechanic likely used by shaxx.ai? Not evidenced: its comments ask "is it free", i.e. it relies on the bio link instead.

### Gaps
- Which tool (ManyChat, Inro, Manychat alternatives popular in Israel) Daniel uses; DM content and landing page: not observed.

## Cross-channel growth mechanics (summary)
- shaxx.ai (verified): high-volume meme animations, brand-tagged captions, bio link to tutorial -> app install funnel; follows 0 accounts; email suggests business management. Monetization model (affiliate/sponsor) INFERRED.
- daniel.moldawsky (verified): AI cartoon storytelling reels + comment-keyword lead capture -> free guide -> paid learning offer (bio "want to learn deeper"); sells e-commerce education atop real business credentials.
