import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置页面标题
st.title("火山图分析应用")

# 侧边栏输入控件
st.sidebar.header("设置参数")
fold_change_threshold = st.sidebar.slider("Fold Change (FC) 阈值", min_value=0.0, max_value=5.0, value=1.5, step=0.1)
pval_threshold = st.sidebar.slider("P 值阈值", min_value=0.0, max_value=0.05, value=0.05, step=0.01)
point_size = st.sidebar.slider("点的大小", min_value=10, max_value=200, value=40, step=10)
point_alpha = st.sidebar.slider("点的透明度", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

# 上传数据文件
st.sidebar.header("上传数据")
uploaded_file = st.sidebar.file_uploader("选择一个CSV文件", type=["csv"])

# 默认数据集
default_data = pd.DataFrame({
    "group_A": [2.0, 1.8, 2.3, 1.0, 3.2, 2.5, 1.7, 2.1, 1.9, 2.6],
    "group_B": [3.5, 2.1, 4.0, 1.2, 5.0, 3.1, 2.0, 3.3, 2.8, 3.7]
})

# 显示默认数据预览在侧边栏
st.sidebar.subheader("默认数据预览")
st.sidebar.write(default_data.head())

# 使用默认数据或上传的数据
if uploaded_file is not None:
    # 读取上传的CSV文件
    data = pd.read_csv(uploaded_file)
    st.subheader("上传的数据预览")
else:
    # 使用默认数据
    data = default_data

# 显示数据
# st.write(data.head())

# 确保数据有两列，分别为group_A和group_B
if data.shape[1] == 2:
    # 计算Fold Change和P-value
    data.columns = ['group_A', 'group_B']

    # 计算Fold Change (log2 scale)
    data['log2FoldChange'] = np.log2(data['group_B'] / data['group_A'])

    # 计算p-value
    _, pval = stats.ttest_ind(data['group_A'], data['group_B'])
    data['pvalue'] = pval

    # 根据FC和P值计算点的颜色
    data["color"] = np.where(
        (data["log2FoldChange"] >= fold_change_threshold) & (data["pvalue"] <= pval_threshold), "red", "blue"
    )

    # 绘制火山图
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(data["log2FoldChange"], -np.log10(data["pvalue"]), 
               c=data["color"], s=point_size, alpha=point_alpha, edgecolor="k")

    # 添加阈值线
    ax.axhline(-np.log10(pval_threshold), color="black", linestyle="--", label="P-value threshold")
    ax.axvline(fold_change_threshold, color="black", linestyle="--", label="Fold Change threshold")
    ax.axvline(-fold_change_threshold, color="black", linestyle="--")

    # 设置标签和标题
    ax.set_xlabel("log2(Fold Change)")
    ax.set_ylabel("-log10(P value)")
    ax.set_title("Volcano Plot")

    # 显示图例
    ax.legend()

    # 显示图形
    st.pyplot(fig)
else:
    st.error("数据必须包含两列，分别表示group_A和group_B。")
