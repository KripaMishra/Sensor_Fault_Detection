from __future__ import annotations

import argparse
from pathlib import Path

from .model import predict, train


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train and run the APS fault classifier.")
    commands = parser.add_subparsers(dest="command", required=True)

    train_parser = commands.add_parser("train", help="Train and evaluate on a held-out split")
    train_parser.add_argument("--data", required=True, type=Path)
    train_parser.add_argument("--schema", type=Path, default=Path("configs/schema.yaml"))
    train_parser.add_argument("--output-dir", type=Path, default=Path("outputs/latest"))
    train_parser.add_argument("--seed", type=int, default=42)
    train_parser.add_argument("--test-size", type=float, default=0.2)

    predict_parser = commands.add_parser("predict", help="Predict labels for a feature-only CSV")
    predict_parser.add_argument("--data", required=True, type=Path)
    predict_parser.add_argument("--model", required=True, type=Path)
    predict_parser.add_argument("--schema", type=Path, default=Path("configs/schema.yaml"))
    predict_parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "train":
        result = train(args.data, args.schema, args.output_dir, seed=args.seed, test_size=args.test_size)
        print(f"Holdout F1: {result['metrics']['f1']:.3f}")
        print(f"Artifacts: {result['output_dir']}")
    else:
        result = predict(args.data, args.model, args.schema, args.output)
        print(f"Wrote {len(result)} predictions to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
