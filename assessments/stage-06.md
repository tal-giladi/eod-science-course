# Stage 6 assessment · Robotics

<div class="module-card">

**Covers** [06.1–06.9](lessons/stage-06/README.md) · **Time** 4–6 h (problems) + simulator
targets + design review · **Pass standard** "Proficient" band ([assessment plan](curriculum/assessment-plan.md)):
correct results *with* units, sanity checks and the main limitations named.

<p class="tags"><span>mathematical</span><span>interpretation</span><span>robotics</span><span>system design</span><span>Sim B · Sim G</span></p>
</div>

Work without the lessons open. Use Python freely. Every numerical answer needs units and one
sentence of sanity check. Fast-track learners: problems 2, 3 and 6 are the test-out problems for
06.2, 06.3 and 06.6.

## Problems

**1 · Test evidence (06.1, mathematical + interpretation).** Two candidate robots are tested on
the same standard 35° stair apparatus. Robot P: 19 successes in 20 trials. Robot Q: 29 in 30.
(a) Compute one-sided 90 % Clopper–Pearson lower bounds on each robot's success probability.
(b) The requirement is "R ≥ 0.9 at 90 % confidence". Does either robot meet it? (c) How many
consecutive successes would a *new* robot need to meet it with zero failures?

<details class="answer"><summary>Answer 1</summary>

(a) P: 0.819; Q: 0.876. (b) Neither: both lower bounds are below 0.9. Q is closer and simply needs
more successful trials. (c) $n \ge \ln0.1/\ln0.9 = 21.85$, so 22. Sanity check: more data with a
similar success rate raises the bound, and zero-failure testing is the cheapest route to a
reliability claim, but it is fragile, because one failure resets the argument.

</details>

**2 · Frames and projection (06.2, mathematical).** A robot is at world $(2, 1)$ on flat ground
with yaw 30°. A forward-looking camera (level, no tilt) sits at body $(0.2, 0, 0.6)$. Its
intrinsics are $f_x=f_y=600$ px and $(c_x,c_y)=(640,360)$. Body frame: $x$ forward, $y$ left,
$z$ up. Optical frame: $z$ forward, $x$ right, $y$ down. A fictional marker is at world
$(5, 2.5, 0.1)$. (a) Find the marker in the body frame. (b) Find its pixel coordinates. (c) Is it
left or right of image centre, above or below, and does that agree with your intuition?

<details class="answer"><summary>Answer 2</summary>

(a) $p_b = R_z(30°)^\top\big((5,2.5,0.1)-(2,1,0)\big) = (3.348, -0.201, 0.100)$ m. (b) Camera
frame (body-aligned): $(3.148, -0.201, -0.500)$. Optical: $(0.201, 0.500, 3.148)$. Pixels:
$u = 600\cdot0.201/3.148 + 640 = 678.3$, $v = 600\cdot0.5/3.148 + 360 = 455.3$. (c) Right of centre
(the marker is slightly to the robot's right, $y_b<0$) and below (it is 0.5 m below the camera).
Both agree.

</details>

**3 · Arm kinematics and statics (06.3, mathematical).** A planar 2R arm in a vertical plane has
$\ell_1 = 0.8$ m and $\ell_2 = 0.6$ m, with its base joint at the origin. (a) Find the elbow-up IK
solution that places the tool at $(1.0, 0.5)$ m. (b) Compute the manipulability $w$ there, and
state how close the pose is to singular relative to the maximum $\ell_1\ell_2$. (c) With a 3 kg
payload at the tool (massless links), find the holding torques, and check them by lever arms.

<details class="answer"><summary>Answer 3</summary>

(a) $c_2 = (1.25 - 0.64 - 0.36)/0.96 = 0.2604$. Elbow up: $q_2 = -74.91°$,
$q_1 = \operatorname{atan2}(0.5,1.0) - \operatorname{atan2}(0.6\sin q_2, 0.8+0.6\cos q_2) = 57.77°$.
FK returns $(1.0, 0.5)$ ✓. (b) $w = 0.48|\sin q_2| = 0.463$ m², i.e. 97 % of the maximum 0.48.
It is well conditioned. (c) $\tau = -J^\top(0,-29.43) = (29.43, 16.87)$ N m. Lever arms: the tool
is 1.0 m horizontally from the base, giving 29.43 N m ✓. The elbow is at
$x = 0.8\cos57.77° = 0.427$, so $0.573\cdot29.43 = 16.87$ N m ✓.

</details>

**4 · Mobility and stability (06.4, mathematical + interpretation).** A tracked robot with gauge
$B = 0.6$ m runs $v_L = 0.1$, $v_R = 0.5$ m/s, and the gyro reads 0.40 rad/s. (a) Estimate $\chi$.
(b) What turn radius did the operator actually get, compared with the no-slip prediction?
(c) The robot's CoM is $x_c = 0.25$ m ahead of the rear contact and $h = 0.22$ m high. What is its
static tip margin ascending the 35° standard stair? (d) Name two operator actions that reduce this
margin and one controller feature that protects it.

<details class="answer"><summary>Answer 4</summary>

(a) $\chi = (0.5-0.1)/(0.40\cdot0.6) = 1.67$. (b) Actual: $v/\omega = 0.3/0.4 = 0.75$ m.
No-slip: $0.3/(0.4/0.6) = 0.45$ m. (c) $\beta_{\text{tip}} = \arctan(0.25/0.22) = 48.65°$, so the
margin is 13.7°. (d) Raising or rearward-extending the arm (raises $h$, lowers $x_c$) and
accelerating up-slope (tilts effective gravity). Protection: a slope- and arm-pose-aware
acceleration limit and arm-pose interlock driven by the SSM computed from IMU attitude and joint
encoders.

</details>

**5 · Latency (06.5, conceptual + mathematical).** A fine-positioning task needs about 12 discrete
corrections, each taking 2.0 s of motion. (a) Estimate completion time with continuous control at
negligible delay and with a *move-and-wait* strategy under 0.8 s one-way latency. (b) Explain why
operators adopt move-and-wait (Ferrell 1965) instead of continuous control once delay grows, and
name two technologies that recover performance.

<details class="answer"><summary>Answer 5</summary>

(a) 24 s against $12(2.0 + 2\cdot0.8) = 43.2$ s: an 80 % penalty. (b) Under delay, continuous
closed-loop control through a human becomes oscillatory or unstable (the loop's phase lag grows
with delay), so operators open the loop: move, wait for the video to catch up, then correct.
Recovery: predictive displays (render the commanded motion immediately over the delayed video),
and supervisory control / shared autonomy (send goals, and let a local loop on the robot close the
fast loop). Force feedback needs passivity-based schemes under delay.

</details>

**6 · Estimation (06.6, mathematical).** A robot's position along a corridor has prior
$\mathcal N(2.0, 0.5^2)$ m. A range-to-landmark measurement gives $z = 2.6$ m with
$\sigma = 0.3$ m (direct observation of position). (a) Compute the Kalman gain, the posterior mean
and the posterior standard deviation. (b) The next five measurements all fall outside the
predicted 3σ innovation bounds. What do you check first?

<details class="answer"><summary>Answer 6</summary>

(a) $K = 0.25/(0.25+0.09) = 0.735$, mean $= 2.0 + 0.735\cdot0.6 = 2.441$ m,
variance $= (1-K)\cdot0.25 = 0.0662$, so $\sigma = 0.257$ m. The sanity check passes: the posterior
lies between prior and measurement, closer to the more certain one, and is tighter than both.
(b) Filter consistency (NIS test). Likely causes: process noise $Q$ too small (for example
unmodelled track slip, 06.4), a wrong measurement model or frame (06.2), a data-association error
(wrong landmark), or a time-synchronisation or latency offset between sensors.

</details>

**7 · Mapping and planning (06.7–06.8, mathematical + conceptual).** (a) An occupancy-grid cell
with prior 0.5 receives two independent "hit" observations with inverse-sensor probability 0.7.
What is its posterior occupancy probability, using log-odds? (b) An A* planner on this grid uses
straight-line distance as the heuristic but multiplies traversal costs by a terrain factor ≥ 1. Is
the heuristic admissible? What happens if you instead scale the heuristic by 1.5? (c) For a
survey (coverage) task, why is shortest-path planning the wrong objective?

<details class="answer"><summary>Answer 7</summary>

(a) $\ell = 2\ln(0.7/0.3) = 1.695$, so $p = 1/(1+e^{-1.695}) = 0.845$. (b) Yes. Straight-line
distance never exceeds the true cost when all cost factors are ≥ 1, so A* returns optimal paths.
Scaling by 1.5 (weighted A*) is faster but only bounded-suboptimal (cost ≤ 1.5 × optimal).
(c) Coverage needs every cell *swept* with adequate detection probability (05.7). The objective is
coverage per unit time or energy, subject to sensor footprint and overlap (boustrophedon /
cellular decomposition), not reaching one goal.

</details>

**8 · Communications and reliability (06.9, mathematical + design).** A 2.4 GHz link to a robot
300 m away inside a building: transmit 20 dBm, antenna gains 3 dBi each end, receiver sensitivity
−90 dBm, and an estimated 15 dB of wall and body loss. (a) Compute the free-space path loss and the
link margin. (b) The team adds two relays in series, each with 0.95 availability over the
mission. What is the chain's availability? What is it if you instead deploy two independent
relay chains (either suffices)? (c) Specify the robot's loss-of-link behaviour as three verifiable
requirements.

<details class="answer"><summary>Answer 8</summary>

(a) FSPL $= 20\log_{10}(300) + 20\log_{10}(2.4\times10^9) + 20\log_{10}(4\pi/c) = 89.6$ dB.
Margin $= 20 + 3 + 3 - 89.6 - 15 - (-90) = 11.4$ dB. Positive, but indoor multipath fades easily
exceed 10–20 dB, so the link is marginal. (b) Series: $0.95^2 = 0.9025$. Parallel chains:
$1 - (1-0.9025)^2 = 0.9905$. (c) Example: "On loss of command link for > 2 s the robot shall stop
all motion within 0.5 s and hold arm posture"; "After 30 s without link the robot shall
retro-traverse its last 20 m of recorded path at ≤ 0.3 m/s unless the operator disabled this
before the mission"; "Link state shall be displayed on the OCU and logged with timestamps".
Each must name its test method (radio NLOS range test with a controlled link drop).

</details>

## Simulator targets

<div class="callout sim">

- **Sim G** (`sims/robotics-engineering/`): complete **all challenges at Advanced** (obstacle
  course, reach, comms relay placement, energy, fictional-object manipulation, noisy sensors) with
  your own controller for at least the reach and obstacle challenges.
- **Sim B** (`sims/eod-robot/`): complete the standard mission at Advanced (latency and packet
  loss on) with **no contact with the object, no collisions, and ≥ 20 % battery remaining**. In the
  debrief, explain one decision you would now make differently.

</div>

## Design review (required)

<div class="callout exercise">

**Robot specification and failure-mode analysis.** A fictional regional police bomb squad needs
one robot for urban buildings (stairwells, narrow corridors, winter temperatures to −15 °C, NLOS
radio). Produce, in at most 4 pages:

1. **Requirements** (6–10), each quantitative and paired with a standard test method (06.1).
2. **Sizing**: mass, reach, lift-at-reach curve, track geometry, pack size, all justified with
   your 06.1/06.3/06.4 models, including the cold-weather energy budget.
3. **Control and autonomy**: which loops run on the robot, which functions are automated
   (Parasuraman–Sheridan–Wickens levels), and why (06.4–06.5).
4. **FMEA**: at least 8 failure modes across mobility, manipulation, sensing, comms, OCU and power,
   with severity/occurrence/detection and the mitigation for the top three (06.9).
5. **Residual risks** you did not mitigate, stated explicitly.

*Rubric.* Proficient: every requirement is traced to a model or test and the main failure modes are
addressed. Expert: also quantifies uncertainty (for example χ, cold capacity, link fades) and
proposes the experiment that would reduce the largest one.

</div>
