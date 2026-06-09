# Observer AI — Multi-Platform Diagnostic Agents

> Agentic observability for every platform. One pattern, five domains.

This document outlines the roadmap for building 5 derivative agents using the same **Gemini 2.5 Flash + MCP** architecture as ChainObserver.

---

## Overview

**The Vision:**
Every engineer debugs failures the same way:
1. Open logs / dashboards
2. Scroll through noise
3. Find the signal
4. Decode what it means
5. Propose a fix

**Our Approach:**
Build agents for each platform that do steps 1-5 automatically.

**The Stack:**
- **Agentic Brain:** Gemini 2.5 Flash (tool-calling, bounded loops, structured output)
- **Tool Standardization:** MCP (Model Context Protocol)
- **Deployment:** FastAPI + HF Spaces / Cloud Run
- **Testing:** Real-world failure cases, 100% accuracy target

---

## 1. ChainObserver ✅ (COMPLETE)

**Status:** MVP shipped, benchmarks locked  
**Repository:** https://github.com/observer-ai/chainobserver  
**Live Demo:** https://chainobserver.hf.space

**Diagnoses:** Failed Ethereum transactions  
**Performance:** 21.8s avg, 3.25 tool calls, 100% accuracy  
**Tests:** 114 passing, 8 real mainnet txs verified

---

## 2. GitHubGuard (PLANNED)

**Status:** Scheduled for Phase 2  
**Target:** June 18-25, 2026

**Diagnoses:** Failed GitHub Actions workflows  
**Failure Types:** Missing secrets, dependency conflicts, flaky tests, timeout, OOM

---

## 3. KubeObserver (ROADMAP)

**Status:** Scheduled for Phase 3  
**Target:** July 10-20, 2026

**Diagnoses:** Kubernetes pod failures  
**Failure Types:** CrashLoopBackOff, ImagePullBackOff, OOMKilled, probe failures

---

## 4. QueryDebugger (ROADMAP)

**Status:** Scheduled for Phase 3  
**Target:** July 20-28, 2026

**Diagnoses:** Slow SQL queries, deadlocks, schema mismatches

---

## 5. LoggingAgent (FUTURE)

**Status:** Scheduled for Phase 4 (Aug+)

**Diagnoses:** Failed logs / distributed traces

---

## 🎯 How to Contribute

### Option A: Build a Full Agent

1. Fork this repository
2. Create `<platform>observer/` (e.g., `kubeobserver/`)
3. Write 5 MCP tools for your platform
4. Test against 10+ real failure cases
5. Submit PR with benchmarks

### Option B: Build an MCP Server

1. Create standalone MCP server: `observer-<platform>-mcp`
2. Implement 5+ tools for your platform
3. Publish as open-source package
4. We'll integrate it into the marketplace

### Option C: Add Support for New Chain

1. Add chain metadata to `chainobserver/chains.py`
2. Add 1-2 test cases (real failed txs from that chain)
3. Run `pytest` to verify
4. Submit PR

---

**Last updated:** June 9, 2026
