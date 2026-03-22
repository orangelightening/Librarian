These are **GGUF quantization suffixes** used by llama.cpp and related tools. Let me break it all down:

## The Quantization Suffix System

### The "K" suffix — K-quants

The `_K` means **K-quant**, a smarter quantization method that uses a mix of block sizes and applies different precision to different parts of the model (attention layers vs feed-forward layers). It generally gives better quality than the old "legacy" quants at the same bit count.

So `Q5_K` isn't just "5-bit" — it's "5-bit using the K-quant method."

---

### The size modifier after K — `_S`, `_M`, `_L`

When you see `Q5_K_S` vs `Q5_K_M`, this refers to how the K-quant budget is **distributed across different layer types**:

|Suffix|Meaning|Tradeoff|
|---|---|---|
|`_S`|**Small** — more layers get the lower-bit treatment|Smallest file, slightly lower quality|
|`_M`|**Medium** — mixed strategy, balanced|Middle ground (most popular choice)|
|`_L`|**Large** — more layers get higher-bit treatment|Larger file, better quality|

So `Q5_K_M` is generally the recommended sweet spot, while `Q5_K_S` saves a bit more RAM at a small quality cost.

---

### The `IQ` prefix — iQuants (importance-matrix quants)

`IQ` quants are a newer, more sophisticated method. Instead of quantizing all weights equally within a block, they use an **importance matrix** to figure out which weights matter more and preserve those more carefully.

|Name|Approx bits|Notes|
|---|---|---|
|`IQ1_S`|~1.5 bit|Extremely aggressive, mostly experimental|
|`IQ2_XXS`|~2.1 bit|Very small, surprisingly usable|
|`IQ2_XS`|~2.3 bit||
|`IQ2_S` / `IQ2_M`|~2.5–2.7 bit||
|`IQ3_XXS`|~3.0 bit||
|`IQ3_XS`, `IQ3_S`, `IQ3_M`|~3.x bit||
|`IQ4_XS`|~4.25 bit|Very popular, excellent quality/size ratio|
|`IQ4_NL`|~4.5 bit|"Non-linear" variant|

The size tags go: `XXS < XS < S < M` (extra-extra-small up to medium).

---

### The `UD` prefix — Unsloth Dynamic quants

`UD-IQ3_XXS` means it's an **Unsloth Dynamic** quant. Unsloth applies different quantization levels to **different layers** based on their sensitivity — critical layers (like the first and last) stay at higher precision, while middle layers get compressed more. This gives better quality than a uniform quant at the same average file size.

---

### Quick reference cheat sheet

|You see|What it means|
|---|---|
|`Q4_K_M`|4-bit, K-quant method, medium distribution — the classic "just works" pick|
|`Q5_K_S`|5-bit, K-quant, small (more aggressive compression)|
|`Q6_K`|6-bit K-quant (no size variant — only one exists at Q6)|
|`Q8_0`|8-bit, legacy method, near-lossless, large file|
|`IQ4_XS`|~4.25-bit importance-matrix quant, very efficient|
|`UD-IQ3_XXS`|Unsloth Dynamic ~3-bit, intelligently layered|
|`F16`|Full 16-bit float, no quantization at all|

---

### General recommendation ladder

If you're just picking one and unsure: **Q4_K_M** is the community default. **IQ4_XS** is often slightly smaller with similar quality. **Q5_K_M** if you have the VRAM to spare. **UD quants** from Unsloth are worth trying if they're available for your model — they punch above their weight.

I just downloaded the Q6_K. I am having a problem with the 4b models ignoring system prompt instructions when it suits them. Its an old story I know. which of the 9b series would you recommend.

22:58

Good choice on Q6_K — that's essentially near-lossless quality for a 6-bit quant, so you're getting pretty much the best the model can offer.

On the system prompt compliance issue — yeah, 4B models are notoriously "creative" about following instructions. The smaller the model, the more it prioritizes what feels like a natural completion over what you actually told it to do.

For the **Qwen3.5-9B** series I'd suggest:

**Q4_K_M** is probably the pragmatic pick at 9B. Here's the reasoning:

The jump from 4B to 9B is where instruction-following gets meaningfully better — it's not just "more of the same," the model actually has enough capacity to hold the system prompt in mind while generating. The compliance issue you're seeing is largely a **model size problem**, not a quantization problem, so you don't need to chase Q6_K at 9B unless your hardware is comfortable with it.

**Q4_K_M at 9B** will likely outperform **Q6_K at 4B** on instruction following by a noticeable margin.

If your hardware can handle it comfortably, **Q5_K_M** is a nice middle ground — meaningfully better than Q4_K_M, and the file size is still manageable.

**Q6_K at 9B** is excellent if you have the VRAM/RAM headroom, but the gains over Q5_K_M are smaller than you might expect — you'd probably see more improvement going from 4B→9B at any quant level than from Q4→Q6 at the same model size.

---

