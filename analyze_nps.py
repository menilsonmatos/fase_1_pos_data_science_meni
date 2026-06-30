from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "desafio_nps_fase_1.csv"
PROCESSED_DATA = ROOT / "data" / "processed" / "desafio_nps_fase_1_enriched.csv"
REPORT_DIR = ROOT / "reports"
FIG_DIR = REPORT_DIR / "figures"


def nps_class(score: float) -> str:
    if score <= 6:
        return "Detrator"
    if score <= 8:
        return "Neutro"
    return "Promotor"


def write_svg_bar(path: Path, title: str, labels: list[str], values: list[float], suffix: str = "") -> None:
    width, height = 920, 520
    margin_left, margin_top = 220, 72
    bar_h, gap = 36, 18
    max_value = max(values) if values else 1
    plot_w = width - margin_left - 90
    rows = []
    for i, (label, value) in enumerate(zip(labels, values)):
        y = margin_top + i * (bar_h + gap)
        bar_w = 0 if max_value == 0 else value / max_value * plot_w
        rows.append(
            f'<text x="24" y="{y + 24}" class="label">{escape(label)}</text>'
            f'<rect x="{margin_left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="4" class="bar"/>'
            f'<text x="{margin_left + bar_w + 12:.1f}" y="{y + 24}" class="value">{value:.2f}{suffix}</text>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .bg {{ fill: #101114; }}
    .title {{ fill: #f5f7fb; font: 700 28px Arial, sans-serif; }}
    .label {{ fill: #d7dce6; font: 15px Arial, sans-serif; }}
    .value {{ fill: #f5f7fb; font: 700 15px Arial, sans-serif; }}
    .bar {{ fill: #ef2d7a; }}
  </style>
  <rect width="100%" height="100%" class="bg"/>
  <text x="24" y="42" class="title">{escape(title)}</text>
  {''.join(rows)}
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def write_svg_grouped(path: Path, title: str, labels: list[str], series: dict[str, list[float]]) -> None:
    width, height = 980, 560
    margin_left, margin_top = 90, 86
    plot_w, plot_h = width - 150, height - 170
    groups = len(labels)
    names = list(series)
    colors = ["#ef2d7a", "#45d4c9", "#f5b84b"]
    max_value = max([max(v) for v in series.values()] + [1])
    group_w = plot_w / max(groups, 1)
    bar_w = min(34, group_w / (len(names) + 1))
    bars = []
    for i, label in enumerate(labels):
        x0 = margin_left + i * group_w + group_w * 0.18
        for j, name in enumerate(names):
            value = series[name][i]
            h = value / max_value * plot_h
            x = x0 + j * (bar_w + 6)
            y = margin_top + plot_h - h
            bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" class="s{j}" rx="3"/>')
        bars.append(
            f'<text x="{margin_left + i * group_w + group_w / 2:.1f}" y="{margin_top + plot_h + 34}" '
            f'class="tick" text-anchor="middle">{escape(label)}</text>'
        )
    legend = []
    for j, name in enumerate(names):
        x = margin_left + j * 170
        legend.append(f'<rect x="{x}" y="{height - 42}" width="18" height="18" class="s{j}"/>')
        legend.append(f'<text x="{x + 26}" y="{height - 27}" class="legend">{escape(name)}</text>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .bg {{ fill: #101114; }}
    .title {{ fill: #f5f7fb; font: 700 28px Arial, sans-serif; }}
    .tick,.legend {{ fill: #d7dce6; font: 14px Arial, sans-serif; }}
    .axis {{ stroke: #333842; stroke-width: 1; }}
    .s0 {{ fill: {colors[0]}; }}
    .s1 {{ fill: {colors[1]}; }}
    .s2 {{ fill: {colors[2]}; }}
  </style>
  <rect width="100%" height="100%" class="bg"/>
  <text x="24" y="46" class="title">{escape(title)}</text>
  <line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" class="axis"/>
  {''.join(bars)}
  {''.join(legend)}
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def to_markdown_table(df: pd.DataFrame) -> str:
    table = df.reset_index()
    table.columns = [str(c) for c in table.columns]
    formatted = table.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].map(lambda x: f"{x:.2f}" if isinstance(x, (float, np.floating)) else str(x))
    widths = {col: max(len(col), *(len(v) for v in formatted[col])) for col in formatted.columns}
    header = "| " + " | ".join(col.ljust(widths[col]) for col in formatted.columns) + " |"
    sep = "| " + " | ".join("-" * widths[col] for col in formatted.columns) + " |"
    rows = [
        "| " + " | ".join(row[col].ljust(widths[col]) for col in formatted.columns) + " |"
        for _, row in formatted.iterrows()
    ]
    return "\n".join([header, sep, *rows])


def make_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    y = (df["nps_score"] <= 6).astype(int)
    base = df.drop(columns=["nps_score", "nps_group", "customer_id", "order_id"], errors="ignore")
    X = pd.get_dummies(base, columns=["customer_region"], drop_first=False, dtype=float)
    feature_names = list(X.columns)
    return X.astype(float), y, feature_names


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -35, 35)
    return 1 / (1 + np.exp(-z))


def fit_logistic_regression(X: pd.DataFrame, y: pd.Series, epochs: int = 2600, lr: float = 0.07) -> dict:
    rng = np.random.default_rng(42)
    idx = rng.permutation(len(X))
    split = int(len(X) * 0.8)
    train_idx, test_idx = idx[:split], idx[split:]

    X_train_raw = X.iloc[train_idx].to_numpy(dtype=float)
    X_test_raw = X.iloc[test_idx].to_numpy(dtype=float)
    y_train = y.iloc[train_idx].to_numpy(dtype=float)
    y_test = y.iloc[test_idx].to_numpy(dtype=float)

    mean = X_train_raw.mean(axis=0)
    std = X_train_raw.std(axis=0)
    std[std == 0] = 1
    X_train = (X_train_raw - mean) / std
    X_test = (X_test_raw - mean) / std
    X_train = np.c_[np.ones(len(X_train)), X_train]
    X_test = np.c_[np.ones(len(X_test)), X_test]

    weights = np.zeros(X_train.shape[1])
    for _ in range(epochs):
        pred = sigmoid(X_train @ weights)
        grad = X_train.T @ (pred - y_train) / len(y_train)
        weights -= lr * grad

    proba = sigmoid(X_test @ weights)
    pred = (proba >= 0.5).astype(int)
    accuracy = float((pred == y_test).mean())
    tp = int(((pred == 1) & (y_test == 1)).sum())
    tn = int(((pred == 0) & (y_test == 0)).sum())
    fp = int(((pred == 1) & (y_test == 0)).sum())
    fn = int(((pred == 0) & (y_test == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    return {
        "accuracy": accuracy,
        "precision_detractor": precision,
        "recall_detractor": recall,
        "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
        "coefficients": weights[1:].tolist(),
    }


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "processed").mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_DATA)
    df["nps_group"] = df["nps_score"].apply(nps_class)
    df["has_delay"] = (df["delivery_delay_days"] > 0).astype(int)
    df["has_complaint"] = (df["complaints_count"] > 0).astype(int)
    df["had_service_contact"] = (df["customer_service_contacts"] > 0).astype(int)
    PROCESSED_DATA.write_text(df.to_csv(index=False), encoding="utf-8")

    nps_distribution = df["nps_group"].value_counts(normalize=True).reindex(["Detrator", "Neutro", "Promotor"]).fillna(0) * 100
    nps_index = nps_distribution["Promotor"] - nps_distribution["Detrator"]

    numeric_cols = [
        c
        for c in df.select_dtypes(include=[np.number]).columns
        if c not in {"customer_id", "order_id", "nps_score"}
    ]
    corr = df[numeric_cols + ["nps_score"]].corr(numeric_only=True)["nps_score"].drop("nps_score").sort_values()

    operational_cols = [
        "complaints_count",
        "csat_internal_score",
        "resolution_time_days",
        "customer_service_contacts",
        "delivery_delay_days",
        "delivery_time_days",
        "delivery_attempts",
        "freight_value",
        "repeat_purchase_30d",
        "customer_tenure_months",
        "order_value",
    ]
    critical = corr.reindex(operational_cols).dropna().sort_values()

    by_region = df.groupby("customer_region").agg(
        orders=("order_id", "count"),
        avg_nps=("nps_score", "mean"),
        detractor_rate=("nps_group", lambda s: (s == "Detrator").mean() * 100),
        promoter_rate=("nps_group", lambda s: (s == "Promotor").mean() * 100),
    ).sort_values("avg_nps")

    delay_bins = pd.cut(
        df["delivery_delay_days"],
        bins=[-0.1, 0, 1, 3, 8],
        labels=["0 dias", "1 dia", "2-3 dias", "4+ dias"],
    )
    by_delay = df.groupby(delay_bins, observed=False).agg(
        orders=("order_id", "count"),
        avg_nps=("nps_score", "mean"),
        detractor_rate=("nps_group", lambda s: (s == "Detrator").mean() * 100),
    )

    complaint_bins = pd.cut(
        df["complaints_count"],
        bins=[-0.1, 0, 2, 5, 20],
        labels=["0", "1-2", "3-5", "6+"],
    )
    by_complaint = df.groupby(complaint_bins, observed=False).agg(
        orders=("order_id", "count"),
        avg_nps=("nps_score", "mean"),
        detractor_rate=("nps_group", lambda s: (s == "Detrator").mean() * 100),
    )

    service_bins = pd.cut(
        df["customer_service_contacts"],
        bins=[-0.1, 0, 1, 2, 10],
        labels=["0", "1", "2", "3+"],
    )
    by_service = df.groupby(service_bins, observed=False).agg(
        orders=("order_id", "count"),
        avg_nps=("nps_score", "mean"),
        detractor_rate=("nps_group", lambda s: (s == "Detrator").mean() * 100),
    )

    X, y, features = make_features(df)
    model = fit_logistic_regression(X, y)
    coef = pd.Series(model["coefficients"], index=features).sort_values()
    model["top_risk_factors"] = coef.tail(8).sort_values(ascending=False).to_dict()
    model["top_protection_factors"] = coef.head(8).to_dict()

    write_svg_bar(
        FIG_DIR / "01_nps_distribution.svg",
        "Distribuição dos clientes por classe de NPS",
        list(nps_distribution.index),
        [float(v) for v in nps_distribution.values],
        "%",
    )
    write_svg_bar(
        FIG_DIR / "02_critical_factors.svg",
        "Correlação com NPS: fatores operacionais críticos",
        [c.replace("_", " ") for c in critical.index],
        [float(abs(v)) for v in critical.values],
    )
    write_svg_grouped(
        FIG_DIR / "03_delay_impact.svg",
        "Atraso na entrega eleva risco de detrator",
        [str(x) for x in by_delay.index],
        {"NPS médio": by_delay["avg_nps"].tolist(), "% detratores": by_delay["detractor_rate"].tolist()},
    )
    write_svg_grouped(
        FIG_DIR / "04_complaints_impact.svg",
        "Reclamações são o principal ponto de ruptura",
        [str(x) for x in by_complaint.index],
        {"NPS médio": by_complaint["avg_nps"].tolist(), "% detratores": by_complaint["detractor_rate"].tolist()},
    )

    summary = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "nps_mean": float(df["nps_score"].mean()),
        "nps_median": float(df["nps_score"].median()),
        "nps_index": float(nps_index),
        "nps_distribution_pct": nps_distribution.round(2).to_dict(),
        "critical_correlations": critical.round(4).to_dict(),
        "by_region": by_region.round(2).to_dict(orient="index"),
        "by_delay": by_delay.round(2).to_dict(orient="index"),
        "by_complaint": by_complaint.round(2).to_dict(orient="index"),
        "by_service": by_service.round(2).to_dict(orient="index"),
        "model": model,
    }
    (REPORT_DIR / "analysis_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    markdown = [
        "# Relatório Analítico - Tech Challenge Fase 1",
        "",
        "## Sumário executivo",
        f"- Base analisada: {len(df):,} pedidos.".replace(",", "."),
        f"- NPS médio: {df['nps_score'].mean():.2f}; mediana: {df['nps_score'].median():.2f}.",
        f"- NPS calculado por classes: {nps_index:.1f} p.p. (promotores - detratores).",
        f"- Distribuição: {nps_distribution['Detrator']:.1f}% detratores, {nps_distribution['Neutro']:.1f}% neutros e {nps_distribution['Promotor']:.1f}% promotores.",
        "",
        "## Principais achados",
        "- A satisfação é mais sensível a fatores de fricção operacional: reclamações, atendimento, prazo de resolução e atraso logístico.",
        "- O ponto de ruptura mais claro aparece quando o cliente acumula reclamações. A taxa de detratores sobe de forma material conforme o volume de reclamações aumenta.",
        "- Atrasos de entrega e múltiplas tentativas de entrega reduzem a experiência percebida e devem acionar tratativas preventivas.",
        "- O score interno de satisfação acompanha positivamente o NPS e pode funcionar como sinal antecipado, desde que não substitua a pesquisa final.",
        "",
        "## Impacto por atraso de entrega",
        to_markdown_table(by_delay.round(2)),
        "",
        "## Impacto por reclamações",
        to_markdown_table(by_complaint.round(2)),
        "",
        "## Impacto por contatos com atendimento",
        to_markdown_table(by_service.round(2)),
        "",
        "## Regiões",
        to_markdown_table(by_region.round(2)),
        "",
        "## Modelo preditivo opcional",
        "Foi treinado um modelo de regressão logística simples, implementado com NumPy, para prever risco de cliente detrator (NPS <= 6).",
        f"- Acurácia: {model['accuracy']:.2%}.",
        f"- Precisão para detratores: {model['precision_detractor']:.2%}.",
        f"- Recall para detratores: {model['recall_detractor']:.2%}.",
        f"- Matriz de confusão: {model['confusion_matrix']}.",
        "",
        "## Recomendação gerencial",
        "- Criar uma régua de alerta para pedidos com atraso, reclamação ou múltiplos contatos com atendimento.",
        "- Priorizar resolução rápida de problemas antes do envio da pesquisa NPS.",
        "- Integrar logística e atendimento em uma fila única de recuperação de experiência.",
        "- Acompanhar NPS previsto por operação, região e faixa de atraso para orientar ações preventivas.",
    ]
    (REPORT_DIR / "relatorio_analitico.md").write_text("\n".join(markdown), encoding="utf-8")


if __name__ == "__main__":
    main()
