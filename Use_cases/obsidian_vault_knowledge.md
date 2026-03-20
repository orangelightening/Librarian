# Use Case: Personal Knowledge Management (Obsidian Vault)

## Scenario

A researcher's personal Obsidian vault contains:
- Research notes and ideas
- Book summaries and highlights
- Project documentation
- Meeting notes and decisions
- Reference materials

**Challenge:** Find connections across topics that aren't obviously linked.

## Specialist Persona: Knowledge Synthesizer

The Librarian adopts a **specialist knowledge synthesizer persona** to:
- Find thematic connections across unrelated notes
- Identify gaps in research coverage
- Suggest relevant notes based on current context
- Generate literature review summaries
- Create knowledge maps

## Chat Example

```
User: I'm writing about machine learning interpretability. What notes do I have that are relevant?

Librarian (Knowledge Synthesizer): I'll search your vault for relevant concepts and connections.

[Uses search_library for "machine learning interpretability"]

Librarian: Found 23 relevant notes. Let me organize them by theme:

**Core Concepts:**
- SHAP values and feature importance
- LIME and local interpretability
- Model-agnostic approaches
- Black box vs. white box models

[Uses search_documents to find cross-references]

Librarian: I also found connections to notes you might not expect:

**Unexpected Connections:**
- "Medical diagnosis transparency" notes (similar interpretability challenges)
- "Financial model explainability" (regulatory requirements)
- "Cognitive psychology" (human decision-making parallels)

[Uses read_document for related notes]

Librarian: Based on your research, I found a potential gap:
You have extensive notes on technical methods but limited coverage of:
- Human-centered evaluation approaches
- Regulatory requirements for explainable AI
- User interface design for interpretability

[Uses write_document]

Librarian: I've created a knowledge map at
/librarian/knowledge/ml_interpretability_map.md showing:
- All relevant notes with connections
- Thematic clusters
- Research gaps identified
- Suggested reading order

Would you like me to generate a literature review summary?

User: Yes, focus on the regulatory aspects.

Librarian: Searching for regulatory and governance notes...
```

## Key Benefits

**Privacy First:**
- ✅ Personal knowledge never exposed to cloud
- ✅ Private thinking remains private
- ✅ No data mining on your ideas

**Specialist Value:**
- ✅ Finds non-obvious connections
- ✅ Identifies knowledge gaps
- ✅ Suggests relevant context
- ✅ Generates knowledge maps

**Two-Way Communication:**
- ✅ Writes knowledge maps
- ✅ Creates literature reviews
- ✅ Generates reading lists

## Document Types

**Note Types:**
- Concept notes
- Meeting notes
- Book summaries
- Project documentation
- Reference materials
- Quotes and excerpts

**Connections:**
- Backlinks (Obsidian [[links]])
- Thematic tags
- Concept clusters
- Citation networks

## Output Location

`/librarian/knowledge/` - Knowledge synthesis outputs
- ml_interpretability_map.md
- literature_review_summary.md
- knowledge_gap_analysis.md
- reading_suggestions.md

---

*Use Case: Personal Knowledge Management*
*Specialist Persona: Knowledge Synthesizer*
*Privacy: Personal Knowledge Remains Personal*
