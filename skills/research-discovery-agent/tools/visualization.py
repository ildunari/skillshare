"""
Visualization helpers. Uses matplotlib (no seaborn).
"""
from typing import Dict, List
import matplotlib.pyplot as plt

def bar_chart(data: Dict[str, float], title: str = "", xlabel: str = "", ylabel: str = "") -> None:
    labels = list(data.keys())
    values = list(data.values())
    plt.figure()
    plt.bar(labels, values)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def line_chart(xs: List[str], ys: List[float], title: str = "", xlabel: str = "", ylabel: str = "") -> None:
    plt.figure()
    plt.plot(xs, ys)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
