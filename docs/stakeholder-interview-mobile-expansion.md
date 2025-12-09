# Stakeholder Interview: Mobile User Expansion Strategy

**Date:** December 12, 2024  
**Duration:** ~25 minutes  
**Participants:**
- **Sarah Mitchell** — VP of Digital Experience, Cronos Retail Group
- **Dev Team Lead** — Technical Lead / Business Analyst

---

## Interview Transcript

**[00:00]**

**Sarah:** Hey, do you have a minute? I just got out of the quarterly analytics review and I need to talk to you about something.

**Dev Lead:** Sure, what's up? You look concerned.

**Sarah:** I am. I've got the traffic numbers in front of me and... look, I knew mobile wasn't our strong suit, but I didn't realize how bad it actually was.

**Dev Lead:** How bad are we talking?

**Sarah:** So, industry average for retail sites right now is around 65-70% mobile traffic. Some of our competitors are seeing 75% or higher. Want to guess what ours is?

**Dev Lead:** Based on your face... 40%?

**[01:15]**

**Sarah:** 31%. Thirty-one percent.

**Dev Lead:** Wow. That's... that's significantly below where we should be.

**Sarah:** And it gets worse. Mobile conversion rate is 0.8%. Desktop is 3.2%. So not only are fewer people coming to us on mobile, the ones that do are barely buying anything.

**Dev Lead:** That's a pretty huge gap. Industry standard mobile conversion is usually lower than desktop, but not by that much.

**Sarah:** Right! I talked to Priya in marketing after the meeting, and she said they've basically stopped running mobile ad campaigns because the ROI is so bad. They're leaving money on the table because our mobile experience is pushing people away.

**[02:30]**

**Dev Lead:** Did the analytics show where people are dropping off on mobile?

**Sarah:** Yeah, and this is the frustrating part—it's everywhere. We lose a chunk on the homepage, another chunk on product pages, and then checkout on mobile is a disaster. Something like 78% cart abandonment rate on mobile versus 45% on desktop.

**Dev Lead:** So it's not one thing, it's death by a thousand paper cuts.

**Sarah:** Exactly. And here's what's really keeping me up at night. Our customer base is aging with us. Our most loyal customers are 35-55, which is great, but we're not capturing younger shoppers. Gen Z and younger millennials are mobile-first—like, exclusively mobile for a lot of them—and we're basically invisible to that demographic.

**[03:45]**

**Dev Lead:** I pulled up the site on my phone yesterday after our last conversation. I see what you mean. The navigation is cramped, the buttons are small, scrolling through products feels clunky...

**Sarah:** Did you try to checkout?

**Dev Lead:** I did. The form fields are tiny, and I had to pinch-zoom to enter my credit card number. And then when I zoomed, the page layout got all messed up.

**Sarah:** *groans* See? And that's someone who understands the app! Imagine a first-time visitor trying to do that.

**[04:30]**

**Dev Lead:** So we talked about mobile responsiveness as part of the phase one refresh. Are you thinking we need to go bigger?

**Sarah:** I think mobile needs to be THE priority, not just part of phase one. Let me explain what I mean. I had a call with Jennifer from the executive team this morning. She's asking why our digital revenue is flat year-over-year when ecommerce as a whole grew 8%. Part of the answer is that we're missing the mobile market entirely.

**Dev Lead:** Makes sense. If 70% of the market is shopping on mobile and we're only capturing 31% of traffic from that channel...

**Sarah:** We're effectively operating at half capacity. And it's not like we can go open more physical stores—retail foot traffic is declining. Digital is supposed to be our growth engine, and our growth engine is missing a cylinder.

**[05:45]**

**Dev Lead:** Okay, so help me understand what you're envisioning. When you say make mobile THE priority, what does that look like?

**Sarah:** A couple things. First, I want us to flip our design approach. Instead of designing for desktop and then making it work on mobile, we design for mobile first and then scale up to desktop.

**Dev Lead:** Mobile-first design. That's actually a pretty common approach these days, and honestly, it usually results in better experiences on both platforms because you're forced to prioritize.

**Sarah:** Exactly. Second thing—and I want your honest opinion on this—should we be building a native app?

**[06:45]**

**Dev Lead:** *pauses* That's a big question. Let me give you the honest breakdown.

**Sarah:** Please.

**Dev Lead:** A native app—meaning separate iOS and Android apps—gives you the best possible mobile experience. You get push notifications, offline access, smoother performance, access to device features like cameras for barcode scanning. And there's the whole "icon on the home screen" thing that keeps your brand top of mind.

**Sarah:** That all sounds good.

**Dev Lead:** But. Native apps are expensive to build and maintain. You're essentially building and maintaining three products—iOS, Android, and the web app. You need specialized developers for each platform. Updates have to go through app store review processes. And getting people to download an app is actually really hard—app store competition is fierce.

**[08:00]**

**Sarah:** So what's the alternative?

**Dev Lead:** A few options. One is what we discussed—a really excellent mobile web experience. Responsive design done right, fast loading, touch-optimized. A lot of successful retailers do very well with just this.

**Sarah:** But we're clearly not doing it well enough right now.

**Dev Lead:** No, we're not. Another option is a Progressive Web App, or PWA. It's sort of a middle ground. It's still a web app, but it can be installed on a phone's home screen, can work offline, can send push notifications on Android. It gives you some of the native app benefits without building separate apps.

**Sarah:** Interesting. I've heard of PWAs but don't really know much about them.

**[09:15]**

**Dev Lead:** The big advantage is you maintain one codebase. When we update the site, the PWA updates too. No app store gatekeepers. And the gap between PWAs and native apps has been shrinking—modern PWAs are really capable.

**Sarah:** What's the downside?

**Dev Lead:** iOS support is limited. Apple doesn't fully support PWA features because, cynically, they want you in their App Store. So push notifications don't work on iOS PWAs, for example. And some users are just trained to look in app stores for apps—they might not realize they can install from the browser.

**Sarah:** Hmm. What would you recommend?

**[10:00]**

**Dev Lead:** Honestly? I'd say let's do the mobile-first web redesign really, really well. Get the responsive experience to where it should be—fast, beautiful, easy to use on any phone. We can make it a PWA at basically no extra cost, which gets us the Android benefits. And then we see if the numbers move.

**Sarah:** And if they don't?

**Dev Lead:** Then we have the data to justify the investment in native apps. But I think you'll be surprised how much we can move the needle with a proper mobile web experience. A lot of the "we need a native app" impulse comes from having a bad mobile website, not from actually needing native features.

**[11:00]**

**Sarah:** That makes sense. I don't want to spend native app money if we don't need to. Okay, let's talk specifics. What would make our mobile experience actually good?

**Dev Lead:** Let me walk through the big ones. First, performance. Mobile users are impatient. If the site takes more than three seconds to load, most of them bounce. Right now our homepage is loading in about six seconds on a 4G connection.

**Sarah:** Six seconds! That's an eternity.

**Dev Lead:** Yeah. We've got unoptimized images, a lot of JavaScript that blocks rendering, no real caching strategy. Performance optimization alone could significantly improve our mobile conversion.

**[12:15]**

**Sarah:** Okay, that's number one. What else?

**Dev Lead:** Touch targets. Everything needs to be big enough to tap comfortably with a thumb. Industry standard is at least 44 pixels. Our current nav links are like 24 pixels. The add-to-cart buttons are small. The form fields in checkout are tiny.

**Sarah:** That explains the pinch-to-zoom problem.

**Dev Lead:** Right. Number three is thumb-zone design. People hold their phones in one hand and browse with their thumb. That means the most important interactive elements should be in the bottom two-thirds of the screen where thumbs can easily reach. Right now our nav is at the very top.

**[13:15]**

**Sarah:** Oh, interesting. So like, a bottom navigation bar?

**Dev Lead:** Exactly. A lot of apps do this—Instagram, the Twitter app, most banking apps. The main navigation is pinned to the bottom. You might keep a simplified header at the top for branding and search, but the key actions are at the bottom.

**Sarah:** I like that. What about the checkout flow?

**Dev Lead:** Checkout on mobile needs to be completely rethought. Single column layout, large form fields, smart defaults, progress indicators, support for autofill so people don't have to type their address, Apple Pay and Google Pay integration so they can skip forms entirely...

**[14:15]**

**Sarah:** Wait, we don't have Apple Pay?

**Dev Lead:** We don't. And that's a big miss. Apple Pay and Google Pay reduce mobile checkout friction enormously. People can authenticate with their fingerprint or face and the payment just happens. No typing card numbers, no filling out billing addresses.

**Sarah:** How hard is that to add?

**Dev Lead:** It's not trivial, but it's not years of work either. A few weeks of effort, maybe a month to do it properly with testing. And the conversion lift is usually significant—I've seen studies showing 20-30% improvement in mobile checkout completion.

**[15:00]**

**Sarah:** Okay, that feels like a must-have then. What about the product browsing experience?

**Dev Lead:** On mobile, people scroll more than they click. So we want a feed-style experience for product browsing—vertically scrolling, products loading as you go. The current grid layout with small tiles doesn't work great on a narrow screen.

**Sarah:** Like how Instagram works? You just keep scrolling?

**Dev Lead:** Similar, yeah. Larger product images, full-width product cards, easy swipe to see more images on the product detail page. And we should think about filters and sorting—right now it's kind of buried. Maybe a sticky filter bar that's always accessible.

**[16:00]**

**Sarah:** You know what else I noticed? When I searched for—oh wait, we don't have search. But when I'm browsing, if I accidentally tap the back button, I lose my place. I have to scroll all the way back down.

**Dev Lead:** Yeah, that's a state management issue. We need to preserve scroll position and filters when navigating. Also something called "infinite scroll with pagination fallback"—where you can scroll through products but also jump to a specific page if you want.

**Sarah:** All of this is making me realize just how far behind we are.

**Dev Lead:** The good news is none of this is technically groundbreaking. It's established best practices that we just haven't implemented yet.

**[17:00]**

**Sarah:** Okay, let me ask you something strategic. We talked about capturing younger demographics. Is there anything specific we should be thinking about for Gen Z shoppers?

**Dev Lead:** A few things. Speed is even more important to them—they've grown up with fast apps, so tolerance for slow is basically zero. Visual design matters a lot—things need to feel current, not dated. And social integration.

**Sarah:** Social integration?

**Dev Lead:** Yeah. Things like easy sharing of products to social media, maybe user reviews that feel more like social content, integration with things like "shop from Instagram" if we're running social ads. Some retailers are even doing live shopping events—kind of like QVC but on TikTok.

**[18:00]**

**Sarah:** We're probably not ready for live shopping, but the sharing piece makes sense. If someone finds a book they like, they should be able to easily send it to a friend or post it.

**Dev Lead:** Exactly. And one thing we should consider for the younger demographic—a lot of them prefer to browse first and buy later. So wishlists or "save for later" functionality is important. They might add something to a wishlist on their phone during lunch, then actually purchase it later when they're on WiFi or on desktop.

**Sarah:** That cross-device journey. If they save something on mobile, it needs to be there when they open the site on their laptop.

**Dev Lead:** Right. Which ties back to our authentication issue from before. We need proper user accounts that sync across devices.

**[19:00]**

**Sarah:** Okay. Let me try to synthesize all of this because my head is spinning a little. You're saying we should do mobile-first design, make it a PWA, focus on performance, bigger touch targets, maybe bottom navigation, redesign checkout with Apple Pay and Google Pay, better product browsing experience, and make sure accounts work properly across devices.

**Dev Lead:** That's the core of it, yes. Plus the social sharing and wishlist functionality to capture that cross-device, younger demographic behavior.

**Sarah:** And your recommendation is to do this as part of the refresh we already discussed, not as a separate project?

**[19:45]**

**Dev Lead:** I think it has to be. If we do a visual refresh that doesn't prioritize mobile, we're going to be back in this same room in six months having the same conversation. Mobile-first needs to be foundational to the redesign, not an afterthought.

**Sarah:** Fair. Does this change the timeline we talked about? You mentioned phase one by May.

**Dev Lead:** It makes it tighter, but I think it's still doable if we're disciplined about scope. We do mobile-first, which actually simplifies some decisions because mobile forces you to prioritize. The Apple Pay and Google Pay integration might slip to early phase two unless it's a hard requirement.

**Sarah:** Let's see if we can get it in phase one. That conversion lift you mentioned is too significant to delay.

**[20:45]**

**Dev Lead:** Understood. I can prioritize it.

**Sarah:** What about the PWA stuff?

**Dev Lead:** That's almost free if we're building with modern frameworks. We'd add a service worker and a manifest file, do the performance work we're doing anyway, and boom—it's a PWA. Users on Android can install it to their home screen, it works offline for basic browsing, the whole nine yards.

**Sarah:** And on iOS?

**Dev Lead:** Still works as a great mobile website, just without the push notifications. Which honestly, we're not set up to do meaningful push notifications anyway. That's a content and marketing capability we'd need to build out.

**[21:30]**

**Sarah:** Right. Okay, one more thing. How do we measure success? Like, what numbers should I be watching to know if this is working?

**Dev Lead:** A few key metrics. Mobile traffic share—we want to get that from 31% up toward industry average, so 60%+. Mobile conversion rate—closing that gap with desktop, even getting from 0.8% to 1.5-2% would be significant. Cart abandonment rate on mobile—getting that down from 78%. And page load time—under 3 seconds on 4G.

**Sarah:** What's a realistic target for conversion rate?

**Dev Lead:** Mobile will probably always be a bit lower than desktop—people do more "browsing" on mobile—but a well-optimized mobile site should be able to hit 2-2.5% conversion. If we can get there from 0.8%, that's essentially tripling our mobile revenue.

**[22:30]**

**Sarah:** Tripling. I like the sound of that. Okay, I need to take this back to Jennifer and the exec team. Can you put together something that shows the current state, what we're proposing, and expected outcomes? Something I can share up the chain?

**Dev Lead:** Sure. A mobile strategy brief with the analytics, proposed improvements, expected timeline, and projected impact?

**Sarah:** Exactly. Include the competitive context too—that 31% versus industry 65-70% stat really hits home. And maybe some mockups or examples of what good looks like? Even rough ones?

**[23:15]**

**Dev Lead:** I can do that. I'll pull some examples from competitors and apps that do mobile well, annotate what they're doing right. Give people a vision.

**Sarah:** Perfect. And be clear about the risk if we don't do this. I don't want to be alarmist, but if mobile is where the growth is and we can't capture it...

**Dev Lead:** We're ceding market share to competitors who can.

**Sarah:** Right. And once customers build habits with other apps, getting them back is really hard. There's a real cost to waiting.

**[24:00]**

**Dev Lead:** I'll make sure that's in there. Timeline for this brief?

**Sarah:** Can you have something by end of week? I have a call with Jennifer Monday.

**Dev Lead:** I'll make it happen.

**Sarah:** Thank you. I know we keep piling things on, but this mobile stuff... it feels existential. Like, not this quarter, but over the next few years, if we don't figure this out...

**Dev Lead:** No, I hear you. It's the right priority. We'll get it done.

**Sarah:** Thanks. Really. Let's reconnect after you send the brief and we'll figure out next steps.

**Dev Lead:** Sounds good. Talk soon, Sarah.

---

## Summary of Mobile Strategy Requirements

### Current State (Problems)
- **Mobile traffic share:** 31% vs. industry average 65-70%
- **Mobile conversion rate:** 0.8% vs. desktop 3.2%
- **Mobile cart abandonment:** 78% vs. desktop 45%
- **Page load time:** ~6 seconds on 4G (target: <3 seconds)
- **Marketing impact:** Mobile ad campaigns paused due to poor ROI
- **Demographic gap:** Not capturing Gen Z/younger millennial mobile-first shoppers

### Strategic Approach
- **Mobile-first design** — Design for mobile, scale up to desktop
- **Progressive Web App (PWA)** — Low-cost way to get native-like features on Android
- **No native app (for now)** — Revisit if metrics don't improve after mobile web optimization

### Technical Priorities

#### Performance
- Page load under 3 seconds on 4G
- Image optimization
- JavaScript bundle reduction
- Caching strategy
- Lazy loading

#### Touch & Navigation
- Minimum 44px touch targets
- Bottom navigation bar for thumb accessibility
- Mobile-friendly hamburger/drawer menu
- Sticky filter bars for product browsing

#### Checkout Optimization
- Single-column mobile checkout layout
- Large form fields
- Autofill support
- Progress indicators
- **Apple Pay integration** (high priority)
- **Google Pay integration** (high priority)

#### Product Browsing
- Vertical feed-style product display
- Full-width product cards
- Swipeable product images
- Preserved scroll position on back navigation
- Better filter/sort accessibility

#### Cross-Device Experience
- Proper user authentication across all services
- Synced wishlists/saved items
- Consistent cart across devices

#### Social & Engagement (Gen Z Focus)
- Easy product sharing to social media
- Wishlist / "save for later" functionality
- Modern, current visual design

### Success Metrics (Targets)
| Metric | Current | Target |
|--------|---------|--------|
| Mobile traffic share | 31% | 60%+ |
| Mobile conversion rate | 0.8% | 2-2.5% |
| Mobile cart abandonment | 78% | <50% |
| Page load time (4G) | 6s | <3s |

### Timeline
- Mobile strategy brief due: End of this week
- Phase one delivery (mobile-first refresh): Q2 2025 (May)
- Apple Pay/Google Pay: Target phase one, may slip to early phase two

### Risks of Inaction
- Continued market share loss to mobile-optimized competitors
- Inability to capture younger demographics
- Flat or declining digital revenue while market grows
- Customer habit formation with competitor apps is hard to reverse

### Next Steps
1. Dev Lead to prepare mobile strategy brief with:
   - Current analytics and competitive benchmarks
   - Proposed technical improvements
   - Timeline and resource requirements
   - Expected ROI / impact projections
   - Visual examples of best-in-class mobile experiences
2. Sarah to present to executive team (Jennifer) early next week
3. Reconvene to finalize scope and timeline


