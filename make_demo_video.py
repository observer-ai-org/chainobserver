"""
Generate a ChainObserver demo video using Pillow + ffmpeg.
Output: demo/chainobserver_demo.mp4  (~3 min, 1280x720, 30fps)

Segments:
  0:00-0:15  Title card
  0:15-0:30  The problem
  0:30-0:50  The one-command solution
  0:50-1:30  Live diagnosis — tool-call loop
  1:30-2:00  Result card (root cause + fix)
  2:00-2:35  Architecture diagram
  2:35-3:00  Live URLs + closing
"""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H   = 1280, 720
FPS    = 30
FONT_SIZE = 16
LINE_H = 22
PAD_X, PAD_Y = 36, 36

BG      = (13,  17,  23)
FG      = (220, 220, 220)
DIM     = (100, 100, 100)
PURPLE  = (163, 113, 247)   # ChainObserver brand
CYAN    = (97,  214, 214)   # tool calls
GREEN   = (106, 153,  85)
YELLOW  = (220, 187,  68)
RED     = (240,  71,  71)
ORANGE  = (209, 154, 102)
BORDER  = ( 55,  60,  75)
WHITE   = (255, 255, 255)

FONT_PATH      = "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf"
FRAMES_DIR     = Path("/tmp/co_frames")
OUT_VIDEO      = Path("/home/user/chainobserver/demo/chainobserver_demo.mp4")


@dataclass
class Line:
    text:  str
    color: tuple[int, int, int] = field(default_factory=lambda: FG)
    bold:  bool = False

@dataclass
class Segment:
    lines:        list[Line]
    hold_frames:  int = FPS
    typing_speed: int = 1

def _l(text="", color=FG,   bold=False): return Line(text, color, bold)
def _dim(t):    return Line(t, DIM)
def _p(t, b=False): return Line(t, PURPLE, b)
def _c(t, b=False): return Line(t, CYAN, b)
def _g(t, b=False): return Line(t, GREEN, b)
def _y(t):      return Line(t, YELLOW)
def _r(t, b=False): return Line(t, RED, b)
def _o(t):      return Line(t, ORANGE)
def _w(t):      return Line(t, WHITE, True)


SCRIPT: list[Segment] = [

    # ── 0  Title card (5 s) ──────────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _p(" ██████╗██╗  ██╗ █████╗ ██╗███╗  ██╗ ██████╗ ██████╗ ███████╗███████╗██████╗ ", True),
        _p("██╔════╝██║  ██║██╔══██╗██║████╗ ██║██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗", True),
        _p("██║     ███████║███████║██║██╔██╗██║██║   ██║██████╔╝███████╗█████╗  ██████╔╝", True),
        _p("██║     ██╔══██║██╔══██║██║██║╚████║██║   ██║██╔══██╗╚════██║██╔══╝  ██╔══██╗", True),
        _p("╚██████╗██║  ██║██║  ██║██║██║ ╚███║╚██████╔╝██████╔╝███████║███████╗██║  ██║", True),
        _p(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚══╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝", True),
        _l(),
        _dim("         AI agent that diagnoses failed Ethereum transactions in < 30 seconds"),
        _l(),
        _dim("         Gemini 2.5 Flash  ·  5 Ethereum MCP tools  ·  ETHGlobal Lisbon 2026"),
    ], hold_frames=FPS * 5, typing_speed=999),

    # ── 1  The problem (7 s) ─────────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _y("  The problem:"),
        _l(),
        _dim("  Transaction failed."),
        _dim("  Etherscan says: 'Fail with error TRANSFER_FROM_FAILED'"),
        _dim("  You open the contract, trace the call stack... 45 minutes gone."),
        _l(),
        _g("  ChainObserver reads the chain.  Gemini finds the root cause."),
        _g("  You get the fix.  Done.", True),
    ], hold_frames=FPS * 6, typing_speed=1),

    # ── 2  One command (4 s) ─────────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _c("  # Paste any failed transaction hash", True),
        _l(),
        _l("  $ chainobserver diagnose \\", GREEN),
        _l("      0xaa78010df34b38c16b5168ada399b840162bbf3566b398025cad7ba69581bab5", GREEN),
    ], hold_frames=FPS * 3, typing_speed=1),

    # ── 3  Panel appears (3 s) ──────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _dim("  ╭─────────────────────────────────────────────────────────────────╮"),
        _p(  "  │  ChainObserver · tx 0xaa78010d…                                 │", True),
        _dim("  │  Chain: Ethereum · Gemini 2.5 Flash · MCP tools                │"),
        _dim("  ╰─────────────────────────────────────────────────────────────────╯"),
    ], hold_frames=FPS * 2, typing_speed=2),

    # ── 4  Tool 1 — receipt (5 s) ─────────────────────────────────────────
    Segment(lines=[
        _l(),
        _c("  → get_transaction_receipt(tx_hash)", True),
        _l(),
        _dim('    status=0 (FAILED)'),
        _dim('    to=0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af'),
        _dim('    gas_used=401788 / 420000  (95.7%)'),
        _o('    input_selector=0x3593564c'),
        _dim('    etherscan: https://etherscan.io/tx/0xaa780…'),
    ], hold_frames=FPS * 4, typing_speed=1),

    # ── 5  Tool 2 — revert (5 s) ──────────────────────────────────────────
    Segment(lines=[
        _l(),
        _c("  → decode_revert_reason(tx_hash)", True),
        _l(),
        _r('    revert_reason: "TRANSFER_FROM_FAILED"', True),
        _dim('    error_type: Error(string)'),
        _dim('    is_state_dependent: false'),
    ], hold_frames=FPS * 4, typing_speed=1),

    # ── 6  Tool 3 — contract info (5 s) ───────────────────────────────────
    Segment(lines=[
        _l(),
        _c("  → get_contract_info(address, input_selector)", True),
        _l(),
        _dim('    name: sourcify_verified'),
        _g('    called_function: execute(bytes,bytes[],uint256)'),
        _dim('    source: 4byte.directory + Sourcify'),
        _dim('    → Uniswap Universal Router'),
    ], hold_frames=FPS * 4, typing_speed=1),

    # ── 7  Gemini reasoning (3 s) ─────────────────────────────────────────
    Segment(lines=[
        _l(),
        _dim("  Gemini 2.5 Flash reasoning…"),
        _l(),
        _dim('  "execute() calls transferFrom() on the ERC-20 token.'),
        _dim('   TRANSFER_FROM_FAILED means the router is not approved'),
        _dim('   to spend tokens from the sender\'s wallet."'),
        _l(),
        _g("  ✓ Diagnosis complete in 18.6s  ·  3 tool calls"),
    ], hold_frames=FPS * 3, typing_speed=1),

    # ── 8  Result card (10 s) ────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _dim("  ╭──────────────────────── ChainObserver Diagnosis ─────────────────────────╮"),
        _l("  │  Chain        Ethereum                                                    │", DIM),
        _r("  │  Root cause   ERC-20 allowance not set — router cannot move tokens        │", True),
        _p("  │  Failure type insufficient_allowance                                      │", True),
        _g("  │  Confidence   high                                                        │"),
        _l("  │  Affected     0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af                  │", DIM),
        _g("  │  Fix          Call token.approve(router, amount) before the swap          │", True),
        _l("  │  Explorer     https://etherscan.io/tx/0xaa780…                            │", DIM),
        _l("  │  Time         18.6s  ·  3 tool calls                                     │", DIM),
        _dim("  ╰─────────────────────────────────────────────────────────────────────────────╯"),
    ], hold_frames=FPS * 9, typing_speed=2),

    # ── 9  More cases (6 s) ──────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _y("  Works across all failure types:"),
        _l(),
        _g("  ✅  slippage_exceeded     INSUFFICIENT_OUTPUT_AMOUNT — Uniswap V2"),
        _g("  ✅  insufficient_balance  ERC20: transfer amount exceeds balance — USDC"),
        _g("  ✅  out_of_gas            gas_used 99.5% of limit — any contract"),
        _g("  ✅  contract_revert       Seaport TransferFromIncorrectOwner — custom error"),
        _g("  ✅  insufficient_allowance TRANSFER_FROM_FAILED — Uniswap Universal Router"),
    ], hold_frames=FPS * 5, typing_speed=1),

    # ── 10  Architecture (12 s) ───────────────────────────────────────────
    Segment(lines=[
        _l(),
        _p("  Architecture", True),
        _l(),
        _dim("  ┌────────────────────────────────────────────────┐"),
        _p(  "  │  EthereumDiagnosisAgent  ·  Gemini 2.5 Flash   │"),
        _dim("  │  agentic loop — stops when confident (≤6 calls) │"),
        _dim("  └──────────────────────┬─────────────────────────┘"),
        _dim("                         │ MCP stdio subprocess"),
        _dim("                         ▼"),
        _dim("  ┌──────────────────────────────────────────────────┐"),
        _c(  "  │  ChainObserver MCP Server                        │"),
        _dim("  │  ├─ get_transaction_receipt  (eth_getTransaction) │"),
        _dim("  │  ├─ decode_revert_reason     (eth_call replay)    │"),
        _dim("  │  ├─ get_contract_info        (Etherscan + Sourcify)│"),
        _dim("  │  ├─ simulate_transaction     (eth_call + OOG check)│"),
        _dim("  │  └─ get_pool_info            (Uniswap V2 factory)  │"),
        _dim("  └──────────────────────────────────────────────────┘"),
        _dim("       Ethereum RPC  ·  4byte.directory  ·  Sourcify"),
    ], hold_frames=FPS * 10, typing_speed=1),

    # ── 11  Multi-chain (5 s) ─────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _p("  5-chain support", True),
        _l(),
        _dim("  chainobserver diagnose 0x...  --chain 1      # Ethereum"),
        _dim("  chainobserver diagnose 0x...  --chain 42161  # Arbitrum One"),
        _dim("  chainobserver diagnose 0x...  --chain 8453   # Base"),
        _dim("  chainobserver diagnose 0x...  --chain 10     # Optimism"),
        _dim("  chainobserver diagnose 0x...  --chain 137    # Polygon"),
        _l(),
        _dim("  Or via REST API:  POST /diagnose  {\"tx_hash\": \"0x...\", \"chain_id\": 42161}"),
    ], hold_frames=FPS * 4, typing_speed=1),

    # ── 12  Benchmarks (5 s) ─────────────────────────────────────────────
    Segment(lines=[
        _l(),
        _p("  Benchmarks  (8 real mainnet transactions)", True),
        _l(),
        _g("  100% accuracy  ·  21.8s avg  ·  3.25 tool calls avg"),
        _l(),
        _dim("  TX-1  insufficient_allowance   18.6s  3 calls  ✅"),
        _dim("  TX-2  slippage_exceeded        21.4s  3 calls  ✅"),
        _dim("  TX-3  insufficient_balance     11.9s  3 calls  ✅"),
        _dim("  TX-4  contract_revert (Seaport) ~36s  4 calls  ✅"),
        _dim("  TX-5  out_of_gas               auto  1 call   ✅"),
    ], hold_frames=FPS * 4, typing_speed=1),

    # ── 13  Live URLs + closing (8 s) ─────────────────────────────────────
    Segment(lines=[
        _l(),
        _p("  Try it live", True),
        _l(),
        _g("  https://huggingface.co/spaces/johnlee007/chainobserver", True),
        _l(),
        _dim("  POST /diagnose  {\"tx_hash\": \"0x...\"}"),
        _dim("  GET  /health"),
        _l(),
        _dim("  github.com/64johnlee/chainobserver  ·  MIT  ·  123 tests"),
        _l(),
        _p("  Built for ETHGlobal Lisbon 2026 — on-chain observability", True),
        _dim("  Powered by Gemini 2.5 Flash · MCP Protocol · web3.py"),
    ], hold_frames=FPS * 7, typing_speed=1),
]


def load_fonts():
    reg  = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    bold = ImageFont.truetype(BOLD_FONT_PATH, FONT_SIZE)
    return reg, bold


def render_frame(lines: list[Line], reg, bold) -> Image.Image:
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 28], fill=(22, 24, 34))
    draw.text((12, 6), "● ● ●  ChainObserver Demo  —  ETHGlobal Lisbon 2026",
              font=reg, fill=DIM)
    draw.line([(0, 28), (W, 28)], fill=BORDER, width=1)

    max_lines = (H - PAD_Y * 2 - 28) // LINE_H
    visible   = lines[-max_lines:] if len(lines) > max_lines else lines

    y = PAD_Y + 28
    for line in visible:
        f = bold if line.bold else reg
        draw.text((PAD_X, y), line.text, font=f, fill=line.color)
        y += LINE_H

    return img


def generate_frames() -> int:
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    reg, bold = load_fonts()
    frame_idx  = 0
    accumulated: list[Line] = []

    def save(n: int = 1) -> None:
        nonlocal frame_idx
        img = render_frame(accumulated, reg, bold)
        for _ in range(n):
            img.save(FRAMES_DIR / f"frame_{frame_idx:06d}.png")
            frame_idx += 1

    for seg in SCRIPT:
        chunk   = max(1, seg.typing_speed)
        pending = list(seg.lines)
        while pending:
            accumulated.extend(pending[:chunk])
            pending = pending[chunk:]
            save(max(1, FPS // 4))
        save(seg.hold_frames)

    print(f"Generated {frame_idx} frames ({frame_idx / FPS:.0f}s)")
    return frame_idx


def encode_video(frame_count: int) -> None:
    OUT_VIDEO.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%06d.png"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={W}:{H}",
        str(OUT_VIDEO),
    ]
    print("Encoding video…")
    subprocess.run(cmd, check=True, capture_output=True)
    mb = OUT_VIDEO.stat().st_size / 1_048_576
    print(f"Output: {OUT_VIDEO}  ({mb:.1f} MB, {frame_count / FPS:.0f}s)")


if __name__ == "__main__":
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    n = generate_frames()
    encode_video(n)
