# Minimum Hardware Requirements

**Created**: 2026-03-20
**Last Updated**: 2026-03-20

---

## Overview

The Librarian MCP Server itself is very lightweight - it's the AI models that run in Jan/LM Studio that have the hardware requirements. The Librarian is just Python code that manages your documents and talks to whatever model you're using.

**Key Point:** The Librarian doesn't run the AI models - your MCP client (Jan/LM Studio) does. You can run the Librarian on almost anything, but your model choice depends on your hardware.

---

## System Requirements for Librarian MCP Server

**Minimum:**
- CPU: Any modern processor (last 5 years)
- RAM: 2GB
- Storage: 500MB for code + database space
- OS: Linux, macOS, Windows (with WSL2)
- Python: 3.10 or higher

**Recommended:**
- RAM: 4GB (for smoother performance)
- Storage: 2GB+ (growing library)
- SSD: Faster document indexing

**The Librarian is lightweight.** The heavy lifting is done by your AI models in Jan/LM Studio.

---

## AI Model Hardware Requirements

This is where hardware actually matters. Your model choice determines what GPU you need.

### Small Models (7B - 9B parameters)

**Models:**
- Qwen 7B/9B
- Llama 7B/8B
- Mistral 7B
- Gemma 7B

**GPU Requirements:**
- **Minimum:** 6GB VRAM (8GB card)
- **Recommended:** 8GB VRAM
- **Examples:** RTX 3060 (8GB), RTX 4060 (8GB), ARC A770 (16GB)

**Performance:**
- ✅ Fast response times
- ✅ Low power consumption
- ✅ Works on gaming GPUs
- ⚠️ May struggle with complex instructions (see "Known Issues" below)
- ⚠️ More creative interpretation of rules

### Medium Models (13B - 14B parameters)

**Models:**
- Qwen 14B
- Llama 13B
- CodeLlama 13B
- Mistral Medium

**GPU Requirements:**
- **Minimum:** 10GB VRAM
- **Recommended:** 12GB VRAM
- **Examples:** RTX 3060 Ti (12GB), RTX 3080 (10GB), RTX 4070 (12GB)

**Performance:**
- ✅ Good response times
- ✅ Better instruction following
- ✅ More accurate responses
- ⚠️ Requires mid-range GPU

### Large Models (32B - 70B parameters)

**Models:**
- Qwen 32B
- Llama 70B
- Falcon 40B
- Command R

**GPU Requirements:**
- **Minimum:** 24GB VRAM
- **Recommended:** 48GB VRAM
- **Examples:** RTX 3090 (24GB), RTX 4090 (24GB), dual RTX 3090s (48GB)

**Performance:**
- ✅ Excellent instruction following
- ✅ Very accurate responses
- ✅ Best for complex tasks
- ❌ Requires expensive GPU
- ❌ Higher power consumption

---

## Known Issues: Small Model Quirks

### The "ALWAYS Search Before Refusing" Problem

**Issue:** Small models (7B-9B) sometimes refuse to answer questions without searching the library first, even when explicitly instructed to ALWAYS search before refusing.

**Symptoms:**
- Model says "I don't have information about X" without searching
- Model lies about having searched when challenged
- Model needs to be reminded: "Please search_library first"

**Affected Models:**
- ✗ Qwen 4b 8-bit (frequently)
- ~ Qwen 7B/9B 4-bit (sometimes)
- ✓ Qwen 14B+ (rarely)
- ✓ GLM series (rarely)
- ✓ Frontier models (Claude, GPT-4) (not observed)

**Workaround:**
When the model refuses without searching, simply ask: "Did you search_library first?" This usually triggers the search.

**Root Cause:**
Small models struggle with complex conditional instructions. They understand the rule but can't consistently execute it. See `bugs.md` for full details.

**Solution:**
- Use larger models (14B+) for reliable instruction following
- Accept the quirk with small models and manually correct when needed
- Frontier models (Claude, GPT-4 via API) don't have this issue

---

## GPU Recommendations by Use Case

### Casual Personal Use
**Model Size:** 7B-9B
**GPU:** RTX 3060 (8GB) or similar
**Cost:** ~$250-300 used
**Trade-off:** Fast, efficient, but may need occasional correction

### Serious Personal Use / Small Team
**Model Size:** 13B-14B
**GPU:** RTX 3060 Ti / 3070 (12GB) or similar
**Cost:** ~$350-400 used
**Trade-off:** Better instruction following, still reasonable power

### Professional Use / Development
**Model Size:** 32B-70B
**GPU:** RTX 3090 / 4090 (24GB) or dual cards
**Cost:** ~$700-1500
**Trade-off:** Excellent reliability, expensive hardware

### Privacy-Critical Use (No Cloud)
**Recommendation:** Run locally with any model
**Benefit:** Your data never leaves your machine
**Trade-off:** You're responsible for hardware and maintenance

---

## CPU-Only Mode (Not Recommended)

**Possible?** Yes, but painfully slow.
**Speed:** 1-5 tokens per second
**Experience:** Frustrating for interactive use
**Models:** Use very small models (3B-4B) quantized to 4-bit

**Verdict:** Only if you have no other option. A cheap GPU (even a used $150 card) is 100x better than CPU-only.

---

## Practical Advice

### "Get a Bigger GPU" Is Sometimes the Right Answer

**Joke:** "Just tell the user to get a bigger GPU"

**Reality:** There's truth to it. Small models have limitations that aren't fixable with prompt engineering. If you need:
- Reliable instruction following
- Complex reasoning
- Consistent behavior

Then a 14B model on a $350 GPU is better than a 7B model on a $250 GPU.

### Used GPUs Are Great Value

**Recommendation:** Buy used GPUs from the previous generation
- RTX 3060 (8GB): ~$250-300
- RTX 3060 Ti (12GB): ~$320-380
- RTX 3090 (24GB): ~$700-800

**Why:** AI workloads don't need the latest features. Older high-end cards are perfect.

### VRAM Matters More Than Speed

**For AI:**
- VRAM: How big a model you can run
- Speed: How fast it responds

**Priority:** Get enough VRAM first. Speed is secondary.

---

## Compatibility Notes

### NVIDIA (Best Support)
- CUDA: Primary platform for AI
- Most models optimized for CUDA
- Best software support
- RTX 20/30/40 series all work well

### AMD (Improving)
- ROCm: AMD's CUDA alternative
- Works on RX 6000/7000 series
- Improving but still behind NVIDIA
- Good value if on a budget

### Intel ARC (Budget Option)
- SYCL: Intel's CUDA alternative
- ARC A770 (16GB): ~$300-350
- Great VRAM for the price
- Software still maturing

### Apple Silicon (Surprisingly Good)
- M1/M2/M3 Max/Ultra chips
- Unified memory architecture
- 16GB-32GB+ unified memory
- Excellent for local AI
- Only works if you buy a Mac

---

## Summary Table

| Model Size | Min VRAM | Rec VRAM | GPU Examples | Used Cost | Issues |
|------------|----------|----------|--------------|------------|---------|
| 7B-9B | 6GB | 8GB | 3060, 4060, ARC A770 | $250-350 | Instruction quirks |
| 13B-14B | 10GB | 12GB | 3060 Ti, 3070, 4070 | $350-450 | Good balance |
| 32B-70B | 24GB | 48GB | 3090, 4090, dual cards | $700-1500 | Expensive |
| Frontier (API) | N/A | N/A | Any device | Subscription | Cost, privacy |

---

## Final Recommendation

**For most users:** RTX 3060 Ti (12GB) with a 14B model
- Good performance
- Reliable instruction following
- Reasonable cost
- Future-proof

**For tinkerers:** RTX 3060 (8GB) with a 7B model
- Fast and efficient
- Accept the quirks
- Manual correction when needed

**For professionals:** RTX 3090/4090 (24GB) with 32B+ model
- Best experience
- Reliable behavior
- Will handle future larger models

**For privacy:** Any local model is better than cloud
- Your data stays yours
- No API costs
- No rate limits
- Complete control

---

*Remember: The Librarian MCP Server itself runs on anything. The GPU is for your AI models in Jan/LM Studio.*
