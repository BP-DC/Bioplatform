import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置页面标题
st.title("火山图分析应用")

# 创建两列布局
col1, col2 = st.columns([1, 3])  # 右侧列较宽，用于火山图

# 左侧栏：上传文件、设置参数和示例数据
with col1:
    st.header("上传文件")
    uploaded_file = st.file_uploader("选择一个CSV文件", type=["csv"])

    st.header("分析参数")
    fold_change_threshold = st.slider("Fold Change (FC) 阈值", min_value=0.0, max_value=5.0, value=1.5, step=0.1)
    pval_threshold = st.slider("P 值阈值", min_value=0.0, max_value=0.05, value=0.05, step=0.01)
    
    st.header("绘图参数")
    point_size = st.slider("点的大小", min_value=10, max_value=200, value=40, step=10)
    point_alpha = st.slider("点的透明度", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

    # 显示示例数据
    default_data = pd.DataFrame({
        "group_A": [2.0, 1.8, 2.3, 1.0, 3.2, 2.5, 1.7, 2.1, 1.9, 2.6, 2.0, 1.8, 2.3, 1.0, 3.2, 2.5, 1.7, 2.1, 1.9, 2.6],
        "group_B": [3.5, 2.1, 4.0, 1.2, 5.0, 3.1, 2.0, 3.3, 2.8, 3.7, 2.0, 1.8, 2.3, 1.0, 3.2, 2.5, 1.7, 2.1, 1.9, 2.6]
    })
    st.subheader("示例数据")
    st.write(default_data.head())

# 使用默认数据或上传的数据
data = default_data if uploaded_file is None else pd.read_csv(uploaded_file)

# 右侧栏：显示火山图
with col2:
    # 确保数据有两列，分别为group_A和group_B
    if data.shape[1] == 2:
        # 计算Fold Change和P-value
        data.columns = ['group_A', 'group_B']
        data['log2FoldChange'] = np.log2(data['group_B'] / data['group_A'])
        _, pval = stats.ttest_ind(data['group_A'], data['group_B'])
        data['pvalue'] = pval

        # 设置点的颜色，显著性高的为红色，显著性中等为橙色，其余为蓝色
        data["color"] = np.where(
            (data["log2FoldChange"] >= fold_change_threshold) & (data["pvalue"] <= pval_threshold), "red",
            np.where((data["log2FoldChange"] < fold_change_threshold) & (data["pvalue"] <= pval_threshold), "orange", "blue")
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
        
        # 显示火山图
        st.pyplot(fig)
    else:
        st.error("数据必须包含两列，分别表示group_A和group_B。")
