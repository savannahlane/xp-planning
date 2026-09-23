# Claude briefing — ENT book growth tiering

**How to use this file.** Paste this entire file into Claude as the working context.
It is self-contained: it includes the hypothesis, the scoring rules, every state score,
every countable account with its tier, and the XP rollups. Do not invent data that is
not in this file. If something is missing, say so.

Internal and confidential. Contains account names, ARR and staffing. Do not republish.
Working hypothesis, not an approved plan. No account assignments have been changed.

Generated 2026-09-23 from `savannahlane/xp-planning` branch `cursor/ent-book-growth-tiering-47dc`.
PR: https://github.com/savannahlane/xp-planning/pull/2

---

## 0. Who you are talking to and what this is

The user is staffing Experience Partners (XPs) against a Granicus Enterprise book of
US state agencies and large local governments (counties and big cities). Products in
this book include Email & SMS, Public Records Request, Engagement & Sentiment,
Recurring Services, Agenda & Video, Websites/Portals/Intranets, Forms & Workflows,
Land & Vitals, Experience Agents, Service Request Management, Short-term Rentals,
Channel Shift, govXCloud, Permitting & Licensing.

There is already an XP ↔ AE rebalance model (`XP_AE_Rebalance_Model.xlsx` and
`index.html`) that assigns 277 records / 209 countable accounts across 13 XP seats
under these rules:

- Cap: 17 countable accounts per Enterprise XP (manager books can exceed).
- Complex accounts (more than 7 capabilities, or Service Cloud Advanced) no more than one third of a book.
- XP time zone ±1 hour of the account.
- Holds: San Antonio with Steffany Amador; DC with Paige Wendle; Denver with a Savannah Lane report; Columbus with an Ashley Hill report; LA and GLACVCD with Colleen Moran; WA with Paige Wendle; CT and ME with Halena Martin.
- Allocated child records carry $0 ARR, travel with the parent, and do not count against the cap. They still consume XP time.

The user then asked to research and hypothesise **growth-potential tiering** of the
ENT book, because Florida / Texas / California still have significant growth, mountain
states look saturated, and some states have very low transformation budgets and few
grant opportunities. They also want this model to eventually cover **the whole XP team**,
not just Enterprise.

If the user asks you to rebalance, recommend, or extend the model: preserve the holds,
the 17-account cap, the complex-share rule, and the time-zone rule unless they explicitly
waive them. Treat local whitespace as an upper bound (see caveats). Do not treat this
hypothesis as an approved staffing plan.

---

## 1. Hypothesis (full text)

The following section is the canonical write-up. Prefer it over any paraphrase.

# ENT book growth tiering — hypothesis

Internal and confidential. Working hypothesis, not an approved plan.

Companion files: `tiering/state_tiers.csv`, `tiering/account_tiers.csv`,
`tiering/xp_tier_summary.csv`, `tiering/build_tiering.py` (the model),
`tiering/state_overlay.csv` (the judgement calls). Underlying research is in the four
reports alongside this file.

---

## The short version

The starting intuition — Florida, Texas and California keep growing, the Mountain states are
worked out, and a handful of states have neither budget nor grants — holds up against the
evidence. But the line does not fall where it was drawn. **Growth potential does not separate
by state. It separates by which side of the house you are selling into inside that state.**

In 32 of 51 jurisdictions the state-agency motion and the 100k-plus local motion land in
different tiers — 24 of the 39 states this book actually touches — and several of the
disagreements are two full tiers wide. Texas is the only
territory in the book that is unambiguously top-tier on both sides. California is the reverse
of how it is usually described: its state-agency estate is the most penetrated book we have
sitting inside a distressed budget, while its 112 large counties and cities are the single
largest pool of unheld enterprise-scale jurisdictions in the country. Washington is the
sharpest split in the book — bottom tier for state agencies, top tier for locals — and all
five Washington accounts we hold are state-side.

For the book itself, the finding that matters most is that **the 17-account cap balances
workload but does nothing to balance opportunity.** Growth load varies 2.3x across the
thirteen Enterprise XPs even though every book is at or under cap. One XP3 carries no growth
accounts at all; one XP1 carries $3.6M of the revenue most exposed to churn.

---

## Why the model is built the way it is

Growth potential is expected **incremental ARR**, and incremental ARR is a size quantity, not
a rate. A territory growing 50% on a $50k base deserves less XP capacity than one growing 10%
on a $5M base. The first version of this model did not respect that and put Montana in the top
tier on the strength of having a funded modernization program and no Granicus presence — both
true, and both irrelevant next to a 1.1M population and five jurisdictions over 100k. Market
scale now carries real weight on both sides, and an untouched small state no longer outranks a
large one on untouched-ness alone.

Two scores are computed per state because the book contains two different motions. The 193
State-map accounts sell into state agencies, where what matters is the general fund, whether
there is a named modernization appropriation to attach to, and whether the budget is annual or
biennial. The 83 Local ENT accounts sell into counties and cities, where what matters is
population and permit growth, state grant programs that flow to locals, property tax caps, and
how many large jurisdictions we do not yet hold. A state can be good at one and poor at the
other, and most are.

| Weight | State-agency side | | Local ENT side |
|---|---|---|---|
| Size of the prize | 20 agency market scale | | 26 whitespace (jurisdictions >100k unheld) |
| Share unclaimed | 14 penetration headroom | | 8 penetration headroom |
| Ability to fund | 22 fiscal posture, 6 reserves | | 16 grant environment net of ARPA cliff |
| Demand | 16 named IT modernization funding | | 20 population, migration, permits |
| Friction | 12 purchasing access, 10 budget cycle | | 14 purchasing access, 8 tax cap headwind |
| Inside the logo | — | | 8 cross-sell depth |

Scores run 0–100 and band into tiers at 58 / 47 / 37. Every input traces to a sourced research
table or to `tiering/state_overlay.csv`, where each judgement call carries a note.

---

## Territory tiers

### Where the prior is confirmed

**Texas is the strongest territory in the book and the only Tier A on both sides.** Stable
posture on a 23.3% rainy day fund, a named DIR pipeline of 88 projects worth $788.1M plus
$135M for the Texas Cyber Command, and the best local purchasing access in the country
(DIR, SmartBuy, TXMAS, TIPS, BuyBoard). We hold 10 of 87 jurisdictions over 100k. The two
drags are real but second-order: the biennial cycle halves the buying windows, and $51B has
been committed to property tax relief, which squeezes the locals we sell to.

**The low-budget, low-grant states are exactly the ones that were named.** Maine scores 27 on
the state side, North Dakota and Kentucky 35, Washington 34. These are not close calls, and
they share a profile: constrained or distressed budgets, no verified IT modernization funding,
biennial cycles, national cooperatives only, high ARPA cliff exposure, and — critically — a
state-agency estate we have already worked hard. Maine, Connecticut, Kentucky and North Dakota
carry 20, 38, 19 and 16 account records for $356k, $745k, $1.0M and $399k of ARR respectively.
That is a lot of relationship surface for very little revenue, and it is the clearest signal
in the book that those territories are finished rather than starting.

Connecticut and Maine also expose a second problem the cap cannot see. Those 38 and 20 records
collapse to just **4 and 2 countable accounts**, because the rest are allocated $0 child
agencies rolling up to a parent. The XP still services every one of those relationships. A
Maine book and a Texas book can both read as "2 accounts" against a 17-account cap while
representing completely different amounts of work and completely different amounts of upside.

North Dakota deserves a specific mention because the research found a hard number behind the
intuition: **six of its 53 counties employ full-time IT staff**, against a statutory hiring
freeze and a 10% budget-cut mandate.

### Where the prior needs splitting

**California.** State side B at 54, local side A at 62. The state is in a documented deficit
with the IT budget "holding the line" and no new modernization fund, and our 16 state-agency
accounts there are worth $3.3M — among the most penetrated estates in the book. Meanwhile
California has 112 jurisdictions over 100k, we hold 10, and the grant environment is rich.
The honest read is that California's growth is in the counties and cities, and Sacramento is a
defend motion. The one caution on the local side is that the channel is crowded: Accela is
strong in large California counties, Streamline owns the SB 929 special-district niche, and
both Cal Cities and CSDA endorse VC3, so the trusted-referral slot is occupied.

**Florida.** State side A at 62, local side B at 58 — and the local number is a live binary,
not a settled score. Amendment 3 is on the November 2026 ballot at a 60% threshold and would
cut local non-school property tax revenue by $4.93B in FY2027-28, rising to $11.83B by
FY2031-32, $45.84B over five years, with no state backfill and roughly 65% of it landing on
county commissions. We hold 13 of 63 large Florida jurisdictions and $2.57M of local ARR
there. **Florida's local tier should not be finalised before the vote.** On the state side,
note that HB 1197 expanded Florida Digital Service oversight of agency technology purchases —
that lengthens approval paths without adding money, so it is friction rather than funding.

**Washington.** The sharpest disagreement in the book: state side D at 34, local side A at 70.
The state is distressed on a 2.8% rainy day fund, second-lowest in the country, and we have
$994k across five state accounts. The locals are a different market entirely — 23
jurisdictions over 100k of which we hold zero in this book, permits up 10.5%, population up
0.92%, a rich grant environment with $16.6M+ already allocated under SLCGP, and a DES master
contract that names Granicus directly and carries out-of-state cooperative access. That
contract's published term dates appear to have lapsed and should be verified with WA DES
before anyone plans against it.

### Where the prior is wrong, or at least testable

**The Mountain West reads as middling rather than saturated, and the reason matters.** The
scores mostly agree with the intuition — Colorado C/B, Arizona C/B, Nevada B/B, Wyoming B/C —
but not because we have sold everything. We hold *zero* Local ENT accounts in Idaho, Montana,
Nevada, Utah and Wyoming. What actually holds these territories down is small market scale,
high ARPA cliff exposure, thin grant environments, and property tax caps in Colorado, Montana
and North Dakota. Colorado specifically is distressed under TABOR with an IT capital request
of only $9.8M general fund.

Two exceptions are worth treating as falsifiable claims rather than conclusions:

- **Idaho** scores local A at 60. It is the second-fastest-growing state in the country at
  +1.44% with +9.8 net domestic migrants per 1,000. The book holds one Idaho account, the
  Labor Department, and no locals at all.
- **Utah** scores local A at 67 on similar logic, with 11 jurisdictions over 100k and none held.

Both have low or medium research confidence and thin grant environments. If the team's
experience is that these are genuinely worked out, the most likely explanation is that the
large jurisdictions there are already customers in another segment's book — which this model
cannot see, and which is the subject of the caveat below.

**Indiana** is the other whitespace surprise: local A at 64, 24 jurisdictions over 100k, and
exactly one account in the book (Lake County).

---

## What this implies for the book

Projecting territory scores onto accounts gives each account a growth-potential index that
blends its territory (60%) with its own remaining capability whitespace (40%). Crossing that
against ARR produces four tiers. The two axes are independent in practice — the correlation
between log ARR and growth potential across the 209 countable accounts is **-0.01** — so this
is a genuine two-dimensional split rather than a re-labelling of account size.

| Tier | | Accounts | ARR | Median caps | What the XP is being asked to do |
|---|---|---|---|---|---|
| 1 | Growth engine | 48 | $12.2M | 2 | Expansion, exec relationships, roadmap |
| 2 | Expansion | 57 | $3.1M | 1 | Land and expand; coachable, lower risk |
| 3 | Defend | 57 | $19.8M | 4 | Retention, adoption, renewal risk |
| 4 | Maintain | 47 | $2.0M | 3 | Efficient coverage, pooled or low-touch |

**More than half the book's revenue — $19.8M of $37.0M — sits in Tier 3.** These are deep,
mature accounts in territories that are not growing: Los Angeles at $1.77M with six
capabilities, Cook County at $1.11M, Columbus at $870k with nine, Franklin County at $619k
with eight. That is not a problem to be fixed, it is the shape of a mature book, but it does
mean that a staffing model which treats all 17 accounts as equivalent will systematically
under-resource retention where the revenue actually is.

### The imbalance

| XP | Level | Accts | T1 | T2 | T3 | T4 | Growth load | Total ARR | Defend ARR |
|---|---|---|---|---|---|---|---|---|---|
| Steffany Amador | XP3 | 16 | 10 | 5 | 1 | 0 | 14.5 | $3.00M | $0.76M |
| Open XP2 (PT) | XP2 | 16 | 8 | 5 | 3 | 0 | 13.5 | $3.30M | $1.01M |
| Cody Nichols | XP1 | 17 | 3 | 11 | 2 | 1 | 13.1 | $1.25M | $0.25M |
| Taylor Roman | XP3 | 17 | 6 | 4 | 4 | 3 | 12.1 | $2.13M | $0.80M |
| Halena Martin | XP3 | 16 | 3 | 7 | 3 | 3 | 11.0 | $3.50M | $0.52M |
| Andy O'Brien | XP3 | 14 | 6 | 2 | 4 | 2 | 10.2 | $2.60M | $0.91M |
| Carolina Cambronero | XP3 | 17 | 2 | 5 | 6 | 4 | 10.2 | $3.25M | $2.07M |
| Colleen Moran | XP3 | 12 | 6 | 3 | 3 | 0 | 9.9 | $3.65M | $2.16M |
| Alejandro Solano | XP1 | 17 | 1 | 6 | 4 | 6 | 9.6 | $2.30M | $1.03M |
| Marcy Castro | XP1 | 16 | 2 | 3 | 6 | 5 | 8.9 | $4.34M | $3.60M |
| Brooke Minichino | XP2 | 13 | 1 | 6 | 5 | 1 | 8.6 | $2.04M | $1.58M |
| Carolina Prieto | Manager | 23 | 0 | 0 | 7 | 16 | 8.3 | $2.49M | $2.29M |
| Paige Wendle | XP3 | 15 | 0 | 0 | 9 | 6 | 6.3 | $3.15M | $2.79M |

Growth load weights each countable account by tier (1.0 / 0.8 / 0.5 / 0.3). Four things stand
out.

**Paige Wendle holds no growth accounts.** Fifteen accounts, zero in Tier 1 or 2, $2.79M in
Defend. That is a direct consequence of geography: hers is the Mountain and Pacific Northwest
book, and every state in it lands in the bottom half on the side we actually sell into there.
This is not a performance observation — it is a structural one, and it is the strongest
argument in the data for tiering the book at all.

**Marcy Castro is an XP1 carrying the largest and most exposed book.** $4.34M total and $3.60M
in Defend, including Cook County, Columbus, Franklin County and Jackson County. Seniority and
revenue risk are inverted here.

**Steffany Amador is over-indexed the other way** at 94% growth accounts and almost no
retention load, and **the second-heaviest growth book belongs to an unfilled requisition.** The
Open XP2 (PT) book carries eight Tier 1 accounts. Whatever the hiring timeline is, this is the
book that decays fastest while the seat is empty.

**The XP1 pattern is otherwise healthy.** Cody Nichols at 3 Tier 1 and 11 Tier 2 is close to an
ideal junior book: high growth potential concentrated in lower-ARR accounts, so mistakes are
survivable. That is a useful template for what an XP1 book should look like, and Marcy Castro's
is its opposite.

---

## Caveats, in order of how much they should worry you

**1. Local whitespace is an upper bound, and probably a loose one.** The model counts a
jurisdiction over 100k as open if it is not in this book. The ENT book holds 83 of 959 such
jurisdictions nationally, or 8.7% — but Granicus company-wide claims 48 of the 50 largest US
cities and 45% of top counties. Most of those 876 "open" jurisdictions are therefore already
customers, held in another segment's book. **The local-side scores are useful for ranking
states against each other and are inflated in absolute terms.** This is the single biggest
reason to extend the model to the whole XP team, and it is why the Idaho and Utah results
should be treated as questions rather than answers.

**2. Every FY2027 fiscal figure is a governor's recommendation, not an enacted budget.**
Legislatures will move these. Virginia is missing from NASBO's FY2027 data entirely. Texas at
+54.1% then -30.5%, and similar swings in Mississippi, Georgia and Michigan, are biennial
appropriation artifacts rather than demand signals.

**3. ARPA cliff exposure is inferred, not measured.** No state-level dataset of ARPA spending
on technology exists, because 53% of state and 67% of local spending ran through revenue
replacement, where software purchases are reported as generic government services. The ratings
come from GAO spend-pace and per-capita allocation. The six states GAO identified as having
spent under half their award as of March 2025 — Mississippi, New Jersey, Oklahoma, South
Carolina, Tennessee, West Virginia — are the part of that column worth defending.

**4. Penetration is proxied by this book's ARR per capita.** No Granicus-wide ARR, pipeline or
install-base data was available for this exercise. That makes "penetration headroom" really
"headroom relative to where the Enterprise book already is," which is the right measure for
tiering *this* book and the wrong one for sizing the market.

**5. Capability data is missing for 16 of the 209 countable accounts**, all State-map. Those
are imputed at the median depth of State accounts that do have data and flagged as `imputed`
in `account_tiers.csv`, rather than being scored as pure whitespace and letting a data gap
masquerade as opportunity. The other 68 accounts with no capability string are the allocated
$0 child records, which are excluded from tiering entirely.

**6. Two purchasing vehicles that materially affect scores may be dead.** The Washington DES
01313 and Montana state MSA documents both show terms that appear lapsed (ending 11-15-2019
and 01-31-2021). Both need a phone call. Ohio's State Term Schedule 534354 expires in December
2026 and needs renewing or replacing.

**7. Research confidence is low for 14 of the states in the book**, including Georgia, New
Mexico, North Carolina, Arizona and Idaho — several of which score Tier A. The confidence
column is carried through to `state_tiers.csv`; a Tier A on low confidence is a prompt to
validate, not a green light.

---

## Extending this to the whole XP team

The territory scoring is deliberately independent of the book. All 50 states plus DC are scored
whether or not Enterprise has an account there, so adding another segment requires no changes
to `state_signals` or to the weights. What it requires is data:

1. **An account export per segment**, in the same shape as the Assignments sheet: account,
   ultimate parent, state, map side, AE, current XP, ARR, capabilities, market segment. The
   segment column is what lets the model compute penetration and whitespace correctly for the
   first time, because it can then net out jurisdictions held anywhere in the company rather
   than only in Enterprise.
2. **The XP roster for each segment** — level, manager, time zone, location — so the same
   growth-load and seniority checks run across the whole team.
3. **A decision on the addressable denominator per segment.** Enterprise addressability is
   jurisdictions over 100k, which is why that is the denominator here. Mid-market and SMB have
   a different one, and the Census of Governments counts in the competitive research give the
   raw material: 90,837 local governments in 2022, with the sub-2,500-population share running
   as high as 99% in North Dakota and 90% in Minnesota. **Those two facts together will invert
   several of these tiers for a smaller-segment book** — the township-heavy states that are
   dead ends for Enterprise are exactly where the unit count lives.

Once the other segments are loaded, three things in this document should be re-run before being
trusted: the local whitespace figures, the Idaho and Utah results, and the national 8.7%
coverage number.

## What would falsify this

- Idaho, Utah, Montana or Nevada turning out to have their large jurisdictions already held in
  another segment's book. That would confirm the saturation intuition and drop the Mountain
  West local scores by roughly a tier.
- Florida Amendment 3 passing in November 2026, which moves Florida's local side from B toward
  C and makes 13 accounts worth $2.57M a defend motion rather than a growth one.
- Texas's DIR pipeline not converting, which would remove the main evidence behind the single
  highest score in the model.
- The Washington DES and Montana MSA vehicles proving to be dead, which would cut purchasing
  access in both and drop Washington's local score out of Tier A.


---

## 2. Model constants

```json
{
  "weights": {
    "state_side": {
      "agency_market_scale": 20,
      "penetration_headroom": 14,
      "fiscal_posture": 22,
      "it_modernization": 16,
      "reserves": 6,
      "purchasing_access": 12,
      "cycle_friction": 10
    },
    "local_side": {
      "whitespace": 26,
      "penetration_headroom": 8,
      "demand_momentum": 20,
      "funding_environment": 16,
      "local_fiscal_headwind": 8,
      "purchasing_access": 14,
      "crosssell_depth": 8
    },
    "territory_bands": [
      [
        "A",
        58.0
      ],
      [
        "B",
        47.0
      ],
      [
        "C",
        37.0
      ],
      [
        "D",
        0.0
      ]
    ],
    "account_blend": {
      "territory": 0.6,
      "whitespace": 0.4
    },
    "capability_ceiling": 8,
    "growth_load": {
      "1": 1.0,
      "2": 0.8,
      "3": 0.5,
      "4": 0.3
    }
  },
  "cuts": {
    "growth_cut": 0.5764,
    "arr_cut": 98315
  },
  "account_blend": {
    "territory": 0.6,
    "whitespace": 0.4
  },
  "capability_ceiling": 8,
  "growth_load": {
    "1": 1.0,
    "2": 0.8,
    "3": 0.5,
    "4": 0.3
  },
  "territory_bands": [
    [
      "A",
      58.0
    ],
    [
      "B",
      47.0
    ],
    [
      "C",
      37.0
    ],
    [
      "D",
      0.0
    ]
  ]
}
```

Account growth potential = 0.60 × (side territory score / 100) + 0.40 × (1 − min(ncap, 8)/8).
Accounts missing capability data are imputed at the State-map median depth and flagged `imputed`.
Tier 1 = high growth potential AND high ARR; Tier 2 = high GP only; Tier 3 = high ARR only; Tier 4 = neither.
Cut points: growth_potential ≥ 0.5764; ARR ≥ $98,315.

Growth load per countable account: T1=1.0, T2=0.8, T3=0.5, T4=0.3.

---

## 3. State territory scores (all 50 + DC)

Blended score is weighted by where *this book's countable accounts* sit. Per-side tiers
are what drive account scoring. `held` is local ENT accounts in this book only.
`open` = jurisdictions ≥100k minus held. That overstates whitespace wherever another
segment already holds the logo.

| Abbr | State | Blend | St tier | St score | Loc tier | Loc score | Split | St accts | Loc accts | ≥100k | Held | St ARR | Loc ARR | Posture | RDF% | Cycle | IT mod | Grants | ARPA cliff | Access | Tax cap | Conf | Pop chg% | Dom mig/1k |
|---|---|---:|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|---|---|---|---|---|---:|---:|
| TX | Texas | 74.0 | A | 82.4 | A | 63.1 |  | 13 | 10 | 87 | 10 | $2.01M | $2.82M | Stable | 23.3 | Biennial | funded | thin | med | strong | Y | med | 1.25 | 2.12 |
| GA | Georgia | 72.9 | A | 77.5 | A | 61.3 |  | 5 | 2 | 36 | 2 | $328K | $407K | Stable | 15.4 | Annual | funded | moderate | med | present |  | low | 0.88 | 2.42 |
| VA | Virginia | 68.9 | A | 78.8 | A | 63.9 |  | 1 | 2 | 18 | 2 | $82K | $831K | Stable | 12.4 | Biennial | funded | rich | med | strong |  | high | 0.69 | 0.71 |
| NM | New Mexico | 65.3 | A | 67.0 | B | 53.4 | Y | 7 | 1 | 8 | 1 | $384K | $90K | Expanding | 24.1 | Annual | funded | moderate | med | present |  | low | -0.06 | -1.07 |
| NC | North Carolina | 64.9 | A | 62.1 | A | 64.9 |  | 0 | 2 | 39 | 2 | $0K | $202K | Stable | 11.1 | Biennial | none | moderate | med | present |  | low | 1.32 | 7.51 |
| MN | Minnesota | 64.4 | A | 67.4 | A | 58.5 |  | 4 | 2 | 15 | 2 | $137K | $403K | Constrained | 10.6 | Biennial | funded | rich | med | strong |  | med | 0.57 | 1.42 |
| IN | Indiana | 63.7 | B | 51.8 | A | 63.7 | Y | 0 | 1 | 24 | 1 | $0K | $71K | Constrained | 9.5 | Biennial | none | moderate | med | present |  | low | 0.56 | 1.75 |
| MA | Massachusetts | 61.8 | A | 61.8 | A | 65.3 |  | 1 | 0 | 20 | 0 | $215K | $0K | Stable | 15.8 | Annual | none | rich | low | present |  | med | 0.22 | -4.66 |
| NY | New York | 61.7 | B | 57.0 | A | 64.9 | Y | 2 | 3 | 34 | 3 | $1.63M | $227K | Constrained | 7.7 | Annual | none | rich | low (state) / med (nyc & locals) | strong |  | med | 0.01 | -6.88 |
| AR | Arkansas | 60.2 | A | 65.2 | B | 55.3 | Y | 0 | 0 | 9 | 0 | $0K | $0K | Expanding | 27.9 | Annual | none | thin | med | coop_only |  | low | 0.6 | 4.65 |
| FL | Florida | 58.8 | A | 62.0 | B | 57.8 | Y | 4 | 13 | 63 | 13 | $505K | $2.57M | Constrained | 8.6 | Annual | governance | rich | med | present | Y | med | 0.85 | 0.96 |
| OH | Ohio | 58.1 | A | 74.7 | B | 47.0 | Y | 2 | 3 | 32 | 3 | $206K | $1.78M | Stable | 12.6 | Biennial | funded | moderate | med | present |  | med | 0.34 | 1.0 |
| PA | Pennsylvania | 57.9 | A | 72.6 | B | 57.9 | Y | 0 | 3 | 34 | 3 | $0K | $286K | Distressed | 15.5 | Annual | funded | moderate | med | strong |  | med | 0.1 | -0.22 |
| UT | Utah | 57.5 | B | 57.5 | A | 66.6 | Y | 1 | 0 | 11 | 0 | $95K | $0K | Stable | 10.9 | Annual | none | moderate | low–med | present |  | med | 1.03 | 0.94 |
| CA | California | 57.4 | B | 54.4 | A | 62.3 | Y | 16 | 10 | 112 | 10 | $3.30M | $3.91M | Distressed | 17.4 | Annual | neutral | rich | low–med | present |  | med | -0.02 | -5.82 |
| MT | Montana | 57.0 | A | 65.8 | B | 48.3 | Y | 0 | 0 | 5 | 0 | $0K | $0K | Stable | 15.3 | Biennial | funded | thin | high | present | Y | low | 0.63 | 5.55 |
| AL | Alabama | 56.8 | A | 58.4 | B | 55.1 | Y | 1 | 1 | 19 | 1 | $75K | $58K | Stable | 19.5 | Annual | none | moderate | med | coop_only |  | low | 0.58 | 4.5 |
| MD | Maryland | 56.3 | B | 52.0 | B | 56.3 |  | 0 | 2 | 15 | 2 | $0K | $257K | Distressed | 7.8 | Annual | headwind | rich | med | strong |  | high | 0.32 | -1.94 |
| OK | Oklahoma | 55.7 | B | 57.6 | B | 52.0 |  | 2 | 1 | 11 | 1 | $79K | $300K | Constrained | 17.1 | Annual | none | thin | high | strong |  | med | 0.62 | 3.51 |
| DC | District of Columbia | 51.7 | D | 34.3 | B | 51.7 | Y | 0 | 1 | 1 | 0 | $0K | $0K | Distressed | 8.2 | Annual | none | moderate | low | coop_only |  | med | 0.34 | -5.95 |
| SC | South Carolina | 51.3 | B | 51.0 | B | 51.3 |  | 0 | 1 | 19 | 1 | $0K | $238K | Constrained | 13.8 | Annual | none | thin | high | coop_only |  | med | 1.46 | 11.96 |
| MS | Mississippi | 50.8 | B | 54.8 | C | 46.9 | Y | 0 | 0 | 7 | 0 | $0K | $0K | Stable | 9.9 | Annual | none | thin | high | coop_only |  | med | 0.14 | -0.31 |
| WI | Wisconsin | 49.9 | B | 57.8 | C | 44.7 | Y | 2 | 3 | 19 | 3 | $54K | $430K | Stable | 9.3 | Biennial | none | moderate | high | present |  | med | 0.26 | 1.17 |
| AZ | Arizona | 49.8 | C | 46.6 | B | 57.3 | Y | 7 | 3 | 23 | 3 | $598K | $366K | Constrained | 9.1 | Annual | headwind | moderate | med | present |  | low | 0.89 | 4.08 |
| MI | Michigan | 49.5 | A | 62.7 | B | 49.5 | Y | 0 | 1 | 27 | 1 | $0K | $489K | Constrained | 13.1 | Annual | none | moderate | high | strong |  | med | 0.28 | 0.18 |
| SD | South Dakota | 49.3 | B | 49.9 | B | 48.8 |  | 0 | 0 | 3 | 0 | $0K | $0K | Stable | 12.4 | Annual | none | thin | high | coop_only |  | low | 0.86 | 2.32 |
| NV | Nevada | 49.1 | B | 49.1 | B | 53.3 |  | 3 | 0 | 7 | 0 | $164K | $0K | Stable | 18.5 | Biennial | none | moderate | high | coop_only |  | med | 0.88 | 4.54 |
| TN | Tennessee | 48.4 | B | 47.9 | B | 48.7 |  | 1 | 2 | 23 | 2 | $244K | $667K | Constrained | 8.5 | Annual | none | moderate | high | coop_only |  | med | 0.88 | 5.79 |
| DE | Delaware | 47.6 | C | 41.0 | B | 54.2 | Y | 0 | 0 | 3 | 0 | $0K | $0K | Constrained | 5.1 | Annual | none | moderate | high | coop_only |  | low | 0.94 | 6.47 |
| IA | Iowa | 46.3 | C | 42.3 | B | 50.3 | Y | 1 | 1 | 11 | 1 | $512K | $90K | Constrained | 9.0 | Annual | none | moderate | med | strong |  | low | 0.25 | -0.3 |
| NJ | New Jersey | 46.3 | C | 42.5 | B | 54.0 | Y | 2 | 1 | 23 | 1 | $228K | $23K | Distressed | 0.0 | Annual | none | rich | high | coop_only |  | high | 0.44 | -3.92 |
| WV | West Virginia | 45.5 | B | 47.9 | C | 43.2 | Y | 0 | 0 | 3 | 0 | $0K | $0K | Constrained | 23.5 | Annual | none | thin | high | coop_only |  | med | -0.07 | 3.63 |
| WY | Wyoming | 45.2 | B | 47.3 | C | 43.1 | Y | 0 | 0 | 1 | 0 | $0K | $0K | Stable | 70.3 | Biennial | none | thin | high | coop_only |  | low | 0.35 | 2.5 |
| CO | Colorado | 45.0 | C | 42.5 | B | 50.1 | Y | 4 | 2 | 24 | 2 | $308K | $702K | Distressed | 9.0 | Annual | headwind | rich | med | present | Y | high | 0.4 | -2.01 |
| RI | Rhode Island | 45.0 | C | 41.3 | B | 48.8 | Y | 0 | 0 | 4 | 0 | $0K | $0K | Constrained | 5.2 | Annual | none | moderate | high | coop_only |  | low | 0.37 | -1.39 |
| NH | New Hampshire | 44.2 | C | 40.4 | B | 48.0 | Y | 0 | 0 | 5 | 0 | $0K | $0K | Constrained | 11.5 | Biennial | none | thin | high | coop_only |  | med | 0.48 | 4.63 |
| KS | Kansas | 44.1 | C | 44.1 | B | 48.1 | Y | 4 | 0 | 10 | 0 | $403K | $0K | Stable | 18.1 | Annual | none | thin | high | coop_only |  | low | 0.4 | -0.17 |
| OR | Oregon | 43.3 | C | 42.0 | C | 46.0 |  | 4 | 2 | 16 | 2 | $232K | $411K | Constrained | 17.1 | Biennial | none | moderate | med | coop_only |  | low | 0.19 | 0.52 |
| LA | Louisiana | 43.2 | C | 45.9 | C | 40.6 |  | 3 | 3 | 18 | 3 | $159K | $570K | Constrained | 9.8 | Annual | none | moderate | high | coop_only |  | low | 0.07 | -3.12 |
| NE | Nebraska | 42.8 | C | 37.5 | C | 42.8 |  | 0 | 1 | 5 | 1 | $0K | $29K | Distressed | 15.2 | Biennial | none | thin | med | coop_only | Y | low | 0.62 | -0.18 |
| IL | Illinois | 42.4 | B | 52.2 | C | 40.0 | Y | 1 | 4 | 27 | 4 | $76K | $1.67M | Constrained | 4.5 | Annual | none | moderate | med | coop_only |  | med | 0.13 | -3.15 |
| ID | Idaho | 42.3 | C | 42.3 | A | 59.7 | Y | 1 | 0 | 7 | 0 | $89K | $0K | Constrained | 21.3 | Annual | headwind | thin | med | coop_only |  | low | 1.44 | 9.81 |
| HI | Hawai'i | 42.2 | C | 41.2 | C | 43.3 |  | 0 | 0 | 4 | 0 | $0K | $0K | Constrained | 14.5 | Biennial | none | moderate | high | coop_only |  | low | -0.15 | -6.19 |
| MO | Missouri | 42.1 | C | 42.3 | C | 41.9 |  | 3 | 2 | 18 | 2 | $127K | $661K | Distressed | 5.8 | Annual | none | thin | med | coop_only |  | low | 0.43 | 2.24 |
| VT | Vermont | 41.2 | C | 41.8 | C | 40.7 |  | 0 | 0 | 1 | 0 | $0K | $0K | Constrained | 18.2 | Annual | none | moderate | high | coop_only |  | low | -0.29 | -1.13 |
| CT | Connecticut | 40.5 | C | 40.5 | B | 51.4 | Y | 4 | 0 | 13 | 0 | $745K | $0K | Stable | 18.8 | Biennial | none | moderate | med | coop_only |  | med | 0.38 | -1.61 |
| AK | Alaska | 40.2 | C | 38.6 | C | 41.9 |  | 0 | 0 | 3 | 0 | $0K | $0K | Distressed | 51.7 | Annual | none | moderate | high | coop_only |  | low | 0.1 | -6.14 |
| KY | Kentucky | 35.8 | D | 34.7 | B | 49.1 | Y | 12 | 1 | 11 | 1 | $937K | $72K | Constrained | 22.5 | Biennial | none | moderate | med | coop_only |  | low | 0.5 | 1.58 |
| ND | North Dakota | 34.7 | D | 34.7 | C | 42.5 | Y | 7 | 0 | 3 | 0 | $399K | $0K | Stable | 30.0 | Biennial | none | moderate | high | coop_only | Y | med | 0.75 | 0.64 |
| WA | Washington | 33.6 | D | 33.6 | A | 70.1 | Y | 5 | 0 | 23 | 0 | $994K | $0K | Distressed | 2.8 | Biennial | none | rich | med | present |  | med | 0.92 | 1.15 |
| ME | Maine | 26.9 | D | 26.9 | B | 52.9 | Y | 2 | 0 | 5 | 0 | $356K | $0K | Constrained | 13.2 | Biennial | none | moderate | high | coop_only |  | med | 0.46 | 5.23 |

### Sub-scores (0–1), state-agency side then local side

| Abbr | fiscal | reserves | IT mod | st headroom | agency scale | st access | cycle | whitespace | loc headroom | demand | funding | tax headwind | loc access | crosssell |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| TX | 0.700 | 0.932 | 1.000 | 0.574 | 0.945 | 1.000 | 0.650 | 0.849 | 0.155 | 0.634 | 0.358 | 0.350 | 1.000 | 0.575 |
| GA | 0.700 | 0.616 | 1.000 | 0.805 | 0.699 | 0.600 | 1.000 | 0.653 | 0.658 | 0.559 | 0.550 | 1.000 | 0.360 | 0.750 |
| VA | 0.700 | 0.496 | 1.000 | 0.938 | 0.642 | 1.000 | 0.650 | 0.508 | 0.112 | 0.526 | 0.798 | 1.000 | 1.000 | 0.562 |
| NM | 1.000 | 0.964 | 1.000 | 0.000 | 0.301 | 0.600 | 1.000 | 0.408 | 0.598 | 0.292 | 0.550 | 1.000 | 0.600 | 0.875 |
| NC | 0.700 | 0.444 | 0.150 | 1.000 | 0.697 | 0.600 | 0.650 | 0.672 | 0.828 | 0.862 | 0.550 | 1.000 | 0.198 | 0.500 |
| MN | 0.350 | 0.424 | 1.000 | 0.842 | 0.541 | 1.000 | 0.650 | 0.474 | 0.344 | 0.524 | 0.798 | 1.000 | 0.550 | 0.562 |
| IN | 0.350 | 0.380 | 0.150 | 1.000 | 0.584 | 0.600 | 0.650 | 0.583 | 0.903 | 0.509 | 0.550 | 1.000 | 0.600 | 0.750 |
| MA | 0.700 | 0.632 | 0.150 | 0.799 | 0.590 | 0.600 | 1.000 | 0.570 | 1.000 | 0.264 | 1.000 | 1.000 | 0.600 | 0.600 |
| NY | 0.350 | 0.308 | 0.150 | 0.452 | 0.835 | 1.000 | 1.000 | 0.626 | 0.892 | 0.279 | 0.865 | 1.000 | 0.550 | 0.792 |
| AR | 1.000 | 1.000 | 0.150 | 1.000 | 0.392 | 0.250 | 1.000 | 0.465 | 1.000 | 0.658 | 0.358 | 1.000 | 0.250 | 0.600 |
| FL | 0.350 | 0.344 | 0.350 | 0.855 | 0.873 | 0.600 | 1.000 | 0.704 | 0.000 | 0.573 | 0.798 | 0.350 | 0.600 | 0.510 |
| OH | 0.700 | 0.504 | 1.000 | 0.884 | 0.711 | 0.600 | 0.650 | 0.612 | 0.000 | 0.402 | 0.550 | 1.000 | 0.330 | 0.208 |
| PA | 0.100 | 0.620 | 1.000 | 1.000 | 0.733 | 1.000 | 1.000 | 0.626 | 0.792 | 0.341 | 0.550 | 1.000 | 0.550 | 0.500 |
| UT | 0.700 | 0.436 | 0.150 | 0.819 | 0.423 | 0.600 | 1.000 | 0.487 | 1.000 | 0.705 | 0.663 | 1.000 | 0.600 | 0.600 |
| CA | 0.100 | 0.696 | 0.300 | 0.437 | 0.996 | 0.600 | 1.000 | 0.950 | 0.058 | 0.257 | 0.910 | 1.000 | 0.360 | 0.550 |
| MT | 0.700 | 0.612 | 1.000 | 1.000 | 0.154 | 0.600 | 0.650 | 0.410 | 1.000 | 0.711 | 0.200 | 0.350 | 0.330 | 0.600 |
| AL | 0.700 | 0.780 | 0.150 | 0.903 | 0.514 | 0.250 | 1.000 | 0.540 | 0.894 | 0.602 | 0.550 | 1.000 | 0.150 | 0.375 |
| MD | 0.100 | 0.312 | 0.050 | 1.000 | 0.559 | 1.000 | 1.000 | 0.474 | 0.611 | 0.197 | 0.798 | 1.000 | 0.600 | 0.750 |
| OK | 0.350 | 0.684 | 0.150 | 0.871 | 0.459 | 1.000 | 1.000 | 0.453 | 0.309 | 0.576 | 0.200 | 1.000 | 1.000 | 0.125 |
| DC | 0.100 | 0.328 | 0.150 | 1.000 | 0.035 | 0.250 | 1.000 | 0.322 | 1.000 | 0.352 | 0.753 | 1.000 | 0.250 | 0.600 |
| SC | 0.350 | 0.552 | 0.150 | 1.000 | 0.531 | 0.250 | 1.000 | 0.540 | 0.595 | 0.909 | 0.200 | 1.000 | 0.150 | 0.125 |
| MS | 0.700 | 0.396 | 0.150 | 1.000 | 0.380 | 0.250 | 1.000 | 0.439 | 1.000 | 0.399 | 0.200 | 1.000 | 0.250 | 0.600 |
| WI | 0.700 | 0.372 | 0.150 | 0.940 | 0.547 | 0.600 | 0.650 | 0.497 | 0.317 | 0.462 | 0.393 | 1.000 | 0.198 | 0.375 |
| AZ | 0.350 | 0.364 | 0.050 | 0.473 | 0.605 | 0.600 | 1.000 | 0.537 | 0.544 | 0.587 | 0.550 | 1.000 | 0.600 | 0.250 |
| MI | 0.350 | 0.524 | 0.150 | 1.000 | 0.673 | 1.000 | 1.000 | 0.605 | 0.541 | 0.370 | 0.393 | 1.000 | 0.550 | 0.000 |
| SD | 0.700 | 0.496 | 0.150 | 1.000 | 0.106 | 0.250 | 1.000 | 0.374 | 1.000 | 0.658 | 0.200 | 1.000 | 0.138 | 0.600 |
| NV | 0.700 | 0.740 | 0.150 | 0.665 | 0.405 | 0.250 | 0.650 | 0.439 | 1.000 | 0.565 | 0.393 | 1.000 | 0.250 | 0.600 |
| TN | 0.350 | 0.340 | 0.150 | 0.776 | 0.595 | 0.250 | 1.000 | 0.556 | 0.134 | 0.664 | 0.393 | 1.000 | 0.150 | 0.438 |
| DE | 0.350 | 0.204 | 0.150 | 1.000 | 0.135 | 0.250 | 1.000 | 0.374 | 1.000 | 0.693 | 0.393 | 1.000 | 0.250 | 0.600 |
| IA | 0.350 | 0.360 | 0.150 | 0.000 | 0.401 | 1.000 | 1.000 | 0.453 | 0.737 | 0.412 | 0.550 | 1.000 | 0.330 | 0.375 |
| NJ | 0.100 | 0.000 | 0.150 | 0.840 | 0.659 | 0.250 | 1.000 | 0.575 | 0.977 | 0.228 | 0.640 | 1.000 | 0.250 | 0.625 |
| WV | 0.350 | 0.940 | 0.150 | 1.000 | 0.257 | 0.250 | 1.000 | 0.374 | 1.000 | 0.377 | 0.200 | 1.000 | 0.138 | 0.600 |
| WY | 0.700 | 1.000 | 0.150 | 1.000 | 0.000 | 0.250 | 0.650 | 0.322 | 1.000 | 0.439 | 0.200 | 1.000 | 0.138 | 0.600 |
| CO | 0.100 | 0.360 | 0.050 | 0.657 | 0.549 | 0.600 | 1.000 | 0.565 | 0.000 | 0.448 | 0.798 | 0.350 | 0.600 | 0.312 |
| RI | 0.350 | 0.208 | 0.150 | 1.000 | 0.147 | 0.250 | 1.000 | 0.393 | 1.000 | 0.401 | 0.393 | 1.000 | 0.250 | 0.600 |
| NH | 0.350 | 0.460 | 0.150 | 1.000 | 0.204 | 0.250 | 0.650 | 0.410 | 1.000 | 0.570 | 0.200 | 1.000 | 0.138 | 0.600 |
| KS | 0.700 | 0.724 | 0.150 | 0.092 | 0.381 | 0.250 | 1.000 | 0.476 | 1.000 | 0.490 | 0.200 | 1.000 | 0.138 | 0.600 |
| OR | 0.350 | 0.684 | 0.150 | 0.636 | 0.467 | 0.250 | 0.650 | 0.486 | 0.088 | 0.417 | 0.550 | 1.000 | 0.250 | 0.500 |
| LA | 0.350 | 0.392 | 0.150 | 0.769 | 0.486 | 0.250 | 1.000 | 0.485 | 0.000 | 0.225 | 0.393 | 1.000 | 0.250 | 0.708 |
| NE | 0.100 | 0.608 | 0.150 | 1.000 | 0.289 | 0.250 | 0.650 | 0.343 | 0.865 | 0.473 | 0.358 | 0.350 | 0.138 | 0.875 |
| IL | 0.350 | 0.180 | 0.150 | 0.960 | 0.727 | 0.250 | 1.000 | 0.556 | 0.000 | 0.191 | 0.550 | 1.000 | 0.138 | 0.375 |
| ID | 0.350 | 0.852 | 0.050 | 0.706 | 0.290 | 0.250 | 1.000 | 0.439 | 1.000 | 0.914 | 0.358 | 1.000 | 0.250 | 0.600 |
| HI | 0.350 | 0.580 | 0.150 | 1.000 | 0.207 | 0.250 | 0.650 | 0.393 | 1.000 | 0.126 | 0.393 | 1.000 | 0.250 | 0.600 |
| MO | 0.100 | 0.232 | 0.150 | 0.864 | 0.559 | 0.250 | 1.000 | 0.508 | 0.000 | 0.478 | 0.358 | 1.000 | 0.138 | 0.438 |
| VT | 0.350 | 0.728 | 0.150 | 1.000 | 0.017 | 0.250 | 1.000 | 0.322 | 1.000 | 0.168 | 0.393 | 1.000 | 0.138 | 0.600 |
| CT | 0.700 | 0.752 | 0.150 | 0.000 | 0.432 | 0.250 | 0.650 | 0.508 | 1.000 | 0.323 | 0.550 | 1.000 | 0.150 | 0.600 |
| AK | 0.100 | 1.000 | 0.150 | 1.000 | 0.049 | 0.250 | 1.000 | 0.374 | 1.000 | 0.079 | 0.393 | 1.000 | 0.250 | 0.600 |
| KY | 0.350 | 0.900 | 0.150 | 0.000 | 0.485 | 0.250 | 0.650 | 0.453 | 0.852 | 0.409 | 0.550 | 1.000 | 0.250 | 0.250 |
| ND | 0.700 | 1.000 | 0.150 | 0.000 | 0.068 | 0.250 | 0.650 | 0.374 | 1.000 | 0.450 | 0.393 | 0.350 | 0.138 | 0.600 |
| WA | 0.100 | 0.112 | 0.150 | 0.166 | 0.617 | 0.600 | 0.650 | 0.593 | 1.000 | 0.638 | 0.798 | 1.000 | 0.600 | 0.600 |
| ME | 0.350 | 0.528 | 0.150 | 0.000 | 0.204 | 0.250 | 0.650 | 0.410 | 1.000 | 0.663 | 0.393 | 1.000 | 0.138 | 0.600 |

---

## 4. Judgement overlay (source of purchasing / channel / capacity / tax-cap / IT-signal calls)

```csv
# Hand-curated overlay. Every row traces to research/granicus-market-and-competitive-landscape.md
# (purchasing_access, channel_occupied, local_capacity),
# research/govtech-state-demand-growth-2026.md section 5d (tax_cap_pressure), and
# research/state-fiscal-capacity-and-it-modernization-fy2026-fy2027.md section 2 (it_mod_signal).
#
# purchasing_access: strong = live, Granicus-named or statutorily-open statewide vehicle.
#                    present = usable state vehicle, but reseller paper, expiring, or currency unverified.
#                    coop_only = national cooperatives (OMNIA 159768, NASPO, NACo PPP) only.
# channel_occupied:  yes = VC3 holds the state municipal league endorsement, so the trusted-referral
#                    slot into locals is taken. Granicus holds no state league endorsement anywhere.
# local_capacity:    constrained = documented township fragmentation or documented absence of local IT
#                    staff/procurement capacity. typical = no adverse evidence found (a default, not a finding).
# tax_cap_pressure:  yes = enacted or on-ballot property tax cap/relief that squeezes local own-source revenue.
# it_mod_signal:     funded = named, funded state IT modernization appropriation.
#                    governance = named program that adds oversight but no money.
#                    headwind = identified negative signal (cuts, holdbacks, or a tax on IT services).
#                    none = no 2025-2026 signal verified. Means "not found", not "nothing happening".
state,purchasing_access,channel_occupied,local_capacity,tax_cap_pressure,it_mod_signal,note
Alabama,coop_only,yes,typical,no,none,VC3 holds the Alabama league endorsement
Alaska,coop_only,no,typical,no,none,Structural deficit despite 51.7pct reserves
Arizona,present,no,typical,no,headwind,ADOA/ASET statewide contracts open to locals; ~5pct across-the-board agency reductions proposed
Arkansas,coop_only,no,typical,no,none,
California,present,yes,typical,no,neutral,CMAS/NASPO via Carahsoft only; Cal Cities and CSDA both endorse VC3; state IT budget holding the line
Colorado,present,no,typical,yes,headwind,SIPA doubles as procurement vehicle and grant source; IT capital request only 9.8M GF; TABOR caps
Connecticut,coop_only,yes,typical,no,none,VC3 holds the CCM endorsement
Delaware,coop_only,no,typical,no,none,
District of Columbia,coop_only,no,typical,no,none,Single consolidated OCTO buyer
Florida,present,no,typical,yes,governance,OMNIA/Cobb vehicle to Apr 2028; HB 1197 adds Florida Digital Service oversight without funding; Amendment 3 on the Nov 2026 ballot
Georgia,present,yes,typical,no,funded,GTA statewide contracts; Technology Empowerment Fund 57.5M AFY2026; VC3 holds the GMA endorsement
Hawaii,coop_only,no,typical,no,none,Consolidated state plus four counties
Idaho,coop_only,no,typical,no,headwind,4pct agency holdback FY26 and a further 5pct planned FY27
Illinois,coop_only,no,constrained,no,none,No Granicus statewide vehicle found; 6930 local governments is the most in the nation
Indiana,present,no,typical,no,none,State QPA contracts
Iowa,strong,yes,constrained,no,none,Two state master agreements incl. 2019-BUS-228 open to other governmental entities; Iowa League endorses VC3
Kansas,coop_only,no,constrained,no,none,Township-heavy; 2026 property tax attempts failed
Kentucky,coop_only,no,typical,no,none,
Louisiana,coop_only,no,typical,no,none,
Maine,coop_only,no,constrained,no,none,
Maryland,strong,yes,typical,no,headwind,COTS Master to Sep 2027; 3pct state tax on IT and data services is a direct vendor headwind; MML endorses VC3
Massachusetts,present,no,typical,no,none,OSD statewide contracts open to munis; Community Compact IT grant prioritises ADA Title II
Michigan,strong,no,constrained,no,none,Live MiDEAL contract to 9/30/2027 covering state and locals; Revize entrenched in small-city web; ~1300 munis with thin IT
Minnesota,strong,no,constrained,no,funded,Cooperative Purchasing Venture open to counties and cities; Human Services Systems Modernization Fund ~50M FY27 plus 10M county IT
Mississippi,coop_only,no,typical,no,none,
Missouri,coop_only,no,constrained,no,none,
Montana,present,no,constrained,yes,funded,State MSA cooperative clause reaches other states but initial term ran to 1/31/2021 - verify; SITSD 2027 biennium +19.0M
Nebraska,coop_only,no,constrained,yes,none,
Nevada,coop_only,no,typical,no,none,
New Hampshire,coop_only,no,constrained,no,none,
New Jersey,coop_only,no,typical,no,none,LEAP implementation grants explicitly cover technology; zero rainy day fund
New Mexico,present,no,typical,no,funded,Carahsoft 30-00000-23-00067 to Apr 2027; Computer Systems Enhancement Fund plus 20M Technology Enhancement Fund
New York,strong,no,constrained,no,none,GovQA is the de facto statewide FOIL standard at 63 of 72 agencies; township in every county outside NYC
North Carolina,present,yes,constrained,no,none,NCDIT statewide term contracts; documented county procurement-capacity gap; VC3 holds the NCLM endorsement
North Dakota,coop_only,no,constrained,yes,none,Only 6 of 53 counties employ full-time IT staff; statutory hiring freeze and 10pct cut mandate
Ohio,present,no,constrained,no,funded,State Term Schedule 534354 expires Dec 2026 - renew or replace; DAS IT ~1.1B across the FY26-27 biennium; 2025 law requires local cyber plans
Oklahoma,strong,no,typical,no,none,OMES SW1041C runs to Oct 2030 and OMES actively markets statewide contracts to cities
Oregon,coop_only,no,typical,no,none,
Pennsylvania,strong,no,constrained,no,funded,COSTARS opens 9500+ buyers and DGS 4400028357 runs to Aug 2028; but 2559 subcounty units; +10M cyber and CODE PA
Rhode Island,coop_only,no,typical,no,none,
South Carolina,coop_only,yes,typical,no,none,VC3 holds the MASC endorsement
South Dakota,coop_only,no,constrained,no,none,
Tennessee,coop_only,yes,typical,no,none,VC3 holds the TML endorsement
Texas,strong,no,typical,yes,funded,DIR plus SmartBuy plus TXMAS plus TIPS plus BuyBoard is the strongest local purchasing access in the country; DIR pipeline 88 projects/788.1M; 51B committed to property tax relief
Utah,present,no,typical,no,none,Utah DTS provides shared cyber services to ~80pct of local governments
Vermont,coop_only,no,constrained,no,none,
Virginia,strong,no,typical,no,funded,Statute opens VITA contracts to all localities and VITA policy disfavours co-op workarounds; VITA 393.1M FY26 and an 85-project 929.8M portfolio
Washington,present,no,typical,no,none,DES 01313 names Granicus with MCUA and out-of-state access but term dates appear lapsed - verify
West Virginia,coop_only,no,constrained,no,none,
Wisconsin,present,yes,constrained,no,none,VendorNet cooperative purchasing; township in 71 of 72 counties; VC3 holds the League of Wisconsin Municipalities endorsement
Wyoming,coop_only,no,constrained,no,none,
```

---

## 5. XP rollup (revised book)

| XP | Level | Manager | Records | Countable | ARR | T1 | T2 | T3 | T4 | Growth share | Load | Load/acct | T1 ARR | T2 ARR | T3 ARR | T4 ARR | Terr A | B | C | D | Caps imputed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Steffany Amador | XP3 | Ashley Hill | 17 | 16 | $3.00M | 10 | 5 | 1 | 0 | 94% | 14.5 | 0.906 | $2.03M | $215K | $756K | $0K | 16 | 0 | 0 | 0 | 2 |
| Open XP2 (PT) | XP2 | TBD | 16 | 16 | $3.30M | 8 | 5 | 3 | 0 | 81% | 13.5 | 0.844 | $1.95M | $342K | $1.01M | $0K | 0 | 16 | 0 | 0 | 0 |
| Cody Nichols | XP1 | Ashley Hill | 17 | 17 | $1.25M | 3 | 11 | 2 | 1 | 82% | 13.1 | 0.771 | $370K | $592K | $254K | $38K | 7 | 3 | 7 | 0 | 1 |
| Taylor Roman | XP3 | Savannah Lane | 17 | 17 | $2.13M | 6 | 4 | 4 | 3 | 59% | 12.1 | 0.712 | $956K | $199K | $804K | $176K | 8 | 9 | 0 | 0 | 0 |
| Halena Martin | XP3 | Savannah Lane | 68 | 16 | $3.50M | 3 | 7 | 3 | 3 | 62% | 11.0 | 0.688 | $2.42M | $406K | $517K | $160K | 4 | 4 | 6 | 2 | 52 |
| Andy O'Brien | XP3 | Savannah Lane | 14 | 14 | $2.60M | 6 | 2 | 4 | 2 | 57% | 10.2 | 0.729 | $1.46M | $129K | $912K | $98K | 5 | 6 | 0 | 3 | 0 |
| Carolina Cambronero | XP3 | Savannah Lane | 17 | 17 | $3.25M | 2 | 5 | 6 | 4 | 41% | 10.2 | 0.600 | $723K | $271K | $2.07M | $194K | 9 | 5 | 3 | 0 | 3 |
| Colleen Moran | XP3 | Ashley Hill | 12 | 12 | $3.65M | 6 | 3 | 3 | 0 | 75% | 9.9 | 0.825 | $1.33M | $164K | $2.16M | $0K | 9 | 3 | 0 | 0 | 0 |
| Alejandro Solano | XP1 | Ashley Hill | 17 | 17 | $2.30M | 1 | 6 | 4 | 6 | 41% | 9.6 | 0.565 | $465K | $421K | $1.03M | $391K | 2 | 4 | 11 | 0 | 0 |
| Marcy Castro | XP1 | Ashley Hill | 16 | 16 | $4.34M | 2 | 3 | 6 | 5 | 31% | 8.9 | 0.556 | $295K | $150K | $3.60M | $294K | 3 | 4 | 9 | 0 | 0 |
| Brooke Minichino | XP2 | Savannah Lane | 13 | 13 | $2.04M | 1 | 6 | 5 | 1 | 54% | 8.6 | 0.662 | $178K | $190K | $1.58M | $90K | 6 | 4 | 3 | 0 | 1 |
| Carolina Prieto | Manager | Carolina Prieto (manager book) | 38 | 23 | $2.49M | 0 | 0 | 7 | 16 | 0% | 8.3 | 0.361 | $0K | $0K | $2.29M | $201K | 1 | 4 | 2 | 16 | 25 |
| Paige Wendle | XP3 | Savannah Lane | 15 | 15 | $3.15M | 0 | 0 | 9 | 6 | 0% | 6.3 | 0.420 | $0K | $0K | $2.79M | $368K | 0 | 3 | 7 | 5 | 0 |

WIP proposed-book rollup exists in `tiering.json` as `xp_wip` if needed; revised book is the working scenario.

---

## 6. Countable accounts (n=209)

Allocated $0 children are omitted. `xp_new` is the revised assignment; `xp_wip` is the WIP proposed book.
`tt` is the side-specific territory tier (state-agency score if Map=State, local score if Map=Local ENT).
`gp` is growth potential. `cd` is reported vs imputed capability depth.

| Account | St | Side | AE | XP revised | XP WIP | ARR | Caps | cd | Terr | Score | WS | GP | Tier | Label |
|---|---|---|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---|
| New York State Department of Labor | NY | State | Stephanie DelSignore | Halena Martin | Halena Martin | $1.60M | 3 | reported | B | 57.0 | 0.625 | 0.592 | 1 | Growth engine |
| Connecticut Department of Administrative Services | CT | State | Stephanie DelSignore | Halena Martin | Halena Martin | $606K | 1 | reported | C | 40.5 | 0.875 | 0.593 | 1 | Growth engine |
| Harris County TX - Universal Services | TX | Local ENT | Pete Redondo | Carolina Cambronero | Taylor Roman | $590K | 2 | reported | A | 63.1 | 0.75 | 0.6786 | 1 | Growth engine |
| California Department of Healthcare Services (DHCS) | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $557K | 2 | reported | B | 54.4 | 0.75 | 0.6264 | 1 | Growth engine |
| Virginia Beach, VA | VA | Local ENT | Josh Gondwe | Andy O'Brien | Andy O'Brien | $502K | 3 | reported | A | 63.9 | 0.625 | 0.6334 | 1 | Growth engine |
| California Department of Corrections and Rehabilitation (CDCR) | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $489K | 2 | reported | B | 54.4 | 0.75 | 0.6264 | 1 | Growth engine |
| Dallas Area Rapid Transit (DART) | TX | Local ENT | Dallas SAM (open) | Alejandro Solano | (not in WIP) | $465K | 3 | reported | A | 63.1 | 0.625 | 0.6286 | 1 | Growth engine |
| Sonoma County CA | CA | Local ENT | Jason Spanier | Colleen Moran | Colleen Moran | $353K | 3 | reported | A | 62.3 | 0.625 | 0.6238 | 1 | Growth engine |
| Texas Department of Motor Vehicles | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $331K | 2 | reported | A | 82.4 | 0.75 | 0.7944 | 1 | Growth engine |
| Prince William County VA | VA | Local ENT | Josh Gondwe | Andy O'Brien | Andy O'Brien | $329K | 4 | reported | A | 63.9 | 0.5 | 0.5834 | 1 | Growth engine |
| Texas Department of Transportation (TXDOT) | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $321K | 3 | reported | A | 82.4 | 0.625 | 0.7444 | 1 | Growth engine |
| Los Angeles County CA, Board of Supervisors | CA | Local ENT | Jeff Gaisford | Colleen Moran | Colleen Moran | $305K | 3 | reported | A | 62.3 | 0.625 | 0.6238 | 1 | Growth engine |
| DeKalb County, GA | GA | Local ENT | Spencer Ferrell | Taylor Roman | Andy O'Brien | $277K | 3 | reported | A | 61.3 | 0.625 | 0.6178 | 1 | Growth engine |
| Texas Department of Insurance | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $260K | 2 | reported | A | 82.4 | 0.75 | 0.7944 | 1 | Growth engine |
| Tennessee General Assembly | TN | State | State AE – KY/TN/AR | Andy O'Brien | (not in WIP) | $244K | 1 | reported | B | 47.9 | 0.875 | 0.6374 | 1 | Growth engine |
| Texas Department of Licensing and Regulation | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $226K | 2 | reported | A | 82.4 | 0.75 | 0.7944 | 1 | Growth engine |
| Texas Workforce Commission | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $226K | 5 | reported | A | 82.4 | 0.375 | 0.6444 | 1 | Growth engine |
| Superior Court of California, County of San Francisco | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $217K | 1 | reported | B | 54.4 | 0.875 | 0.6764 | 1 | Growth engine |
| Riverside County CA | CA | Local ENT | Jason Spanier | Colleen Moran | Colleen Moran | $217K | 2 | reported | A | 62.3 | 0.75 | 0.6738 | 1 | Growth engine |
| Massachusetts Department of Transportation | MA | State | Stephanie DelSignore | Halena Martin | Halena Martin | $215K | 2 | reported | A | 61.8 | 0.75 | 0.6708 | 1 | Growth engine |
| Metropolitan Water District of Southern California | CA | Local ENT | Jeff Gaisford | Colleen Moran | (not in WIP) | $207K | 2 | reported | A | 62.3 | 0.75 | 0.6738 | 1 | Growth engine |
| California Department of Public Health | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $184K | 2 | reported | B | 54.4 | 0.75 | 0.6264 | 1 | Growth engine |
| Ramsey County MN | MN | Local ENT | Tyler Carlson | Brooke Minichino | Brooke Minichino | $178K | 3 | reported | A | 58.5 | 0.625 | 0.601 | 1 | Growth engine |
| Texas Health & Human Services Commission | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $175K | 4 | reported | A | 82.4 | 0.5 | 0.6944 | 1 | Growth engine |
| Palm Beach County FL Sheriff’s Office | FL | Local ENT | Bill Marshall | Taylor Roman | Carolina Cambronero | $156K | 1 | reported | B | 57.8 | 0.875 | 0.6968 | 1 | Growth engine |
| Ohio Workers' Compensation Bureau | OH | State | Bettsy Desjarlais | Marcy Castro | Steffany Amador | $155K | 3 | reported | A | 74.7 | 0.625 | 0.6982 | 1 | Growth engine |
| Placer County CA | CA | Local ENT | Jason Spanier | Colleen Moran | Colleen Moran | $151K | 2 | reported | A | 62.3 | 0.75 | 0.6738 | 1 | Growth engine |
| California Department of Housing & Community Development | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $145K | 2 | reported | B | 54.4 | 0.75 | 0.6264 | 1 | Growth engine |
| Arizona Department of Transportation | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $141K | 2 | reported | C | 46.6 | 0.75 | 0.5796 | 1 | Growth engine |
| Kansas City, MO, Police Department | MO | Local ENT | David Cliff | Marcy Castro | Marcy Castro | $139K | 1 | reported | C | 41.9 | 0.875 | 0.6014 | 1 | Growth engine |
| Palm Beach County, FL | FL | Local ENT | Bill Marshall | Taylor Roman | Carolina Cambronero | $139K | 1 | reported | B | 57.8 | 0.875 | 0.6968 | 1 | Growth engine |
| Texas Department of Public Safety | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $139K | 1 | reported | A | 82.4 | 0.875 | 0.8444 | 1 | Growth engine |
| California Judicial Council of California | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $139K | 2 | reported | B | 54.4 | 0.75 | 0.6264 | 1 | Growth engine |
| Houston Independent School District | TX | Local ENT | Pete Redondo | Carolina Cambronero | (not in WIP) | $134K | 3 | reported | A | 63.1 | 0.625 | 0.6286 | 1 | Growth engine |
| Pedernales Electric Cooperative | TX | Local ENT | Cedric Simpkins | Steffany Amador | (not in WIP) | $131K | 2 | reported | A | 63.1 | 0.75 | 0.6786 | 1 | Growth engine |
| Cobb County GA | GA | Local ENT | Spencer Ferrell | Taylor Roman | Andy O'Brien | $130K | 1 | reported | A | 61.3 | 0.875 | 0.7178 | 1 | Growth engine |
| Frederick County MD | MD | Local ENT | Josh Gondwe | Andy O'Brien | Andy O'Brien | $130K | 2 | reported | B | 56.3 | 0.75 | 0.6378 | 1 | Growth engine |
| Georgia Department of Natural Resources | GA | State | Sarah Duncan | Taylor Roman | Andy O'Brien | $130K | 3 | reported | A | 77.5 | 0.625 | 0.715 | 1 | Growth engine |
| Shelby County TN | TN | Local ENT | Carter Bradford | Andy O'Brien | Marcy Castro | $128K | 2 | reported | B | 48.7 | 0.75 | 0.5922 | 1 | Growth engine |
| Howard County MD | MD | Local ENT | Josh Gondwe | Andy O'Brien | Andy O'Brien | $127K | 2 | reported | B | 56.3 | 0.75 | 0.6378 | 1 | Growth engine |
| Miami-Dade County FL | FL | Local ENT | Bill Marshall | Taylor Roman | Carolina Cambronero | $125K | 2 | reported | B | 57.8 | 0.75 | 0.6468 | 1 | Growth engine |
| Texas Commission on Law Enforcement | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $121K | 4 | reported | A | 82.4 | 0.5 | 0.6944 | 1 | Growth engine |
| New Mexico Department of Public Safety | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $120K | 1 | reported | A | 67.0 | 0.875 | 0.752 | 1 | Growth engine |
| California Department of General Services | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $111K | 3 | reported | B | 54.4 | 0.625 | 0.5764 | 1 | Growth engine |
| Arizona Department of Gaming | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $109K | 2 | reported | C | 46.6 | 0.75 | 0.5796 | 1 | Growth engine |
| California Department of State Hospitals | CA | State | State AE – CA/HI | Open XP2 (PT) | (not in WIP) | $106K | 1 | reported | B | 54.4 | 0.875 | 0.6764 | 1 | Growth engine |
| Los Angeles County Sanitation District | CA | Local ENT | Jeff Gaisford | Colleen Moran | (not in WIP) | $101K | 3 | reported | A | 62.3 | 0.625 | 0.6238 | 1 | Growth engine |
| VIA Metropolitan Transit | TX | Local ENT | Cedric Simpkins | Steffany Amador | (not in WIP) | $98K | 1 | reported | A | 63.1 | 0.875 | 0.7286 | 1 | Growth engine |
| Jefferson Parish - LA | LA | Local ENT | Austin Goodman | Alejandro Solano | Alejandro Solano | $97K | 1 | reported | C | 40.6 | 0.875 | 0.5936 | 2 | Expansion |
| Utah Department of Corrections | UT | State | Che Bustos | Alejandro Solano | Paige Wendle | $95K | 1 | reported | B | 57.5 | 0.875 | 0.695 | 2 | Expansion |
| Florida Department of Corrections - Public Records | FL | State | Demi Washington | Carolina Cambronero | Carolina Cambronero | $91K | 0 | imputed | A | 62.0 | 0.75 | 0.672 | 2 | Expansion |
| Albuquerque, NM | NM | Local ENT | Stephen Allen | Cody Nichols | Cody Nichols | $90K | 1 | reported | B | 53.4 | 0.875 | 0.6704 | 2 | Expansion |
| Texas Higher Education Coordinating Board | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $90K | 2 | reported | A | 82.4 | 0.75 | 0.7944 | 2 | Expansion |
| California Department of Developmental Services | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $90K | 1 | reported | B | 54.4 | 0.875 | 0.6764 | 2 | Expansion |
| California Energy Commission | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $89K | 2 | reported | B | 54.4 | 0.75 | 0.6264 | 2 | Expansion |
| Arizona Department of Economic Security | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $88K | 1 | reported | C | 46.6 | 0.875 | 0.6296 | 2 | Expansion |
| Dutchess County NY | NY | Local ENT | Territory 4a (open) | Halena Martin | Halena Martin | $86K | 2 | reported | A | 64.9 | 0.75 | 0.6894 | 2 | Expansion |
| North Central Texas Council of Governments | TX | Local ENT | Dallas SAM (open) | Alejandro Solano | (not in WIP) | $83K | 1 | reported | A | 63.1 | 0.875 | 0.7286 | 2 | Expansion |
| Virginia Department of General Services | VA | State | Grant Samson | Andy O'Brien | Andy O'Brien | $82K | 3 | reported | A | 78.8 | 0.625 | 0.7228 | 2 | Expansion |
| Rochester, NY | NY | Local ENT | Territory 4a (open) | Halena Martin | Halena Martin | $81K | 1 | reported | A | 64.9 | 0.875 | 0.7394 | 2 | Expansion |
| Arizona Department of Corrections, Rehabilitation & Reentry | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $78K | 1 | reported | C | 46.6 | 0.875 | 0.6296 | 2 | Expansion |
| Philadelphia, PA | PA | Local ENT | Andrew Wyzkoski | Halena Martin | Halena Martin | $77K | 1 | reported | B | 57.9 | 0.875 | 0.6974 | 2 | Expansion |
| California Alcoholic Beverage Control Department | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $77K | 1 | reported | B | 54.4 | 0.875 | 0.6764 | 2 | Expansion |
| Lake County IN | IN | Local ENT | Kent Hartsfield | Marcy Castro | Brooke Minichino | $71K | 2 | reported | A | 63.7 | 0.75 | 0.6822 | 2 | Expansion |
| Georgia Office of the Commissioner of Insurance and Safety Fire | GA | State | Sarah Duncan | Taylor Roman | Andy O'Brien | $70K | 1 | reported | A | 77.5 | 0.875 | 0.815 | 2 | Expansion |
| Webb County TX | TX | Local ENT | Pete Redondo | Carolina Cambronero | Taylor Roman | $70K | 2 | reported | A | 63.1 | 0.75 | 0.6786 | 2 | Expansion |
| New Mexico Energy, Minerals & Natural Resources Department | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $68K | 2 | reported | A | 67.0 | 0.75 | 0.702 | 2 | Expansion |
| Kansas Highway Patrol | KS | State | Matt Russell | Alejandro Solano | Alejandro Solano | $66K | 1 | reported | C | 44.1 | 0.875 | 0.6146 | 2 | Expansion |
| Nevada Department of Human Services | NV | State | Cameron Chadsey | Colleen Moran | Cody Nichols | $64K | 1 | reported | B | 49.1 | 0.875 | 0.6446 | 2 | Expansion |
| Georgia Bureau of Investigation | GA | State | Sarah Duncan | Taylor Roman | Andy O'Brien | $63K | 1 | reported | A | 77.5 | 0.875 | 0.815 | 2 | Expansion |
| Hillsborough County FL | FL | Local ENT | Desmond Davis | Carolina Cambronero | Carolina Cambronero | $60K | 1 | reported | B | 57.8 | 0.875 | 0.6968 | 2 | Expansion |
| Dutchess County NY, District Attorney’s Office | NY | Local ENT | Territory 4a (open) | Halena Martin | Halena Martin | $60K | 2 | reported | A | 64.9 | 0.75 | 0.6894 | 2 | Expansion |
| California Department of Forestry and Fire Protection | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $60K | 1 | reported | B | 54.4 | 0.875 | 0.6764 | 2 | Expansion |
| Oklahoma Dept of Agriculture, Food and Forestry | OK | State | Matt Russell | Alejandro Solano | Alejandro Solano | $55K | 2 | reported | B | 57.6 | 0.75 | 0.6456 | 2 | Expansion |
| Nevada Health Authority | NV | State | Cameron Chadsey | Colleen Moran | Cody Nichols | $52K | 1 | reported | B | 49.1 | 0.875 | 0.6446 | 2 | Expansion |
| Minnesota Public Utilities Commission | MN | State | Joe Spair | Brooke Minichino | Brooke Minichino | $51K | 0 | imputed | A | 67.4 | 0.75 | 0.7044 | 2 | Expansion |
| Ohio Department of Natural Resources | OH | State | Bettsy Desjarlais | Marcy Castro | Steffany Amador | $51K | 2 | reported | A | 74.7 | 0.75 | 0.7482 | 2 | Expansion |
| Louisiana Department of Health | LA | State | Demi Washington | Carolina Cambronero | Alejandro Solano | $50K | 1 | reported | C | 45.9 | 0.875 | 0.6254 | 2 | Expansion |
| Arizona Corporation Commission | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $49K | 1 | reported | C | 46.6 | 0.875 | 0.6296 | 2 | Expansion |
| New Mexico Regulation & Licensing Department | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $48K | 3 | reported | A | 67.0 | 0.625 | 0.652 | 2 | Expansion |
| Nevada Department of Motor Vehicles | NV | State | Cameron Chadsey | Colleen Moran | Cody Nichols | $48K | 1 | reported | B | 49.1 | 0.875 | 0.6446 | 2 | Expansion |
| Onslow County NC | NC | Local ENT | Joel Parris | Andy O'Brien | Andy O'Brien | $46K | 1 | reported | A | 64.9 | 0.875 | 0.7394 | 2 | Expansion |
| New Mexico Environment Department | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $45K | 3 | reported | A | 67.0 | 0.625 | 0.652 | 2 | Expansion |
| New Mexico Early Childhood Education & Care Department | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $43K | 1 | reported | A | 67.0 | 0.875 | 0.752 | 2 | Expansion |
| Texas Division of Emergency Management | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $41K | 2 | reported | A | 82.4 | 0.75 | 0.7944 | 2 | Expansion |
| Connecticut Public Utilities Regulatory Authority [PURA], | CT | State | Stephanie DelSignore | Halena Martin | Halena Martin | $41K | 1 | reported | C | 40.5 | 0.875 | 0.593 | 2 | Expansion |
| Georgia Department of Community Affairs | GA | State | Sarah Duncan | Taylor Roman | Andy O'Brien | $40K | 1 | reported | A | 77.5 | 0.875 | 0.815 | 2 | Expansion |
| Minnesota Department of Children, Youth, and Families | MN | State | Joe Spair | Brooke Minichino | Brooke Minichino | $37K | 1 | reported | A | 67.4 | 0.875 | 0.7544 | 2 | Expansion |
| New Mexico Health Care Authority | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $37K | 1 | reported | A | 67.0 | 0.875 | 0.752 | 2 | Expansion |
| New York Office of the Inspector General | NY | State | Stephanie DelSignore | Halena Martin | (not in WIP) | $31K | 1 | reported | B | 57.0 | 0.875 | 0.692 | 2 | Expansion |
| Connecticut Department of Emergency Services and Public Protection | CT | State | Stephanie DelSignore | Halena Martin | Halena Martin | $30K | 1 | reported | C | 40.5 | 0.875 | 0.593 | 2 | Expansion |
| Texas Ethics Commission | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $29K | 1 | reported | A | 82.4 | 0.875 | 0.8444 | 2 | Expansion |
| Texas Lottery Commission | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $29K | 0 | imputed | A | 82.4 | 0.75 | 0.7944 | 2 | Expansion |
| DOTComm (Douglas Omaha Technology Commission) | NE | Local ENT | David Cliff | Marcy Castro | (not in WIP) | $29K | 1 | reported | C | 42.8 | 0.875 | 0.6068 | 2 | Expansion |
| California Board of State & Community Corrections | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $27K | 1 | reported | B | 54.4 | 0.875 | 0.6764 | 2 | Expansion |
| Wisconsin Court System | WI | State | Joe Spair | Brooke Minichino | Brooke Minichino | $27K | 3 | reported | B | 57.8 | 0.625 | 0.5968 | 2 | Expansion |
| Wisconsin Department of Public Instruction | WI | State | Joe Spair | Brooke Minichino | Brooke Minichino | $27K | 3 | reported | B | 57.8 | 0.625 | 0.5968 | 2 | Expansion |
| Texas Board of Nursing | TX | State | No State AE shown (TX) | Steffany Amador | Taylor Roman | $26K | 5 | reported | A | 82.4 | 0.375 | 0.6444 | 2 | Expansion |
| Minnesota Attorney General | MN | State | Joe Spair | Brooke Minichino | Brooke Minichino | $26K | 3 | reported | A | 67.4 | 0.625 | 0.6544 | 2 | Expansion |
| Georgia Environmental Protection Division | GA | State | Sarah Duncan | Taylor Roman | Andy O'Brien | $25K | 3 | reported | A | 77.5 | 0.625 | 0.715 | 2 | Expansion |
| Oklahoma Public Employees Retirement System | OK | State | Matt Russell | Alejandro Solano | Alejandro Solano | $24K | 3 | reported | B | 57.6 | 0.625 | 0.5956 | 2 | Expansion |
| Arizona State Schools for the Deaf & the Blind | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $23K | 0 | imputed | C | 46.6 | 0.75 | 0.5796 | 2 | Expansion |
| New Mexico Department of Justice | NM | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $23K | 3 | reported | A | 67.0 | 0.625 | 0.652 | 2 | Expansion |
| Minnesota State Auditor's Office | MN | State | Joe Spair | Brooke Minichino | Brooke Minichino | $22K | 3 | reported | A | 67.4 | 0.625 | 0.6544 | 2 | Expansion |
| Florida Department of Corrections | FL | State | Demi Washington | Carolina Cambronero | Carolina Cambronero | $0K | 0 | imputed | A | 62.0 | 0.75 | 0.672 | 2 | Expansion |
| Los Angeles, CA | CA | Local ENT | Jeff Gaisford | Colleen Moran | Colleen Moran | $1.77M | 6 | reported | A | 62.3 | 0.25 | 0.4738 | 3 | Defend |
| Cook County, IL | IL | Local ENT | Kent Hartsfield | Marcy Castro | Steffany Amador | $1.11M | 3 | reported | C | 40.0 | 0.625 | 0.49 | 3 | Defend |
| Orange County FL | FL | Local ENT | Desmond Davis | Carolina Cambronero | Carolina Cambronero | $974K | 5 | reported | B | 57.8 | 0.375 | 0.4968 | 3 | Defend |
| Columbus OH | OH | Local ENT | Kent Hartsfield | Marcy Castro | Steffany Amador | $870K | 9 | reported | B | 47.0 | 0.0 | 0.282 | 3 | Defend |
| San Antonio, TX | TX | Local ENT | Cedric Simpkins | Steffany Amador | Steffany Amador | $756K | 6 | reported | A | 63.1 | 0.25 | 0.4786 | 3 | Defend |
| District of Columbia | DC | Neither map | Not on either map | Paige Wendle | Paige Wendle | $725K | 4 | reported | B | 51.7 | 0.5 | 0.5102 | 3 | Defend |
| Franklin County OH | OH | Local ENT | Kent Hartsfield | Marcy Castro | Steffany Amador | $619K | 8 | reported | B | 47.0 | 0.0 | 0.282 | 3 | Defend |
| California Secretary of State | CA | State | State AE – CA/HI | Open XP2 (PT) | (not in WIP) | $597K | 4 | reported | B | 54.4 | 0.5 | 0.5264 | 3 | Defend |
| Nashville-Davidson County TN | TN | Local ENT | Carter Bradford | Carolina Prieto | Marcy Castro | $539K | 7 | reported | B | 48.7 | 0.125 | 0.3422 | 3 | Defend |
| Jackson County MO | MO | Local ENT | David Cliff | Marcy Castro | Marcy Castro | $521K | 9 | reported | C | 41.9 | 0.0 | 0.2514 | 3 | Defend |
| Iowa Division of Information Technology | IA | State | No State AE shown (IA) | Brooke Minichino | Steffany Amador | $512K | 3 | reported | C | 42.3 | 0.625 | 0.5038 | 3 | Defend |
| Wayne County MI | MI | Local ENT | Tyler Carlson | Brooke Minichino | Brooke Minichino | $489K | 8 | reported | B | 49.5 | 0.0 | 0.297 | 3 | Defend |
| New Orleans LA | LA | Local ENT | Austin Goodman | Alejandro Solano | Alejandro Solano | $424K | 3 | reported | C | 40.6 | 0.625 | 0.4936 | 3 | Defend |
| Oakland, CA | CA | Local ENT | Jason Spanier | Carolina Prieto | Colleen Moran | $417K | 5 | reported | A | 62.3 | 0.375 | 0.5238 | 3 | Defend |
| Kentucky Commonwealth Office of Technology | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $393K | 3 | reported | D | 34.7 | 0.625 | 0.4582 | 3 | Defend |
| Kentucky Cabinet for Health & Family Services (CHFS) | KY | State | State AE – KY/TN/AR | Andy O'Brien | Marcy Castro | $376K | 4 | reported | D | 34.7 | 0.5 | 0.4082 | 3 | Defend |
| Denver City and County, CO | CO | Local ENT | David Cliff | Paige Wendle | Steffany Amador | $371K | 4 | reported | B | 50.1 | 0.5 | 0.5006 | 3 | Defend |
| North Dakota Information Technology Department | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $360K | 3 | reported | D | 34.7 | 0.625 | 0.4582 | 3 | Defend |
| Arapahoe County CO | CO | Local ENT | David Cliff | Paige Wendle | Steffany Amador | $332K | 7 | reported | B | 50.1 | 0.125 | 0.3506 | 3 | Defend |
| Miami FL | FL | Local ENT | Bill Marshall | Taylor Roman | Taylor Roman | $305K | 4 | reported | B | 57.8 | 0.5 | 0.5468 | 3 | Defend |
| Washington Department of Transportation | WA | State | Todd Bowers | Paige Wendle | Paige Wendle | $302K | 4 | reported | D | 33.6 | 0.5 | 0.4016 | 3 | Defend |
| Oklahoma City OK | OK | Local ENT | Austin Goodman | Alejandro Solano | Alejandro Solano | $300K | 7 | reported | B | 52.0 | 0.125 | 0.362 | 3 | Defend |
| Washington State Department of Health | WA | State | Todd Bowers | Paige Wendle | Paige Wendle | $296K | 2 | reported | D | 33.6 | 0.75 | 0.5016 | 3 | Defend |
| Cleveland, OH | OH | Local ENT | Kent Hartsfield | Marcy Castro | Steffany Amador | $292K | 3 | reported | B | 47.0 | 0.625 | 0.532 | 3 | Defend |
| Maine | ME | State | No State AE shown (ME) | Halena Martin | Halena Martin | $289K | 3 | reported | D | 26.9 | 0.625 | 0.4114 | 3 | Defend |
| Corpus Christi, TX | TX | Local ENT | Pete Redondo | Carolina Cambronero | Taylor Roman | $288K | 6 | reported | A | 63.1 | 0.25 | 0.4786 | 3 | Defend |
| Aurora, IL | IL | Local ENT | Kent Hartsfield | Carolina Prieto | Steffany Amador | $278K | 9 | reported | C | 40.0 | 0.0 | 0.24 | 3 | Defend |
| Florida Department of Health | FL | State | Demi Washington | Carolina Cambronero | Carolina Cambronero | $249K | 4 | reported | A | 62.0 | 0.5 | 0.572 | 3 | Defend |
| Richland County SC | SC | Local ENT | Joel Parris | Andy O'Brien | Andy O'Brien | $238K | 7 | reported | B | 51.3 | 0.125 | 0.3578 | 3 | Defend |
| Washington County OR | OR | Local ENT | Carrie Breedlove | Paige Wendle | Paige Wendle | $230K | 6 | reported | C | 46.0 | 0.25 | 0.376 | 3 | Defend |
| St. Paul MN | MN | Local ENT | Tyler Carlson | Brooke Minichino | Brooke Minichino | $226K | 4 | reported | A | 58.5 | 0.5 | 0.551 | 3 | Defend |
| California State Teachers' Retirement System | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $223K | 4 | reported | B | 54.4 | 0.5 | 0.5264 | 3 | Defend |
| Greater Los Angeles County Vector Control District CA | CA | Local ENT | Jeff Gaisford | Colleen Moran | Colleen Moran | $219K | 4 | reported | A | 62.3 | 0.5 | 0.5738 | 3 | Defend |
| Washington State Patrol | WA | State | Todd Bowers | Paige Wendle | Paige Wendle | $210K | 3 | reported | D | 33.6 | 0.625 | 0.4516 | 3 | Defend |
| Laredo, TX | TX | Local ENT | Pete Redondo | Carolina Cambronero | Taylor Roman | $208K | 9 | reported | A | 63.1 | 0.0 | 0.3786 | 3 | Defend |
| Collier County FL | FL | Local ENT | Bill Marshall | Taylor Roman | Carolina Cambronero | $199K | 6 | reported | B | 57.8 | 0.25 | 0.4468 | 3 | Defend |
| California Department of Justice | CA | State | State AE – CA/HI | Open XP2 (PT) | Colleen Moran | $195K | 4 | reported | B | 54.4 | 0.5 | 0.5264 | 3 | Defend |
| Kansas Department for Children & Families | KS | State | Matt Russell | Alejandro Solano | Alejandro Solano | $189K | 3 | reported | C | 44.1 | 0.625 | 0.5146 | 3 | Defend |
| Lake County IL | IL | Local ENT | Kent Hartsfield | Marcy Castro | Steffany Amador | $186K | 5 | reported | C | 40.0 | 0.375 | 0.39 | 3 | Defend |
| Glendale, AZ | AZ | Local ENT | Conrad Taylor | Carolina Prieto | Cody Nichols | $184K | 7 | reported | B | 57.3 | 0.125 | 0.3938 | 3 | Defend |
| Milwaukee County WI | WI | Local ENT | Tyler Carlson | Brooke Minichino | Brooke Minichino | $183K | 4 | reported | C | 44.7 | 0.5 | 0.4682 | 3 | Defend |
| Orlando, FL | FL | Local ENT | Desmond Davis | Carolina Cambronero | Carolina Cambronero | $181K | 5 | reported | B | 57.8 | 0.375 | 0.4968 | 3 | Defend |
| Tri-County Metropolitan Transportation District of Oregon (TriMet) | OR | Local ENT | Carrie Breedlove | Paige Wendle | (not in WIP) | $181K | 2 | reported | C | 46.0 | 0.75 | 0.576 | 3 | Defend |
| Fort Lauderdale, FL | FL | Local ENT | Bill Marshall | Taylor Roman | Carolina Cambronero | $175K | 6 | reported | B | 57.8 | 0.25 | 0.4468 | 3 | Defend |
| Milwaukee, WI | WI | Local ENT | Tyler Carlson | Brooke Minichino | Brooke Minichino | $172K | 5 | reported | C | 44.7 | 0.375 | 0.4182 | 3 | Defend |
| Glendale, CA | CA | Local ENT | Jeff Gaisford | Colleen Moran | Colleen Moran | $171K | 6 | reported | A | 62.3 | 0.25 | 0.4738 | 3 | Defend |
| Florida Department of Law Enforcement | FL | State | Demi Washington | Carolina Cambronero | Carolina Cambronero | $166K | 5 | reported | A | 62.0 | 0.375 | 0.522 | 3 | Defend |
| Fayetteville, NC | NC | Local ENT | Joel Parris | Andy O'Brien | Andy O'Brien | $156K | 7 | reported | A | 64.9 | 0.125 | 0.4394 | 3 | Defend |
| Yavapai County AZ | AZ | Local ENT | Stephen Allen | Cody Nichols | Cody Nichols | $144K | 6 | reported | B | 57.3 | 0.25 | 0.4438 | 3 | Defend |
| Kentucky Transportation Cabinet | KY | State | State AE – KY/TN/AR | Andy O'Brien | Marcy Castro | $142K | 3 | reported | D | 34.7 | 0.625 | 0.4582 | 3 | Defend |
| Washington Department of Corrections | WA | State | Todd Bowers | Paige Wendle | Paige Wendle | $140K | 1 | reported | D | 33.6 | 0.875 | 0.5516 | 3 | Defend |
| Health Care District of Palm Beach County - FL | FL | Local ENT | Bill Marshall | Taylor Roman | (not in WIP) | $125K | 5 | reported | B | 57.8 | 0.375 | 0.4968 | 3 | Defend |
| New Jersey Department of Children and Families | NJ | State | Stephanie DelSignore | Halena Martin | Halena Martin | $123K | 4 | reported | C | 42.5 | 0.5 | 0.455 | 3 | Defend |
| Housing Authority of the City of Pittsburgh | PA | Local ENT | Andrew Wyzkoski | Carolina Prieto | (not in WIP) | $121K | 6 | reported | B | 57.9 | 0.25 | 0.4474 | 3 | Defend |
| Colorado Department of Regulatory Agencies | CO | State | Che Bustos | Alejandro Solano | Alejandro Solano | $114K | 3 | reported | C | 42.5 | 0.625 | 0.505 | 3 | Defend |
| Arizona Department of Environmental Quality | AZ | State | Cameron Chadsey | Cody Nichols | Cody Nichols | $110K | 4 | reported | C | 46.6 | 0.5 | 0.4796 | 3 | Defend |
| New Jersey Cybersecurity and Communications Integration Cell | NJ | State | Stephanie DelSignore | Halena Martin | Halena Martin | $105K | 3 | reported | C | 42.5 | 0.625 | 0.505 | 3 | Defend |
| Chicago Metropolitan Agency for Planning | IL | Local ENT | Kent Hartsfield | Marcy Castro | Steffany Amador | $91K | 4 | reported | C | 40.0 | 0.5 | 0.44 | 4 | Maintain |
| Des Moines IA | IA | Local ENT | Tyler Carlson | Brooke Minichino | Steffany Amador | $90K | 5 | reported | B | 50.3 | 0.375 | 0.4518 | 4 | Maintain |
| Idaho Labor Department | ID | State | Scott Mark | Paige Wendle | Paige Wendle | $89K | 3 | reported | C | 42.3 | 0.625 | 0.5038 | 4 | Maintain |
| Kansas Insurance Department | KS | State | Matt Russell | Alejandro Solano | Alejandro Solano | $88K | 6 | reported | C | 44.1 | 0.25 | 0.3646 | 4 | Maintain |
| Allegheny County Treasurer Office | PA | Local ENT | Andrew Wyzkoski | Carolina Prieto | Halena Martin | $87K | 5 | reported | B | 57.9 | 0.375 | 0.4974 | 4 | Maintain |
| Colorado Department of Natural Resources | CO | State | Che Bustos | Alejandro Solano | Alejandro Solano | $86K | 2 | reported | C | 42.5 | 0.75 | 0.555 | 4 | Maintain |
| Louisiana Governor's Office of Homeland Security & Emergency Preparedness | LA | State | Demi Washington | Carolina Cambronero | Alejandro Solano | $86K | 3 | reported | C | 45.9 | 0.625 | 0.5254 | 4 | Maintain |
| Illinois Department of Financial and Professional Regulation | IL | State | Bill Pintsak | Marcy Castro | Steffany Amador | $76K | 3 | reported | B | 52.2 | 0.625 | 0.5632 | 4 | Maintain |
| Alabama Department of Education | AL | State | Sarah Duncan | Taylor Roman | Carolina Cambronero | $75K | 4 | reported | A | 58.4 | 0.5 | 0.5504 | 4 | Maintain |
| Outagamie County, WI | WI | Local ENT | Tyler Carlson | Carolina Prieto | Brooke Minichino | $75K | 6 | reported | C | 44.7 | 0.25 | 0.3682 | 4 | Maintain |
| Oregon Department of Corrections | OR | State | Todd Bowers | Paige Wendle | Paige Wendle | $73K | 4 | reported | C | 42.0 | 0.5 | 0.452 | 4 | Maintain |
| Jefferson County KY | KY | Local ENT | Carter Bradford | Andy O'Brien | Marcy Castro | $72K | 6 | reported | B | 49.1 | 0.25 | 0.3946 | 4 | Maintain |
| Missouri Department of Elementary and Secondary Education | MO | State | Bill Pintsak | Marcy Castro | Marcy Castro | $71K | 3 | reported | C | 42.3 | 0.625 | 0.5038 | 4 | Maintain |
| Connecticut Workers' Compensation Commission | CT | State | Stephanie DelSignore | Halena Martin | Halena Martin | $69K | 2 | reported | C | 40.5 | 0.75 | 0.543 | 4 | Maintain |
| Maine Department of Health & Human Services | ME | State | No State AE shown (ME) | Halena Martin | Halena Martin | $67K | 1 | reported | D | 26.9 | 0.875 | 0.5114 | 4 | Maintain |
| Oregon Housing and Community Services | OR | State | Todd Bowers | Paige Wendle | Paige Wendle | $64K | 2 | reported | C | 42.0 | 0.75 | 0.552 | 4 | Maintain |
| Kansas State Department of Education | KS | State | Matt Russell | Alejandro Solano | Alejandro Solano | $60K | 3 | reported | C | 44.1 | 0.625 | 0.5146 | 4 | Maintain |
| Montgomery, AL | AL | Local ENT | Spencer Ferrell | Taylor Roman | Carolina Cambronero | $58K | 5 | reported | B | 55.1 | 0.375 | 0.4806 | 4 | Maintain |
| Sarasota County/Clerk of the Circuit Court - FL | FL | Local ENT | Desmond Davis | Carolina Cambronero | (not in WIP) | $57K | 5 | reported | B | 57.8 | 0.375 | 0.4968 | 4 | Maintain |
| Colorado Department of Labor and Employment | CO | State | Che Bustos | Alejandro Solano | Alejandro Solano | $57K | 3 | reported | C | 42.5 | 0.625 | 0.505 | 4 | Maintain |
| Oregon Public Utility Commission | OR | State | Todd Bowers | Paige Wendle | Paige Wendle | $53K | 2 | reported | C | 42.0 | 0.75 | 0.552 | 4 | Maintain |
| Colorado Department of Corrections | CO | State | Che Bustos | Alejandro Solano | Alejandro Solano | $50K | 3 | reported | C | 42.5 | 0.625 | 0.505 | 4 | Maintain |
| Calcasieu Parish LA | LA | Local ENT | Austin Goodman | Alejandro Solano | Alejandro Solano | $50K | 3 | reported | C | 40.6 | 0.625 | 0.4936 | 4 | Maintain |
| Washington Military Department | WA | State | Todd Bowers | Paige Wendle | Paige Wendle | $47K | 2 | reported | D | 33.6 | 0.75 | 0.5016 | 4 | Maintain |
| North Collier Fire Control and Rescue District | FL | Local ENT | Bill Marshall | Taylor Roman | (not in WIP) | $43K | 5 | reported | B | 57.8 | 0.375 | 0.4968 | 4 | Maintain |
| Oregon Teacher Standards and Practices Commission | OR | State | Todd Bowers | Paige Wendle | Paige Wendle | $42K | 4 | reported | C | 42.0 | 0.5 | 0.452 | 4 | Maintain |
| Yuma County AZ | AZ | Local ENT | Stephen Allen | Cody Nichols | Cody Nichols | $38K | 5 | reported | B | 57.3 | 0.375 | 0.4938 | 4 | Maintain |
| Missouri State Treasurer | MO | State | Bill Pintsak | Marcy Castro | Marcy Castro | $29K | 3 | reported | C | 42.3 | 0.625 | 0.5038 | 4 | Maintain |
| Hillsborough County FL, Environmental Protection Commission | FL | Local ENT | Desmond Davis | Carolina Cambronero | (not in WIP) | $28K | 5 | reported | B | 57.8 | 0.375 | 0.4968 | 4 | Maintain |
| Missouri Public Service Commission | MO | State | Bill Pintsak | Marcy Castro | Marcy Castro | $27K | 3 | reported | C | 42.3 | 0.625 | 0.5038 | 4 | Maintain |
| Kentucky Office of Homeland Security | KY | State | State AE – KY/TN/AR | Andy O'Brien | Marcy Castro | $26K | 3 | reported | D | 34.7 | 0.625 | 0.4582 | 4 | Maintain |
| North Jersey Transportation Planning Authority | NJ | Local ENT | Andrew Wyzkoski | Halena Martin | (not in WIP) | $23K | 3 | reported | B | 54.0 | 0.625 | 0.574 | 4 | Maintain |
| Louisiana Attorney General (Justice Department) | LA | State | Demi Washington | Carolina Cambronero | Alejandro Solano | $23K | 0 | imputed | C | 45.9 | 0.75 | 0.5754 | 4 | Maintain |
| North Dakota Workforce Safety & Insurance | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $19K | 1 | reported | D | 34.7 | 0.875 | 0.5582 | 4 | Maintain |
| North Dakota Department of Health and Human Services | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $11K | 1 | reported | D | 34.7 | 0.875 | 0.5582 | 4 | Maintain |
| North Dakota Department of Commerce | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $4K | 1 | reported | D | 34.7 | 0.875 | 0.5582 | 4 | Maintain |
| North Dakota Retirement and Investment Office | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $4K | 1 | reported | D | 34.7 | 0.875 | 0.5582 | 4 | Maintain |
| Kentucky Energy & Environment Cabinet | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky General Government Cabinet | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky Justice and Public Safety Cabinet | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky Personnel Cabinet | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky Portal (Kentucky.gov) | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky Public Pensions Authority | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky Public Protection Cabinet | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| Kentucky Tourism, Arts and Heritage Cabinet | KY | State | State AE – KY/TN/AR | Carolina Prieto | Marcy Castro | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| North Dakota Department of Agriculture | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |
| North Dakota Ethics Commission | ND | State | Scott Mark | Carolina Prieto | Brooke Minichino | $0K | 0 | imputed | D | 34.7 | 0.75 | 0.5082 | 4 | Maintain |

---

## 7. Research digest (load-bearing facts only)

Full sourced reports live in the repo and are *not* inlined here (they are ~200k characters).
If you need primary sources, ask the user to also attach:
`research/state-fiscal-capacity-and-it-modernization-fy2026-fy2027.md`,
`research/govtech-grant-funding-landscape-2026.md`,
`research/govtech-state-demand-growth-2026.md`,
`research/granicus-market-and-competitive-landscape.md`.

Fiscal (NASBO Spring 2026): FY2027 median general-fund spending growth +0.6%, aggregate −1.4%;
23 states propose flat or declining spending; total balances down from $437B peak (FY2023) to
$274B recommended FY2027. RDF extremes: WY 70.3%, AK 51.7%; WA 2.8%, NJ 0.0%. Named funded
IT modernization is scarce (only ~14 states verified). FL HB 1197 adds Digital Service oversight
without money. MD taxes IT/data services at 3%.

Grants: SLFRF expenditure deadline 31 Dec 2026; ~$60B nominally unspent but essentially all
obligated. 53% of state and 67% of local SLFRF ran through revenue replacement, so tech spend
is invisible. GAO slow spenders (<50% as of 31 Mar 2025): MS, NJ, OK, SC, TN, WV. Digital Equity
Act mostly cancelled May 2025; SLCGP last funded cycle FY2025 $91.75M with 40% match.
Countervailing demand: ADA Title II WCAG 2.1 AA deadlines Apr 2027 / Apr 2028; Medicaid work
requirements by 1 Jan 2027 with 90% federal match on systems. Named local-tech grant programs:
MA Community Compact IT, NY LGRMIF, CO SIPA, FL local cyber $15M, MD Local Cybersecurity Support
Fund, NJ LEAP, VA VITA cyber with state match.

Demand (Census Vintage 2025, year to 1 Jul 2025): US population growth 1.78M vs 3.25M prior year,
almost entirely from collapsed international migration. Fastest %: SC +1.46, ID +1.44, NC +1.32,
TX +1.25, UT +1.03. CA −0.02% with −229k domestic. FL +0.85% but 91% of that is international.
Jurisdictions ≥100k (county+city, deduped): CA 112, TX 87, FL 63, NC 39, GA 36, NY 34, PA 34, OH 32.
FL Amendment 3 (Nov 2026, 60% threshold): local non-school property tax cut $4.93B FY2027-28 to
$11.83B by FY2031-32, $45.84B over five years, no state backfill, ~65% on county commissions.
TX committed $51B of 2026-27 budget to property tax relief.

Competitive: Granicus claims 7,000+ orgs, 48 of 50 largest US cities, 45% of top counties.
Independent .gov scan puts CivicPlus at 20.5% of reachable US gov websites vs Granicus 1.1%.
Documented statewide Granicus vehicles: NY GovQA (63 of 72 agencies), MI MiDEAL through 9/30/2027,
OK OMES SW1041C through Oct 2030. WA DES 01313 and MT MSA appear lapsed. Granicus has no found
state municipal-league endorsement; VC3 holds 11 endorsements across 10 states. ND: only 6 of 53
counties have full-time IT staff.

---

## 8. What is *not* in this briefing

- The four full research reports (attach separately if you want citations or to re-score).
- The 68 allocated $0 child records (they do not affect tiers; they do affect XP workload).
- Pipeline, win rates, NRR, or Granicus-wide install-base by state.
- Mid-market / SMB / federal books. Extending the model requires those exports.
- Any approved rebalance. The revised XP column in section 6 is a *capacity* rebalance, not a growth-tier rebalance.

## 9. Sensible next asks

These are things this context is already sufficient for:
1. Propose a growth-aware rebalance of the 13 ENT seats that preserves holds, cap, complex share, and TZ.
2. Design an XP1 vs XP3 book template from the Cody Nichols vs Marcy Castro contrast.
3. Produce a one-page exec brief or a talking deck outline.
4. Specify the schema needed to load the rest of the XP team and recompute whitespace.
5. Sensitivity: what happens to FL local if Amendment 3 passes; what happens to WA local if DES 01313 is dead.
6. Challenge or reweight the model, using the sub-score table in section 3.

