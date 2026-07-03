---
name: kicad-hardware-verification
description: Ground-truth verification patterns for KiCad PCB work driven from Python - measuring boards, catching placement defects, and avoiding pcbnew API traps. Use when editing or auditing .kicad_pcb files programmatically, verifying digital-twin renders against boards, or preparing boards for fabrication.
---

# KiCad hardware verification

PCB mistakes ship in resin. These patterns catch them while they are still
bytes. All examples use KiCad's bundled Python (pcbnew) on macOS.

## Session setup traps

- `import wx; _APP = wx.App(False)` BEFORE `import pcbnew` on macOS builds,
  or expect crashes far from the cause.
- Headless zone-fill can segfault on some builds; zone CREATION headless can
  crash reproducibly. Fill/create zones in scripts that do only that, so a
  crash loses nothing else.
- Pad size APIs differ across builds: try `pad.SetSize(VECTOR2I(...))` when
  `PADSTACK_ALL_LAYERS` variants are missing.
- Manually placed vias can get their net silently re-derived from filled zone
  copper at `Save()` time - unfill zones before adding vias, refill after.

## Measurement ground truth (ranked by trust)

1. **Pad geometry** (positions, nets, per-pad bounding boxes) - the only
   truth JLCPCB sees. Assembly follows pads, not your intent.
2. **Footprint library definition** (the .kicad_mod) - for anchor conventions
   and mouth/orientation questions.
3. **Courtyard layer** - conservative clearance truth; overlapping courtyards
   usually mean pads are too dense to route at the clearance rules, even when
   bodies physically fit (autorouters see the pads and clearances, not the
   courtyards themselves).
4. **Component bounding boxes** - polluted by text items; never use
   `GetBoundingBox()` centers to infer orientation.
5. Docs, comments, renders - subjects of verification, never sources.

## The traps that actually shipped bad geometry (real incidents)

- **Anchor is not center**: slide-pot footprints anchor at PAD 1 (one end of
  the pad span). Placing the anchor at a slot's travel-center displaced the
  part by half its length and pushed pads off the board. Before placing ANY
  part to a mechanical target, measure the pad-span midpoint offset from the
  anchor and compensate.
- **Pads rotated inside the instance**: a board's embedded footprint can carry
  pads pre-rotated 180 relative to the library while the rotation field reads
  0 - renders look right, the assembled part faces backwards. Detect by
  comparing the instance's local pad centroid sign against the library's.
  Fix by replacing with a fresh library footprint (preserve nets by pad name),
  never by flipping the rotation field.
- **Copper past the board edge**: pad copper must end INSIDE Edge.Cuts by at
  least the copper-edge clearance rule (check
  `GetDesignSettings().m_CopperEdgeClearance`). Copper at or past the edge
  gets milled off at fab AND makes autorouters rip-up forever. Verify with
  per-pad bounding boxes vs the outline, per edge.
- **Same-net duplication hides dead controls**: N identical controls wired to
  ONE net looks fine in every render and routes cleanly - and N-1 controls are
  dead silicon. Audit: group control pads by net; duplicates across distinct
  user controls are a design gap.
- **Placed but unrouted to nothing**: a component whose signal pads belong to
  nets that reach no MCU pad passes DRC and routes "successfully". Audit each
  control net's pad list for an MCU endpoint.

## Fresh-load verification (non-negotiable)

In-process connectivity lies after fills and imports. The ONLY trustworthy
unconnected count:

```python
b = pcbnew.LoadBoard(path)   # fresh load, not the instance you edited
b.BuildConnectivity()
b.GetConnectivity().GetUnconnectedCount(False)
```

For fab-readiness use `kicad-cli pcb drc --format json --severity-error` and
read `unconnected_items` + shorts. GND-pour islands split by traces are
usually fab-acceptable; real shorts and courtyard overlaps are not.

## Autorouting (freerouting) survival notes

- CLI batch mode (v2.1-v2.2.4) routes fine but can HANG at exit on some Java
  runtimes (observed under Java 26; Java 21 was stable) and never write the
  .ses (scheduler thread busy-loop; output only materializes on graceful
  exit). If pinning an older JRE is not an option, the reliable headless path
  is v2.2.4's REST API: start with
  `FREEROUTING__API_SERVER__AUTHENTICATION__ENABLED=false`, submit the DSN as
  a job, poll, download the .ses over HTTP. This hang is the incident behind
  watch-the-live-log - apply that discipline to any autorouter run that seems
  slow.
- SES files can contain `::N` component names (pin headers, USB footprints)
  that make `ImportSpecctraSES` fail silently; clean with
  `re.sub(r'\(component\s+::(\d+)', r'(component "ph_\1"', s)` first.
  Genuinely empty names need the same quote-and-rename treatment before
  import.
- A partially-routed board grinds; a clean skeleton routes in seconds. When
  placement changed, strip tracks and route fresh rather than incrementally.
