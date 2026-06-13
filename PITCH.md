---
marp: true
theme: default
paginate: true
backgroundColor: #0B0E14
color: #E6EDF3
style: |
  section { font-size: 26px; }
  h1 { color: #7CC4FF; }
  strong { color: #C8F542; }
  code { color: #FFB454; }
---

<!-- ChainObserver — ETHGlobal Lisbon 2026 pitch deck.
     Render: npx @marp-team/marp-cli@latest PITCH.md --pdf   (or --pptx / --html)
     Each "---" starts a new slide. -->

# ChainObserver 🔍

### Paste a failed Ethereum tx → get the root cause **and** the fix — in **seconds**, not a 20-minute Etherscan dig

Powered by **Gemini 2.5 Flash** + custom Ethereum **MCP** tools

*ETHGlobal Lisbon 2026 · live at johnlee007-chainobserver.hf.space*

---

# The problem

Every Ethereum dev has stared at this:

> `execution reverted` · `0xa1148100` · `TRANSFER_FROM_FAILED`

Diagnosing one failed transaction means:

- 5 min digging through **Etherscan**
- decoding a **4-byte custom error** by hand
- guessing whether it's allowance, slippage, balance, gas, or a contract bug

**Multiply by every failed tx, every day.** The answer is on-chain — you just don't have time to dig it out.

---

# The solution

**One input: a tx hash. One output: a structured diagnosis.**

```
$ chainobserver 0xaa78010d...
```

- **Root cause** in plain English
- **Failure category** (allowance / slippage / balance / gas / revert)
- **The fix** — exactly what to do next
- **Confidence** + an Etherscan link

Works on **mainnet, Arbitrum, Base, Optimism, Polygon.**

---

# How it works

**An agent, not a script.** Gemini 2.5 Flash plans its own investigation over 5 purpose-built **Ethereum MCP tools**:

`get_transaction_receipt` → `decode_revert_reason` → `get_contract_info` → `simulate_transaction` → `get_pool_info`

- The model decides which tool to call next, and stops when confident (≤5 calls)
- Custom Solidity errors resolved via **4byte.directory** + **Sourcify**
- Reusable from any MCP client (Claude Desktop, Cursor) — the tools outlive the demo

---

# Proof — 8 real mainnet failures, 6 categories

| Failure type | Example | E2E time |
|---|---|---|
| insufficient_allowance | Uniswap Universal Router | 18.6s |
| insufficient_balance | USDC transfer | 11.9s |
| slippage_exceeded | DEX swap *(also CoW, ParaSwap)* | 21.4s |
| contract_revert | Seaport `0xa1148100` | ~36s |
| out_of_gas | gas at 99.5% of limit | tool-verified |

**8 / 8 correctly classified ✅** — and on the 4 end-to-end timed runs:
**100% accuracy · 21.8s avg · 3.25 tool calls (target ≤5).**
Decoded a Seaport custom error *and* a ParaSwap `QuoteExpired()` with **zero hardcoding.**

---

# Why it matters

- **Real intelligence, not a lookup table** — the agent reasons over live chain data and handles errors it's never seen.
- **MCP-native** — the 5 Ethereum tools are a reusable building block for the whole agent ecosystem, not a one-off.
- **Multi-chain from day one** — same agent, five networks.
- **Live now** — public, no install: `johnlee007-chainobserver.hf.space`.

---

# What's next

- Auto-suggest the corrected transaction (ready-to-send calldata)
- Wallet & block-explorer integration ("Diagnose" button on any failed tx)
- Expand the MCP toolset → L2-specific failure modes, MEV/sandwich detection
- Part of **observer-ai** — agentic diagnostics across platforms (see also: PipelineGuard for CI)

---

# ChainObserver

### Failed tx in. Root cause + fix out. In seconds.

**Try it:** johnlee007-chainobserver.hf.space
**Code:** github.com/observer-ai-org/chainobserver
**Built with:** Gemini 2.5 Flash · Ethereum MCP · Python

*Thank you — questions?*
