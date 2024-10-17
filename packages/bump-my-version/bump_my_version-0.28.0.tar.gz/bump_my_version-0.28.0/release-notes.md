[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.27.0...0.28.0)

### New

- Added container labels and version hooks. [d4cb8f2](https://github.com/callowayproject/bump-my-version/commit/d4cb8f2231dbe5faa4bc68b769a00ea199beed8e)
    
- Add Docker support and configure Dependabot for Docker updates. [0315db4](https://github.com/callowayproject/bump-my-version/commit/0315db458db260653180ba95a106cecad8eea425)
    
  Introduce a Dockerfile for containerized environments and add a .dockerignore file to exclude unnecessary files. Also, update dependabot.yml to include daily checks for Docker image updates.
- Add `inputs` section in GHA workflow example. [813e7f5](https://github.com/callowayproject/bump-my-version/commit/813e7f526479e278ab12db2bc8a873c9f7fc2dd7)
    
### Other

- Switch from ADD to COPY in Dockerfile. [a5fc5c0](https://github.com/callowayproject/bump-my-version/commit/a5fc5c0e595530650059dd6ab821927933f0ef58)
    
  This change updates the Dockerfile to use the COPY instruction instead of ADD. COPY is preferred when only copying files because it is more explicit and simpler.
- [pre-commit.ci] pre-commit autoupdate. [7c48f98](https://github.com/callowayproject/bump-my-version/commit/7c48f987fd782b1c5665e49dd9e0e491416d39cd)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.6.8 → v0.6.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.6.8...v0.6.9)

### Updates

- Changed dependency manager to uv. [cce9e1d](https://github.com/callowayproject/bump-my-version/commit/cce9e1dead3507791e866c0daf5e3f6818a55e14)
    
