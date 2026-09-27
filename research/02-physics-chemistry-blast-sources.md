# 02 — Physics, Chemistry & Blast-Effects Sources (Stages 1, 2, 4)

Research date: 2026-09-27. Scope boundary: scientific understanding only (no formulations, synthesis, device design, or optimization). Everything below is public textbook / standards / peer-reviewed material.

Verification legend:
- **V-F** = URL fetched (WebFetch or curl) and title/author/date/content confirmed.
- **V-S** = confirmed via publisher/library/index listings in search results; direct fetch blocked (403/redirect/captcha) or not needed for a catalog entry.
- **U** = could not verify; treat citation details as provisional.

Stage key: S1 = physics foundations, S2 = chemistry/energetic materials, S4 = blast effects.

---

## 1. Physics foundations (Stage 1)

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 1.1 | 2.26 Compressible Fluid Dynamics (lecture notes, psets) | MIT OCW, Prof. A. E. Hosoi | Spring 2004 | https://ocw.mit.edu/courses/2-26-compressible-fluid-dynamics-spring-2004/ | V-F | Free graduate course: conservation laws, normal/oblique shocks, shock structure, unsteady flows, Riemann invariants, piston and shock-tube problems, self-similar flows. Best free spine for S1. | S1 |
| 1.2 | 16.120 Compressible Flow (syllabus + materials) | MIT OCW | Spring 2003 | https://ocw.mit.edu/courses/16-120-compressible-flow-spring-2003/pages/syllabus/ | V-F (HTTP 200) | Alternate/complement to 2.26; quasi-1D flow and shocks. | S1 |
| 1.3 | Normal Shock Wave (equations page) | NASA Glenn Research Center | n.d. (live) | https://www.grc.nasa.gov/www/k-12/airplane/normal.html | V-F | Clean public statement of normal-shock ratios (p, ρ, T, M2, p0) vs. upstream Mach; ideal for checking code. | S1 |
| 1.4 | Modern Compressible Flow: With Historical Perspective, 4th ed. | John D. Anderson Jr. / McGraw-Hill | 2021 | https://www.mheducation.com/highered/product/modern-compressible-flow-with-historical-perspective-anderson.html | V-F | Standard engineering text. Ch. 3 (1-D flow, normal shocks) and Ch. 7 (unsteady wave motion, moving shocks, shock tube) are the core reading. | S1 |
| 1.5 | Physics of Shock Waves and High-Temperature Hydrodynamic Phenomena | Ya. B. Zel'dovich & Yu. P. Raizer / Dover | 2002 (reprint) | https://www.amazon.com/dp/0486420027 (Dover ISBN 0-486-42002-7; JFM review: https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/physics-of-shock-waves-and-hightemperature-hydrodynamic-phenomena-by-ya-b-zeldovich-yu-p-raizer-dover-2002-916-pp-isbn-0486420027-3495/41F41F7093EC790610C38A67F37B0AFF) | V-S | Physicist's reference: shock structure, strong explosions (point-blast / Sedov–Taylor), real-gas effects. Reference, not first read. | S1 |
| 1.6 | Supersonic Flow and Shock Waves (Appl. Math. Sci. 21) | R. Courant & K. O. Friedrichs / Springer | 1948; Springer reprint 1976 | https://books.google.com/books/about/Supersonic_Flow_and_Shock_Waves.html?id=Qsxec0QfYw8C | V-S | Mathematical theory of nonlinear waves, characteristics, shocks. Optional for the math-inclined software engineer. | S1 |
| 1.7 | The Effects of Nuclear Weapons, 3rd ed., Ch. III "Air Blast Phenomena…" | S. Glasstone & P. J. Dolan / US DoD & DOE | 1977 | https://atomicarchive.com/resources/documents/effects/glasstone-dolan/chapter3.html (OSTI record: https://www.osti.gov/biblio/6852629) | V-F | Public-domain, very readable account of blast-wave physics and the Rankine–Hugoniot relations for ideal air (§3.53–3.56). Source of the reflected-pressure formula below. Use it only for the physics. | S1/S4 |

## 2. Blast effects (Stage 4)

### 2a. Core texts and standards

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 2.1 | Explosive Shocks in Air, 2nd ed. | G. F. Kinney & K. J. Graham / Springer | 1985 | https://link.springer.com/book/10.1007/978-3-642-86682-1 | V-S (Springer redirected to login; confirmed via Google Books/ADS/Semantic Scholar) | Classic, compact treatment of blast from spherical free-air bursts. Source of the Kinney–Graham analytic overpressure fit, scaling laws, confined explosions, and structural loads. | S4 |
| 2.2 | Explosion Hazards and Evaluation (Fundamental Studies in Engineering 5) | W. E. Baker, P. A. Cox, P. S. Westine, J. J. Kulesz, R. A. Strehlow / Elsevier | 1983 | https://shop.elsevier.com/books/explosion-hazards-and-evaluation/baker/978-0-444-42094-7 | V-F | Covers free-field blast, loading, SDOF response (P–I diagrams), fragments, thermal effects, and damage criteria in one book. Best single S4 text. | S4 |
| 2.3 | Blast Waves, 2nd ed. (Shock Wave & High Pressure Phenomena) | Charles E. Needham / Springer | 2018 | https://link.springer.com/book/10.1007/978-3-319-65382-2 | V-S (redirect to login; confirmed via Springer/AbeBooks listings) | Modern text on blast-wave generation, propagation, reflection (regular vs. Mach), height of burst, and numerical hydrodynamics. The 2nd ed. adds a chapter on blast injury. | S4 |
| 2.4 | UFC 3-340-02 Structures to Resist the Effects of Accidental Explosions (w/ Change 2) | US DoD (USACE / NAVFAC / AFCEC); supersedes TM 5-1300 | 5 Dec 2008, Change 2 1 Sep 2014 | https://www.wbdg.org/dod/ufc/ufc-3-340-02 (WBDG blocks automated fetch; cover verified from public mirror https://archive.org/download/manualzilla-id-6021564/6021564.pdf) | V-F (mirror) / V-S (WBDG page) | "Approved for public release; distribution unlimited." Ch. 2 is the public source for the Kingery–Bulmash-based blast curves (incident/reflected pressure, impulse, reflection coefficient vs. angle, figure 2-193). Ch. 3 covers SDOF response. Read it as a textbook of curves, not a design exercise. | S4 |
| 2.5 | Airblast Parameters from TNT Spherical Air Burst and Hemispherical Surface Burst (ARBRL-TR-02555) | C. N. Kingery & G. Bulmash / US Army BRL | Apr 1984 | DTIC AD-B082713 (catalog: https://search.worldcat.org/title/Air-blast-parameters-from-TNT-spherical-air-burst-and-hemispherical-surface-burst/oclc/26785780) | V-S; **distribution-limited** ("AD-B" prefix; reported FOUO) | The canonical polynomial fits behind ConWep and UFC. **Do not plan on getting the original.** Public routes: UFC 3-340-02 Ch. 2 curves; the UN SaferGuard K-B calculator (https://unsaferguard.org/un-saferguard/kingery-bulmash, V-S; fetch returned an empty/202 page); and IATG 01.80, which states the validity range (Z ≤ 40 for K-B). | S4 |
| 2.6 | Simplified Kingery Airblast Calculations | M. M. Swisdak Jr. (NSWC), DDESB seminar | 1994 | https://apps.dtic.mil/sti/pdfs/ADA526744.pdf | U (DTIC 403 to automated clients; NTIS record exists: https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/ADA526744.xhtml) | Public simplified form of the K-B polynomials. Worth trying in a browser. | S4 |
| 2.7 | IATG 01.80 Formulae for ammunition management, 3rd ed. | UNODA (UN SaferGuard) | Mar 2021 | https://data.unsaferguard.org/iatg/en/IATG-01.80-Formulae-ammunition-management-IATG-V.3.pdf | V-F (text extracted) | **Very useful free public source.** Gives the Hopkinson–Cranz law, the Sachs altitude scaling, and the dynamic-pressure formula. Explains when to use K-B vs. Kinney–Graham (K-G is for spherical air bursts and is valid to Z = 500; K-B is for hemispherical surface bursts, Z ≤ 40). Also covers reflected pressure vs. angle and the debris/fragment models. | S4 |
| 2.8 | IATG 02.20 Quantity and separation distances, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/V3_IATG-02.20_en.pdf | V-F (text extracted) | International quantity-distance (QD) concepts: inter-magazine, inhabited-building, and public-traffic-route distances, all as Z·W^(1/3). **Correction to brief:** IATG **02.10** is *Introduction to risk management principles and processes* (https://data.unsaferguard.org/iatg/en/V3_IATG-02.10_en.pdf, V-F). QD is **02.20**. Include both: 02.10 for the risk framing, 02.20 for QD. | S4 |
| 2.9 | DESR 6055.09 Defense Explosives Safety Regulation — DoD Explosives Safety Standards, Ed. 1 Change 2 | USD(A&S) via DDESB (formerly DoDM 6055.09-M) | 25 Nov 2025 | https://www.denix.osd.mil/ddes/denix-files/sites/32/2022/08/DESR-6055.09-Edition1-Change-2-251208.pdf (hub: https://www.denix.osd.mil/ddes/) | V-F (PDF downloaded; cover confirms "cleared for public release") | US hazard divisions, compatibility groups, and quantity-distance tables. Read V1 (hazard classification) and V3 (QD concepts) for understanding. | S4 |
| 2.10 | DHS-DOJ Bomb Threat Stand-Off Card | DHS/CISA, DOJ, FBI (earlier edition: NCTC) | Aug 2025 (current); NCTC chart 2006 | https://www.cisa.gov/resources-tools/resources/dhs-doj-bomb-threat-stand-card | V-F (CISA page). PDF mirrors (tripwire.cisa.dhs.gov, archive.dni.gov) unreachable/403 → U for direct PDF | Public quick-reference chart giving mandatory evacuation and shelter-in-place distances by threat size. Use it as a teaching example that links TNT-equivalent mass to a standoff distance through scaled distance. | S4 |
| 2.11 | The Dependence of Blast on Ambient Pressure and Temperature (BRL Report 466) | R. G. Sachs / US Army BRL | 1944 | https://apps.dtic.mil/sti/citations/tr/ADA800535 | V-S (DTIC 403; record confirmed via search index; DTIC notes the scan is partially illegible) | Original source of Sachs scaling. For practical use, cite the IATG 01.80 restatement. | S4 |
| 2.12 | The diffraction of sound pulses I. Diffraction by a semi-infinite plane | F. G. Friedlander, Proc. R. Soc. A 186(1006):322–344 | 1946 | DOI 10.1098/rspa.1946.0046 (cited in Rigby et al. 2014, item 5.2) | V-S (citation verified from Rigby 2014 reference list) | Origin of the "Friedlander waveform." | S4 |
| 2.13 | Explosions in Air | W. E. Baker / Univ. of Texas Press | 1973 | (cited as Hopkinson–Cranz source in Rigby 2014) | V-S | Classic scaling text (Hopkinson, Sachs, and dimensional analysis). A secondary reading to Baker et al. 1983. | S4 |

### 2b. Blast injury

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 2.14 | Injuries from explosions: physics, biophysics, pathology, and required research focus | H. R. Champion, J. B. Holcomb, L. A. Young; J. Trauma 66(5):1468–1477 | 2009 | PubMed https://pubmed.ncbi.nlm.nih.gov/19430256/ ; free DTIC copy https://apps.dtic.mil/sti/tr/pdf/ADA627553.pdf | V-S (PubMed shows a captcha, DTIC and LWW return 403; title/authors/journal confirmed across PubMed, Semantic Scholar, and ResearchGate listings) | The standard review of primary through quaternary blast injury, with physics explained for non-clinicians. | S4 |
| 2.15 | Estimate of Man's Tolerance to the Direct Effects of Air Blast (DASA-2113) | I. G. Bowen, E. R. Fletcher, D. R. Richmond / Lovelace Foundation for DASA | Oct 1968 | https://www.semanticscholar.org/paper/846a261b91b315c329c2ab507572b40bbfee4de6 | V-S | Origin of the "Bowen curves": survival probability as a function of peak overpressure and positive-phase duration, from 13 mammal species. | S4 |
| 2.16 | Primary blast injury on thorax: a critical review of the studies and their outcomes (IRC-15-77) | J. Boutillier, C. Deck, P. Magnan, R. Willinger, P. Naz; IRCOBI Conf. | 2015 | https://www.ircobi.org/wordpress/downloads/irc15/pdf_files/77.pdf | V-F (text extracted) | Open-access critical review of the Bowen curves, the Axelsson chest-wall-velocity model, and the Stuhmiller model, including their limitations. Best free companion to Bowen. | S4 |
| 2.17 | Incorporating the Bowen Survivability Curves into Blast Analysis | OSTI tech report 1068297 | ~2013 | https://www.osti.gov/biblio/1068297 | U (fetch socket error twice) | Practical notes on applying the Bowen curves. | S4 |

### 2c. Fragmentation and structural response (conceptual references only)

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 2.18 | The Initial Velocities of Fragments from Bombs, Shell and Grenades (BRL-405) | R. W. Gurney / BRL | 1943 | https://apps.dtic.mil/sti/citations/tr/ADA800105 | V-S (DTIC 403) | Historical origin of the Gurney energy-balance concept. **For teaching, cite textbook treatments**: Cooper (3.1) Part 6 "fragment dynamics" and Zukas & Walters (3.5) chapter "The Gurney Model for Explosive Output." | S4 |
| 2.19 | Fragmentation of shell cases | N. F. Mott, Proc. R. Soc. A 189(1018):300–308 | 1947 | https://royalsocietypublishing.org/rspa/article/189/1018/300/6540/Fragmentation-of-shell-cases (DOI 10.1098/rspa.1947.0042) | V-S | Origin of the statistical fragment-size-distribution concept. Teach it through Baker et al. 1983, Ch. 6. | S4 |
| 2.20 | Introduction to Structural Dynamics | John M. Biggs / McGraw-Hill | 1964 | https://archive.org/details/introductiontost0000bigg | V-S | The source of the SDOF equivalent-system method (load/mass factors, dynamic load factor) used by UFC 3-340-02. The archive.org entry is a borrowable library copy. | S4 |

## 3. Chemistry / energetic materials at textbook level (Stage 2)

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 3.1 | Explosives Engineering | Paul W. Cooper / Wiley-VCH | 1996 | https://www.wiley-vch.de/en/areas-interest/engineering/explosives-engineering-978-0-471-18636-6 | V-F | The best single engineering text. Six parts: chemistry, energetics/thermochemistry, shock waves (Rankine–Hugoniot, the "bead model"), detonation, initiation theory, and applications (scaling, fragments, blast, craters). Written for engineers who know calculus. | S1/S2/S4 |
| 3.2 | The Chemistry of Explosives, 4th ed. | Jacqueline Akhavan (Cranfield) / RSC | 7 Mar 2022 | https://books.rsc.org/books/monograph/944/The-Chemistry-of-Explosives | V-F | Short (~194 pp) conceptual chemistry. Chapters cover classification, combustion vs. deflagration vs. detonation, thermal decomposition, thermochemistry, and kinetics. Ch. 7 (manufacture) is out of scope: **skip it.** | S2 |
| 3.3 | Detonation: Theory and Experiment | W. Fickett & W. C. Davis / Dover (orig. UC Press 1979) | 2000 (Dover corrected ed.) | https://www.amazon.com/dp/0486414566 (JFM review: https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/detonation-theory-and-experiment-by-w-fickett-w-c-davis-dover-2000-386-pp-isbn-0-486414566-us1895/9B75697FD96F977C03E4C750DD577E62) | V-S | Rigorous CJ and ZND theory, steady-detonation structure, and detonation-front instability. Graduate-level reference for S2 theory. | S1/S2 |
| 3.4 | Explosives, 7th ed. | R. Meyer, J. Köhler, A. Homburg / Wiley-VCH | 2016 | https://www.wiley.com/en-us/Explosives,+7th+Edition-p-9783527337767 | V-S | Alphabetical encyclopedia with about 500 entries and test-method definitions. Use it as a glossary/reference. | S2 |
| 3.5 | Explosive Effects and Applications | J. A. Zukas & W. P. Walters (eds.) / Springer | 1998 (softcover 2003) | https://link.springer.com/book/10.1007/978-1-4612-0589-0 | V-S | Edited survey with chapters on shock waves and EOS, detonation physics, chemistry, initiation, the Gurney model, hazard assessment, and safe handling. | S2/S4 |
| 3.6 | SDToolbox: Numerical Solution Methods for Shock and Detonation Jump Conditions (GALCIT FM2018.001) + Shock & Detonation Toolbox | S. T. Browne, J. L. Ziegler, N. P. Bitter, B. E. Schmidt, J. Lawson, J. E. Shepherd / Caltech EDL | Report rev. 10 Jan 2023; software 3 Mar 2025 | https://shepherd.caltech.edu/EDL/PublicResources/sdt/ | V-F | Open theory report plus Python/Cantera code for shock jump conditions, CJ speed, and ZND structure. **Ideal for a software engineer**: read the theory, then run the demos (e.g., demo_CJ.py). Note that it covers gas-phase detonation only. | S1/S2 |
| 3.7 | Detonation Waves and Pulse Detonation Engines (Ae103 lecture slides) | E. Wintenberger & J. E. Shepherd / Caltech | 27 Jan 2004 | https://shepherd.caltech.edu/EDL/projects/pde/Ae103-012704.pdf | V-F (text extracted) | Short slide deck deriving the Hugoniot, the Rayleigh line, and the CJ condition from the conservation equations. Good first exposure. | S1/S2 |
| 3.8 | UN Manual of Tests and Criteria, Rev. 8 (+ Amend. 1, 2025) | UNECE | 2023 / Sep 2025 | https://unece.org/transport/publications/un-manual-tests-and-criteria-rev8-2023 (Rev.7 PDF, V-F in search: https://unece.org/fileadmin/DAM/trans/danger/publi/manual/Rev7/Manual_Rev7_E.pdf) | V-S (UNECE 403 to fetch; free consultation PDF confirmed in search listing) | Part I shows how Class 1 test series (sensitivity, thermal stability, and so on) feed into hazard-division assignment. Read it for the concepts (what "sensitivity" means operationally), not the procedures. | S2 |
| 3.9 | UN Model Regulations Rev. 24 (Orange Book), Part 2 Ch. 2.1 Class 1 | UNECE | 2025 | https://unece.org/transport/dangerous-goods/un-model-regulations-rev-24 | V-S (403 to fetch) | Authoritative definitions of divisions 1.1–1.6 and compatibility groups A–L, N, S. | S2/S4 |
| 3.10 | IATG 01.50 UN explosive hazard classification system and codes, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/IATG-01.50-Explosive-hazard-classification-system-IATG-V.3.pdf | V-F (text extracted) | Free and readable. Covers HD 1.1–1.6 (mass explosion, projection, fire, minor, very insensitive, extremely insensitive), compatibility groups with examples, and GHS-style signal words and labels. **Recommended primary source for the S2 classification lesson.** | S2 |
| 3.11 | IATG 07.10 Surveillance and in-service proof, 3rd ed. | UNODA | Mar 2021 | https://data.unsaferguard.org/iatg/en/IATG-07.10-Surveillance-proof-IATG-V.3.pdf | V-F (text extracted) | Munition ageing: §13 "Chemical stability of propellant" (stabiliser depletion, stability tests) and §15 "Stability surveillance system." **Recommended primary source for the ageing/degradation lesson.** Companion: IATG 07.20 *Inspection of ammunition* (https://data.unsaferguard.org/iatg/en/IATG-07.20-Inspection-ammunition-IATG-V.3.pdf, V-S). | S2 |
| 3.12 | Stabilizer selection and formulation strategies for enhanced stability of single base nitrocellulose propellants: A review | S. N. A. Rusly, S. H. Jamal, A. Samsuri, S. A. Mohd Noor, K. S. Abdul Rahim; Energetic Materials Frontiers 5(1):52–69 | 2024 | https://www.sciencedirect.com/science/article/pii/S2666647224000083 (DOI 10.1016/j.enmf.2024.02.007) | V-S (403; the journal is open access and listed in DOAJ) | Open-access review of nitrocellulose decomposition and how stabilisers (e.g., diphenylamine and its daughter products) deplete over time. This is the science behind "old propellant is dangerous." **Use it for the chemistry of ageing only; skip the formulation discussion.** | S2 |

## 4. University courses / syllabi

| # | Program | Org | URL | Status | Notes |
|---|---|---|---|---|---|
| 4.1 | Explosives Engineering (EXP ENG) graduate course list | Missouri S&T | https://catalog.mst.edu/graduate/courselist/exp-eng/ | V-F | Relevant: 6212 Theory of High Explosives (thermodynamics + hydrodynamic theory), 5112 Explosives Handling & Safety, 6112 Explosives Regulations, 6464 Advanced Blast Vibration, 6312 Instrumentation. Use the course descriptions as a model for syllabus structure. Graduate certificate: https://explosives.mst.edu/studentresources/minor/ (V-S). |
| 4.2 | MENG explosives courses / Graduate Certificate in Explosives Engineering | New Mexico Tech (with EMRTC) | https://www.nmt.edu/academics/mecheng/classes.php ; https://catalog.nmt.edu/programs/NuVJx0lzgRRTomVJ0ci1 | V-F | 545 Intro to Explosives Engineering (chemistry, thermodynamics, shock, detonation), 546 Detonation Theory, 549 Wave Propagation, 553 Computer Modeling of Detonations, **555 Shock Propagation in Air (blast + structural response)**. The certificate core is 5045 + 5049. **This is the closest match to our S1→S2→S4 progression.** |
| 4.3 | Explosives Ordnance Engineering MSc | Cranfield University (Defence Academy, Shrivenham) | https://www.cranfield.ac.uk/courses/taught/explosives-ordnance-engineering | V-F | Core modules: Intro to Explosives Engineering, Munitions & Target Response, Research Tools, Future Developments. Electives include Testing & Evaluation of Explosives, Safety Assurance in EOE, Weapon Life Assessment (ageing), Counter-IED Capability. Security clearance required for enrolment. The short courses are listed publicly. |

## 5. Peer-reviewed reviews (engineer-friendly, open access preferred)

| # | Title | Authors / Journal | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 5.1 | Blast wave interaction with structures – an overview | O. S. Isaac, O. G. Alshammari, E. G. Pickering, S. D. Clarke, S. E. Rigby; Int. J. Protective Structures 14(4):584–630 | 2023 (online 2022) | https://eprints.whiterose.ac.uk/192170/ (DOI 10.1177/20414196221118595) | V-F; **CC-BY 4.0** | Comprehensive open-access review: reflection, clearing, diffraction, and blast walls/obstacles. Best single S4 review paper. | S4 |
| 5.2 | The Negative Phase of the Blast Load | S. E. Rigby, A. Tyas, T. Bennett, S. D. Clarke, S. D. Fay; IJPS 5(1):1–20 | 2014 | https://eprints.whiterose.ac.uk/id/eprint/78295/ | V-F (text extracted) | Open-access. States the modified Friedlander equation, Hopkinson–Cranz scaling, and positive/negative-phase parameter fits, with SDOF examples. **Used below as the Friedlander citation.** | S4 |
| 5.3 | Far-field positive phase blast parameter characterisation of RDX and PETN based explosives | D. G. Farrimond, S. Woolford, A. Tyas, S. E. Rigby, S. D. Clarke, A. Barr, M. Whittaker, D. J. Pope; IJPS 15(1):141–165 | 2024 (online 2023) | https://eprints.whiterose.ac.uk/id/eprint/195373/ | V-F; **CC-BY** | Critically assesses how accurate Kingery–Bulmash is against historic and new arena data, and whether blast loading is deterministic. Teaches students to be skeptical of empirical curves. | S4 |
| 5.4 | Air Blast Reflection Ratios and Angle of Incidence | L. Schwer; 11th European LS-DYNA Conf. | 2017 | https://lsdyna.ansys.com/wp-content/uploads/attachments/air-blast-reflections-and-angle-of-incidence.pdf | V-F (text extracted) | Short explanation of the UFC Fig. 2-193 reflection coefficients, regular vs. Mach reflection, and checks against Rankine–Hugoniot (e.g., ratio 2.297 at 36.4 kPa). | S4 |

---

## 6. Standard published equation forms (for course writing)

All forms below are for **ideal air, γ = 1.4**, unless γ is written explicitly. Symbols: p0 = ambient absolute pressure; Δp (or ps) = peak incident (side-on) overpressure; Δpr = peak normally reflected overpressure; M = shock Mach number relative to still air; c0 = ambient sound speed.

### 6.1 Friedlander waveform (positive phase)

    p(t) = p_max · (1 − t/t_d) · exp(−b·t/t_d),   0 ≤ t ≤ t_d

(time measured from shock arrival)

- p_max is the peak overpressure (incident or reflected, depending on the gauge location), t_d is the positive-phase duration, and b is the dimensionless waveform/decay coefficient.
- Positive-phase impulse (integrate the expression above): i = p_max·t_d·[1/b − (1 − e^(−b))/b²]. This is **derived here, not quoted**. Rigby 2014 §3.2 describes the same integration.
- Citation: Rigby et al. 2014, Eq. (1) (item 5.2, V-F), the "modified Friedlander equation," after Friedlander 1946 (item 2.12).

### 6.2 Hopkinson–Cranz (cube-root) scaled distance

    Z = R / W^(1/3)      [m/kg^(1/3)],  W = TNT-equivalent mass

- Equivalent statement: (R1/R2) = (W1/W2)^(1/3). Two charges produce the same peak overpressure at the same Z. Impulse and time scale by W^(1/3), meaning i/W^(1/3) and t/W^(1/3) are functions of Z.
- Citations: IATG 01.80 §5.1.1, Table 1 (item 2.7, V-F); Rigby et al. 2014, Eq. (2), citing Baker 1973 (V-F).

### 6.3 Sachs (ambient-condition) scaling

Quoted as IATG 01.80 §5.1.3 presents it (V-F). The subscript z means "at altitude," and 0 means sea-level reference: P0 = 101.33 kPa, T0 = 288.16 K.

- Scaled distance factor: Sd_z = (P0/P_z)^(1/3)
- Scaled pressure factor: Sp_z = P_z/P0
- Scaled impulse factor: Si_z = (P_z/P0)^(2/3) · (T0/T_z)^(1/2)
- IATG also gives a scaled-time factor in the same table.

Original source: Sachs 1944, BRL-466 (item 2.11).

### 6.4 Rankine–Hugoniot relations for a normal shock in ideal air

**(a) Static-pressure ratio across the shock.** NASA GRC (item 1.3, V-F):

    p1/p0 = [2γM² − (γ − 1)] / (γ + 1)

Subtracting 1 gives the overpressure form (algebra, not quoted):

    Δp/p0 = 2γ(M² − 1)/(γ + 1)   →   γ = 1.4:   Δp/p0 = (7/6)(M² − 1)

Inverted: M = √(1 + 6Δp/(7p0)).

This agrees with Glasstone & Dolan §3.55 (item 1.7, V-F), which gives the shock-front velocity:

    U = c0 · (1 + 6p/(7P0))^(1/2)

**(b) Peak dynamic pressure.** Glasstone & Dolan §3.55 (V-F); the same form appears in IATG 01.80 Table 6 (V-F):

    q = (5/2) · Δp² / (7p0 + Δp)

**(c) Normal reflection from a rigid wall, γ = 1.4.** Glasstone & Dolan §3.56 (V-F):

    Δpr = 2Δp · (7p0 + 4Δp) / (7p0 + Δp)

The reflection factor Δpr/Δp therefore tends to 2 for weak shocks and to 8 for very strong shocks.

- General-γ form (standard textbook form, e.g., Baker 1973 and Kinney & Graham; checked algebraically here to reduce exactly to the γ = 1.4 form above):

      Δpr = 2Δp + (γ + 1)Δp² / [(γ − 1)Δp + 2γp0]

  The strong-shock limit of Δpr/Δp is (3γ − 1)/(γ − 1), which equals 8 for γ = 1.4.
- Mach-number form for γ = 1.4. This is derived here by chaining p2/p1 with the reflected-shock relation. It matches the form reported in search results for the reflected **absolute** pressure over ambient:

      p_r/p0 = (7M² − 1)(4M² − 1) / [3(M² + 5)]

- Caveats to teach alongside these formulas:
  - Real explosive blasts show larger reflection factors than the ideal-gas limit of 8 because of real-gas effects; Baker 1983 and UFC charts show about 13 or more near the charge.
  - Oblique incidence transitions to Mach reflection, and the reflection coefficient can exceed the normal-incidence value (Schwer 2017; IATG 01.80 notes up to about +50%).

### 6.5 Kinney–Graham analytic peak-overpressure fit

Spherical free-air burst of TNT; Z in m/kg^(1/3):

    Δp/p0 = 808·[1 + (Z/4.5)²] / { √[1 + (Z/0.048)²] · √[1 + (Z/0.32)²] · √[1 + (Z/1.35)²] }

- Primary citation: Kinney & Graham, *Explosive Shocks in Air*, 2nd ed., Springer 1985 (item 2.1).
- Form verified from Dlubal's engineering formula page (https://www.dlubal.com/en/support-and-learning/support/formulas/000875, V-F), which uses p0 = 101.3 kPa.
- The same form appears in several open-access papers found in search, e.g., https://pdfs.semanticscholar.org/a53b/39ed01cd20b001647b61e213f250aac3ef93.pdf.
- IATG 01.80 §5.1.1 (V-F) states that the K-G fit is derived from spherical air bursts and is validated up to Z = 500, whereas Kingery–Bulmash (hemispherical surface burst) is limited to Z ≤ 40.
- Teaching note: for a hemispherical surface burst, textbooks commonly apply a ground-reflection factor to W (about 1.8× for real ground, 2× for an ideal rigid surface) before using spherical-burst curves. Cite Baker 1983, Ch. 2 for this. **U**: this factor was not verified by fetch in this pass.

---

## 7. Recommended minimal reading set

| Stage | Read | Keep as reference |
|---|---|---|
| S1 | MIT OCW 2.26 lecture notes; Anderson Ch. 3 & 7; Glasstone & Dolan Ch. III §3.1–3.60 | Zel'dovich & Raizer; Courant & Friedrichs |
| S2 | Akhavan Ch. 1–6; Cooper Parts 1–4; Shepherd Ae103 slides followed by SDToolbox report/demos; IATG 01.50; IATG 07.10 §13–15 | Fickett & Davis; Meyer; Zukas & Walters; UN Manual of Tests Part I; Rusly et al. 2024 |
| S4 | Baker et al. 1983 Ch. 2–4, 6, 8; Kinney & Graham; IATG 01.80 + 02.20; Rigby 2014; Isaac et al. 2023; Champion 2009; Boutillier 2015 (IRCOBI) | UFC 3-340-02 Ch. 2–3; DESR 6055.09 V1/V3; Needham; Biggs; Farrimond 2024; Schwer 2017; DHS-DOJ stand-off card |

## 8. Open issues / follow-ups
- Kingery–Bulmash original (AD-B082713) is distribution-limited. Rely on UFC 3-340-02, IATG 01.80, and the UN SaferGuard calculator.
- DTIC and several publisher sites (SAGE, Springer, LWW, UNECE, ScienceDirect, WBDG) block automated fetch. Items marked V-S should be spot-checked in a browser before publication.
- The IATG 02.10 vs. 02.20 numbering in the original brief is corrected in item 2.8.
