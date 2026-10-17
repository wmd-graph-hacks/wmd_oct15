"""Expand the eight non-mathematics catalogs into concept-sized lessons and quizzes.

The topic scope in each source page is split into small, ordered units. The first
unit keeps the existing `*-core-concepts` ID so an in-place graph reload preserves
existing references. Remaining units get stable IDs from their scope terms.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "artifacts"
BANK = Path(__file__).resolve().parents[1] / "question_bank"

# Topic prerequisites are authored relationships within each course. They are
# intentionally sparse: a suggested pathway is not a claim that all learners
# need every earlier topic.
PREREQS: dict[str, dict[str, list[str]]] = {
    "artificial-intelligence-and-machine-learning": {
        "programming-and-data-handling": ["mathematical-foundations"],
        "classical-machine-learning": ["programming-and-data-handling", "mathematical-foundations"],
        "neural-networks-and-deep-learning": ["classical-machine-learning"],
        "probabilistic-and-bayesian-methods": ["mathematical-foundations"],
        "reinforcement-learning": ["classical-machine-learning", "probabilistic-and-bayesian-methods"],
        "natural-language-processing": ["neural-networks-and-deep-learning"],
        "computer-vision": ["neural-networks-and-deep-learning"],
        "learning-theory": ["classical-machine-learning", "mathematical-foundations"],
        "systems-and-mlops": ["programming-and-data-handling", "neural-networks-and-deep-learning"],
        "responsible-ai-and-safety": ["learning-theory", "systems-and-mlops"],
    },
    "backend-engineering": {
        "databases": ["software-engineering-practice"],
        "distributed-systems": ["databases"],
        "api-design": ["software-engineering-practice"],
        "authentication-and-authorization": ["api-design"],
        "messaging-and-asynchronous-processing": ["distributed-systems"],
        "caching": ["databases", "distributed-systems"],
        "software-architecture": ["software-engineering-practice", "databases"],
        "reliability-and-observability": ["distributed-systems"],
        "testing": ["software-engineering-practice"],
        "software-engineering-practice": [],
    },
    "biology": {
        "molecular-biology": ["cell-biology"],
        "genetics-and-genomics": ["molecular-biology"],
        "biochemistry": ["cell-biology", "molecular-biology"],
        "physiology": ["cell-biology", "biochemistry"],
        "immunology": ["cell-biology", "molecular-biology"],
        "microbiology": ["cell-biology", "molecular-biology"],
        "evolutionary-biology": ["genetics-and-genomics"],
        "ecology": ["evolutionary-biology"],
        "developmental-biology": ["cell-biology", "genetics-and-genomics"],
        "neuroscience-introductory": ["cell-biology", "physiology"],
        "plant-biology": ["cell-biology", "physiology"],
        "laboratory-and-computational-techniques": ["cell-biology", "molecular-biology", "genetics-and-genomics"],
    },
    "chemistry": {
        "chemical-bonding-and-molecular-structure": ["general-chemistry"],
        "thermochemistry": ["general-chemistry"],
        "chemical-kinetics": ["general-chemistry"],
        "chemical-equilibrium": ["general-chemistry", "thermochemistry"],
        "electrochemistry": ["chemical-equilibrium", "thermochemistry"],
        "organic-chemistry": ["chemical-bonding-and-molecular-structure"],
        "spectroscopy-and-structure-determination": ["chemical-bonding-and-molecular-structure", "organic-chemistry"],
        "inorganic-chemistry": ["chemical-bonding-and-molecular-structure"],
        "physical-chemistry": ["thermochemistry", "chemical-kinetics", "chemical-equilibrium"],
        "analytical-chemistry": ["chemical-equilibrium", "laboratory-skills-and-safety"],
        "biochemistry-bridge": ["organic-chemistry", "chemical-equilibrium"],
        "polymer-and-materials-chemistry": ["organic-chemistry", "inorganic-chemistry"],
        "laboratory-skills-and-safety": ["general-chemistry"],
    },
    "computer-science-foundations": {
        "data-structures-and-algorithms": ["programming-fundamentals"],
        "operating-systems-fundamentals": ["programming-fundamentals"],
        "computer-networks": ["programming-fundamentals"],
    },
    "cybersecurity": {
        "cryptography": ["security-foundations"],
        "network-security": ["security-foundations"],
        "operating-system-and-host-security": ["security-foundations"],
        "application-security": ["security-foundations"],
        "web-security": ["network-security", "application-security"],
        "identity-and-access-management": ["security-foundations"],
        "offensive-security-ethical-hacking": ["network-security", "web-security"],
        "binary-exploitation-and-reverse-engineering": ["operating-system-and-host-security"],
        "defensive-security-and-security-operations": ["network-security", "operating-system-and-host-security"],
        "threat-intelligence-and-frameworks": ["security-foundations"],
        "cloud-and-container-security": ["network-security", "operating-system-and-host-security", "identity-and-access-management"],
        "governance-risk-and-compliance": ["security-foundations"],
        "security-of-ai-systems": ["application-security", "governance-risk-and-compliance"],
        "practical-labs-and-experience": ["security-foundations", "governance-risk-and-compliance"],
    },
    "devops-and-cloud": {
        "networking-for-infrastructure": ["linux-and-shell"],
        "virtualization-and-containers": ["linux-and-shell"],
        "container-orchestration-kubernetes": ["virtualization-and-containers", "networking-for-infrastructure"],
        "infrastructure-as-code": ["networking-for-infrastructure", "virtualization-and-containers"],
        "cloud-platforms": ["networking-for-infrastructure"],
        "ci-cd-and-release-engineering": ["linux-and-shell", "scripting-and-automation"],
        "monitoring-and-observability": ["linux-and-shell", "networking-for-infrastructure"],
        "configuration-and-secrets-management": ["cloud-platforms"],
        "site-reliability-engineering-sre": ["monitoring-and-observability", "ci-cd-and-release-engineering"],
        "backup-disaster-recovery-and-high-availability": ["cloud-platforms", "monitoring-and-observability"],
        "devsecops-and-supply-chain-security": ["ci-cd-and-release-engineering", "configuration-and-secrets-management"],
        "scripting-and-automation": ["linux-and-shell"],
        "performance-and-cost-optimization": ["cloud-platforms", "monitoring-and-observability"],
    },
    "physics": {
        "electromagnetism": ["classical-mechanics"],
        "thermodynamics": ["classical-mechanics"],
        "statistical-mechanics": ["thermodynamics"],
        "quantum-mechanics": ["mathematical-methods-for-physics"],
        "special-relativity": ["classical-mechanics", "electromagnetism"],
        "general-relativity-advanced-or-optional": ["special-relativity", "mathematical-methods-for-physics"],
        "optics-and-waves": ["electromagnetism"],
        "modern-physics": ["quantum-mechanics", "special-relativity"],
        "condensed-matter-and-solid-state-physics-advanced": ["quantum-mechanics", "statistical-mechanics"],
        "experimental-physics-and-data-analysis": ["classical-mechanics", "mathematical-methods-for-physics"],
        "mathematical-methods-for-physics": ["classical-mechanics"],
    },
}

METHOD = {
    "artificial-intelligence-and-machine-learning": "Separate training, validation, and test evidence; compare against a simple baseline; inspect errors by subgroup; and state what distribution the result is expected to generalize to.",
    "backend-engineering": "Trace one request from caller to storage and back. Mark trust boundaries, state changes, failure points, and retry behavior; then test the contract at both normal and partial-failure cases.",
    "biology": "State the biological scale and hypothesis, identify the control and measured outcome, trace the proposed mechanism, and distinguish correlation from causal evidence. Consider biological variability and ethical limits.",
    "chemistry": "Write a balanced equation or particle-level model first. Track atoms, charge, units, and conditions; show the calculation; then check whether the magnitude and direction agree with the chemical model.",
    "computer-science-foundations": "Trace a small input by hand, state the invariant that should remain true, and account for time, space, and edge cases. Use a test case that distinguishes the intended behavior from a plausible bug.",
    "cybersecurity": "Start from an explicit asset, threat, and trust boundary. Analyze the least-privilege defensive control and its evidence. Practical exercises must remain in an isolated environment with explicit authorization and scope.",
    "devops-and-cloud": "Trace a change from source through deployment to runtime signals. Make the desired state, access boundaries, failure signal, rollback path, and recovery objective explicit before changing a system.",
    "physics": "Draw the system and choose coordinates and sign conventions. State approximations, derive the relation before inserting values, preserve units, and check limiting cases or conservation laws.",
}

TOPIC_NOTES = {
    "artificial-intelligence-and-machine-learning": {
        "mathematical-foundations": "Vectors and matrices represent examples and transformations; gradients describe how an objective changes with parameters. Keep tensor shapes explicit and verify derivatives on a small case.",
        "programming-and-data-handling": "A reliable ML result begins with a reproducible data pipeline. Split before fitting transformations, prevent target leakage, inspect label quality, and record how features were produced.",
        "classical-machine-learning": "Match the model to the task: regression predicts numeric values, classification predicts categories, and regularization controls complexity. Compare with a baseline and evaluate data not used for fitting.",
        "neural-networks-and-deep-learning": "A neural network composes parameterized transformations and nonlinear activations. Backpropagation applies the chain rule; validation behavior matters because training loss alone does not establish generalization.",
        "probabilistic-and-bayesian-methods": "Likelihood measures how well parameters explain data; a prior encodes assumptions before observing it, and the posterior combines prior and likelihood. Separate parameter uncertainty from observation noise.",
        "reinforcement-learning": "An agent learns from sequential interaction: states, actions, rewards, and transitions define the problem. The Bellman relation connects immediate reward with future value; reward design and safe exploration matter.",
        "natural-language-processing": "Text systems turn token sequences into representations and predictions. Tokenization changes the input; evaluate on representative held-out text and inspect errors across language varieties and tasks.",
        "computer-vision": "Images are spatial signals, so resolution and preprocessing affect detection. Convolutions use local shared filters; evaluate spatial predictions rather than relying only on aggregate accuracy.",
        "learning-theory": "Generalization relates sampled examples to unseen ones. Complexity bounds depend on assumptions about data and hypothesis classes, so they guide reasoning but do not replace checks for distribution shift.",
        "systems-and-mlops": "Training coordinates data, compute, code, and artifacts. Version experiments and monitor deployed models for latency, failures, drift, and resource cost.",
        "responsible-ai-and-safety": "A model's impact depends on users, affected people, and deployment context. Fairness measures can conflict and explanations have limits; document choices and evaluate harms before release.",
    },
    "backend-engineering": {
        "databases": "Transactions group operations around consistency and isolation guarantees. Indexes can reduce lookup work but add storage and write cost; design around invariants and access patterns.",
        "distributed-systems": "Independent processes communicate over an unreliable network. Delays, retries, and partial failure mean a timeout does not prove an operation failed; design idempotency and recovery explicitly.",
        "api-design": "An API contracts inputs, outputs, errors, and evolution. Make operations predictable, validate at trust boundaries, and define compatibility before changing a public schema.",
        "authentication-and-authorization": "Authentication establishes identity; authorization decides whether it may act on a resource. Check permissions on each relevant request and keep credentials scoped and protected.",
        "messaging-and-asynchronous-processing": "Queues separate producers from workers but introduce duplicate delivery, reordering, and delay. Consumers should be idempotent, messages versioned, and retries observable.",
        "caching": "A cache trades freshness and consistency for lower latency or load. Define keys, invalidation, expiration, and miss behavior; measure hit rate and stale-data risk.",
        "software-architecture": "Architecture allocates responsibilities and boundaries. Choose boundaries that protect invariants and allow likely changes independently; evaluate coupling and operational cost.",
        "reliability-and-observability": "Reliability is measured from user outcomes. Metrics, logs, and traces answer different questions; connect them with request context and service objectives.",
        "testing": "Unit, integration, and end-to-end tests provide evidence at different boundaries. Prefer deterministic assertions about behavior and failure modes.",
        "software-engineering-practice": "Small reviewable changes, clear interfaces, repeatable checks, and documented decisions make regressions easier to find and ownership easier to share.",
    },
    "biology": {
        "cell-biology": "Cells maintain internal conditions through membranes, transport, signaling, and regulated expression. Structure suggests function but does not prove it; compare cell types and use controls to test mechanisms.",
        "molecular-biology": "DNA is copied into RNA and used to direct protein synthesis, with regulation at multiple stages. Mutations can affect sequence or expression, but consequences depend on context.",
        "genetics-and-genomics": "Inheritance tracks alleles through families and populations. Recombination changes linkage; selection, drift, mutation, and migration change frequencies. Separate population patterns from individual outcomes.",
        "biochemistry": "Molecular structure and chemical environment shape protein function and reactions. Enzyme rates depend on substrate and conditions; pathway diagrams should show inputs, outputs, and control points.",
        "physiology": "Physiological systems maintain function through feedback. Trace a perturbation from sensor to control response and effector; distinguish compensation from the original cause.",
        "immunology": "Innate defenses respond rapidly to common signals; adaptive responses use specific receptors and can form memory. Antigen presentation links the arms, while immune activity can also damage tissue.",
        "microbiology": "Microbes differ in structure, replication, and host interaction. Measure growth and susceptibility under stated conditions; resistance can arise and spread under selection.",
        "evolutionary-biology": "Evolution is change in heritable variation across generations. Selection, drift, migration, and mutation all matter; phylogenetic trees are hypotheses of relatedness, not ladders of progress.",
        "ecology": "Ecological outcomes emerge from organisms and environments interacting. Resources constrain growth; spatial boundaries and time horizon affect interpretation.",
        "developmental-biology": "Development coordinates cell fate, movement, and patterning over time. Signaling and gene expression create positional information; perturbation experiments help test causality.",
        "neuroscience-introductory": "Neural signaling depends on membrane potentials, ion channels, and synapses. Circuit behavior emerges from connected cells and should be interpreted alongside the measurement method.",
        "plant-biology": "Plant growth integrates light, water, minerals, hormones, and environmental signals. Xylem and phloem have different transport roles; trace tissue, signal, and resource flow.",
        "laboratory-and-computational-techniques": "Each technique measures a property with limits in sensitivity, specificity, and bias. Use controls, replicates, calibration, and documented analysis to answer the biological question.",
    },
    "chemistry": {
        "general-chemistry": "Balanced equations conserve atoms and charge. Connect particles, moles, mass, and measurements; identify limiting reactants and state conditions before interpreting yield.",
        "chemical-bonding-and-molecular-structure": "Bonding models connect electron distribution to shape and properties. Polarity depends on bond dipoles and molecular arrangement; state the approximation used.",
        "thermochemistry": "Energy changes depend on the defined system and sign convention. Hess's law combines reaction enthalpies; calorimetry infers heat from temperature and heat capacity.",
        "chemical-kinetics": "Rate laws come from measured dependence on concentration and conditions, not generally from coefficients in an overall equation. Proposed mechanisms should agree with observed kinetics.",
        "chemical-equilibrium": "At equilibrium, forward and reverse rates match. Compare reaction quotient Q with K to predict direction; temperature can change K while concentration changes Q.",
        "electrochemistry": "Redox reactions transfer electrons. Galvanic cells separate oxidation and reduction; balance half-reactions and use consistent potential signs.",
        "organic-chemistry": "Organic reactions transform functional groups through electron movement. Curved arrows track electron pairs; mechanism, sterics, solvent, and conditions help explain products.",
        "spectroscopy-and-structure-determination": "Spectra provide evidence about molecular structure, with each method sensitive to different interactions. Combine independent signals instead of assigning structure from one peak.",
        "inorganic-chemistry": "Composition, oxidation state, bonding, and structure shape inorganic reactivity. Coordination geometry and ligand effects influence transition-metal behavior.",
        "physical-chemistry": "Thermodynamic, kinetic, and quantum models relate microscopic behavior to measurements. Check idealizations, units, and limiting behavior.",
        "analytical-chemistry": "Analytical results depend on sampling, calibration, selectivity, and uncertainty. Use standards and blanks, validate the range, and distinguish precision from accuracy.",
        "biochemistry-bridge": "Biological molecules react in aqueous, regulated environments. Connect molecular structure and charge to reaction energetics and pathway context.",
        "polymer-and-materials-chemistry": "Material properties depend on composition, structure, processing, and defects. Polymer architecture affects bulk behavior; compare measurements under stated conditions.",
        "laboratory-skills-and-safety": "Reliable lab work combines hazard assessment, protective controls, calibrated measurement, and clear records. Follow the specific protocol and local safety rules.",
    },
    "computer-science-foundations": {
        "programming-fundamentals": "Programs transform inputs through state, control flow, and representation. Define boundary behavior, handle invalid input, and use small tests to expose assumptions.",
        "data-structures-and-algorithms": "A data structure organizes information for operations; an algorithm defines the steps that use it. Analyze time and space as input grows and verify edge cases.",
        "operating-systems-fundamentals": "An OS manages processes, memory, files, and devices while mediating hardware access. Concurrency introduces interleavings and shared-state hazards.",
        "computer-networks": "Networks move data through layered protocols. Addressing, routing, transport, and application protocols solve different parts; trace where a request can fail.",
    },
    "cybersecurity": {
        "security-foundations": "Security starts by identifying assets, threats, trust boundaries, and risk. Confidentiality, integrity, and availability are goals; match controls to a concrete threat model.",
        "cryptography": "Cryptographic security depends on established primitives, correct protocols, and protected keys. Encryption alone does not provide authenticity; use trusted libraries.",
        "network-security": "Segmentation, filtering, and monitoring should follow explicit communication flows and threat assumptions. An allow rule has security and operational consequences.",
        "operating-system-and-host-security": "Patching, permissions, isolation, and monitoring reduce host exposure and limit compromise. Verify against an approved baseline and preserve forensic evidence.",
        "application-security": "Application security follows untrusted inputs across code and data boundaries. Validate for context, enforce authorization server-side, and test failure paths.",
        "web-security": "Web security crosses browser, server, identity, and transport boundaries. Match controls to the flow and test only systems explicitly in scope.",
        "identity-and-access-management": "Identity establishes principals and credentials; access control maps them to actions. Least privilege and lifecycle review reduce stale access.",
        "offensive-security-ethical-hacking": "A penetration test is an authorized, scoped assessment that produces evidence and remediation guidance. Define written permission and stop conditions first.",
        "binary-exploitation-and-reverse-engineering": "Binary analysis studies compiled behavior, memory, and control flow. Use intentionally vulnerable samples in isolated labs; never target real systems without authorization.",
        "defensive-security-and-security-operations": "Security operations combine telemetry, triage, containment, and recovery. An alert is a lead, not a conclusion; preserve evidence and record decisions.",
        "threat-intelligence-and-frameworks": "Threat intelligence organizes evidence about adversaries and behavior. Frameworks provide vocabulary, not proof; include source, confidence, and relevance.",
        "cloud-and-container-security": "Cloud security follows shared-responsibility boundaries and identity-first access. Container isolation does not replace patching, least privilege, provenance, or monitoring.",
        "governance-risk-and-compliance": "Governance turns obligations and risk decisions into ownership, controls, and evidence. Compliance supports assurance but does not guarantee security.",
        "security-of-ai-systems": "AI systems add risks from data, model behavior, tools, and deployment. Evaluate trust boundaries, privacy, misuse, and oversight proportional to impact.",
        "practical-labs-and-experience": "A useful lab has an objective, isolated environment, approved assets, repeatable steps, and cleanup plan. Keep activity inside authorized scope.",
    },
    "devops-and-cloud": {
        "linux-and-shell": "Linux exposes processes, files, permissions, and services. Commands can alter many resources, so inspect targets and privileges, prefer repeatable scripts, and verify effects.",
        "networking-for-infrastructure": "Infrastructure networking combines addressing, routing, name resolution, and filtering. Trace a connection layer by layer rather than treating reachability as one property.",
        "virtualization-and-containers": "VMs virtualize hardware; containers share a host kernel while isolating processes and filesystems. Packaging improves portability but does not remove host risks.",
        "container-orchestration-kubernetes": "Kubernetes controllers reconcile declared resources toward desired state. Debug by comparing configuration with observed state, events, and health checks.",
        "infrastructure-as-code": "Infrastructure as code makes changes reviewable and repeatable. Plans reveal intended mutations, state tracks managed resources, and secrets stay out of source control.",
        "cloud-platforms": "Cloud services expose compute, storage, identity, and networking through APIs. Shared responsibility varies by service; design access, recovery, and cost around workload needs.",
        "ci-cd-and-release-engineering": "A delivery pipeline turns changes into tested, versioned releases. Reproducible builds, staged rollout, health checks, and rollback contain failures.",
        "monitoring-and-observability": "Metrics show trends, logs show events, and traces show request paths. Link telemetry to user-facing objectives and use it to investigate unknown behavior.",
        "configuration-and-secrets-management": "Configuration defines environment behavior; secrets are credentials needing controlled access and rotation. Keep secrets out of logs and audit retrieval.",
        "site-reliability-engineering-sre": "SRE manages reliability through objectives, error budgets, and automation. Error budgets make the reliability-versus-change tradeoff explicit.",
        "backup-disaster-recovery-and-high-availability": "Backups, replication, and failover address different failures. Define recovery time and recovery point objectives and test restoration.",
        "devsecops-and-supply-chain-security": "Supply-chain security follows code, dependencies, builds, and artifacts to deployment. Verify inputs, protect signing credentials, and make checks actionable.",
        "scripting-and-automation": "Automation can amplify mistakes. Make scripts idempotent, validate inputs, handle errors, and provide a safe preview for destructive changes.",
        "performance-and-cost-optimization": "Performance and cost are workload properties measured over time. Use telemetry, representative load, and account for reliability and transfer costs.",
    },
    "physics": {
        "classical-mechanics": "Newton's laws relate net force to changes in motion; energy and momentum methods simplify systems with suitable boundaries. Draw forces and choose a frame first.",
        "electromagnetism": "Electric and magnetic fields describe interactions and changing fields. Maxwell's equations connect sources, induction, and propagation; symmetry and boundaries guide solutions.",
        "thermodynamics": "The first law accounts for energy; the second constrains processes through entropy. Define the system and sign convention before calculating.",
        "statistical-mechanics": "Statistical mechanics links microscopic states to macroscopic observables through probability. Partition functions encode state weights; equilibrium assumptions matter.",
        "quantum-mechanics": "A quantum state predicts measurement probabilities through operators and the Born rule. The Schrödinger equation evolves states; boundary conditions determine allowed solutions.",
        "special-relativity": "Special relativity keeps the speed of light invariant across inertial frames. Lorentz transformations relate space and time measurements; simultaneity can depend on frame.",
        "general-relativity-advanced-or-optional": "General relativity models gravity through spacetime geometry. Curvature relates to stress-energy; distinguish coordinate choices from measurable effects.",
        "optics-and-waves": "Wave behavior explains interference, diffraction, and polarization; geometrical optics is a short-wavelength approximation. Check scales before choosing a model.",
        "modern-physics": "Modern physics treats phenomena where classical models fail, including quantized energy and relativistic effects. Compare scales with evidence to choose necessary corrections.",
        "mathematical-methods-for-physics": "Differential equations, vector calculus, transforms, and complex methods encode physical laws. Choose tools using symmetry and boundary conditions.",
        "condensed-matter-and-solid-state-physics-advanced": "Collective behavior in solids depends on structure, bonding, and quantum states. Band models distinguish conductors, semiconductors, and insulators; defects and temperature matter.",
        "experimental-physics-and-data-analysis": "Measurements have uncertainty, calibration limits, and systematic effects. Report uncertainty, inspect residuals, and distinguish repeatability from accuracy.",
    },
}

METHOD_CHECKS = {
    "artificial-intelligence-and-machine-learning": ("Which evidence best supports a claim that a model will generalize?", "Evaluate a representative held-out set, compare to a baseline, and inspect relevant error groups."),
    "backend-engineering": ("Which check best supports a claim that a service change is safe?", "Test contracts on success and failure paths, including retries and state changes."),
    "biology": ("Which evidence best supports a causal biological explanation?", "Use a controlled comparison that tests a prediction while measuring the relevant outcome."),
    "chemistry": ("Which check best supports a chemical calculation?", "Check atom and charge balance, units, conditions, and agreement with the chemical model."),
    "computer-science-foundations": ("Which check best supports an algorithm's correctness?", "Trace edge cases and verify invariants as well as time and space behavior."),
    "cybersecurity": ("Which evidence best supports a security control claim?", "Use an approved bounded test and preserve evidence tied to the stated threat and asset."),
    "devops-and-cloud": ("Which evidence best supports a safe infrastructure change?", "Review the plan, stage the change, monitor health, and verify rollback or recovery."),
    "physics": ("Which check best supports a physical model's prediction?", "Check dimensions and limiting cases, then compare with measurement and uncertainty."),
}

DISTRACTORS = {
    "artificial-intelligence-and-machine-learning": ["membrane transport", "Kubernetes scheduling", "chemical equilibrium"],
    "backend-engineering": ["Hardy-Weinberg equilibrium", "orbital angular momentum", "electrochemical potential"],
    "biology": ["HTTP cache invalidation", "Bellman optimality equation", "Coulomb's law"],
    "chemistry": ["OAuth token rotation", "backpropagation", "population bottleneck"],
    "computer-science-foundations": ["antigen presentation", "titration curve", "wave-particle duality"],
    "cybersecurity": ["calorimetry", "PCR amplification", "Jordan normal form"],
    "devops-and-cloud": ["Pauli exclusion principle", "Mendelian segregation", "Michaelis-Menten kinetics"],
    "physics": ["access control list", "DNA replication", "transaction isolation"],
}

# Preserve the Physics seed bank IDs created before this curriculum expansion.
LEGACY_PHYSICS_QUESTIONS = {
    "classical-mechanics": [
        {"id": "cm-1", "level": 1, "stem": "Newton's second law relates net force to which quantity?", "options": ["Mass times acceleration", "Mass times velocity", "Work divided by time", "Momentum divided by distance"], "answer": 0, "hints": ["It describes the rate of change of momentum.", "For constant mass, the relation is F_net = ma."], "explanation": "For constant mass, the net force is the mass multiplied by acceleration.", "subtopic_id": "physics-classical-mechanics-core-concepts"},
        {"id": "cm-2", "level": 2, "stem": "What does the work-energy theorem state?", "options": ["Net work equals the change in kinetic energy", "Net work equals the change in momentum", "Power equals the change in position", "Force equals the change in potential energy"], "answer": 0, "hints": ["Work is energy transferred by a force over displacement.", "The theorem relates work to a scalar measure of motion."], "explanation": "The net work done on an object equals its change in kinetic energy.", "subtopic_id": "physics-classical-mechanics-core-concepts"},
        {"id": "cm-3", "level": 3, "stem": "When is the total momentum of a system conserved?", "options": ["When the net external impulse on the system is zero", "Whenever the objects move at constant speed", "Only when all collisions are elastic", "Whenever internal forces are absent"], "answer": 0, "hints": ["Consider the system boundary and external forces.", "Momentum changes according to net external impulse."], "explanation": "Total momentum is conserved when the net external impulse on the system is zero; internal forces cancel in the system total.", "subtopic_id": "physics-classical-mechanics-core-concepts"},
    ],
    "thermodynamics": [
        {"id": "thermo-1", "level": 1, "stem": "What does the first law of thermodynamics express?", "options": ["Conservation of energy for a thermodynamic system", "That heat always flows into a system", "That every process is reversible", "That temperature is conserved"], "answer": 0, "hints": ["It is an energy balance.", "Heat and work transfer energy across the system boundary."], "explanation": "The first law accounts for changes in internal energy through heat and work, with signs set by convention.", "subtopic_id": "physics-thermodynamics-core-concepts"},
        {"id": "thermo-2", "level": 2, "stem": "For an isolated system, what does the second law say about entropy?", "options": ["It does not decrease for a spontaneous process", "It must remain zero", "It always decreases", "It equals the system's internal energy"], "answer": 0, "hints": ["An isolated system exchanges neither matter nor energy.", "The law gives a direction to spontaneous change."], "explanation": "The entropy of an isolated system stays constant for an ideal reversible process and increases for an irreversible spontaneous process.", "subtopic_id": "physics-thermodynamics-core-concepts"},
        {"id": "thermo-3", "level": 3, "stem": "For an ideal gas undergoing an isothermal change, which statement is correct?", "options": ["Its internal energy change is zero because internal energy depends only on temperature", "Its internal energy must increase because volume changes", "Its entropy change is always zero", "No heat can enter or leave the gas"], "answer": 0, "hints": ["For an ideal gas, internal energy is a function of temperature.", "Isothermal means the temperature is constant."], "explanation": "At constant temperature an ideal gas has no change in internal energy, though heat and work may be exchanged.", "subtopic_id": "physics-thermodynamics-core-concepts"},
    ],
    "quantum-mechanics": [
        {"id": "qm-1", "level": 1, "stem": "In the Born interpretation, what does |ψ(x)|² represent?", "options": ["The particle's energy at x", "The probability density of finding the particle near x", "The particle's momentum at x", "The force on the particle at x"], "answer": 1, "hints": ["It is always non-negative.", "Integrated over all space it equals 1."], "explanation": "|ψ|² is the probability density; its integral over all space is 1 for a normalized state.", "subtopic_id": "physics-quantum-mechanics-core-concepts"},
        {"id": "qm-2", "level": 2, "stem": "What does the Heisenberg uncertainty principle say about position and momentum?", "options": ["Both can be known exactly at once", "The product of their uncertainties has a lower bound of ħ/2", "Momentum is always zero when position is known", "Uncertainty only comes from poor instruments"], "answer": 1, "hints": ["It is a property of the state, not of the equipment.", "Δx Δp ≥ ħ/2."], "explanation": "Δx·Δp ≥ ħ/2 is a fundamental limit of quantum states.", "subtopic_id": "physics-quantum-mechanics-core-concepts"},
        {"id": "qm-3", "level": 3, "stem": "Two electrons cannot occupy the same quantum state. Which principle is this?", "options": ["Pauli exclusion principle", "Correspondence principle", "Superposition principle", "Equivalence principle"], "answer": 0, "hints": ["It applies to identical fermions.", "It helps explain the structure of the periodic table."], "explanation": "The Pauli exclusion principle forbids identical fermions from sharing a quantum state.", "subtopic_id": "physics-quantum-mechanics-core-concepts"},
    ],
}

def split_terms(text: str) -> list[str]:
    """Split a scope list on commas outside parentheses."""
    out, buf, depth = [], [], 0
    for ch in text:
        if ch == "(": depth += 1
        elif ch == ")": depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            term = "".join(buf).strip()
            if term: out.append(term)
            buf = []
        else:
            buf.append(ch)
    term = "".join(buf).strip()
    if term: out.append(term)
    return out

def slug(text: str) -> str:
    text = re.sub(r"\([^)]*\)", "", text.lower())
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:62].rstrip("-") or "concepts"

def fm_and_body(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not m: raise ValueError(f"missing frontmatter: {path}")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)

def get_scope(topic_path: Path, body: str) -> list[str]:
    # The first prose paragraph after the topic title is the authored scope list.
    lines = [x.strip() for x in body.splitlines() if x.strip() and not x.startswith("#")]
    if not lines: raise ValueError(f"no scope paragraph in {topic_path}")
    return split_terms(lines[0])

def chunks(xs: list[str], size: int = 4) -> list[list[str]]:
    return [xs[i:i+size] for i in range(0, len(xs), size)]

def title_for(items: list[str], idx: int) -> str:
    # A concrete lead term makes the graph label useful, with a short scope subtitle.
    head = re.sub(r"\s*\([^)]*\)", "", items[0]).strip()
    if len(head) > 68: head = head[:65].rstrip() + "…"
    suffixes = ["foundations", "mechanisms and methods", "applications and analysis", "integration and limits"]
    suffix = suffixes[min(idx, len(suffixes)-1)]
    return f"{head}: {suffix}"

def lesson_text(subject: str, topic_slug: str, topic_title: str, unit_title: str, items: list[str], prev_title: str | None) -> str:
    bullets = "\n".join(f"- **{x}** — define the object or process, name the conditions under which it applies, and connect it to the neighboring concepts in this unit." for x in items)
    prior = f"Build on **{prev_title}**: retrieve its key model before adding this unit's ideas.\n\n" if prev_title else ""
    return f'''# {unit_title}

## Core idea

{prior}This lesson narrows **{topic_title}** to a connected set of concepts. The scope terms below come from the subject outline; use them as a map of the model, not as a vocabulary list to memorize in isolation.

{TOPIC_NOTES[subject][topic_slug]} For this unit, focus on **{items[0]}** and how it fits the wider model.

{bullets}

## How to reason through the material

{METHOD[subject]}

For each item, make a three-column note: what it describes, what evidence or operation identifies it, and how changing one relevant condition changes the prediction. Then draw arrows between the items to show whether they represent prerequisites, steps in a process, alternative models, or ways of measuring the same system. Do not assume that two adjacent terms have a causal relationship unless the model or evidence supports it.

## Worked study example

Choose **{items[0]}** from the list. State a concrete question that can be answered using it; write down the system boundary, observations available, assumptions, and expected result. Work from the definition or governing model to the result, and annotate each step with why it is valid. Change one condition and predict the effect before looking up the answer. If the prediction fails, identify whether the cause is a violated assumption, a measurement issue, or a mistaken link between concepts.

## Check your understanding

1. Explain the difference between the first two concepts in your own words, including one condition that changes how they should be used.
2. Give an example where a learner could recognize the vocabulary but still apply the model incorrectly. State the correction.
3. What observation, calculation, or test would most directly challenge your explanation?

## Retrieval practice

Close the lesson and reconstruct the concept map from memory. Work one example without notes, then explain the assumptions and one limitation. Revisit the hardest step after a delay and solve a changed example.
'''

def qbank(subject: str, topic_title: str, unit_title: str, items: list[str], sid: str) -> dict:
    # Two scope checks make the local question bank genuinely curriculum-specific;
    # the final item assesses transferable reasoning in the subject's method.
    qs = []
    for n, concept in enumerate(items[:2], 1):
        opts = [concept] + DISTRACTORS[subject][:3]
        qs.append({
            "id": f"{slug(unit_title)}-{n}", "level": n,
            "stem": f"Which item is explicitly included in the scope of {topic_title} and this lesson?",
            "options": opts, "answer": 0,
            "hints": ["Use the lesson scope list.", f"Look for the concept {concept} in the unit."],
            "explanation": f"{concept} is one of the named concepts in this unit. Use its definition and relationships in context, rather than treating the name alone as understanding.",
        })
    if len(items) == 1:
        concept = items[0]
        qs.append({
            "id": f"{slug(unit_title)}-application", "level": 2,
            "stem": f"Before drawing a conclusion about {concept}, what should you do?",
            "options": [
                "Define how the concept is used in this problem and check the relevant assumptions or evidence.",
                "Assume the term has the same meaning in every context.",
                "Ignore conditions that could limit the model.",
                "Accept the first plausible result without checking it.",
            ], "answer": 0,
            "hints": ["A familiar label does not establish that a model applies.", "Check the concept in its specific context."],
            "explanation": f"{concept} should be interpreted in context. {METHOD[subject]}",
        })
    stem, method_answer = METHOD_CHECKS[subject]
    qs.append({
        "id": f"{slug(unit_title)}-reasoning", "level": 3,
        "stem": stem,
        "options": [
            method_answer,
            "Apply a familiar rule without checking whether its assumptions fit.",
            "Report an outcome without retaining the evidence or inputs needed to reproduce it.",
            "Change several relevant conditions at once, making the cause of the outcome unclear.",
        ], "answer": 0,
        "hints": ["Choose evidence that tests the claim made in the question.", "Keep assumptions and the relevant comparison visible."],
        "explanation": f"{method_answer} {METHOD[subject]}",
    })
    return {"subtopic_id": sid, "questions": qs}

def main() -> None:
    for subject, prereq_map in PREREQS.items():
        root = ROOT / subject
        topic_paths = sorted(root.glob("*/README.md"))
        topic_fms = [(p, *fm_and_body(p)) for p in topic_paths]
        topics = {p.parent.name: (p.parent, fm) for p, fm, _ in topic_fms if fm.get("type") == "topic"}
        terminal_by_dir: dict[str, str] = {}
        for topic_path, fm, body in topic_fms:
            if fm.get("type") != "topic": continue
            topic_dir = topic_path.parent.name
            topic_id = fm["id"]
            terms = get_scope(topic_path, body)
            groups = chunks(terms, 4)
            existing = topic_dir / Path("core-concepts")
            # First concept unit deliberately keeps the previous stable node ID.
            units: list[tuple[str, str, list[str]]] = []
            for i, group in enumerate(groups):
                unit_title = title_for(group, i)
                folder = "core-concepts" if i == 0 else slug(group[0])
                sid = f"{topic_id}-core-concepts" if i == 0 else f"{topic_id}-{slug(group[0])}"
                units.append((folder, sid, group))

            # Resolve the topic prerequisites by directory slug. Keep graph edges
            # inside this course and use the final unit of each prerequisite topic.
            prereq_dirs = prereq_map.get(topic_dir, [])
            missing = [d for d in prereq_dirs if d not in topics]
            if missing: raise ValueError(f"{subject}/{topic_dir}: missing prerequisite topic folders {missing}")
            first_prereqs = [{"id": terminal_by_dir[d], "target_type": "subtopic", "strength": "recommended"}
                             for d in prereq_dirs if d in terminal_by_dir]
            # A forward reference can occur in a graph; IDs are deterministic.
            for d in prereq_dirs:
                if d not in terminal_by_dir:
                    dep_path = topics[d][0] / "README.md"
                    dep_id = topics[d][1]["id"]
                    dep_groups = chunks(get_scope(dep_path, fm_and_body(dep_path)[1]), 4)
                    dep_tail = dep_groups[-1]
                    first_prereqs.append({"id": f"{dep_id}-{slug(dep_tail[0])}" if len(dep_groups)>1 else f"{dep_id}-core-concepts",
                                          "target_type": "subtopic", "strength": "recommended"})

            previous_id = None
            previous_title = None
            for i, (folder, sid, group) in enumerate(units):
                unit_title = title_for(group, i)
                prereqs = first_prereqs[:] if i == 0 else [{"id": previous_id, "target_type": "subtopic", "strength": "recommended"}]
                # No self-topic edge; the course is the starting point for root topics.
                if not prereqs:
                    prereqs = [{"id": f"{subject}-course", "target_type": "course", "strength": "recommended"}]
                tag = slug(topic_dir)
                fmtext = yaml.safe_dump({
                    "id": sid, "type": "subtopic", "title": f"{unit_title} — study lesson",
                    "parent_topic": topic_id, "phase": str(fm.get("phase", "core")),
                    "estimated_minutes": max(45, min(100, 20 + 15 * len(group))),
                    "prerequisites": prereqs,
                    "learning_outcomes": [
                        f"explain the key ideas in {unit_title} and how they relate",
                        "apply an appropriate model or method to a worked example",
                        "state assumptions, check the result, and identify a limitation",
                    ], "tags": [subject, tag],
                }, sort_keys=False, allow_unicode=True)
                target = topic_path.parent / folder / "README.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"---\n{fmtext}---\n\n" + lesson_text(subject, topic_dir, fm["title"], unit_title, group, previous_title), encoding="utf-8")
                # Keep the old filename as a user-facing link for the first unit.
                bank_path = BANK / subject / f"{sid}.yaml"
                bank_path.parent.mkdir(parents=True, exist_ok=True)
                bank_data = qbank(subject, fm["title"], unit_title, group, sid)
                if subject == "physics" and i == 0 and topic_dir in LEGACY_PHYSICS_QUESTIONS:
                    preserved = [{k: v for k, v in q.items() if k != "subtopic_id"} for q in LEGACY_PHYSICS_QUESTIONS[topic_dir]]
                    bank_data["questions"] = preserved + bank_data["questions"]
                bank_path.write_text(yaml.safe_dump(bank_data, sort_keys=False, allow_unicode=True), encoding="utf-8")
                previous_id, previous_title = sid, unit_title
            terminal_by_dir[topic_dir] = units[-1][1]

            # Replace the one-lesson list with a stable subtopic index.
            listing = "\n".join(f"- [{title_for(g, i)}](./{folder}/README.md) (`{sid}`)" for i, (folder, sid, g) in enumerate(units))
            new_body = re.sub(r"## Study lesson\n.*?(?=\n## |\Z)", "## Subtopics\n\n" + listing + "\n", body, flags=re.S)
            if new_body == body:
                # Previous topic page may already have a Subtopics section.
                new_body = re.sub(r"## Subtopics\n.*?(?=\n## |\Z)", "## Subtopics\n\n" + listing + "\n", body, flags=re.S)
            topic_path.write_text(f"---\n{yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)}---\n{new_body}", encoding="utf-8")

        # Update the graph note to reflect the expanded unit structure.
        course_path = root / "README.md"
        cfm, cb = fm_and_body(course_path)
        cb = cb.replace("each nested `core-concepts/README.md` is a graph-linked `subtopic` teaching resource", "each topic's linked lesson pages are graph-linked `subtopic` teaching resources")
        course_path.write_text(f"---\n{yaml.safe_dump(cfm, sort_keys=False, allow_unicode=True)}---\n{cb}", encoding="utf-8")

if __name__ == "__main__":
    main()
