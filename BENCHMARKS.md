# ChainObserver Benchmarks

Testing across 4 real failed mainnet transactions covering the main failure categories.

## Target Metrics
- Diagnosis time: < 2 minutes (excluding API rate-limit waits)
- Tool calls: ≤ 5
- Classification accuracy: correct failure_type

---

## Test Results

### TX-1: INSUFFICIENT_ALLOWANCE — Uniswap Universal Router
**Hash:** `0xaa78010df34b38c16b5168ada399b840162bbf3566b398025cad7ba69581bab5`  
**Contract:** `0x66a9893c…` (Uniswap Universal Router — `execute(bytes,bytes[],uint256)`)  
**Revert:** `TRANSFER_FROM_FAILED`

| Metric | Result |
|--------|--------|
| Diagnosis Time | **18.6s** |
| Tool Calls | **3** |
| failure_type | `insufficient_allowance` ✅ |
| Confidence | **high** |
| Root Cause | "Contract not approved to spend ERC-20 tokens from sender's address" |
| Fix | "Call `approve()` on the token contract first" |

---

### TX-2: SLIPPAGE — DEX swap
**Hash:** `0x791cddd199261dbca8562001c55a0b11aa51cf22ba0681d926dfe85c9274f7d5`  
**Contract:** `0x278d858f…` (DEX aggregator — `0x70521ae9`)  
**Revert:** `INSUFFICIENT_OUTPUT_AMOUNT`

| Metric | Result |
|--------|--------|
| Diagnosis Time | **21.4s** |
| Tool Calls | **3** |
| failure_type | `slippage_exceeded` ✅ |
| Confidence | **high** |
| Root Cause | "Actual output amount from DEX swap was less than the minimum acceptable (slippage tolerance exceeded)" |
| Fix | "Increase slippage tolerance in DEX settings and retry" |

---

### TX-3: INSUFFICIENT_BALANCE — USDC direct transfer
**Hash:** `0xb7d9acfa1450a0d54fe09c1d83c87598220fc97af44b81669dac6eedff997f19`  
**Contract:** `0xA0b869…` (USDC — `transfer(address,uint256)`)  
**Revert:** `ERC20: transfer amount exceeds balance`

| Metric | Result |
|--------|--------|
| Diagnosis Time | **11.9s** |
| Tool Calls | **3** |
| failure_type | `insufficient_balance` ✅ |
| Confidence | **high** |
| Root Cause | "Sender attempted to transfer more USDC than they hold in their wallet" |
| Fix | "Ensure sender address has sufficient USDC balance before calling transfer()" |

---

### TX-4: CONTRACT_REVERT — OpenSea Seaport custom error
**Hash:** `0xd546940038094f8a50254f8d75ed9dfba2c692d38b0c857a167d2f941982cde8`  
**Contract:** `0x000000…68` (Seaport — `fulfillAdvancedOrder(…)`)  
**Revert:** custom error `0xa1148100` (InvalidSignature / TransferFromIncorrectOwner)

| Metric | Result |
|--------|--------|
| Diagnosis Time | **~36s** (166s wall including 2×65s rate-limit wait) |
| Tool Calls | **4** |
| failure_type | `contract_revert` ✅ |
| Confidence | **high** |
| Root Cause | "Signature for the advanced Seaport order was invalid — order signature mismatch" |
| Fix | "Verify the order signature matches the order parameters; NFT may have been transferred or sold" |

---

## Summary

| Test | Hash (prefix) | Time | Calls | Type | Result |
|------|--------------|------|-------|------|--------|
| TX-1 Allowance | `0xaa780…` | 18.6s | 3 | `insufficient_allowance` | ✅ PASS |
| TX-2 Slippage | `0x791cd…` | 21.4s | 3 | `slippage_exceeded` | ✅ PASS |
| TX-3 Balance | `0xb7d9a…` | 11.9s | 3 | `insufficient_balance` | ✅ PASS |
| TX-4 Revert | `0xd5469…` | ~36s* | 4 | `contract_revert` | ✅ PASS |

**Overall: 4/4 correct (100% accuracy)**  
**Avg time (net): 21.8s**  
**Avg tool calls: 3.25 / 5 target**

*TX-4 elapsed 166s due to free-tier rate-limit waits (2×65s). Net diagnosis was ~36s.

---

## Notes

- Gemini 2.5 Flash free tier: 5 RPM. Space tests ≥60s apart to avoid rate limits.
- Agent correctly decoded custom Solidity error (`0xa1148100`) via contract context inference.
- 4byte.directory resolved `0xe7acab24` → `fulfillAdvancedOrder(…)` enabling correct Seaport identification.
- All 3 standard tools fired per diagnosis: `get_transaction_receipt` → `decode_revert_reason` → `get_contract_info`.
- TX-4 used 4 tools (added `simulate_transaction`) for the ambiguous custom error case.

---

*Generated Day 10 of ETHGlobal Lisbon 25-day sprint (June 8, 2026)*

---

## Days 13-15: Expanded Test Suite (8 real txs + 2 unit-tested)

### TX-5: OUT_OF_GAS — Unknown contract
**Hash:** `0xc85afb8c601aabc2d0fa55ae930ef7d29030f5a346c94bb7919f07b08314302d`
**Gas:** 509,039 / 511,453 (99.5%)

| Metric | Result |
|--------|--------|
| Tool Result | OOG detected by simulate_transaction ✅ |
| failure_type | `out_of_gas` |
| Signal | gas_used >= 98% threshold |
| Fix | Increase gas limit by 1.5x |

---

### TX-6: SLIPPAGE — CoW Protocol / DAG Swap
**Hash:** `0x7321fb0ff871d2cbfa30e2b0131881eed34dd17e4560d2fe81dcec1b34b79534`
**Revert:** `Min return not reached`

| Metric | Result |
|--------|--------|
| Tool Result | decode_revert_reason → "Min return not reached" ✅ |
| failure_type | `slippage_exceeded` |
| Fix | Increase slippage tolerance or use limit order |

---

### TX-7: SLIPPAGE — Unknown DEX aggregator
**Hash:** `0x894df9372b1ea83c19e46906f36bf7eb52d4ec716fed337d022b99cd47330d07`
**Revert:** `INSUFFICIENT_OUTPUT`

| Metric | Result |
|--------|--------|
| Tool Result | decode_revert_reason → "INSUFFICIENT_OUTPUT" ✅ |
| failure_type | `slippage_exceeded` |
| Fix | Retry with wider slippage; market moved |

---

### TX-8: CONTRACT_REVERT — ParaSwap QuoteExpired
**Hash:** `0x21c9c841c0a1b77eab457bb5417c94332c89eee44cae73a640564839794370f9`
**Revert:** Custom error `0x8727a7f9` = `QuoteExpired()`

| Metric | Result |
|--------|--------|
| Tool Result | Custom error decoded via 4byte → QuoteExpired() ✅ |
| failure_type | `contract_revert` |
| Fix | Refresh the ParaSwap quote and retry within expiry window |

---

## Full Suite Summary (8 real txs)

| # | Type | Hash (prefix) | Signal | MCP Verified |
|---|------|--------------|--------|-------------|
| 1 | insufficient_allowance | `0xaa780` | TRANSFER_FROM_FAILED | ✅ |
| 2 | slippage_exceeded | `0x791cd` | INSUFFICIENT_OUTPUT_AMOUNT | ✅ |
| 3 | insufficient_balance | `0xb7d9a` | ERC20: transfer amount exceeds balance | ✅ |
| 4 | contract_revert | `0xd5469` | Seaport custom error 0xa1148100 | ✅ |
| 5 | out_of_gas | `0xc85af` | gas 99.5% of limit | ✅ |
| 6 | slippage_exceeded | `0x7321f` | Min return not reached (CoW) | ✅ |
| 7 | slippage_exceeded | `0x894df` | INSUFFICIENT_OUTPUT (aggregator) | ✅ |
| 8 | contract_revert | `0x21c9c` | QuoteExpired() ParaSwap | ✅ |

**+ 10 unit tests verifying all 7 failure type classifications (no network)**

*Generated Days 13-15 of ETHGlobal Lisbon sprint (June 8, 2026)*
