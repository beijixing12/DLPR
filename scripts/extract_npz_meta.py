"""
Utility script to derive KSS meta-data files from a sequential interaction NPZ dataset.

Expected NPZ keys
-----------------
- `question_id`: question identifiers (shape [num_seq, seq_len] or flat)
- `skill`: knowledge/skill identifiers aligned with `question_id`
- `y`: binary correctness labels aligned with `question_id`
- `mask`: optional boolean/int mask indicating valid timesteps (1/True = valid)

Outputs
-------
- learning_order.json: list of knowledge IDs ordered by frequency (descending).
- items.json: list of question records {"id", "knowledge", "difficulty", "content"}.
- know_item.json: mapping knowledge ID -> list of question IDs.

Usage
-----
python scripts/extract_npz_meta.py \
    --npz_path path/to/dataset.npz \
    --output_dir EduSim/Envs/KSS/meta_data
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


def _flatten_field(field):
    """Flatten ndarray or object array of variable-length sequences."""

    arr = np.asarray(field)
    if arr.dtype == object:
        return np.concatenate([np.asarray(seq).reshape(-1) for seq in arr])
    return arr.reshape(-1)


def load_valid_fields(npz_data):
    """Flatten aligned fields and apply mask if available (supports ragged inputs)."""

    question_ids = _flatten_field(npz_data["question_id"])
    knowledge_ids = _flatten_field(npz_data["skill"])
    correctness_raw = npz_data.get("y")
    correctness = _flatten_field(correctness_raw) if correctness_raw is not None else None

    mask = npz_data.get("mask")
    if mask is not None:
        flat_mask = _flatten_field(mask).astype(bool)

        expected = len(flat_mask)
        if not (expected == len(question_ids) == len(knowledge_ids) == (len(correctness) if correctness is not None else expected)):
            raise ValueError(
                "Mask, question_id, skill, and y fields must align after flattening."
            )

        question_ids = question_ids[flat_mask]
        knowledge_ids = knowledge_ids[flat_mask]
        if correctness is not None:
            correctness = correctness[flat_mask]

    # Normalize to built-in Python scalars for JSON serialization downstream.
    question_ids = [int(q) for q in question_ids]
    knowledge_ids = [int(k) for k in knowledge_ids]
    if correctness is not None:
        correctness = [float(c) for c in correctness]

    return question_ids, knowledge_ids, correctness


def build_learning_order(knowledge_ids):
    counts = Counter(knowledge_ids)
    # Order by frequency (descending) then by knowledge id for determinism.
    ordered = [int(k) for k, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
    return ordered


def build_items(question_ids, knowledge_ids, correctness):
    question_to_knowledge = {}
    question_correctness = defaultdict(list)

    for qid, kid, label in zip(question_ids, knowledge_ids, correctness if correctness is not None else [None] * len(question_ids)):
        question_to_knowledge.setdefault(int(qid), int(kid))
        if label is not None:
            question_correctness[int(qid)].append(float(label))

    items = []
    for qid, kid in question_to_knowledge.items():
        if question_correctness[qid]:
            acc = float(np.mean(question_correctness[qid]))
            difficulty = float(1.0 - acc)
        else:
            difficulty = 0.5
        items.append({
            "id": qid,
            "knowledge": kid,
            "difficulty": difficulty,
            "content": {},
        })
    # Stable ordering for reproducibility.
    items.sort(key=lambda item: item["id"])
    return items


def build_know_item(items):
    mapping = defaultdict(list)
    for item in items:
        mapping[item["knowledge"]].append(item["id"])
    return {int(k): v for k, v in sorted(mapping.items(), key=lambda pair: pair[0])}


def write_json(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Extract KSS meta-data from NPZ dataset.")
    parser.add_argument("--npz_path", required=True, type=Path, help="Path to the source NPZ file.")
    parser.add_argument("--output_dir", default='/home/zengxiangyu/DLPR-main/DLPR-main/EduSim/Envs/assist09', required=True, type=Path, help="Directory to write JSON outputs.")
    args = parser.parse_args()

    data = np.load(args.npz_path, allow_pickle=True)
    question_ids, knowledge_ids, correctness = load_valid_fields(data)

    learning_order = build_learning_order(knowledge_ids)
    items = build_items(question_ids, knowledge_ids, correctness)
    know_item = build_know_item(items)

    write_json(learning_order, args.output_dir / "learning_order.json")
    write_json(items, args.output_dir / "items.json")
    write_json(know_item, args.output_dir / "know_item.json")

    print(f"Wrote learning_order.json, items.json, know_item.json to {args.output_dir}")


if __name__ == "__main__":
    main()


# python extract_npz_meta.py --npz_path /home/zengxiangyu/DIMKT-main/data/assist09.npz --output_dir /home/zengxiangyu/DLPR-main/DLPR-main/EduSim/Envs/assist09
# python extract_npz_meta.py --npz_path /home/zengxiangyu/DIMKT-main/data/assist12.npz --output_dir /home/zengxiangyu/DLPR-main/DLPR-main/EduSim/Envs/assist12
