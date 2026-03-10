 
Project Compass: Hobby Finder
Purpose of This Document
This document defines the common direction for the Hobby Finder project. It acts as a compass to help human developers and AI agents align their work. It is not a rigid contract: within this direction, contributors are encouraged to innovate and improve. Changes to the core principles and architecture described here should be proposed and agreed upon before being implemented.
Project Goal
The goal of Hobby Finder is to build a system that evaluates whether a given activity counts as a hobby for a particular person. The system is based on four components:
Definition Research – analyse existing definitions to extract core hobby criteria.
Activity Knowledge Base – a curated catalogue of potential activities, including categories, aliases and descriptive attributes.
Matching Engine – map user‑entered text to standard activity entries and assign basic attributes.
Hobby Qualification – combine the activity attributes with user context to determine hobby status (active hobby, dormant, former, interest or no hobby).
Architecture Overview
The project is organised as a set of modules:
research/ – code and data used to analyse definitions of “hobby” and derive core hobby features.
knowledge_base/ – the activity catalogue and any scripts to manage it. Each activity includes categories, synonyms and graded descriptive attributes (physical, creative, social, technical, etc.).
matching/ – the normalisation and matching logic that translates free‑form text into a standard activity. This includes normalisers, alias lookups, fuzzy matching and a confidence mechanism.
qualification/ – the logic that determines whether a matched activity qualifies as a hobby for an individual. It combines the activity profile with user answers about frequency, voluntariness, interest, etc., and produces a hobby status.
app/ – the interface layer (APIs or UI) that interacts with users. The app should use, but not duplicate, the underlying knowledge base and engines.
A pipeline step proceeds from the activity input through matching and attribute loading to the final hobby classification. The modules are designed to be loosely coupled: improvements in one layer should not require rewriting the others.
Guiding Principles
These principles should guide development:
Separation of Concerns – keep research, matching, and qualification logic in separate modules. Activities have descriptive attributes; hobby status is evaluated separately.
Explainability – each classification should be accompanied by a rationale. The user should understand why their activity was classified in a certain way.
Knowledge Base First – a curated list of activities and attributes is more robust and maintainable than trying to infer everything on the fly.
Flexibility for Developers and Agents – agents may refactor code, add tests, improve performance or extend data, provided they respect the core direction described here. They should propose larger architectural changes rather than implementing them silently.
Incremental Enhancement – improvements to matching algorithms, confidence scoring or attribute modelling are welcome as long as they fit within the overall pipeline.
Agent Contribution Guidelines
Agents and automated tools are empowered to contribute significantly to the project. To maintain coherence:
Allowed without proposal
Fix bugs and add tests.
Refactor modules internally without altering the high‑level pipeline.
Expand the activity catalogue with new entries, synonyms and descriptive attributes.
Optimise performance and code readability.
Extend documentation (including this compass) with clarifications or examples.
Require proposal
Introducing new modules or renaming existing ones.
Changing the data model of activities or hobby qualification criteria.
Adding or removing core hobby criteria derived from definition research.
Altering the pipeline flow (e.g. merging matching and qualification).
Switching runtime dependencies (e.g. adding a large language model in production).
Not allowed without explicit approval
Changing the project goal.
Removing or bypassing the knowledge base and matching engine in favour of an opaque AI model.
Editing this Project Compass to reflect a new direction without prior agreement.
Open Questions and Tasks
This document can also capture outstanding tasks that align with the current direction. Examples:
Finalise the list of core hobby criteria extracted from definition analysis.
Clean up and extend the activity catalogue with categories and aliases.
Implement and evaluate a confidence scoring mechanism in the matching engine.
Define the scoring thresholds for active, dormant and former hobbies.
Contributors are welcome to suggest additional tasks or improvements. Use this file as a living compass to stay aligned on the project's objectives while allowing room for creative solutions.
