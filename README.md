or

# ErosDiffusion — ControlNet Map Cache & Browser

Lightweight helper nodes for caching, browsing, and re-using ControlNet preprocess maps inside ComfyUI.

## Overview

This package provides two ComfyUI nodes that simplify working with ControlNet maps by caching generated maps to disk and exposing a visual browser:

- `CacheMapNode` — smart cache layer that checks a disk cache before requesting expensive preprocessors and can save generated maps for reuse.
- `CacheMapBrowserNode` — sidebar/browser integration to preview and load cached maps (returns image + mask).

These nodes are designed to reduce repeated preprocessing work and help organize map assets by filename and type.

## Key Features

- Cache lookup by filename and map type (supports multiple extensions).
- `auto` mode detects existing map types and only runs connected preprocessors when needed.
- `generate_all` option to batch-save all connected preprocessors and the original image.
- Tagging: comma-separated `tags` input is persisted to a lightweight metadata DB for later retrieval and UI updates.
- Browser node returns both image and alpha mask (if present) for quick selection.

## Nodes

**CacheMapNode**

- Category: `ErosDiffusion`
- Returns: `IMAGE` (`map`)
- Useful inputs (see node UI for full list): `cache_path`, `filename`, `map_type` (auto | depth | canny | ... | browser), `save_if_new`, `force_generation`, `generate_all`, `tags`, `source_<map_type>` image inputs, `source_original`.
- Behavior summary:
  - If `map_type` is `browser` the node simply passes through the `source_browser` image.
  - In `auto` mode it searches cache subfolders for existing maps and only requests the necessary preprocessor inputs on cache miss.
  - `save_if_new` saves generated maps to `<cache_path>/<type>/<basename>.png`.
  - `generate_all` forces evaluation of all connected preprocessor inputs and saves them.
  - Tags are parsed, deduplicated, and stored via the included metadata manager.

**CacheMapBrowserNode**

- Category: `ErosDiffusion`
- Returns: `IMAGE, MASK` (`image, mask`)
- Opens a map browser in the ComfyUI sidebar (button on the node). Select a file and the node loads the image and corresponding mask (if any).

## Default Map Types

Default map types are configured in `eros_config.json`. The shipped defaults are:

```
depth, canny, openpose, lineart, scribble, softedge, normal, seg, shuffle, mediapipe_face, custom
```

You can customize that list in `eros_config.json` (node will read this file on load).

## Installation

1. Copy this folder into your ComfyUI `custom_nodes` directory.
2. Ensure the Python dependencies listed in `requirements.md` are installed.
3. Restart ComfyUI; the nodes appear under the `ErosDiffusion` category.

## Typical Workflows

- Quick reuse: Connect a preprocessor node to `CacheMapNode`'s `source_<type>` and set `filename` to a stable identifier; future runs will load the cached map instead of re-running the preprocessor.
- Batch export: Enable `generate_all` to save all connected preprocessor outputs and the original image to disk.
- Browse & inject: Use the `CacheMapBrowserNode` to visually pick maps and feed them into downstream nodes.

## Paths & Defaults

- Default cache root (node UI): `<ComfyUI input directory>/maps` (can be changed in the node's `cache_path`).
- Cache layout: `<cache_path>/<map_type>/<basename>.png` and originals under `<cache_path>/original/`.

## Tags & Metadata

Provide a comma-separated `tags` string to `CacheMapNode` and tags will be parsed, normalized (deduplicated case-insensitive), and stored in a local metadata DB (see `metadata_manager.py`). The node also notifies the frontend when tags are updated.

## Troubleshooting

- If cached maps are not being found, verify `cache_path` and that filenames use the same basename (node strips extensions when checking).
- For `auto` mode misses, ensure the corresponding `source_<type>` input is connected so the preprocessor can run and generate the map.
- If browser doesn't show files, confirm the UI has access to the configured `cache_path` and any `extra_path` you provided.

## Files of interest

- `cache_map_nodes.py` — node implementations (CacheMapNode, CacheMapBrowserNode)
- `eros_config.json` — map type configuration
- `metadata_manager.py` — tagging/DB helper
- `requirements.md` — dependency notes

## Contributing

PRs welcome. Keep changes focused and add tests/examples where possible.

---

If you'd like, I can also add a short example flow (JSON) demonstrating a typical `CacheMapNode` + preprocessor setup.
