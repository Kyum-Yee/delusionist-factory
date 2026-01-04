# Delusionist Factory

> A Meta-Creative Engine for AI-Driven Ideation via Stochastic Context Pollution

## 🧠 What is this?

Traditional LLMs optimize for probability—they predict the "most likely" next token. This is mimicry, not creativity.

**Delusionist Factory** flips this paradigm. It deliberately pollutes the context with random, unrelated tokens, forcing the AI to hallucinate novel conceptual bridges. The result? Ideas that could never emerge from a clean context.

## ⭐ Recommended Setup (Official Guide)

> **Best Performance: Use with Code Editor AI Agents**

This project performs best when used with **AI agents integrated into code editors** (e.g., Cursor, GitHub Copilot Chat, Claude for VS Code, Gemini Code Assist).

**Why?** Code agents have direct access to the project's file context—they can read `request.json`, execute `main.py`, and write to output files autonomously. This enables true **one-click execution** of the entire pipeline.

**How to use:**
1. Open this project folder in your code editor
2. Copy the prompt from `prompt.txt`
3. Paste it to your code agent
4. Watch it complete all 3 steps automatically

---

## 🚀 Quick Start

1. **Configure your topic** in `input/request.json`
2. **Run the engine**: `python main.py`
3. **Follow agent instructions** to generate chains
4. **Repeat** until "ALL STEPS COMPLETE"

Or use the **One-Click Prompt** in `prompt.txt` with any AI agent.

## 📁 Project Structure

```
delusionist_factory/
├── input/
│   ├── request.json      # Configuration (topic, keywords, etc.)
│   └── 100000word.txt    # Random word pool (100k words)
├── output/
│   ├── section_a_chains.txt   # Step 1: Raw delusional chains
│   ├── section_b_refined.txt  # Step 2: Refined sentences
│   └── section_c_final.txt    # Step 3: Final output
├── staging/
│   └── state.json        # Progress tracking
├── main.py               # Engine core
├── prompt.txt            # One-click AI agent prompt
└── README.md
```

## ⚙️ Configuration (request.json)

| Field | Description | Example |
|-------|-------------|---------|
| `STARTING_SENTENCE` | Topic/seed sentence | `"AI creativity mechanisms"` |
| `MANDATORY_WORD` | Required words in every chain | `["entropy", "bridge"]` |
| `PREFERRED_IMAGERY` | Reference imagery for AI | `["neural", "chaos"]` |
| `CHAINS_COUNT` | Number of chains in Step 1 | `120` |
| `MODE_SELECTION` | `"CHAOS"` (70% random) or `"NUANCE"` (30% random) | `"CHAOS"` |
| `SELECTION_B_COUNT` | Refined sentences in Step 2 | `8` |
| `REFINING_COUNT` | Final outputs in Step 3 | `2` |
| `DIRECTION` | Direction for final output | `"Generate innovative..."` |
| `FINAL_LANGUAGE` | Output language | `"English"` or `"Korean"` |

## 🔄 Reset

```bash
rm -rf output/* staging/*
```

## 💡 Core Mechanism

### The "Context Pollution" Protocol

| Step | Name | Mechanism |
|------|------|-----------|
| 1 | **Injection** (Chaos) | Inject unrelated random tokens from 100k-word pool |
| 2 | **Forced Integration** (Bridge) | Force LLM to treat noise as signal → novel bridges emerge |
| 3 | **Refinement** (Convergence) | Extract structural logic, discard noise → "Delusional Variation" |

### Why it works

An LLM cannot surprise itself—it only moves within its probability distribution. External randomness (Python's `random.sample`) breaks that distribution.

> **Creativity is not a command. It's a consequence of environment.**

## 📜 License

MIT License
