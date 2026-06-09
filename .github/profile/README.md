# observer-ai

> **Agentic observability for every platform.**

We're building 5 diagnostic agents that use Gemini 2.5 Flash + MCP to instantly diagnose failures across:
- **Ethereum** (on-chain transactions)
- **GitHub** Actions (CI/CD pipelines)  
- **Kubernetes** (pod failures)
- **SQL** (slow queries, deadlocks)
- **Logs** (distributed traces)

## 🎯 Current Focus

### ✅ ChainObserver (Live Now)
**Diagnose failed Ethereum transactions in ~25 seconds**

- 7 failure types covered (slippage, insufficient balance, OOG, custom reverts, etc.)
- 100% accuracy across 4 test cases
- Multi-chain support: Ethereum, Arbitrum, Base, Optimism, Polygon
- **114 tests passing** · Open source (MIT) · Built for ETHGlobal Lisbon 2026

👉 **Try it:** https://chainobserver.hf.space

### 🚀 Coming Next
- **GitHubGuard** (June 18) — GitHub Actions workflow diagnostics
- **KubeObserver** (July 10) — Kubernetes pod failure diagnosis
- **QueryDebugger** (July 20) — SQL query optimization + deadlock detection
- **LoggingAgent** (Aug+) — Distributed trace analysis

## 📂 Repositories

| Repo | Status | Description |
|------|--------|-------------|
| [chainobserver](https://github.com/observer-ai/chainobserver) | ✅ Live | Ethereum transaction diagnostics |
| [pipelineguard](https://github.com/observer-ai/pipelineguard) | ✅ Live | GitLab CI diagnostics (origin agent) |
| [observer-ai.dev](https://github.com/observer-ai/observer-ai.dev) | 🚀 Coming | Landing page + SaaS dashboard |

## 🤝 Contributing

**Want to build a diagnostic agent?** See [chainobserver/docs/AGENTS.md](https://github.com/observer-ai/chainobserver/tree/main/docs/AGENTS.md) for:
- How to build a full agent (GitHubGuard, etc.)
- How to create a standalone MCP server
- How to add support for a new blockchain

**All skill levels welcome** — from bug reports to full feature implementations.

## 📊 Stats

- **114 tests passing** across all agents
- **8 real-world failure cases** in benchmarks
- **4.9s avg diagnosis time** (Ethereum)
- **100% accuracy** on supported failure types
- **Multi-chain support** (5 blockchains)

## 🎓 Built With

- **Gemini 2.5 Flash** — Agentic reasoning + tool calling
- **Model Context Protocol (MCP)** — Standardized tool interface
- **Python 3.11+** — Fast, type-safe
- **FastAPI** — REST endpoints
- **Pydantic** — Structured output validation

## 📧 Get Involved

- **GitHub Issues:** Bug reports & feature requests
- **GitHub Discussions:** Ideas & architecture questions
- **Twitter:** [@observer_ai](https://twitter.com/observer_ai) (updates coming soon)

---

**Mission:** Make debugging fast, cheap, and accessible. One agent at a time.

**Status:** Actively building for ETHGlobal Lisbon 2026 + Build with Gemini XPRIZE.

