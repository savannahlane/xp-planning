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
