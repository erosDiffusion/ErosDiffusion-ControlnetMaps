# Requirements Tracking

## Active Branch: master

## Requirements
<!-- id: 0 -->
### 1. Initial Project Requirements (Base State)

#### 1.1 Functional Requirements
*   **Centralized Map Caching**:
    *   Store ControlNet preprocessor outputs (depth, canny, openpose, etc.) in a structured file system hierarchy (`/cache_root/map_type/filename.png`).
    *   Support for multiple map types defined in `eros_config.json` (depth, canny, openpose, lineart, scribble, softedge, normal, seg, shuffle, mediapipe_face, custom).
*   **Smart Generation Node (`CacheMapNode`)**:
    *   **Auto-Detection**: Automatically detect map type based on connected inputs (`auto` mode).
    *   **Cache-First**: Check for existing maps before triggering generation to save compute time.
    *   **Force Generation**: Boolean toggle to overwrite existing cache.
    *   **Generate All**: Batch process all connected inputs and source original image in one go.
    *   **Lazy Input**: Use `LazyInput` for source connections to prevent unnecessary upstream execution when cache hits.
*   **Visual Map Browser (`CacheMapBrowserNode`)**:
    *   **Interactive UI**: A drawer-based file browser accessible via "Open Browser" button on the node.
    *   **Grid View**: Responsive grid displaying cached maps with lazy loading and cache busting.
    *   **Filtering**: Tabs for different map types and a search bar for filename/tag filtering.
    *   **Overlay Mode**: Ability to overlay the "original" source image on top of maps with adjustable opacity and blend modes (luminosity, multiply, etc.) for visual alignment verification.
*   **Metadata & Tagging System**:
    *   **Tagging**: Add, remove, and list tags for specific images.
    *   **Visual Badges**: Show tag counts and specific tags as badges on map thumbnails in the browser.
    *   **Favorites**: Mark specific maps as favorites (backend API support).
    *   **Persistence**: Store metadata in a local SQLite database (`metadata.db`).

#### 1.2 Architectural Requirements
*   **ComfyUI Integration**: Must function as a self-contained custom node extension.
*   **Hybrid Stack**:
    *   **Backend (Python)**: Handles file I/O, SQLite database interactions, and ComfyUI node logic. Exposes REST-like API endpoints (`/eros/cache/*`, `/eros/tags/*`).
    *   **Frontend (JavaScript/Web Components)**: Uses standard Web Components (Custom Elements) or Lit for a modern, reactive UI within the ComfyUI interface. Encapsulated styles (Shadow DOM).
*   **Configuration**: Runtime configuration driven by `eros_config.json` to allow easy addition of new map types without code changes.
*   **Namespace Isolation**: All API routes and node names must be namespaced (e.g., `ErosDiffusion`) to avoid conflicts with other extensions.
*   **Relative Paths**: Caching should default to `[input_path]/maps` but support user overrides. Filesystem structure must be predictable to allow frontend retrieval.
