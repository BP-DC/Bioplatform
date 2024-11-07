import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = pd.DataFrame({
    "gene": ["GeneA", "GeneB", "GeneC", "GeneD", "GeneE"],
    "log2FoldChange": [1.5, -2.0, 0.5, 3.0, -1.2],
    "pvalue": [0.001, 0.05, 0.02, 0.001, 0.03]
})

# 设置参数
fold_change_threshold = st.slider("Fold Change 阈值", min_value=0, max_value=3, value=1.5, step=0.1)
pval_threshold = st.slider("P 值阈值", min_value=0.0, max_value=0.05, value=0.05, step=0.01)

# 绘制火山图
fig, ax = plt.subplots()
data["color"] = np.where((data["log2FoldChange"] >= fold_change_threshold) & (data["pvalue"] <= pval_threshold), "red", "blue")
ax.scatter(data["log2FoldChange"], -np.log10(data["pvalue"]), c=data["color"])
ax.axhline(-np.log10(pval_threshold), color="black", linestyle="--")
ax.axvline(fold_change_threshold, color="black", linestyle="--")
ax.axvline(-fold_change_threshold, color="black", linestyle="--")
ax.set_xlabel("log2(Fold Change)")
ax.set_ylabel("-log10(P value)")
ax.set_title("Volcano Plot")

st.pyplot(fig)
