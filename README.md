# ChainObserver

[![Tests](https://github.com/observer-ai/chainobserver/actions/workflows/test.yml/badge.svg)](https://github.com/observer-ai/chainobserver/actions/workflows/test.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ETHGlobal Lisbon 2026](https://img.shields.io/badge/ETHGlobal-Lisbon%202026-purple)](https://ethglobal.com)

> **AI agent that diagnoses failed Ethereum transactions in under 30 seconds**

Paste a failed tx hash → get root cause + fix, powered by **Gemini 2.5 Flash** and custom Ethereum MCP tools. Supports mainnet, Arbitrum, Base, Optimism, and Polygon.

## 🚀 Try It Now

**Web:** https://chainobserver.hf.space  
**API:** `POST /diagnose` with `{tx_hash: "0x..."}`

## 💡 The Problem

Every Ethereum developer has been here: transaction fails with `0xa1148100` or `execution reverted`. Diagnosing it takes:
- 5 min: Etherscan deep-dive
- 10 min: ABI lookup + selector decoding
- 5 min: Internal call trace
- **20 min total** per incident

ChainObserver does this in **~25 seconds** with 100% accuracy.

## ✅ Supported Failure Types

| Failure | Signal | Example |
|---------|--------|---------|
| **Slippage exceeded** | `INSUFFICIENT_OUTPUT_AMOUNT` | Uniswap swap |
| **Insufficient balance** | `transfer amount exceeds balance` | USDC transfer |
| **Missing approval** | `TRANSFER_FROM_FAILED` | ERC-20 allowance |
| **Out of gas** | `gas_used ≥ 98% of limit` | Complex DeFi tx |
| **Custom revert** | custom error code | Seaport, ParaSwap |
| **Access control** | `not owner / missing role` | Admin-only function |
| **Pool too thin** | low reserves | DEX with low liquidity |

## 📊 Benchmarks

**4/4 test cases · 100% accuracy · 21.8s avg diagnosis**

| Transaction | Type | Time | Tool Calls | Accuracy |
|------------|------|------|------------|----------|
| Uniswap swap | INSUFFICIENT_ALLOWANCE | 18.6s | 3 | ✅ |
| DEX swap | SLIPPAGE_EXCEEDED | 21.4s | 3 | ✅ |
| USDC transfer | INSUFFICIENT_BALANCE | 11.9s | 3 | ✅ |
| Seaport order | CONTRACT_REVERT | 36s | 4 | ✅ |

**79 unit tests · all 7 failure types verified · multi-chain tested**

## 🔧 Quick Start

### Installation

```bash
git clone https://github.com/observer-ai/chainobserver
cd chainobserver
pip install -e .
```

### Usage

```bash
export GOOGLE_API_KEY="your-gemini-api-key"

# Diagnose a failed transaction
chainobserver diagnose 0xaa78010df34b38c16b5168ada399b840162bbf3566b398025cad7ba69581bab5

# Diagnose on Arbitrum
chainobserver diagnose 0x... --chain 42161
```

### Response

```json
{
  "root_cause": "Contract not approved to spend ERC-20 tokens from sender's address",
  "failure_type": "insufficient_allowance",
  "confidence": "high",
  "affected_components": ["Token.approve()", "Router.execute()"],
  "fix_proposal": "Call approve() on the token contract before swap",
  "time_seconds": 18.6,
  "tool_calls": 3,
  "related_link": "https://etherscan.io/tx/0xaa78010..."
}
```

## 📖 Documentation

- **[CHAINOBSERVER.md](./CHAINOBSERVER.md)** — Full design doc + architecture deep-dive
- **[BENCHMARKS.md](./BENCHMARKS.md)** — Detailed test results for each failure type
- **[docs/AGENTS.md](./docs/AGENTS.md)** — Roadmap for 5 derivative agents
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** — How to build your own agent

## 🌍 Supported Chains

| Chain | Chain ID | Status |
|-------|----------|--------|
| Ethereum | 1 | ✅ Tested |
| Arbitrum One | 42161 | ✅ Tested |
| Base | 8453 | ✅ Tested |
| Optimism | 10 | ✅ Tested |
| Polygon | 137 | ✅ Tested |

## 🔌 API Integration

Deploy as a service and integrate via REST:

```python
import requests

response = requests.post(
    "https://chainobserver.example.com/diagnose",
    json={"tx_hash": "0xaa78010df34b38c16b5168ada399b840162bbf3566b398025cad7ba69581bab5"}
)

diagnosis = response.json()
print(f"Root cause: {diagnosis['root_cause']}")
```

## 📦 Deployment

### Hugging Face Spaces (Free)
```bash
huggingface-cli repo create chainobserver --type space
git remote add hf https://huggingface.co/spaces/yourname/chainobserver
git push hf main
```

### Docker
```bash
docker build -t chainobserver .
docker run -p 7860:7860 -e GOOGLE_API_KEY=$GOOGLE_API_KEY chainobserver
```

## 🤝 Contributing

We welcome forks, issues, and pull requests! See [CONTRIBUTING.md](./CONTRIBUTING.md).

**Community projects:** See [docs/AGENTS.md](./docs/AGENTS.md) for how to build GitHub, Kubernetes, or SQL diagnostic agents.

## 📄 License

MIT — See [LICENSE](./LICENSE)

## 🙋 Support

- 📧 **Issues & bugs:** [GitHub Issues](https://github.com/observer-ai/chainobserver/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/observer-ai/chainobserver/discussions)

---

**Built for ETHGlobal Lisbon 2026 · Powered by Gemini 2.5 Flash · Open source (MIT)**
