# 04 - Robotics, HRI, AI/CV and Software Sources for the EOD Technology Course

Research date: 2026-09-27. Scope: educational, graduate-level, engineering-oriented (robotics / AI / CV).
No render-safe procedures or device specifics are included or needed; sources are about platforms, human factors, math, perception and evaluation.

Verification legend:
- **V** = URL fetched directly and content confirmed.
- **S** = publisher page blocked automated fetch (403/empty), but bibliographic data confirmed via search results across 2+ independent indexes (Semantic Scholar, ADS, ACM DL, ResearchGate, etc.). Treat as reliable; spot-check the link manually.
- **U** = unverified.

Stage codes: **R** = Robotics stage, **AI** = AI-CV stage, **C** = Capstone.

---

## 1. EOD robot systems and history

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 1.1 | Wheelbarrow (robot) | Wikipedia (cites UK Parliament, Telegraph, Times, Army Technology) | article; robot 1972, retired 2019 | https://en.wikipedia.org/wiki/Wheelbarrow_(robot) | V | Origin story: Lt-Col Peter Miller, 1972, Northern Ireland; 400+ destroyed in service; replaced by L3Harris T7 in 2019. Good opening lecture hook: "the robot is the consumable." | R |
| 1.2 | Making safe: The dirty history of a bomb disposal robot | Queen's University Belfast (academic history paper) | c. 2019 | https://pure.qub.ac.uk/files/194511128/Safe.pdf (also https://www.researchgate.net/publication/337846304) | S (PDF 403 to fetcher; listed by search on QUB Pure + ResearchGate) | Scholarly STS history of the Wheelbarrow; better citation than Wikipedia. | R |
| 1.3 | ANDROS | Wikipedia; manufacturer Remotec (Northrop Grumman) | article | https://en.wikipedia.org/wiki/ANDROS | V | Heavy-class family (F6A ~485 lb, 25-lb arm lift; Wolverine, Mini-ANDROS). 2016 Dallas incident is a strong ethics discussion point. | R |
| 1.4 | Foster-Miller TALON | Wikipedia; manufacturer Foster-Miller / QinetiQ NA | article; deployed since 2000 | https://en.wikipedia.org/wiki/Foster-Miller_TALON | V | First deployed Bosnia 2000; Ground Zero 2001; manufacturer claims ~20,000 EOD missions in Iraq/Afghanistan; SWORDS armed variant (never authorized to fire). | R |
| 1.5 | tEODor Explosive Ordnance (EOD) Robot | Army Technology | project page | https://www.army-technology.com/projects/teodor-explosive-ordnance-eod-robot/ | V | Heavy tracked European platform (Telerob/Cobham): ~375 kg, 6-axis arm on turret, ~100 kg lift, 2.86 m reach; 40+ user nations. Good for payload/reach trade-off exercises. | R |
| 1.6 | PackBot: a versatile platform for military robotics | Brian M. Yamauchi (iRobot), Proc. SPIE 5422, Unmanned Ground Vehicle Technology VI | 2004 | https://doi.org/10.1117/12.538328 (SPIE: https://www.spiedigitallibrary.org/conference-proceedings-of-spie/5422/1/PackBot-a-versatile-platform-for-military-robotics/10.1117/12.538328.short) | S (SPIE, ADS 2004SPIE.5422..228Y, Semantic Scholar) | The canonical PackBot design paper: man-portable UGV, flippers, modular payload bus, CHARS sensor payload, Griffon. Assign as the "design paper" reading. | R |
| 1.7 | Army Developing Family of Explosive Ordnance Disposal Robots | National Defense Magazine | 2018-05-25 | https://www.nationaldefensemagazine.org/articles/2018/5/25/army-developing-family-of-explosive-ordnance-disposal-robots | S (page fetch empty; snippet confirmed via search) | Explains MTRS Inc II, CRS-I, CRS-H as one family with a common interoperability profile (plug-and-play payloads, 5-DOF arm, handheld OCU). Key for the "modular open architecture" lesson. | R, C |
| 1.8 | Common Robotic System (Individual) brief to NDIA | US Army PM Force Projection / Robotics | July 2017 | https://www.ndia.org/-/media/sites/ndia/divisions/robotics/anulare_pm-fp-robotics-brief-to-ndia_final---july-2017.pdf | S | Primary-source program brief (requirements, UGV Interoperability Profile). | R, C |
| 1.9 | 82nd Airborne tests new portable robot for individual Soldiers | US Army (army.mil) | 2019 | https://www.army.mil/article/228363/82nd_airborne_tests_new_portable_robot_for_individual_soldiers | S | CRS-I in use: ~32 lb tracked robot fitting in an assault pack. | R |
| 1.10 | Culture and Human-Robot Interaction in Militarized Spaces: A War Story | Julie Carpenter, Routledge (Ashgate), Emerging Technologies, Ethics and International Affairs series | 2016 | https://www.routledge.com/Culture-and-Human-Robot-Interaction-in-Militarized-Spaces-A-War-Story/Carpenter/p/book/9781032928456 | S | Interview-based study of EOD technicians and their robots (attachment, naming, trust, emotional impact of robot loss). The best qualitative HRI source specific to EOD. | R, C |

---

## 2. Teleoperation and human-robot interaction

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 2.1 | Human Performance Issues and User Interface Design for Teleoperated Robots | J.Y.C. Chen, E.C. Haas, M.J. Barnes, IEEE Trans. SMC Part C 37(6):1231-1245 | 2007 | https://doi.org/10.1109/TSMCC.2007.905819 | S (ACM DL, Semantic Scholar, ResearchGate) | Review of 150+ studies: bandwidth, latency, frame rate, FOV, frame of reference, lack of proprioception. The single best teleop-HF review; ARL authors. | R |
| 2.2 | Remote manipulation with transmission delay | W.R. Ferrell, IEEE Trans. Human Factors in Electronics 6:24-32 | 1965 | https://ieeexplore.ieee.org/document/6591253/ (NASA NTRS: https://ntrs.nasa.gov/citations/19660064449) | S | Origin of the "move-and-wait" strategy under delay. Short, classic; motivates predictive displays. | R |
| 2.3 | A Brief Survey of Telerobotic Time Delay Mitigation | P. Farajiparvar, H. Ying, A. Pandya, Frontiers in Robotics and AI | 2020 | https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2020.578805/full | V | Open access. Taxonomy: supervisory/predictive/passivity control, time-series prediction, RNN/LSTM/seq2seq prediction. Bridges classical and ML approaches. | R, AI |
| 2.4 | Bilateral teleoperation: An historical survey | P.F. Hokayem, M.W. Spong, Automatica 42(12):2035-2057 | 2006 | https://doi.org/10.1016/j.automatica.2006.06.027 | S | Haptics / force-feedback control under delay: passivity, wave variables, stability. The haptics math reference. | R |
| 2.5 | Telerobotics, Automation, and Human Supervisory Control | T.B. Sheridan, MIT Press | 1992 | https://archive.org/details/teleroboticsauto0000sher | S (Internet Archive lending copy + publisher listings) | Foundational supervisory-control text; defines the human-as-supervisor model used in EOD robots. | R |
| 2.6 | A model for types and levels of human interaction with automation | R. Parasuraman, T.B. Sheridan, C.D. Wickens, IEEE Trans. SMC Part A 30(3):286-297 | 2000 | https://doi.org/10.1109/3468.844354 | S | 4 stages x 10 levels of automation. Use it to frame "what should the EOD robot automate, and what must stay human." | R, AI, C |
| 2.7 | Toward a Theory of Situation Awareness in Dynamic Systems | M.R. Endsley, Human Factors 37(1):32-64 | 1995 | https://journals.sagepub.com/doi/10.1518/001872095779049543 | S | Three-level SA model (perceive, comprehend, project). Basis for OCU/UI design and evaluation. | R, C |
| 2.8 | Disaster Robotics | Robin R. Murphy, MIT Press (Intelligent Robotics and Autonomous Agents) | 2014 | https://direct.mit.edu/books/monograph/3408/Disaster-Robotics | S (MIT Press direct 403; confirmed via MIT Press Books Gateway listing, Wikipedia, AbeBooks ISBN 9780262027359) | Analysis of 34 real deployments (WTC, Katrina, Fukushima, mines): failure modes, 2-person operator rule, comms loss. Closest civilian analog to EOD field robotics. | R, C |

---

## 3. Robotics / estimation / vision textbooks (free versions noted)

| # | Title | Author / Org | Date | URL | Status | Free? | Why useful | Stage |
|---|---|---|---|---|---|---|---|---|
| 3.1 | Modern Robotics: Mechanics, Planning, and Control | K.M. Lynch, F.C. Park, Cambridge UP | 2017 | https://hades.mech.northwestern.edu/index.php/Modern_Robotics | V | Yes (preprint PDF + videos) | Screw theory, PoE kinematics, dynamics, planning, control. Primary manipulator-arm text. | R |
| 3.1b | Modern Robotics Specialization (6 courses) | Northwestern / Coursera (K. Lynch) | ongoing | https://www.coursera.org/specializations/modernrobotics | V | Audit free | Six courses incl. mobile-manipulation capstone (very close to an EOD UGV + arm). | R, C |
| 3.2 | Probabilistic Robotics | S. Thrun, W. Burgard, D. Fox, MIT Press | 2005 | https://mitpress.mit.edu/9780262201629/probabilistic-robotics/ | S | No | Bayes filters, EKF/UKF, particle filters, MCL, SLAM, occupancy grids. | R |
| 3.3 | Robotics: Modelling, Planning and Control | B. Siciliano, L. Sciavicco, L. Villani, G. Oriolo, Springer | 2009 | https://link.springer.com/book/10.1007/978-1-84628-642-1 | S | No (often via university SpringerLink) | Rigorous manipulator kinematics/dynamics, force and visual control; complements Lynch & Park. | R |
| 3.4 | Robotics, Vision and Control (3rd ed., Python and MATLAB editions) | P. Corke (Python ed.); Corke, Jachimczyk, Pilat (MATLAB ed.), Springer | 2023/2024 | https://petercorke.com/rvc/home/ | V | Code free (Colab/toolboxes); book paid, often SpringerLink | Hands-on bridge between math and code; Robotics Toolbox for Python. Free companion: Robot Academy videos. | R, AI |
| 3.5 | Planning Algorithms | S.M. LaValle, Cambridge UP | 2006 | https://lavalle.pl/planning/ | V | Yes (full PDF/HTML) | Configuration space, sampling-based planning (RRT/PRM), planning under uncertainty. | R |
| 3.6 | State Estimation for Robotics (2nd ed.) | T.D. Barfoot, Cambridge UP | 2024 | https://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser24.pdf (index: http://asrl.utias.utoronto.ca/~tdb/) | V | Yes | Batch/recursive estimation, Lie groups SO(3)/SE(3), factor-graph style. Modern estimation text. | R |
| 3.7 | An Introduction to the Kalman Filter (TR 95-041) | G. Welch, G. Bishop, UNC Chapel Hill | 1995 (rev. 2006) | https://www.cs.utexas.edu/~pstone/Courses/393Rfall15/readings/Welch+Bishop-TR-95.pdf | S (original UNC URL now 404; mirror confirmed via search at UT Austin and Yale) | Yes | 16-page gentle KF/EKF intro; ideal first reading before Thrun/Barfoot. | R |
| 3.8 | Simultaneous Localization and Mapping: Part I (and Part II) | H. Durrant-Whyte, T. Bailey, IEEE Robotics & Automation Magazine 13(2):99-110 / 13(3):108-117 | 2006 | https://doi.org/10.1109/MRA.2006.1638022 | S | No (widely mirrored) | The standard SLAM tutorial pair. | R |
| 3.9 | Multiple View Geometry in Computer Vision (2nd ed.) | R. Hartley, A. Zisserman, Cambridge UP | 2004 | https://www.robots.ox.ac.uk/~vgg/hzbook/ | V | Sample chapters free | Projective geometry, camera models, epipolar geometry; needed for stereo/photogrammetry on robot cameras and drone imagery. | AI |
| 3.10 | Computer Vision: Algorithms and Applications (2nd ed.) | R. Szeliski | 2022 | https://szeliski.org/Book/ | V | Yes (PDF after registration, personal use) | Broad modern CV reference incl. deep learning, detection, 3D reconstruction. | AI |

---

## 4. AI for EOD / mine action / UXO

### 4a. Domain papers and datasets

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 4.1 | Applying Deep Learning to Automate UAV-Based Detection of Scatterable Landmines | J. Baur, G. Steinberg, A. Nikulin, K. Chiu, T. de Smet, Remote Sensing 12(5):859 | 2020 | https://www.mdpi.com/2072-4292/12/5/859 (ADS: https://ui.adsabs.harvard.edu/abs/2020RemS...12..859B/abstract) | S (MDPI 403 to fetcher; ADS + Semantic Scholar + ResearchGate) | Seminal UAV RGB/thermal + CNN (Faster R-CNN) work on PFM-1 scatterable mines. Open access. | AI |
| 4.2 | How to Implement Drones and Machine Learning to Reduce Time, Costs, and Dangers Associated with Landmine Detection | Baur, Steinberg, Nikulin, Chiu, de Smet, Journal of Conventional Weapons Destruction 25(1) | 2021 | https://commons.lib.jmu.edu/cisr-journal/vol25/iss1/29/ | V | Open access, practitioner-oriented version of 4.1: workflow, costs, operational constraints. Good bridge to mine-action practice. | AI, C |
| 4.3 | A UAV-Based VNIR Hyperspectral Benchmark Dataset for Landmine and UXO Detection | S. Lekhak, E.J. Ientilucci, J. Baur, S. Ghosh (RIT) | arXiv 2025-10 (rev. 2026-02) | https://arxiv.org/abs/2510.02700 | V | Public dataset: 143 surrogate targets, 270 bands, radiance cubes + GCPs + reference spectra released. | AI, C |
| 4.4 | AMLID: An Adaptive Multispectral Landmine Identification Dataset for Drone-Based Detection | J.E. Gallagher, E.J. Oughton | arXiv 2025-12 | https://arxiv.org/abs/2512.18738 | V | Open RGB + LWIR dataset, 12,078 labeled images, 21 mine types, multiple altitudes/seasons/lighting. Best candidate capstone dataset. | AI, C |
| 4.5 | SULAND v2: A Refined RGB Dataset and Deep Learning Object Detection Benchmark for UAV/UGV-Based Surface Landmine Detection Under Domain Shift | S. Lekhak et al. (RIT) | arXiv 2026-07 | https://arxiv.org/abs/2607.28996 | V | ~33.8k images; shows label-quality fixes give +14.6-19.6 pts YOLOv8 and that in-distribution accuracy does not transfer OOD. Perfect case study for dataset hygiene and domain shift. | AI, C |
| 4.6 | UXO and Landmine Detection using Drones and Multi-modal Imaging (project page) | RIT Digital Imaging and Remote Sensing Lab | ongoing | https://www.rit.edu/dirs/research/unexploded-ordinance-uxo-and-landmine-detection-using-drones-and-multi-modal-imaging | V | Multi-sensor (HSI, MSI, LiDAR, SAR, thermal, magnetometer/EMI) field campaign context for 4.3/4.5. | AI |
| 4.7 | LANDMINE object detection dataset (v1) | Roboflow Universe (community) | 2023-09 | https://universe.roboflow.com/prashant-choudhary/landmine/dataset/1 | S (page 403 to fetcher; ~703 images per search listing) | Small, easy-to-load YOLO-format toy dataset for a first lab. Low quality/provenance; use only as a warm-up. | AI |
| 4.8 | Application of Convolutional and Recurrent Neural Networks for Buried Threat Detection Using Ground Penetrating Radar Data | M. Moalla, H. Frigui, A. Karem, A. Bouzid, IEEE TGRS 58(10):7022-7034 | 2020 | https://ieeexplore.ieee.org/document/9047150/ | S | CNN+RNN on 2-D B-scans and 3-D GPR volumes; 120,000 m2 of real data. The GPR deep learning reference. | AI |
| 4.9 | Implementation of and Experimentation with GPR for Real-Time Automatic Detection of Buried IEDs | P. Srimuk et al., Sensors 22 | 2022 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9693345/ | V | Open access, end-to-end system (hardware + preprocessing + R-CNN on hyperbolas), vehicle-mounted. Good systems-integration example. | AI, C |

### 4b. Method papers (general ML, applied to the EOD setting)

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 4.10 | Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, P. Abbeel (IROS 2017) | 2017 | https://arxiv.org/abs/1703.06907 | V | Sim-to-real with randomized rendering; justifies synthetic ordnance imagery when real data is scarce/restricted. | AI, C |
| 4.11 | Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning | Y. Gal, Z. Ghahramani (ICML 2016) | 2016 | https://arxiv.org/abs/1506.02142 | V | MC dropout epistemic uncertainty. | AI |
| 4.12 | Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles | B. Lakshminarayanan, A. Pritzel, C. Blundell (NIPS 2017) | 2017 | https://arxiv.org/abs/1612.01474 | V | Deep ensembles; strong OOD baseline. | AI |
| 4.13 | On Calibration of Modern Neural Networks | C. Guo, G. Pleiss, Y. Sun, K.Q. Weinberger (ICML 2017) | 2017 | https://arxiv.org/abs/1706.04599 | V | Temperature scaling, ECE. Needed before any "confidence" is shown to an operator. | AI, C |
| 4.14 | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | A.N. Angelopoulos, S. Bates | 2021 (arXiv 2107.07511) | https://arxiv.org/abs/2107.07511 (code: https://github.com/aangelopoulos/conformal-prediction) | V (search + arXiv listing) | Guaranteed-coverage prediction sets; natural fit for "never miss a hazard at rate > alpha" requirements. | AI, C |
| 4.15 | Adversarial Patch | T.B. Brown, D. Mane, A. Roy, M. Abadi, J. Gilmer | 2017 | https://arxiv.org/abs/1712.09665 | V | Physical universal patches; threat model for adversaries who can place objects in the scene. | AI |
| 4.16 | Robust Physical-World Attacks on Deep Learning Models | K. Eykholt et al. (CVPR 2018) | 2018 | https://arxiv.org/abs/1707.08945 | V | RP2 stickers on stop signs; methodology for lab-vs-field adversarial evaluation. | AI |
| 4.17 | Revisiting Active Perception | R. Bajcsy, Y. Aloimonos, J.K. Tsotsos, Autonomous Robots 42(2):177-196 | 2018 | https://doi.org/10.1007/s10514-017-9615-3 | S | Robot chooses viewpoints/sensing actions to reduce uncertainty; ties uncertainty (4.11-4.14) to robot behavior. (Bajcsy's original "Active Perception", Proc. IEEE 1988, is the classic.) | AI, C |
| 4.18 | You Only Look Once: Unified, Real-Time Object Detection | J. Redmon, S. Divvala, R. Girshick, A. Farhadi (CVPR 2016) | 2015/2016 | https://arxiv.org/abs/1506.02640 | V | One-stage detector; used by nearly all recent landmine UAV papers (current practice: Ultralytics YOLOv8+). | AI |
| 4.19 | End-to-End Object Detection with Transformers (DETR) | N. Carion et al. (ECCV 2020) | 2020 | https://arxiv.org/abs/2005.12872 | V | Set-prediction / transformer detector; contrast with YOLO (no NMS, no anchors). | AI |

---

## 5. Software (official docs)

| # | Title | Org | URL | Status | Notes | Stage |
|---|---|---|---|---|---|---|
| 5.1 | ROS 2 Documentation (Jazzy LTS; Kilted current) | Open Robotics / OSRF | https://docs.ros.org/en/jazzy/ | S (site bot-protected; confirmed via search) | Use the LTS distro for course stability. | R, C |
| 5.2 | Gazebo docs (Getting Started) | Open Robotics | https://gazebosim.org/docs/latest/getstarted/ | V | Jetty LTS (2025-2031) current; Harmonic pairs with ROS 2 Jazzy. | R, C |
| 5.3 | Nav2 | Open Navigation / ROS community | https://docs.nav2.org/ | V | Behavior-tree based navigation stack; planners, controllers, costmaps. | R, C |
| 5.4 | MoveIt 2 Documentation | PickNik / MoveIt community | https://moveit.picknik.ai/main/index.html | V | Manipulator motion planning for ROS 2; the arm side of an EOD UGV sim. | R, C |
| 5.5 | PyBullet (Bullet Physics) + Quickstart Guide | E. Coumans et al. | https://github.com/bulletphysics/bullet3 ; quickstart: https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/ | V (GitHub README) ; pybullet.org fetch failed | Lightweight Python sim for kinematics/grasping labs and domain-randomized data generation. | R, AI |
| 5.6 | OpenCV documentation (4.x; tutorials incl. camera calibration) | OpenCV.org | https://docs.opencv.org/4.x/ ; calib: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html | S (403 to fetcher; confirmed via search, current 4.13) | Calibration, ArUco/ChArUco, stereo. | AI |
| 5.7 | PyTorch documentation | PyTorch Foundation | https://docs.pytorch.org/docs/stable/ | V (redirects to current 2.14) | Training detectors, MC dropout, ensembles. | AI |

---

## 6. Autonomy, multi-robot, evaluation standards

| # | Title | Author / Org | Date | URL | Status | Why useful | Stage |
|---|---|---|---|---|---|---|---|
| 6.1 | Standard Test Methods for Response Robots | NIST Intelligent Systems Division (A. Jacoff) / ASTM E54.09 | ongoing | https://www.nist.gov/el/intelligent-systems-division-73500/standard-test-methods-response-robots | V | Quantitative, reproducible test methods for ground/aerial/aquatic response robots: mobility, manipulation dexterity, sensors, energy, comms, operator proficiency. JIEDDO-funded - directly relevant to bomb-squad robots. Blueprint for capstone evaluation design. | R, C |
| 6.2 | ASTM E54.09 Ground Test Methods - Introduction (2021A) | NIST | 2021 | https://www.nist.gov/document/astm-e5409-ground-test-methods-introduction-2021a | V (PDF downloaded, 8 MB; text not extractable by tool) | Overview deck of all ground robot test methods with apparatus photos. | R, C |
| 6.3 | ASTM E54.09 Ground Test Methods - Dexterity and Strength (2021A) | NIST | 2021 | https://www.nist.gov/document/astm-e5409-ground-test-methods-dexterity-and-strength-2021a | S (exists; >10 MB, too large to fetch) | Manipulator dexterity tests (rotate, grasp/place, extract/place, touch/insert, underbody inspection) - maps directly onto EOD arm tasks. | R, C |
| 6.4 | C-IED Training Using Standard Test Methods for Response Robots (v2015) | NIST | 2015 | https://www.nist.gov/document/c-ied-training-using-standard-test-methods-response-robots-v2015pdf | S | Using the test methods for counter-IED operator training/proficiency. The most EOD-specific NIST document. | R, C |
| 6.5 | Subcommittee E54.09 on Response Robots (standards list) | ASTM International | ongoing | https://www.astm.org/membership-participation/technical-committees/committee-e54/subcommittee-e54/jurisdiction-e5409 | S (403) | Official list of published standards (e.g., E2830 towing/grasped sleds). Standards themselves are paid. | C |
| 6.6 | Into the Robotic Depths: Analysis and Insights from the DARPA Subterranean Challenge | T.H. Chung, V. Orekhov, A. Maio, Annual Review of Control, Robotics, and Autonomous Systems | 2023 | https://www.annualreviews.org/content/journals/10.1146/annurev-control-062722-100728 | S (403; SSRN mirror https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4437754) | DARPA PM's official analysis of SubT results and lessons (comms-denied autonomy, single-operator multi-robot). | C |
| 6.7 | Team CERBERUS Wins the DARPA Subterranean Challenge: Technical Overview and Lessons Learned | M. Tranzatto et al. (36 authors; later Field Robotics) | 2022 | https://arxiv.org/abs/2207.04914 | V | Winner's system paper: legged + aerial robots, multi-modal SLAM, exploration planning, single-operator C2. | C |
| 6.8 | Team CERBERUS and Team Dynamo Win DARPA Subterranean Challenge Final Event | DARPA | 2021-09-24 | https://www.darpa.mil/news/2021/subterranean-challenge-winners | V | Official results (CERBERUS, CSIRO Data61, MARBLE; virtual: Dynamo). | C |
| 6.9 | NeBula: Team CoSTAR at the DARPA Subterranean Challenge | Agha et al. (NASA JPL) | 2021 | https://arxiv.org/abs/2103.11470 | S (search listing) | Uncertainty-aware autonomy architecture (belief-space planning); complements CERBERUS. | C |

---

## Minimal core reading list (if only ~12 items)

1. Yamauchi 2004 PackBot (1.6) + Carpenter 2016 (1.10) - platforms and people.
2. Chen, Haas & Barnes 2007 (2.1) + Endsley 1995 (2.7) + Parasuraman et al. 2000 (2.6) - HRI.
3. Lynch & Park (3.1, free) + Barfoot 2024 (3.6, free) + LaValle (3.5, free) - math.
4. Baur et al. 2020 (4.1) + AMLID (4.4) + SULAND v2 (4.5) - domain AI and data.
5. Guo 2017 (4.13) + Angelopoulos & Bates (4.14) - calibrated, guaranteed uncertainty.
6. NIST/ASTM E54.09 test methods (6.1, 6.3) + Chung et al. 2023 SubT (6.6) - evaluation and autonomy.

## Notes / gaps
- Welch & Bishop's original UNC URL (cs.unc.edu/~welch/kalman/) returns 404; use the UT Austin mirror.
- Many publisher pages (IEEE, MDPI, MIT Press, Springer, Annual Reviews, ASTM) block automated fetch; those are marked S.
- ASTM standards themselves are paywalled; NIST's free test-method PDFs are the practical teaching source.
- 4.3-4.5 are arXiv preprints (2025-2026); check for peer-reviewed versions before final course release.
