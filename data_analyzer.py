import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_numeric_data(self, json1):
        """分析数值型数据"""
        try:
            df = pd.DataFrame(json1)
            
            # 基本统计描述
            basic_stats = df.describe().to_dict()
            
            # 异常值检测
            outliers = {}
            for column in df.columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers[column] = {
                    'count': len(df[(df[column] < lower_bound) | (df[column] > upper_bound)]),
                    'percentage': len(df[(df[column] < lower_bound) | (df[column] > upper_bound)]) / len(df) * 100
                }
            
            # 相关性分析
            correlation = df.corr().to_dict()
            
            return {
                'basic_stats': basic_stats,
                'outliers': outliers,
                'correlation': correlation
            }
        except Exception as e:
            raise Exception(f"数值型数据分析失败: {str(e)}")
    
    def analyze_text_data(self, json2):
        """分析文本型数据"""
        try:
            df = pd.DataFrame(json2)
            
            # 文本长度分析
            text_lengths = {}
            for column in df.columns:
                if df[column].dtype == 'object':
                    text_lengths[column] = {
                        'mean_length': df[column].str.len().mean(),
                        'max_length': df[column].str.len().max(),
                        'min_length': df[column].str.len().min()
                    }
            
            # 唯一值分析
            unique_values = {}
            for column in df.columns:
                if df[column].dtype == 'object':
                    unique_values[column] = {
                        'count': df[column].nunique(),
                        'top_values': df[column].value_counts().head(5).to_dict()
                    }
            
            return {
                'text_lengths': text_lengths,
                'unique_values': unique_values
            }
        except Exception as e:
            raise Exception(f"文本型数据分析失败: {str(e)}")
    
    def analyze_diagnosis_data(self, json2):
        """分析诊断数据"""
        try:
            df = pd.DataFrame(json2)
            
            # 诊断频率分析
            diagnosis_freq = {}
            if '病理诊断（病案首页）' in df.columns:
                diagnosis_freq = df['病理诊断（病案首页）'].value_counts().head(10).to_dict()
            
            # 诊断词云分析
            diagnosis_words = {}
            if '病理诊断（病案首页）' in df.columns:
                words = df['病理诊断（病案首页）'].str.split(',').explode().str.strip()
                diagnosis_words = words.value_counts().head(20).to_dict()
            
            return {
                'diagnosis_freq': diagnosis_freq,
                'diagnosis_words': diagnosis_words
            }
        except Exception as e:
            raise Exception(f"诊断数据分析失败: {str(e)}")
    
    def analyze_temporal_data(self, json1):
        """分析时间序列数据"""
        try:
            df = pd.DataFrame(json1)
            
            # 时间趋势分析
            temporal_trends = {}
            for column in df.columns:
                if 'date' in column.lower() or 'time' in column.lower():
                    temporal_trends[column] = {
                        'min_date': df[column].min(),
                        'max_date': df[column].max(),
                        'date_range': (df[column].max() - df[column].min()).days
                    }
            
            return temporal_trends
        except Exception as e:
            raise Exception(f"时间序列数据分析失败: {str(e)}")
    
    def analyze_data(self, json1, json2):
        """完整的数据分析流程"""
        try:
            self.analysis_results = {
                'numeric_analysis': self.analyze_numeric_data(json1),
                'text_analysis': self.analyze_text_data(json2),
                'diagnosis_analysis': self.analyze_diagnosis_data(json2),
                'temporal_analysis': self.analyze_temporal_data(json1)
            }
            return self.analysis_results
        except Exception as e:
            raise Exception(f"数据分析失败: {str(e)}")
    
    def get_summary_statistics(self):
        """获取汇总统计信息"""
        try:
            summary = {
                'total_records': len(pd.DataFrame(json1)),
                'numeric_features': len(pd.DataFrame(json1).columns),
                'text_features': len(pd.DataFrame(json2).columns),
                'diagnosis_categories': len(self.analysis_results['diagnosis_analysis']['diagnosis_freq'])
            }
            return summary
        except Exception as e:
            raise Exception(f"获取汇总统计信息失败: {str(e)}")