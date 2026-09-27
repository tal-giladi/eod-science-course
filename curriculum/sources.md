# Sources: textbooks, papers and official training resources

This page covers three deliverables: **recommended textbooks**, **academic papers** and
**official/public training resources**. It is a curated selection, not a full dump. It holds
the smallest set that covers every lesson in the
[course outline](curriculum/course-outline.md). The longer source lists, with notes on how each
item was checked, are in `research/01`–`04`. Standards are mapped in detail in
[references/standards.md](references/standards.md). A per-stage "read this first" list is in
[references/bibliography.md](references/bibliography.md).

**How to read the tables.** Every entry has a short **key** for citing it in lessons, for
example `[UFC-3-340-02]`. "Lessons" gives lesson ids. Lesson `NN.M` lives at
`lessons/stage-NN/lesson-0M.md`; `CS` means case studies and `C1`–`C4` are the capstones.
"Status" carries over the verification from the research files:

| Status | Meaning |
|---|---|
| **Verified** | The URL was fetched in Sept 2026 and the title and content matched. |
| **Verified (index)** | The title and URL were confirmed through the publisher, a catalogue or search indexes, but a direct fetch was blocked (403/login). Spot-check it in a browser. |
| **Unverified** | The citation details are provisional. |

**Access flags:** *free* free/public · *paid* paid or paywalled · *restricted* distribution-limited.

<div class="callout boundary">

**Safety filter applied to this list.** Everything here is read for science, effects,
protection, classification, sensing, robotics, decision-making or forensic *method*. Some
otherwise excellent texts also contain chapters on manufacture, formulation or operational
technique. Those chapters are marked **SKIP** in the entry and are also collected in the
[skip list](curriculum/sources.md?id=items-and-chapters-to-skip) at the end.

</div>

---

## Minimum reading path (13 items)

If you read nothing else, read these, in this order. Together they cover every stage.

| # | Key | Read | Stage(s) |
|---|---|---|---|
| 1 | [AJP-3.18] | Ch. 1 and the Lexicon. This gives you the vocabulary and the five EOD capability subsets. | 0, 3, 7 |
| 2 | [IMAS-04.10] | Skim it as a dictionary, then keep it open. | 0, 3, 5 |
| 3 | [MIT-2.26] | Lecture notes on conservation laws, normal shocks and shock tubes. | 1 |
| 4 | [Cooper-1996] | Parts 2–4: energetics, shock waves, detonation. | 1, 2 |
| 5 | [Glasstone-Dolan-1977] | Ch. III, §3.1–3.60 on blast-wave physics. | 1, 4 |
| 6 | [IATG-01.80] | Scaling laws, dynamic pressure, which blast fits to use and where they are valid. | 4 |
| 7 | [Baker-1983] | Ch. 2–4 and 6: blast loading, SDOF response, P–I diagrams, fragments. | 4 |
| 8 | [RAND-MR1608] | The whole summary and the per-technology chapters. | 5 |
| 9 | [CWA-14747-1] | How PoD and FAR are actually measured. | 5 |
| 10 | [Lynch-Park-2017] | Ch. 2–6: configuration space, rigid-body motion, kinematics, Jacobians. | 6 |
| 11 | [Chen-Haas-Barnes-2007] | The human factors of teleoperation. | 6, 7 |
| 12 | [Kochenderfer-2022] | Part I (Bayesian networks, utility, VOI) and Part IV (POMDPs). | 7, 9 |
| 13 | [NIJ-181869] | Post-blast investigation as a process model. | 8 |

Stretch item for Stage 9: [Angelopoulos-Bates-2021] on conformal prediction.

---

## 1. Textbooks

| Key | Title | Author / org | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [Cooper-1996] | *Explosives Engineering* | P. W. Cooper, Wiley-VCH | 1996 (reissue 2018) | https://www.wiley-vch.de/en/areas-interest/engineering/explosives-engineering-978-0-471-18636-6 | The best single engineering text. It covers thermochemistry, Rankine–Hugoniot, detonation, initiation *theory* and scaling, and it assumes calculus. **SKIP:** any composition or formulation material in Part 1, and any device or charge-design applications in Part 6. Read Part 6 only for scaling, blast and fragment physics. *paid* | 01.3, 01.5, 01.6, 02.1, 02.2, 04.1 | Verified |
| [Akhavan-2022] | *The Chemistry of Explosives*, 4th ed. | J. Akhavan, Royal Society of Chemistry | 2022 | https://books.rsc.org/books/monograph/944/The-Chemistry-of-Explosives | Short conceptual chemistry: classification, combustion vs deflagration vs detonation, thermal decomposition, thermochemistry, kinetics. **SKIP Ch. 7 (manufacture)** entirely. *paid* | 02.1, 02.2, 02.3 | Verified |
| [Anderson-2021] | *Modern Compressible Flow*, 4th ed. | J. D. Anderson Jr., McGraw-Hill | 2021 | https://www.mheducation.com/highered/product/modern-compressible-flow-with-historical-perspective-anderson.html | The standard text. Ch. 3 covers 1-D flow and normal shocks; Ch. 7 covers moving shocks and the shock tube. *paid* | 01.2, 01.3, 01.4 | Verified |
| [Fickett-Davis-2000] | *Detonation: Theory and Experiment* | W. Fickett, W. C. Davis, Dover | 2000 (orig. 1979) | https://www.amazon.com/dp/0486414566 | Rigorous CJ and ZND theory and detonation-front instability. A graduate-level reference, not a first read. Inexpensive Dover reprint. *paid* | 02.2 | Verified (index) |
| [Kinney-Graham-1985] | *Explosive Shocks in Air*, 2nd ed. | G. F. Kinney, K. J. Graham, Springer | 1985 | https://link.springer.com/book/10.1007/978-3-642-86682-1 | A compact account of free-air blast. It is the source of the Kinney–Graham overpressure fit, and it also covers scaling, confined explosions and loads. *paid* | 01.5, 04.1, 04.2 | Verified (index) |
| [Baker-1983] | *Explosion Hazards and Evaluation* | W. E. Baker, P. A. Cox, P. S. Westine, J. J. Kulesz, R. A. Strehlow, Elsevier | 1983 | https://shop.elsevier.com/books/explosion-hazards-and-evaluation/baker/978-0-444-42094-7 | The best single blast-effects book. It covers free-field blast, loading, SDOF and P–I, fragments (Ch. 6, including Mott statistics), thermal effects and damage criteria. *paid* | 01.6, 04.1–04.4 | Verified |
| [Daniels-2004] | *Ground Penetrating Radar*, 2nd ed. | D. J. Daniels, IET | 2004 | https://shop.theiet.org/ground-penetrating-radar-2-ed | The standard GPR engineering text: propagation in lossy soil, antennas, clutter, A/B/C-scans, and a mine-detection chapter. *paid* | 05.2 | Verified (index) |
| [Beveridge-2012] | *Forensic Investigation of Explosions*, 2nd ed. | A. Beveridge (ed.), CRC Press | 2012 | https://www.routledge.com/Forensic-Investigation-of-Explosions/Beveridge/p/book/9780367778200 | The definitive multi-author text on scene work, residue analysis and casework management. **SKIP** any device-reconstruction detail beyond the situation level. *paid* | 08.1–08.3, CS | Verified |
| [Macmillan-Creelman-2005] | *Detection Theory: A User's Guide*, 2nd ed. (3rd ed. 2022 with Hautus) | N. A. Macmillan, C. D. Creelman, Psychology Press | 2005 | https://archive.org/details/detectiontheoryu0000macm | Signal detection theory done properly: d′, criterion, ROC shape, and multi-detector designs. Borrowable library copy. *paid* | 05.1, 05.6, 09.1 | Verified (index) |
| [Koopman-1946] | *Search and Screening* (OEG Report 56) | B. O. Koopman, US Navy Operations Evaluation Group | 1946 | https://archive.org/details/searchscreening56koop | The origin of sweep width, the random-search formula and optimal effort allocation. Public domain. For rigour, go on to L. D. Stone, *Theory of Optimal Search* (Academic Press 1975, *paid*). *free* | 05.7 | Verified (index) |
| [Lynch-Park-2017] | *Modern Robotics: Mechanics, Planning, and Control* | K. M. Lynch, F. C. Park, Cambridge UP | 2017 | https://hades.mech.northwestern.edu/index.php/Modern_Robotics | Screw theory, PoE kinematics, Jacobians, dynamics, planning and control. Free preprint and videos. *free* | 06.2, 06.3, 06.4, 06.8 | Verified |
| [Thrun-2005] | *Probabilistic Robotics* | S. Thrun, W. Burgard, D. Fox, MIT Press | 2005 | https://mitpress.mit.edu/9780262201629/probabilistic-robotics/ | Bayes filter, EKF/UKF, particle filters, MCL, occupancy grids, SLAM. *paid* | 05.6, 06.6, 06.7 | Verified (index) |
| [Barfoot-2024] | *State Estimation for Robotics*, 2nd ed. | T. D. Barfoot, Cambridge UP | 2024 | https://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser24.pdf | Batch and recursive estimation, and Lie groups SO(3)/SE(3) done properly. Free PDF. *free* | 06.2, 06.6, 06.7 | Verified |
| [LaValle-2006] | *Planning Algorithms* | S. M. LaValle, Cambridge UP | 2006 | https://lavalle.pl/planning/ | C-space, sampling-based planning (RRT/PRM), and planning under uncertainty. Free. *free* | 06.8, 09.5 | Verified |
| [Szeliski-2022] | *Computer Vision: Algorithms and Applications*, 2nd ed. | R. Szeliski | 2022 | https://szeliski.org/Book/ | Camera models, calibration, structure-from-motion/photogrammetry, detection and deep learning. Free PDF (registration). *free* | 08.2, 09.1, 09.4 | Verified |
| [Murphy-2014] | *Disaster Robotics* | R. R. Murphy, MIT Press | 2014 | https://direct.mit.edu/books/monograph/3408/Disaster-Robotics | Analysis of 34 real deployments: failure modes, the two-person operator rule, comms loss. The closest civilian analogue to EOD robotics. *paid* | 06.1, 06.5, 06.9, C1 | Verified (index) |
| [Kochenderfer-2022] | *Algorithms for Decision Making* | M. J. Kochenderfer, T. A. Wheeler, K. H. Wray, MIT Press | 2022 | https://algorithmsbook.com/ | Bayesian networks, utility, VOI, MDPs, POMDPs and belief-state planning, with code. Free PDF. *free* | 05.6, 07.1, 09.5, C4 | Verified |
| [Rappaport-2002] | *Wireless Communications: Principles and Practice*, 2nd ed. (reissued by Cambridge UP) | T. S. Rappaport | 2002 | https://www.oreilly.com/library/view/wireless-communications-principles/0130422320/ | Free-space and log-distance path loss, Fresnel-zone geometry, fading, link-budget design. *paid* | 01.7, 06.9 | Verified (index) |

---

## 2. Government / official documents and standards

Scope and course usage for each standard are mapped in more detail in
[references/standards.md](references/standards.md).

### 2a. Doctrine, mine action and ammunition management

| Key | Title | Author / org | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [AJP-3.18] | AJP-3.18 Ed. B v1, *Allied Joint Doctrine for EOD Support to Operations* (ratified via STANAG 2628) | NATO Standardization Office (UK MOD copy) | Sept 2023 | https://assets.publishing.service.gov.uk/media/65d48f3f38fef90011b5b03b/AJP_3_18_EOD_EdB_V1.pdf | The five EOD capability subsets (EOR, EO clearance, CMD, IEDD, CBRN EOD), operating domains, C2, the C-IED linkage and a Lexicon. *free* | 00.1, 00.2, 03.1, 03.4, 07.2 | Verified |
| [IMAS-04.10] | IMAS 04.10 *Glossary of mine action terms, definitions and abbreviations*, Ed. 2 Amdt 13 | UNMAS / GICHD | 16 Jun 2026 | https://www.mineactionstandards.org/standards/04-10/ | The authoritative definitions of EO, UXO, AXO, ERW, land release, NTS/TS and more. The [glossary](references/glossary.md) follows it. *free* | 00.1, 03.1, 05.7 | Verified |
| [IMAS-07.11] | IMAS 07.11 *Land release*, Ed. 2 | UNMAS / GICHD | 16 Jan 2026 | https://www.mineactionstandards.org/standards/07-11/ | Cancelled / reduced / cleared land, "all reasonable effort", and evidence-based survey. Read it with IMAS 09.10 *Clearance requirements* (Ed. 2 Amdt 6, 2020; https://www.mineactionstandards.org/standards/09-10/, Verified), which defines "cleared" to a specified depth. *free* | 05.7, 07.1 | Verified |
| [IMAS-07.40] | IMAS 07.40 *Monitoring of mine action organisations*, Ed. 2 (replaces the withdrawn IMAS 09.20 on post-clearance inspection) | UNMAS / GICHD | 20 Jan 2016 | https://www.mineactionstandards.org/standards/07-40/ | Quality monitoring and sampling inspection of cleared land. *free* | 05.7 | Verified (index) |
| [IMAS-09.30] | IMAS 09.30 *Explosive Ordnance Disposal* | UNMAS / GICHD | Amdt Sept 2022 | https://www.mineactionstandards.org/standards/09-30/ | EOD Levels 1–3+. Use it for the *organisational* ladder only. *free* | 00.2 | Verified |
| [TEP-09.30] | T&EP 09.30/01/2022 *Conventional EOD Competency Standards*, Ed. 2 | UNMAS / GICHD | 22 Feb 2022 | https://www.mineactionstandards.org/standards/09-30-01-2022/ | Competency categories, clusters and levels. It is a model for the course's own skill map. Read the structure, not the practical competencies. *free* | 00.2 | Verified |
| [TEP-09.31] | T&EP 09.31/01 *IEDD Competency Standards* (Amdt 1) | UNMAS / GICHD | 22 Feb 2022 | https://www.mineactionstandards.org/standards/09-31-01-2019/ | The IEDD role ladder and competency categories. *free* | 00.2, 03.4 | Verified |
| [UN-IEDD-2018] | *United Nations Improvised Explosive Device Disposal Standards* | UNMAS / DPKO / DFS | May 2018 | https://unmas.org/sites/default/files/un_iedd_standards.pdf | IEDD roles, threat assessment at national, area and scene level, and principles. Read the organisational and principles chapters. *free* | 03.4, 07.2 | Verified |
| [IATG-01.50] | IATG 01.50 *UN explosive hazard classification system and codes*, 3rd ed. | UNODA / UN SaferGuard | Mar 2021 | https://data.unsaferguard.org/iatg/en/IATG-01.50-Explosive-hazard-classification-system-IATG-V.3.pdf | HD 1.1–1.6 and compatibility groups, with examples. **The primary source for 02.3.** *free* | 02.3, 03.1 | Verified |
| [IATG-01.80] | IATG 01.80 *Formulae for ammunition management*, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/IATG-01.80-Formulae-ammunition-management-IATG-V.3.pdf | Hopkinson–Cranz, Sachs, dynamic pressure, reflection vs angle, and the validity ranges of K-B (Z ≤ 40) and K-G (Z ≤ 500). *free* | 01.5, 04.1, 04.2, 04.4 | Verified |
| [IATG-02.10] | IATG 02.10 *Introduction to risk management principles and processes*, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/V3_IATG-02.10_en.pdf | Risk framing: tolerable risk and ALARP-style reasoning. *free* | 04.3, 07.1 | Verified |
| [IATG-02.20] | IATG 02.20 *Quantity and separation distances*, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/V3_IATG-02.20_en.pdf | QD concepts (IMD, IBD, PTRD), all as Z·W^(1/3). *free* | 04.3, 04.4 | Verified |
| [IATG-07.10] | IATG 07.10 *Surveillance and in-service proof*, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/IATG-07.10-Surveillance-proof-IATG-V.3.pdf | Ageing: propellant chemical stability and stabiliser depletion (§13, §15). **The primary source for the ageing part of 02.3.** *free* | 02.3, 03.3 | Verified |
| [DESR-6055.09] | DESR 6055.09 *Defense Explosives Safety Regulation*, Ed. 1 Change 2 | USD(A&S) / DDESB | 25 Nov 2025 | https://www.denix.osd.mil/ddes/denix-files/sites/32/2022/08/DESR-6055.09-Edition1-Change-2-251208.pdf | US hazard classification and QD tables, cleared for public release. Read V1 (classification) and V3 (QD concepts). *free* | 02.3, 04.3 | Verified |
| [UN-MTC-Rev8] | *UN Manual of Tests and Criteria*, Rev. 8 (+ Amdt 1 2025); read with the *UN Model Regulations* Rev. 24, Part 2 Ch. 2.1 (https://unece.org/transport/dangerous-goods/un-model-regulations-rev-24) | UNECE | 2023 / 2025 | https://unece.org/transport/publications/un-manual-tests-and-criteria-rev8-2023 | Shows how the Class 1 test series feed into hazard-division assignment; the Model Regulations give the authoritative division and compatibility-group definitions. Read Part I for the *concepts* and **SKIP the test procedures**. *free* | 02.3 | Verified (index) |
| [MIL-STD-1316F] | MIL-STD-1316F *Fuze Design Safety — Design Criteria* | US DoD | 18 Aug 2017 | https://everyspec.com/MIL-STD/MIL-STD-1300-1399/MIL-STD-1316F_55755/ | The public statement of fuze-safety *principles*: at least two independent safety features, arming stimuli drawn from different environments. This is the basis of 03.2's safety-and-arming state-machine abstraction. **Read the general-requirements section only; SKIP everything else.** *free* | 03.2 | Verified (index) |

### 2b. Blast effects and public safety

| Key | Title | Author / org | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [UFC-3-340-02] | UFC 3-340-02 *Structures to Resist the Effects of Accidental Explosions* (Change 2) | US DoD (USACE / NAVFAC / AFCEC) | 2008, Ch. 2 2014 | https://www.wbdg.org/dod/ufc/ufc-3-340-02 | "Approved for public release." Ch. 2 is the public route to the Kingery–Bulmash curves, whose original, ARBRL-TR-02555 (AD-B082713), is *restricted* distribution-limited, so do not plan on getting it. Ch. 3 covers SDOF. Read it as a book of curves, not a design exercise. *free* | 04.1–04.3 | Verified (mirror) |
| [Glasstone-Dolan-1977] | *The Effects of Nuclear Weapons*, 3rd ed., Ch. III "Air Blast Phenomena" | S. Glasstone, P. J. Dolan, US DoD / DOE | 1977 | https://atomicarchive.com/resources/documents/effects/glasstone-dolan/chapter3.html | Public-domain, very readable blast-wave physics: Rankine–Hugoniot for air, dynamic pressure, reflection (§3.53–3.56). Use it for the physics only. *free* | 01.3, 01.4, 04.1, 04.2 | Verified |
| [DHS-DOJ-Standoff] | DHS-DOJ *Bomb Threat Stand-Off Card* | CISA / DOJ / FBI | Aug 2025 | https://www.cisa.gov/resources-tools/resources/dhs-doj-bomb-threat-stand-card | A published public-safety table of evacuation and shelter distances. Use it as a worked example linking TNT-equivalent mass to distance through Z. *free* | 04.4, 07.2 | Verified |
| [NIMS-2017] | *National Incident Management System*, 3rd ed. | FEMA | Oct 2017 | https://training.fema.gov/emiweb/is/is700b/handouts/national_incident_management%20system_third%20edition_october_2017.pdf | ICS, unified command and span of control. This is the command interface a bomb squad plugs into. *free* | 00.2, 07.2 | Verified (index) |
| [NASA-FTA-2002] | *Fault Tree Handbook with Aerospace Applications*, v1.1 | M. Stamatelatos, W. Vesely et al., NASA | Aug 2002 | https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Fault%20Tree%20Handbook_NASA.pdf | Fault trees, minimal cut sets and quantification. The reliability maths in 06.9 follows it. *free* | 06.9, 03.2 | Verified (index) |

### 2c. Detection: technology surveys and test standards

| Key | Title | Author / org | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [RAND-MR1608] | *Alternatives for Landmine Detection* | J. MacDonald, J. R. Lockwood et al., RAND (for OSTP) | 2003 | https://www.rand.org/pubs/monograph_reports/MR1608.html | The best single survey of detection technologies (EMI, GPR, IR, acoustic, NQR, neutron, backscatter, vapour, fusion), framed around the Pd-vs-FAR trade-off. *free* | 05.1–05.6 | Verified |
| [CWA-14747-1] | CWA 14747-1:2003 *Humanitarian Mine Action — Test and Evaluation — Metal Detectors* (Part 2, 2008, covers soil characterisation, *paid*) | CEN WS7 / EC JRC | May 2003 | https://www.mineactionstandards.org/standards/07-05-2003/ | The canonical blind-trial protocol for measuring PoD and FAR. It separates intrinsic capability from environment and operator. *free* | 05.1, 05.2, 09.6 | Verified |
| [GICHD-GMA-2014] | *A Guide to Mine Action*, 5th ed. | GICHD | Mar 2014 | https://www.gichd.org/fileadmin/uploads/gichd/Media/GICHD-resources/rec-documents/Guide-to-mine-action-2014.pdf | System context: survey, land release, clearance, quality management and IMSMA. *free* | 00.1, 03.3, 05.7 | Verified |
| [NRC-mmW-2007] | *Assessment of Millimeter-Wave and Terahertz Technology for Detection and Identification of Concealed Explosives and Weapons* | National Research Council | 2007 | https://www.nationalacademies.org/read/11826/chapter/1 | mmW/THz phenomenology, component maturity and deployment. *free* | 05.5 | Verified |
| [NRC-MS-2004] | *Opportunities to Improve Airport Passenger Screening with Mass Spectrometry* | National Research Council | 2004 | https://www.nationalacademies.org/read/10996/chapter/1 | The limits of trace detection: sampling, IMS selectivity and false alarms. A case study in requirements vs sensor capability. *free* | 05.4 | Verified |
| [IAEA-2012] | *Neutron Generators for Analytical Purposes* (Radiation Technology Reports No. 1) | IAEA | 2012 | https://www-pub.iaea.org/MTCD/Publications/PDF/P1535_web.pdf | Neutron sources and interrogation concepts (TNA, FNA, PFTNA, associated-particle imaging) for elemental signatures. *free* | 05.3 | Verified |

### 2d. Forensics

| Key | Title | Author / org | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [NIJ-181869] | *A Guide for Explosion and Bombing Scene Investigation* (NCJ 181869) | NIJ Technical Working Group | Jun 2000 | https://www.ojp.gov/pdffiles1/nij/181869.pdf | The investigative workflow as a process model: response, evaluation, documentation, evidence, completion. *free* | 08.1 | Verified |
| [NFPA-921] | NFPA 921 *Guide for Fire and Explosion Investigations*, 2024 ed. | NFPA | 2024 | https://www.nfpa.org/product/nfpa-921-guide-for-fire-and-explosion-investigations/p0921code/nfpa-921-guide-for-fire-and-explosion-investigations-2024/92124 | The scientific method for origin and cause. The explosions chapter covers seat analysis and damage indicators; the 2024 edition adds guidance on confirmation bias. *paid* (free read-only access with an NFPA account) | 08.1, 08.2 | Verified (index) |
| [TWGFEX-PB] | *Recommended Guidelines for Forensic Identification of Post-Blast Explosive Residues* | TWGFEX (hosted by NIST) | c. 2007 (hosted 2018) | https://www.nist.gov/document/twgfexrecommendedguidelinesfortheforensicidentificationofpost-blastexplosiveresiduespdf | Analytical methods ranked by how much identifying information they give, and the requirement for orthogonal methods. *free* | 08.3 | Verified |
| [ASTM-E3253] | ANSI/ASTM E3253-21 *Examination Scheme for Intact Explosives* (OSAC Registry); see also ASTM E2998 on smokeless powder (https://www.nist.gov/osac/standards-library/ansiastm-e2998-25a) | ASTM E30 / OSAC | 2021 | https://www.nist.gov/osac/standards-library/ansiastm-e3253-21 | The current consensus lab standard that succeeds TWGFEX. OSAC summary *free*; the standard itself *paid*. | 08.3 | Verified |
| [NIJ-252954] | *Post-Blast Investigative Tools for Structural Forensics by 3D Scene Reconstruction and Advanced Simulation* | M. Whelan, D. Weggel (UNC Charlotte), NIJ | May 2019 | https://www.ojp.gov/library/publications/post-blast-investigative-tools-structural-forensics-3d-scene-reconstruction | Photogrammetry and scanning combined with simulation to infer blast parameters from damage. This is the model for 08.2. *free* | 08.2 | Verified |

### 2e. Robot test methods

| Key | Title | Author / org | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [NIST-RRTM] | *Standard Test Methods for Response Robots* (ASTM E54.09) | NIST Intelligent Systems Division | ongoing | https://www.nist.gov/el/intelligent-systems-division-73500/standard-test-methods-response-robots | Reproducible tests for mobility, dexterity, sensors, energy, comms and operator proficiency. The dexterity-and-strength test methods (2021A, https://www.nist.gov/document/astm-e5409-ground-test-methods-dexterity-and-strength-2021a) map onto EOD arm tasks. The companion *C-IED Training Using Standard Test Methods* (2015) is at https://www.nist.gov/document/c-ied-training-using-standard-test-methods-response-robots-v2015pdf. NIST documents *free*; the ASTM standards themselves *paid*. | 06.1, 06.3, 06.9, C1 | Verified |

---

## 3. University courses

| Key | Course | Org | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|
| [MIT-2.26] | 2.26 *Compressible Fluid Dynamics* (notes, problem sets) | MIT OCW (A. E. Hosoi), 2004 | https://ocw.mit.edu/courses/2-26-compressible-fluid-dynamics-spring-2004/ | The best free spine for Stage 1: conservation laws, shocks, Riemann invariants and shock tubes. *free* | 01.2–01.5 | Verified |
| [Caltech-Ae103] | *Detonation Waves and Pulse Detonation Engines* (lecture slides) | E. Wintenberger, J. E. Shepherd, Caltech, 2004 | https://shepherd.caltech.edu/EDL/projects/pde/Ae103-012704.pdf | Hugoniot, Rayleigh line and the CJ condition derived from conservation laws. A good first exposure. *free* | 02.2 | Verified |
| [NMT-EXPL] | Graduate Certificate in Explosives Engineering (MENG 545/546/549/555) | New Mexico Tech / EMRTC | https://catalog.nmt.edu/programs/NuVJx0lzgRRTomVJ0ci1 | The closest academic analogue to the Stage 1→2→4 progression. Use it as a syllabus model. Comparable programmes: Missouri S&T MS Explosives Engineering (https://catalog.mst.edu/graduate/courselist/exp-eng/) and Cranfield MSc Explosives Ordnance Engineering (https://www.cranfield.ac.uk/courses/taught/explosives-ordnance-engineering); their blasting and demolition courses are out of scope here. | 00.2, Stage 1, 2, 4 | Verified |
| [Coursera-MR] | *Modern Robotics* specialisation (6 courses) | Northwestern / Coursera (K. Lynch) | https://www.coursera.org/specializations/modernrobotics | Video companion to [Lynch-Park-2017]. The mobile-manipulation capstone is very close to an EOD UGV with an arm. *free* (audit) | 06.2–06.4, 06.8, C1 | Verified |

---

## 4. Peer-reviewed papers

### 4a. Blast, injury, ageing

| Key | Title | Authors / venue | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [Rigby-2014] | The Negative Phase of the Blast Load | S. E. Rigby, A. Tyas, T. Bennett, S. D. Clarke, S. D. Fay; *Int. J. Protective Structures* 5(1) | 2014 | https://eprints.whiterose.ac.uk/id/eprint/78295/ | Modified Friedlander equation, Hopkinson–Cranz scaling, positive and negative phase, SDOF. The course's Friedlander citation (after Friedlander 1946, *Proc. R. Soc. A* 186:322, DOI 10.1098/rspa.1946.0046). *free* | 04.1, 01.6 | Verified |
| [Isaac-2023] | Blast wave interaction with structures – an overview | O. S. Isaac et al.; *IJPS* 14(4) | 2023 | https://eprints.whiterose.ac.uk/192170/ | Reflection, clearing, diffraction and barriers. The best single review for Stage 4 (CC-BY). *free* | 01.4, 04.2, 04.3 | Verified |
| [Farrimond-2024] | Far-field positive phase blast parameter characterisation of RDX and PETN based explosives | D. G. Farrimond et al.; *IJPS* 15(1) | 2024 | https://eprints.whiterose.ac.uk/id/eprint/195373/ | Tests Kingery–Bulmash against arena data and asks whether blast is deterministic. It teaches healthy scepticism of empirical curves (CC-BY). *free* | 04.1, 04.2 | Verified |
| [Champion-2009] | Injuries from explosions: physics, biophysics, pathology, and required research focus | H. R. Champion, J. B. Holcomb, L. A. Young; *J. Trauma* 66(5) | 2009 | https://pubmed.ncbi.nlm.nih.gov/19430256/ | The standard review of primary to quaternary blast injury, with the physics explained for non-clinicians. A free copy is on DTIC (ADA627553). | 04.4 | Verified (index) |
| [Boutillier-2015] | Primary blast injury on thorax: a critical review of the studies and their outcomes | J. Boutillier et al.; IRCOBI Conf. | 2015 | https://www.ircobi.org/wordpress/downloads/irc15/pdf_files/77.pdf | A critical review of the Bowen curves (DASA-2113, 1968) and the Axelsson and Stuhmiller models, including their limits. *free* | 04.4 | Verified |
| [Rusly-2024] | Stabilizer selection and formulation strategies for enhanced stability of single base nitrocellulose propellants: a review | S. N. A. Rusly et al.; *Energetic Materials Frontiers* 5(1) | 2024 | https://www.sciencedirect.com/science/article/pii/S2666647224000083 | The chemistry of why stabiliser depletion makes old propellant dangerous. **Read the decomposition and ageing sections only; SKIP the formulation discussion.** *free* | 02.3, 03.3 | Verified (index) |

### 4b. Detection and fusion

| Key | Title | Authors / venue | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [Fawcett-2006] | An introduction to ROC analysis | T. Fawcett; *Pattern Recognition Letters* 27(8):861–874 | 2006 | https://dl.acm.org/doi/10.1016/j.patrec.2005.10.010 | ROC space, AUC, cost- and base-rate-dependent operating points, and averaging. | 05.1, 09.1 | Verified (index) |
| [Wells-Bradley-2012] | A review of X-ray explosives detection techniques for checked baggage | K. Wells, D. A. Bradley; *Appl. Radiat. Isot.* 70(8) | 2012 | https://openresearch.surrey.ac.uk/view/pdfCoverPage?instCode=44SUR_INST&filePid=13140530670002346&download=true | Transmission, dual-energy (effective Z), CT, backscatter and diffraction physics. *free* | 05.3 | Verified |
| [Furton-Myers-2001] | The scientific foundation and efficacy of the use of canines as chemical detectors for explosives | K. G. Furton, L. J. Myers; *Talanta* 54(3) | 2001 | https://www.sciencedirect.com/science/article/abs/pii/S0039914000005464 | Vapour pressure, odour signatures, and canine reliability compared with instruments. *paid* | 05.4 | Verified (index) |
| [Sabatier-2006] | Advances in Acoustic Landmine Detection (RTO-MP-SET-107-05) | J. M. Sabatier; NATO RTO | c. 2006 | https://publications.sto.nato.int/publications/STO%20Meeting%20Proceedings/RTO-MP-SET-107/MP-SET-107-05.pdf | Acoustic-to-seismic coupling and vibrometry, with fused-sensor results. *free* | 05.5 | Verified |
| [Bruschini-Gros-1998] | A Survey of Research on Sensor Technology for Landmine Detection | C. Bruschini, B. Gros; *J. Humanitarian Demining* 2(1) | 1998 | https://commons.lib.jmu.edu/cisr-journal/vol2/iss1/3/ | Makes the case that no single sensor meets the humanitarian clearance requirement, and therefore fusion is needed. *free* | 05.6 | Verified |
| [Akcay-Breckon-2020] | Towards Automatic Threat Detection: A Survey of Advances of Deep Learning within X-ray Security Imaging | S. Akcay, T. Breckon; *Pattern Recognition* (arXiv 2001.01293) | 2020 | https://arxiv.org/abs/2001.01293 | Datasets, detection on 2D and CT imagery, and evaluation pitfalls. *free* | 05.3, 09.1 | Verified |
| [Moalla-2020] | Application of Convolutional and Recurrent Neural Networks for Buried Threat Detection Using GPR Data | M. Moalla, H. Frigui et al.; *IEEE TGRS* 58(10) | 2020 | https://ieeexplore.ieee.org/document/9047150/ | CNN+RNN on B-scans and 3-D GPR volumes, trained on 120,000 m² of real data. *paid* | 05.2, 09.1 | Verified (index) |
| [Baur-2020] | Applying Deep Learning to Automate UAV-Based Detection of Scatterable Landmines | J. Baur et al.; *Remote Sensing* 12(5):859 | 2020 | https://www.mdpi.com/2072-4292/12/5/859 | UAV RGB and thermal imagery with a CNN detector. A seminal paper. Practitioner version: *JCWD* 25(1), https://commons.lib.jmu.edu/cisr-journal/vol25/iss1/29/ (Verified). *free* | 05.5, 09.1, 09.4 | Verified (index) |

### 4c. Teleoperation, human factors, estimation, robots

| Key | Title | Authors / venue | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [Yamauchi-2004] | PackBot: a versatile platform for military robotics | B. M. Yamauchi; *Proc. SPIE* 5422 | 2004 | https://doi.org/10.1117/12.538328 | The canonical EOD-class UGV design paper: flippers, modular payload bus. *paid* | 06.1, 06.4 | Verified (index) |
| [Chen-Haas-Barnes-2007] | Human Performance Issues and User Interface Design for Teleoperated Robots | J. Y. C. Chen, E. C. Haas, M. J. Barnes; *IEEE Trans. SMC-C* 37(6) | 2007 | https://doi.org/10.1109/TSMCC.2007.905819 | A review of 150+ studies on bandwidth, latency, frame rate, FOV and frame of reference. *paid* | 06.5 | Verified (index) |
| [Farajiparvar-2020] | A Brief Survey of Telerobotic Time Delay Mitigation | P. Farajiparvar, H. Ying, A. Pandya; *Frontiers in Robotics and AI* | 2020 | https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2020.578805/full | Predictive, supervisory and passivity control, and ML-based prediction. The move-and-wait strategy goes back to Ferrell 1965, *IEEE Trans. HFE* 6 (https://ntrs.nasa.gov/citations/19660064449). For haptics maths, go on to Hokayem & Spong 2006, *Automatica* 42(12). *free* | 06.5 | Verified |
| [Parasuraman-2000] | A model for types and levels of human interaction with automation | R. Parasuraman, T. B. Sheridan, C. D. Wickens; *IEEE Trans. SMC-A* 30(3) | 2000 | https://doi.org/10.1109/3468.844354 | Four stages × ten levels of automation. It frames what an EOD robot should automate. For the underlying supervisory-control model, see Sheridan, *Telerobotics, Automation, and Human Supervisory Control* (MIT Press 1992, https://archive.org/details/teleroboticsauto0000sher). *paid* | 06.5, 09.6, C4 | Verified (index) |
| [Endsley-1995] | Toward a Theory of Situation Awareness in Dynamic Systems | M. R. Endsley; *Human Factors* 37(1) | 1995 | https://journals.sagepub.com/doi/10.1518/001872095779049543 | The three-level SA model, used as the basis for OCU design and evaluation. *paid* | 06.5, 07.1, 07.2 | Verified (index) |
| [Durrant-Whyte-Bailey-2006] | Simultaneous Localization and Mapping: Part I (Part II in 13(3)) | H. Durrant-Whyte, T. Bailey; *IEEE RAM* 13(2) | 2006 | https://doi.org/10.1109/MRA.2006.1638022 | The standard SLAM tutorial pair. *paid* | 06.7 | Verified (index) |
| [Chung-2023] | Into the Robotic Depths: Analysis and Insights from the DARPA Subterranean Challenge | T. H. Chung, V. Orekhov, A. Maio; *Annu. Rev. Control Robot. Auton. Syst.* | 2023 | https://www.annualreviews.org/content/journals/10.1146/annurev-control-062722-100728 | Comms-denied autonomy and single-operator multi-robot lessons. Winning system paper: Tranzatto et al. 2022, https://arxiv.org/abs/2207.04914 (Verified). SSRN mirror *free*. | 06.9, 09.5, C1 | Verified (index) |

### 4d. Machine learning methods

| Key | Title | Authors / venue | Date | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|---|
| [Guo-2017] | On Calibration of Modern Neural Networks | C. Guo, G. Pleiss, Y. Sun, K. Q. Weinberger; ICML | 2017 | https://arxiv.org/abs/1706.04599 | ECE and temperature scaling. Required before showing any confidence value to an operator. *free* | 09.2 | Verified |
| [Lakshminarayanan-2017] | Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles | B. Lakshminarayanan, A. Pritzel, C. Blundell; NeurIPS | 2017 | https://arxiv.org/abs/1612.01474 | Deep ensembles: the strong OOD baseline. Compare with MC dropout (Gal & Ghahramani, ICML 2016, https://arxiv.org/abs/1506.02142, Verified). *free* | 09.2 | Verified |
| [Angelopoulos-Bates-2021] | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | A. N. Angelopoulos, S. Bates | 2021 | https://arxiv.org/abs/2107.07511 | Prediction sets with guaranteed coverage, which fits "miss rate ≤ α" requirements. Code: https://github.com/aangelopoulos/conformal-prediction. *free* | 09.2, 09.6, C4 | Verified |
| [Tobin-2017] | Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | J. Tobin et al.; IROS | 2017 | https://arxiv.org/abs/1703.06907 | Justifies synthetic ordnance imagery when real data is scarce or restricted. *free* | 09.3 | Verified |
| [Eykholt-2018] | Robust Physical-World Attacks on Deep Learning Models | K. Eykholt et al.; CVPR | 2018 | https://arxiv.org/abs/1707.08945 | Physical adversarial examples and a method for lab-vs-field evaluation. *free* | 09.6 | Verified |
| [Bajcsy-2018] | Revisiting Active Perception | R. Bajcsy, Y. Aloimonos, J. K. Tsotsos; *Autonomous Robots* 42(2) | 2018 | https://doi.org/10.1007/s10514-017-9615-3 | Choosing sensing actions to reduce uncertainty. The conceptual core of 09.5. *paid* | 09.5 | Verified (index) |

---

## 5. Datasets and software documentation

| Key | Resource | Org | URL | Why useful | Lessons | Status |
|---|---|---|---|---|---|---|
| [SDToolbox] | Shock & Detonation Toolbox + GALCIT FM2018.001 theory report | Caltech EDL (J. E. Shepherd et al.), rev. 2023 / sw. 2025 | https://shepherd.caltech.edu/EDL/PublicResources/sdt/ | Python/Cantera code for shock jumps, CJ speed and ZND structure. Gas-phase only (e.g., H₂–O₂), which suits the safety boundary. *free* | 01.3, 02.2 | Verified |
| [UNSG-KB-calc] | Kingery–Bulmash blast calculator | UN SaferGuard | https://unsaferguard.org/un-saferguard/kingery-bulmash | The public route to K-B values for checking code. Valid for Z ≤ 40. *free* | 04.1, 04.2 | Verified (index) |
| [AMLID-2025] | AMLID: Adaptive Multispectral Landmine Identification Dataset | J. E. Gallagher, E. J. Oughton, arXiv 2512.18738 | https://arxiv.org/abs/2512.18738 | 12,078 labelled RGB+LWIR images across seasons and altitudes. The best capstone dataset. Preprint. *free* | 09.1, 09.4, C1 | Verified |
| [RIT-HSI-2025] | UAV-Based VNIR Hyperspectral Benchmark Dataset for Landmine and UXO Detection | S. Lekhak et al. (RIT), arXiv 2510.02700 | https://arxiv.org/abs/2510.02700 | Hyperspectral cubes of surrogate targets with reference spectra. Preprint. *free* | 05.5, 09.4 | Verified |
| [SULAND-v2] | SULAND v2: RGB dataset and detection benchmark under domain shift | S. Lekhak et al. (RIT), arXiv 2607.28996 | https://arxiv.org/abs/2607.28996 | Label-quality fixes and the failure of in-distribution accuracy to transfer out of distribution. The domain-shift case study. Preprint. *free* | 09.3, 09.6 | Verified |
| [ROS2] | ROS 2 documentation (Jazzy LTS); navigation stack Nav2: https://docs.nav2.org/ | Open Robotics | https://docs.ros.org/en/jazzy/ | Middleware for the robotics projects and capstone C1. Arm planning: MoveIt 2 (https://moveit.picknik.ai/main/index.html). *free* | 06.x, C1 | Verified (index) |
| [Gazebo] | Gazebo documentation | Open Robotics | https://gazebosim.org/docs/latest/getstarted/ | Physics simulation paired with ROS 2. *free* | 06.x, 09.3, C1 | Verified |
| [OpenCV] | OpenCV 4.x docs: camera calibration tutorial | OpenCV.org | https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html | Intrinsic and extrinsic calibration and stereo. Used in 09.4 registration and 08.2 photogrammetry. *free* | 08.2, 09.4 | Verified (index) |

Case-study primary sources (FBI history pages, NIST Lew 2002 on Oklahoma City, the MCA SS
*Richard Montgomery* surveys, UXO Lao and the Monitor, and others) are in `research/03` §C and
are cited in each `case-studies/*.md` page. They are not repeated here.

---

## Items and chapters to skip

| Item | What to skip | Why |
|---|---|---|
| [Akhavan-2022] | Ch. 7 (manufacture) | Manufacture is outside the safety boundary. |
| [Cooper-1996] | Formulation/composition material; device or charge-design applications | Outside the boundary. Use only the physics and thermochemistry parts. |
| [Rusly-2024] | Formulation strategies | Only the ageing and decomposition chemistry is needed. |
| [MIL-STD-1316F] | Everything beyond the general safety-principle requirements | Only the principle of independent safety features is used, as an abstraction. |
| [UN-MTC-Rev8] | Test procedures | Only the *concept* of how test results feed into classification is needed. |
| [Beveridge-2012] | Device-reconstruction specifics in case chapters | Cases are used at the situation level only. |
| [TEP-09.30], [TEP-09.31], [UN-IEDD-2018] | Practical EOD/IEDD competencies | Used for organisational structure only. |
| Kingery & Bulmash 1984, ARBRL-TR-02555 (AD-B082713) | The whole report | *restricted* Distribution-limited. Use [UFC-3-340-02] Ch. 2, [IATG-01.80] or [UNSG-KB-calc]. |
| GICHD *Explosive Ordnance Guide for Ukraine* (2022) | The whole guide | It is an item-level identification aid for qualified operators. The course works at category level (Sim H). |
| Missouri S&T / Cranfield blasting, demolition and HME courses | The whole courses | Operational explosive use is outside the course's scope. |

## Paywalled items and free alternatives

| Paywalled | Free alternative |
|---|---|
| [Cooper-1996], [Akhavan-2022] | [MIT-2.26] + [Caltech-Ae103] + [SDToolbox] for shocks and detonation; [IATG-01.50] for classification |
| [Anderson-2021] | [MIT-2.26]; NASA GRC normal-shock page https://www.grc.nasa.gov/www/k-12/airplane/normal.html |
| [Baker-1983], [Kinney-Graham-1985] | [Glasstone-Dolan-1977] + [IATG-01.80] + [Rigby-2014] + [Isaac-2023] + [UFC-3-340-02] |
| [Daniels-2004] | [RAND-MR1608] GPR chapter |
| [Thrun-2005] | [Barfoot-2024] (free) |
| [NFPA-921], ASTM standards | [NIJ-181869], [TWGFEX-PB], OSAC summaries |
| [Macmillan-Creelman-2005] | [Fawcett-2006] (widely mirrored), [RAND-MR1608] |
| IEEE/SAGE HF papers | [Farajiparvar-2020] (open access); author preprints are usually available |
