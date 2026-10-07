from pathlib import Path


def read_uploaded_report(upload_dir: str, filename: str) -> str:
    report_path = Path(upload_dir) / filename
    return report_path.read_text(encoding="utf-8")
