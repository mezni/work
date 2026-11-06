# User Experience - BioViva

## Empathy Map Summary

**User Persona**: "Health-Conscious Maya" - 35, values authenticity, buys olive oil and honey regularly, concerned about quality and origin.

**What Maya SAYS**: "I want to make sure this is real olive oil from the region it claims."
**What Maya THINKS**: "Is this really from the region claimed? Is it cut with cheaper oil? Is the lab test legit?"
**What Maya DOES**: Checks lab reports, looks for certification seals, compares prices across sites, reads producer profiles.
**What Maya FEELS**: Anxious about being misled, proud when she finds authentic product, curious about the source.

**Pain Points**:
- Uncertainty about product authenticity
- Difficulty finding detailed origin info
- Confusing certification jargon
- Worry about freshness/quality degradation

**Desires**:
- Clear, trustworthy sourcing info
- Simple freshness indicators
- Educational content that builds confidence
- Connection to the producer/farmer

---

## Sensory Design System

### Visual Language
- **Color palette**: Earth tones - olive green (#6B8E23), honey amber (#D2691E), herb garden green (#A8D53D)
- **Trust typography**: Bold for trust scores, subtle for details
- **Harvest calendar**: Visual ring showing freshness window

### Product Page Sensory Elements

| Sense | Element | Implementation |
|-------|---------|----------------|
| **Sight** | Trust score badge | Large, color-coded (green=high, yellow=medium, red=low) |
| | Origin map | Interactive mini-map of product source region |
| | Harvest indicator | Seasonal icon + days-since-harvest number |
| **Smell** | Aroma notes | Text tags: "fruity", "peppery", "floral", "earthy" |
| | Freshness meter | Visual gradient from "peak fresh" to "use soon" |
| **Touch** | Texture descriptor | "First cold press", "creamed", "raw & unfiltered" |
| | Quality tier | Card material feel (rough=raw, smooth=refined) |
| **Taste** | Flavor profile | Interactive wheel: bitter, spicy, fruity, bitter, pungent |
| | Pairing suggestions | "Best with sourdough", "drizzle over fresh fruit" |
| | Taste quiz | 3-question quiz matching user palate to products |
| **Sound** | Producer story audio | Play button on farmer profile section |
| | Checkout confirmation | Subtle "harvest complete" chime |
| | Seasonal transition | Ambient soundscape change with seasons |

### Information Architecture

**Top Navigation**:
- Home
- Collections (Seasonal)
- Olive Oil
- Honey
- Herbal Essentials
- Producer Stories
- Education

**Product Card (compact view)**:
- Product image + name
- Trust score badge
- Price + size
- Freshness indicator
- Quick "Learn More" hover

**Product Page Sections**:
1. **Sensory Overview** - aroma, flavor profile, texture tags
2. **Origin Story** - farmer photo, location, farming methods
3. **Certification & Testing** - badges + lab report link
4. **Freshness Tracker** - harvest date + days optimal
5. **Usage & Pairing** - taste quiz + suggestions
6. **Community Notes** - verified buyer experiences

### User Flows

**First-Time Buyer Flow**:
1. Take taste quiz → get personalized recommendations
2. See trust scores prominently displayed
3. View farmer profile before purchasing
4. Receive freshness alert 30 days post-purchase

**Repeat Buyer Flow**:
1. Log in → see "running low" alerts on staples
2. One-click reorder with certification renewal notice
3. Subscription manageability with pause/skip
4. Community engagement prompts (leave tasting note)

**Gift Flow**:
1. Recipient taste quiz (if new to bio products)
2. Gift card with "story card" - explains producer & origin
3. Option to schedule delivery for optimal freshness window

### Micro-interactions

- **Trust score hover**: Shows breakdown components (certification, lab, producer)
- **Freshness pulse**: Subtle animation when product approaches optimal window close
- **Seasonal banner**: Color shift with current harvest season
- **Origin map zoom**: Click-to-zoom on interactive region map
- **Taste wheel selection**: Click a note, highlights products with that flavor profile

### Accessibility Notes

- Trust scores announced via screen reader with "Trust score: 85 out of 100, high trust"
- Color contrast: minimum 4.5:1 for all text over background images
- Keyboard navigation for all product filtering and selection
- Alt text for all farmer/producer images
- Reduced motion preference respects animation disable

### Mobile-First Considerations

- **Thumb zone**: Primary actions (favorite, quick view) at bottom
- **Swipe gestures**: Swipe left on product card to see origin summary
- **Voice search**: "Find me peppery olive oil from Greece"
- **Push notifications**: Freshness alerts, harvest season openings