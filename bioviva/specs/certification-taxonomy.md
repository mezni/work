# Certification Taxonomy — BioViva

*Adopted companion — owned by the project, not edited by bmad-spec. References Trust Score component weighting and certification standards supported.*

## Supported Certification Standards

The following certification standards are supported in the BioViva Trust Score calculation (40% weight — see AD-5 in ARCHITECTURE-SPINE.md):

| Standard | Logo | Category | Validation Method | Trust Score Contribution |
| --- | --- | --- | --- | --- |
| **USDA Organic** | 🟢 | National organic (US) | Database lookup + document upload | ~13.3% of total Trust Score |
| **EU Organic** | 🟢 | Regional organic (EU) | Database lookup + document upload | ~13.3% of total Trust Score |
| **Fair Trade** | 🟤 | Fair trade certification | Database lookup + document upload | ~6.7% of total Trust Score |
| **Regenerative** | 🟢 | Regenerative agriculture | Document upload + third-party verification | ~6.7% of total Trust Score |
| **No certification** | — | — | Declared by producer; Trust Score reduced by 20% baseline | -6.7% (penalty) |

*Weights sum to 40% total (13.3% × 3 standards + 6.7% × 2 standards = 40%).*

## Trust Score Component Weighting

The Trust Score (0-100) is calculated as:

```
Trust Score = 
  (Certification Validity % × 0.40) +
  (Lab Test Results % × 0.30) +
  (Producer Reputation % × 0.20) +
  (Review Recency % × 0.10)
```

### Certification Validity Sub-component (0-40 range)

```
Certification Validity % = 
  Σ (certification_standard_weight × certification_status)
```

Where `certification_status` is:
- `1.0` (100%) if certification is current/valid in the database
- `0.5` (50%) if certification is expired but within grace period
- `0.0` (0%) if no certification or certification is invalid/failed

### Example Calculations

**Example 1: Fully certified olive oil**
- USDA Organic: current (1.0)
- EU Organic: not applicable (0.0)
- Fair Trade: current (1.0)
- Certification Validity = (13.3% × 1.0) + (0% × 0.0) + (6.7% × 1.0) = 20.0% of total range
- Contribution to Trust Score = 20.0 × 0.40 ... wait, let me recalculate

Actually, the certification validity is a percentage (0-100%) that feeds into the overall Trust Score formula. Let me reformulate:

The overall Trust Score formula is:
```
Trust Score = 
  CertValidity% × 0.40 +
  LabResults% × 0.30 +
  ProducerRep% × 0.20 +
  ReviewRecency% × 0.10
```

Where each component is 0-100%.

`CertValidity%` itself is computed from the certification standards present:

```
CertValidity% = (sum of active certification weights) / (max possible weight) × 100
```

Max possible weight = 40% of the total Trust Score range, but as a percentage of the cert component, it's 100% when all supported certs are active.

**Simplified for implementation:**
- Start at 0%
- Add 13.3% for each current USDA Organic certification
- Add 13.3% for each current EU Organic certification
- Add 6.7% for each current Fair Trade certification
- Add 6.7% for each current Regenerative certification
- Result is the Certification Validity % (0-100%), which then feeds into the Trust Score formula above

### Certification Status Logic

| Status | Action | Effect on CertValidity% |
| --- | --- | --- |
| **Current** | Display badge + full weight | Add standard weight (13.3%/6.7%) |
| **Expired (grace period)** | Display badge + reduced weight | Add standard weight × 0.5 |
| **Expired (no grace)** | Display "expired" message + no weight | Add 0 |
| **Failed/Invalid** | Display "not valid" message + penalty | Subtract 6.7% (penalty for no certification) |
| **Not declared** | Show "certification coming" notice | Subtract 6.7% (baseline penalty) |

## Certification Database Schema (referenced by bio-producers crate)

```sql
CREATE TABLE certifications (
  id UUID PRIMARY KEY,
  producer_id UUID REFERENCES producers(id),
  standard VARCHAR(50) NOT NULL, -- 'USDA Organic', 'EU Organic', 'Fair Trade', 'Regenerative'
  status VARCHAR(20) NOT NULL, -- 'current', 'expired_grace', 'expired', 'failed', 'not_declared'
  issued_date DATE,
  expiry_date DATE,
  document_url TEXT, -- URL to certification document
  validated_at TIMESTAMP, -- when last validated against source
  validator VARCHAR(100), -- who validated (e.g., 'usda_api', 'manual_review')
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);
```

## Validation Flow

1. **Producer uploads** certification document via onboarding flow
2. **System parses** standard and expiry date
3. **Automated check** against public databases (USDA API, Fair Trade registry, etc.)
4. **Status set** based on result (current/expired/grace/failed)
5. **Document stored** at `document_url`
6. **Trust Score recalculated** on: certification update, new lab results, producer rating change, new review (per AD-5)

## Grace Period

Certifications within 30 days of expiry receive a "grace period" status:
- Weight reduced by half (× 0.5)
- UI shows "certification renewing soon" badge
- Subscription manager (CAP-5) alerts user to renew

After grace period, status becomes "expired" and weight drops to 0.

## Edge Cases

- **Multiple certifications of same standard:** Only the most recent/current one counts; duplicates are deduplicated by standard type.
- **Organic in-transit:** Producer transitioning to organic may have "in-transition" status; treated as current for 12 months from transition start date.
- **Hand-harvested small producers:** Producers with <$10K annual revenue may declare certification informally; "not declared" penalty applies (6.7% reduction) unless they provide a personal guarantee or third-party review.
- **Imported products:** Certifications from non-supported standards receive a "foreign certification" tag; weight added proportionally based on reciprocity agreements (currently 0% for unsupported standards).

## QA & Validation

- **Monthly reconciliation:** Automated job compares database certifications against producer-submitted documents; mismatches flagged for review.
- **Quarterly Trust Score audit:** Sample of 50 products per quarter; Trust Score manually recalculated from raw component data; discrepancies >5 points investigated.
- **Certification expiry alerts:** Automated emails to producers 60, 30, and 7 days before expiry; "expired" status auto-applied after expiry date + grace period.