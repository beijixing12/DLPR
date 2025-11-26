# Script usage

## extract_npz_meta.py

`extract_npz_meta.py` builds the three KSS meta-data files (`learning_order.json`, `items.json`, `know_item.json`) from a sequential NPZ dataset. It expects `question_id`, `skill`, and optionally `y` (correctness) and `mask` arrays.

### Processing logic
- Loads the NPZ, flattens `question_id`, `skill`, and `y`, and supports ragged/object-array masks by concatenating variable-length sequences before applying the timestep `mask` if present.
- Builds `learning_order.json` by counting knowledge frequency and ordering by descending count (tie-broken by knowledge ID).
- Builds `items.json` by pairing each question ID with its knowledge ID and estimating difficulty as `1 - mean(correctness)` when labels are available (defaults to 0.5 otherwise). Content is left empty (`{}`) for each item.
- Builds `know_item.json` by grouping question IDs under their knowledge ID.

### Example command
```bash
python scripts/extract_npz_meta.py \
  --npz_path path/to/dataset.npz \
  --output_dir EduSim/Envs/KSS/meta_data
```

The script creates the output directory if it does not exist and prints a summary of the generated files.

## Recommended run order and what each step does
1. **准备输出目录**（仅需指定即可）：传入 `--output_dir`，脚本会自动创建目录，无需手工新建。
2. **运行提取命令**（核心一步）：执行上面的命令后，脚本会顺序完成以下操作：
   - 读取 NPZ 并对 `question_id`、`skill`（以及可选的 `y`、`mask`）做展平和遮罩过滤，确保时间步对齐。【F:scripts/extract_npz_meta.py†L32-L70】
   - 基于知识点出现频次降序生成 `learning_order.json`，供环境冷启动时的默认学习路径使用。【F:scripts/extract_npz_meta.py†L73-L78】
   - 生成 `items.json`：为每个题目记录所属知识点、基于正确率估计的难度（无标签时默认 0.5），内容字段留空。【F:scripts/extract_npz_meta.py†L80-L104】
   - 生成 `know_item.json`：将题目按知识点分组映射，便于环境查询每个知识点下的题目列表。【F:scripts/extract_npz_meta.py†L107-L111】
3. **查看输出**：命令结束后会在 `--output_dir` 下看到三份 JSON，并打印提示信息，便于确认路径是否正确。【F:scripts/extract_npz_meta.py†L120-L140】
