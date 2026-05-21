# Source notes

Checked on 2026-04-29. These notes are for human review; skill files should still tell agents to check current docs and issues before acting.

## Apple MLX

- Apple MLX open-source page: https://opensource.apple.com/projects/mlx/
- MLX docs, unified memory: https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html
- MLX docs, lazy evaluation: https://ml-explore.github.io/mlx/build/html/usage/lazy_evaluation.html
- MLX PyPI package: https://pypi.org/project/mlx/

## `mlx-lm`

- GitHub: https://github.com/ml-explore/mlx-lm
- PyPI: https://pypi.org/project/mlx-lm/
- Hugging Face MLX docs: https://huggingface.co/docs/hub/en/mlx
- Hugging Face Transformers MLX integration docs: https://huggingface.co/docs/transformers/main/en/main_classes/mlx
- MLX Community organization: https://huggingface.co/mlx-community

## `mlx-vlm`

- GitHub: https://github.com/Blaizzy/mlx-vlm
- PyPI: https://pypi.org/project/mlx-vlm/
- Example Qwen3-VL MLX model cards:
  - https://huggingface.co/mlx-community/Qwen3-VL-4B-Instruct-3bit
  - https://huggingface.co/mlx-community/Qwen3-VL-30B-A3B-Instruct-3bit
  - https://huggingface.co/mlx-community/Qwen3-VL-8B-Thinking-8bit
- Recent `mlx-vlm` issues used for failure-mode design:
  - https://github.com/Blaizzy/mlx-vlm/issues/614
  - https://github.com/Blaizzy/mlx-vlm/issues/718
  - https://github.com/Blaizzy/mlx-vlm/issues/895

## `mlx-embeddings`

- GitHub: https://github.com/Blaizzy/mlx-embeddings
- PyPI: https://pypi.org/project/mlx-embeddings/
- Example reranker model card: https://huggingface.co/mlx-community/Qwen3-Reranker-4B-mxfp8

## Qwen3-VL and VFIG

- VFIG model card: https://huggingface.co/XunmeiLiu/VFIG-4B
- VFIG GitHub repository: https://github.com/RAIVNLab/VFig
- Qwen3-VL docs in Transformers: https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_vl
- Qwen3-VL-4B-Instruct model card: https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct
- VFIG quantized-derived listing: https://huggingface.co/models?other=base_model%3Aquantized%3AXunmeiLiu%2FVFIG-4B

## Agent-oriented MLX porting

- `transformers-to-mlx` repository: https://github.com/huggingface/transformers-to-mlx
- Hugging Face blog, 2026-04-16: https://huggingface.co/blog/transformers-to-mlx
