# Hacker News Post Template

**Title:**
ChainObserver: Diagnose Failed Ethereum Transactions in ~25 Seconds with Gemini 2.5 Flash

**URL:**
https://github.com/observer-ai-org/chainobserver

**Description (first 80 chars):**
AI agent that instantly diagnoses why your Ethereum transactions failed using agentic reasoning + custom MCP tools.

---

**Comment Template (if asked "Tell us more"):**

We built ChainObserver because every Ethereum developer knows the pain: a transaction fails with a cryptic hex error code or "execution reverted" — and debugging takes 20-60 minutes.

**What it does:**
- Paste a failed tx hash
- Gemini 2.5 Flash reasons over 5 custom Ethereum MCP tools
- You get root cause + fix in ~25 seconds

**The tech:**
- **Agentic loop:** Gemini decides which tools to call and when it has enough info
- **Tool standardization:** Model Context Protocol (MCP) for clean, typed tool interfaces
- **Bounded safety:** ≤5 tool calls per diagnosis (3.25 avg) — it never spirals
- **Multi-chain:** Works on Ethereum, Arbitrum, Base, Optimism, Polygon

**Real benchmarks:**
- 100% correct classification across 8 real mainnet failures (6 categories)
- 21.8s avg diagnosis · 3.25 tool calls on the timed runs
- 123 tests passing

**Why we built it:**
- A showcase of Gemini 2.5 Flash doing genuine agentic reasoning over MCP tools
- Phase 1 of an open-source diagnostic-agent ecosystem (observer-ai)

**Try it:** https://johnlee007-chainobserver.hf.space
**Repo:** https://github.com/observer-ai-org/chainobserver (MIT)
**Roadmap:** We're building the same pattern for GitHub Actions, Kubernetes, SQL, and logs next. Contributions welcome.
