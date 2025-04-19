import pandas as pd
import json
import math

class DataProcessor:
    def __init__(self):
        self.json1 = None
        self.json2 = None
    
    def load_and_clean_data(self, file_path):
        """加载并清理CSV数据"""
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path, encoding='gbk')
            
            # 删除指定的列
            columns_to_drop = ['病案号', '门诊号', '住院号', '就诊标识（医渡云计算）', '报告单号']
            df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
            
            # 删除完全为空的列
            df.dropna(axis=1, how='all', inplace=True)
            
            return df
        except Exception as e:
            raise Exception(f"数据加载和清理失败: {str(e)}")
    
    def clean_nan_in_json(self, data):
        """递归地从字典中去除NaN值，但保留列结构"""
        if isinstance(data, dict):
            return {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.clean_nan_in_json(item) for item in data]
        else:
            return data
    
    def remove_none_values(self, data):
        """去除值为None的键值对"""
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self.remove_none_values(item) for item in data]
        else:
            return data
    
    def separate_data(self, data):
        """根据值的类型将数据分为json1和json2"""
        json1 = []
        json2 = []
        for record in data:
            record_json1 = {}
            record_json2 = {}
            for key, value in record.items():
                if isinstance(value, (int, float)) or isinstance(value, bool):
                    record_json1[key] = value
                else:
                    record_json2[key] = value
            json1.append(record_json1)
            json2.append(record_json2)
        return json1, json2
    
    def prepare_for_model_summary(self, data):
        """将json2转换为适合大模型汇总的格式"""
        model_summary_data = []
        for record in data:
            summary_record = {}
            for key, value in record.items():
                summary_record[key] = value
            model_summary_data.append(summary_record)
        return model_summary_data
    
    def process_data(self, file_path):
        """完整的数据处理流程"""
        try:
            # 1. 加载和清理数据
            df = self.load_and_clean_data(file_path)
            
            # 2. 转换为字典列表
            json_dict = df.to_dict(orient='records')
            
            # 3. 清理NaN值
            cleaned_dict = [self.clean_nan_in_json(record) for record in json_dict]
            
            # 4. 去除None值
            cleaned_dict_no_none = [self.remove_none_values(record) for record in cleaned_dict]
            
            # 5. 分离数据
            self.json1, self.json2 = self.separate_data(cleaned_dict_no_none)
            
            # 6. 准备模型汇总数据
            model_summary_data = self.prepare_for_model_summary(self.json2)
            
            return {
                'json1': self.json1,
                'json2': self.json2,
                'model_summary_data': model_summary_data
            }
        except Exception as e:
            raise Exception(f"数据处理失败: {str(e)}")