## Purpose

This file gives succinct, actionable guidance for an AI coding agent working on this ComfyUI custom node extension. Focus on what is required to be productive immediately: architecture, patterns, integration points, and concrete examples from the repo.

## Big Picture

- Backend: ComfyUI custom nodes implemented in Python (`cache_map_nodes.py`, `extract_metadata_node.py`). Responsible for cache file I/O, saving/loading images, and interacting with a small metadata DB (`metadata.db`).
- Frontend: Vanilla Web Components / Lit under `js/` (notably `cache_service.js` and `cache_map_browser*.js`) that call REST-like endpoints to list files, view images, and manage tags.
- Config: `eros_config.json` drives supported map types. Default cache root uses `folder_paths.get_input_directory()/maps`.

## Key Files

- [cache_map_nodes.py](cache_map_nodes.py): main node logic (CacheMapNode, CacheMapBrowserNode). Important behaviors: `auto` mode, `generate_all`, `save_if_new`, and tag handling.
- [extract_metadata_node.py](extract_metadata_node.py): helper node that extracts embedded prompt / resolution metadata from images.
- [metadata_manager.py](metadata_manager.py): expected metadata DB helper (currently empty in this branch) — implement `add_tag_to_image(basename, tag)` and `get_tags_for_image(basename)` here.
- [eros_config.json](eros_config.json): list of `map_types` (used to generate node inputs dynamically).
- `js/` directory: UI components and `cache_service.js` which defines the client-side API surface used by the browser UI.
- [README.md](README.md) and [requirements.md](requirements.md): high-level usage and dependency notes.

## Critical Patterns & Conventions

- Cache layout: `<cache_path>/<map_type>/<basename>.png`. The node strips extensions and uses the basename for DB keys.
- Image data: nodes accept and return torch tensors shaped like `(1, H, W, 3)` with float values in [0,1]; saving/loading converts via `*255 -> uint8 -> PIL.Image` and back.
- Map types are dynamic: `load_map_types()` reads `eros_config.json` and the node dynamically exposes `source_<type>` lazy inputs. Add new types by updating `eros_config.json` (no code change required).
- Tag normalization: tags parsed from a comma-separated string are trimmed and de-duplicated case-insensitively; original case is preserved when adding to the DB.
- Browser integration: the browser UI expects backend endpoints namespaced under `/eros/*` (see `js/cache_service.js`). The frontend is optimistic about tag changes (adds optimistic UI updates then posts to API).

## Integration Points / External APIs

- `PromptServer` (imported from `server`) is used to send frontend notifications (`eros.tags.updated`). Ensure the server singleton exists in the running ComfyUI environment.
- Frontend API calls used by `cache_service.js`:
  - `GET /eros/tags/list` — returns `{ tags: [{name, count}, ...] }`
  - `GET /eros/tags/for_image?path=<basename>` — returns `{ tags: [...] }`
  - `POST /eros/tags/add_to_image` — body `{ path: basename, tag }`
  - `POST /eros/tags/remove_from_image` — body `{ path: basename, tag }`
  - `POST /eros/tags/auto_tag` — body `{ path: basename }` (optional auto-tagging)
  - `GET /eros/cache/fetch_files?path=<cachePath>&subfolder=<type>` — returns `{ files: [...] }`
  - `GET /eros/cache/view_image?path=<cache>&subfolder=<sub>&filename=<file>` — returns an image URL used by the browser.

## Developer Workflows & Commands

- Install runtime deps (observed imports): Pillow, numpy, torch, aiohttp. Check `requirements.md` for notes; an example quick install:

  ```bash
  pip install pillow numpy torch aiohttp
  ```

- Install: copy this folder into ComfyUI's `custom_nodes` and restart ComfyUI. Nodes register under the `ErosDiffusion` category.
- Frontend changes: edit files in `js/` and reload ComfyUI. The browser component (`Open Browser` button) dynamically imports either the Lit or vanilla web-component implementation.

## Notable Repo State & Tasks for Agents

- `metadata_manager.py` is empty in this branch — core functionality (SQLite `metadata.db` access and the API route handlers) must be implemented or mocked for tag features to work.
- The backend is expected to expose the `/eros/*` endpoints. If they don't exist in the host ComfyUI server, implement them in the extension's server integration layer (the code references `PromptServer` and `server` module).

## Small, Concrete Examples

- To save a 'canny' map for `image.png` into default cache: save to `maps/canny/image.png` (node derives basename and uses that path).
- Tag parsing example (from `cache_map_nodes.py`): input `"Cat, animal, cat , Pet"` → stored unique tags `['Cat','animal','Pet']` and `PromptServer.instance.send_sync("eros.tags.updated", {...})` is called after saving.

If you want me to implement the missing `metadata_manager.py` SQLite helper and minimal API endpoints (`/eros/tags/*`, `/eros/cache/*`), say so and I will add them with tests.

## Feedback

Tell me which parts you want expanded (API shapes, DB schema, or a runnable server scaffold) and I'll iterate.
