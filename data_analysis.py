import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 页面布局
st.set_page_config(layout="wide")

# 页面标题
st.title("交互火山图")

# 文件上传
st.sidebar.header("图表数据")
uploaded_file = st.sidebar.file_uploader("上传文件", type=["txt", "csv"])

# 数据表格显示
if uploaded_file:
    data = pd.read_csv(uploaded_file, sep="\t")  # 根据你的文件格式修改分隔符
    st.sidebar.subheader("查看数据")
    st.sidebar.dataframe(data)

    # 设置阈值
    st.sidebar.header("图表调整")
    fold_change_threshold = st.sidebar.slider("Fold Change 阈值", min_value=0.5, max_value=3.0, step=0.1, value=1.5)
    pvalue_threshold = st.sidebar.slider("P 值阈值", min_value=0.01, max_value=0.1, step=0.01, value=0.05)
    
    # 提交绘图按钮
    if st.sidebar.button("提交绘图"):
        # 火山图绘制逻辑
        data['-log10(pvalue)'] = -np.log10(data['pvalue'])

        # 分类标记
        data['color'] = 'gray'
        data.loc[(data['log2FoldChange'] > fold_change_threshold) & (data['pvalue'] < pvalue_threshold), 'color'] = 'red'
        data.loc[(data['log2FoldChange'] < -fold_change_threshold) & (data['pvalue'] < pvalue_threshold), 'color'] = 'blue'

        # 绘制火山图
        fig, ax = plt.subplots()
        ax.scatter(data['log2FoldChange'], data['-log10(pvalue)'], c=data['color'], alpha=0.7)
        ax.axhline(-np.log10(pvalue_threshold), color='black', linestyle='--')
        ax.axvline(fold_change_threshold, color='black', linestyle='--')
        ax.axvline(-fold_change_threshold, color='black', linestyle='--')
        ax.set_xlabel("log2(Fold Change)")
        ax.set_ylabel("-log10(p-value)")
        ax.legend(["Nodiff", "Down", "Up"], loc="upper right")

        # 展示火山图
        st.subheader("交互火山图")
        st.pyplot(fig)
else:
    st.sidebar.info("请上传数据文件以生成火山图。")
