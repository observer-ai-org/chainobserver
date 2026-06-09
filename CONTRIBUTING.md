# Contributing to Observer AI

Thank you for your interest! We welcome contributions of all kinds — bug reports, docs, code, ideas.

## Getting Started

```bash
git clone https://github.com/<your-username>/chainobserver
cd chainobserver
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
pytest
```

## How to Contribute

### 🐛 Bug Report
1. Check existing issues
2. Include reproduction steps + environment
3. Provide full error message

### ✨ Feature Request
1. Describe use case
2. Provide examples
3. Check [docs/AGENTS.md](./docs/AGENTS.md) for roadmap

### 🔨 Code Contribution

**Small fix (docs, typo):**
- Fork → branch → fix → pytest → commit → PR

**Medium change (new chain, feature):**
- Open issue first to discuss
- Fork → branch → implement with tests → benchmark → PR

**Large change (new MCP tool, refactor):**
- Open issue first
- Implement with tests
- Benchmark against real data
- Update docs → PR

## Testing

```bash
pytest                        # all tests
pytest tests/unit/            # unit only
pytest tests/integration/     # integration (needs GOOGLE_API_KEY)
pytest --cov=chainobserver    # with coverage
```

## Adding a New Chain

```python
# 1. Edit chainobserver/chains.py
CHAINS = {
    "your-chain": {"id": 12345, "name": "Your Chain", "rpc": "https://..."}
}

# 2. Add test case with real failed tx
# 3. Run: pytest tests/integration/test_chains.py::test_diagnose_your_chain
# 4. Submit PR
```

## Coding Standards

- **Style:** PEP 8 (black + ruff)
- **Types:** Required for all functions
- **Comments:** Only for WHY, not WHAT
- **Imports:** Organized (stdlib → third-party → local)

## Commit Message Format

```
<type>(<scope>): <subject>

<body — why this change>

Closes #<issue>
```

Types: `fix`, `feat`, `docs`, `test`, `refactor`  
Scope: `mcp`, `agent`, `chains`, `server`

## PR Checklist

- [ ] Tests pass: `pytest --cov`
- [ ] Code follows style guide
- [ ] No secrets/API keys
- [ ] Docs updated if needed
- [ ] Real test case included (for features)
- [ ] Commit messages clean

## Questions?

Open an issue. We're here to help! 💪

---

**Building a new agent?** See [docs/AGENTS.md](./docs/AGENTS.md) for the full roadmap.
