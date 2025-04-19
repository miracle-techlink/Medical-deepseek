import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

class DataVisualizer:
    def __init__(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置Plotly模板
        self.template = 'plotly_white'
    
    def create_numeric_visualizations(self, json1):
        """创建数值型数据的可视化"""
        try:
            df = pd.DataFrame(json1)
            visualizations = {}
            
            # 1. 箱线图
            fig_box = go.Figure()
            for column in df.columns:
                fig_box.add_trace(go.Box(y=df[column], name=column))
            fig_box.update_layout(
                title='数值变量分布箱线图',
                template=self.template
            )
            visualizations['box_plot'] = fig_box
            
            # 2. 直方图
            fig_hist = go.Figure()
            for column in df.columns:
                fig_hist.add_trace(go.Histogram(x=df[column], name=column))
            fig_hist.update_layout(
                title='数值变量分布直方图',
                template=self.template,
                barmode='overlay'
            )
            visualizations['histogram'] = fig_hist
            
            # 3. 相关性热力图
            corr_matrix = df.corr()
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu'
            ))
            fig_heatmap.update_layout(
                title='数值变量相关性热力图',
                template=self.template
            )
            visualizations['heatmap'] = fig_heatmap
            
            return visualizations
        except Exception as e:
            raise Exception(f"创建数值型数据可视化失败: {str(e)}")
    
    def create_diagnosis_visualizations(self, json2):
        """创建诊断数据的可视化"""
        try:
            df = pd.DataFrame(json2)
            visualizations = {}
            
            # 1. 诊断频率柱状图
            if '病理诊断（病案首页）' in df.columns:
                diagnosis_counts = df['病理诊断（病案首页）'].value_counts().head(10)
                fig_bar = px.bar(
                    x=diagnosis_counts.index,
                    y=diagnosis_counts.values,
                    title='前10位诊断频率分布',
                    labels={'x': '诊断', 'y': '频次'}
                )
                fig_bar.update_layout(template=self.template)
                visualizations['diagnosis_bar'] = fig_bar
            
            # 2. 诊断词云
            if '病理诊断（病案首页）' in df.columns:
                text = ' '.join(df['病理诊断（病案首页）'].dropna())
                wordcloud = WordCloud(
                    font_path='simhei.ttf',
                    width=800,
                    height=400,
                    background_color='white'
                ).generate(text)
                
                fig_wordcloud = go.Figure()
                fig_wordcloud.add_trace(go.Image(z=wordcloud.to_array()))
                fig_wordcloud.update_layout(
                    title='诊断词云',
                    template=self.template
                )
                visualizations['wordcloud'] = fig_wordcloud
            
            return visualizations
        except Exception as e:
            raise Exception(f"创建诊断数据可视化失败: {str(e)}")
    
    def create_temporal_visualizations(self, json1):
        """创建时间序列数据的可视化"""
        try:
            df = pd.DataFrame(json1)
            visualizations = {}
            
            # 1. 时间趋势图
            for column in df.columns:
                if 'date' in column.lower() or 'time' in column.lower():
                    fig_trend = px.line(
                        df,
                        x=column,
                        y=df.select_dtypes(include=[np.number]).columns,
                        title=f'{column}趋势图'
                    )
                    fig_trend.update_layout(template=self.template)
                    visualizations[f'trend_{column}'] = fig_trend
            
            return visualizations
        except Exception as e:
            raise Exception(f"创建时间序列数据可视化失败: {str(e)}")
    
    def create_comparison_visualizations(self, json1, json2):
        """创建对比分析的可视化"""
        try:
            df1 = pd.DataFrame(json1)
            df2 = pd.DataFrame(json2)
            visualizations = {}
            
            # 1. 数值型变量与诊断的关联分析
            if '病理诊断（病案首页）' in df2.columns:
                for column in df1.columns:
                    fig_box = px.box(
                        pd.concat([df1[column], df2['病理诊断（病案首页）']], axis=1),
                        x='病理诊断（病案首页）',
                        y=column,
                        title=f'{column}与诊断的分布关系'
                    )
                    fig_box.update_layout(template=self.template)
                    visualizations[f'comparison_{column}'] = fig_box
            
            return visualizations
        except Exception as e:
            raise Exception(f"创建对比分析可视化失败: {str(e)}")
    
    def create_all_visualizations(self, json1, json2):
        """创建所有可视化"""
        try:
            all_visualizations = {
                'numeric': self.create_numeric_visualizations(json1),
                'diagnosis': self.create_diagnosis_visualizations(json2),
                'temporal': self.create_temporal_visualizations(json1),
                'comparison': self.create_comparison_visualizations(json1, json2)
            }
            return all_visualizations
        except Exception as e:
            raise Exception(f"创建可视化失败: {str(e)}")
    
    def save_visualizations(self, visualizations, output_dir):
        """保存可视化结果"""
        try:
            for category, category_visualizations in visualizations.items():
                for name, fig in category_visualizations.items():
                    fig.write_html(f"{output_dir}/{category}_{name}.html")
                    fig.write_image(f"{output_dir}/{category}_{name}.png")
        except Exception as e:
            raise Exception(f"保存可视化结果失败: {str(e)}")