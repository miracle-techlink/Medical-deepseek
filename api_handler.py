import requests
import json
from typing import Callable, Optional
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from data_analyzer import DataAnalyzer  # 导入 DataAnalyzer

class APIHandler:
    @staticmethod
    def call_deepseek_api(prompt: str, stream_callback: Optional[Callable] = None) -> str:
        """调用DeepSeek API，支持流式输出"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        try:
            # 思维链分析
            analysis_prompt = APIHandler._generate_analysis_prompt(prompt)
            analysis_result = APIHandler._make_api_request(
                analysis_prompt, 
                headers, 
                stream_callback
            )
            
            # 生成诊断报告
            report_prompt = APIHandler._generate_report_prompt(analysis_result)
            report_result = APIHandler._make_api_request(
                report_prompt, 
                headers, 
                stream_callback
            )
            
            return report_result
            
        except Exception as e:
            if stream_callback:
                stream_callback(f"API调用错误: {str(e)}")
            return f"API调用错误: {str(e)}"

    @staticmethod
    def analyze_data(json1, json2) -> dict:
        """分析数据并返回结果"""
        try:
            analyzer = DataAnalyzer()  # 创建 DataAnalyzer 实例
            analysis_results = analyzer.analyze_data(json1, json2)  # 调用分析方法
            return analysis_results
        except Exception as e:
            return f"数据分析失败: {str(e)}"

    @staticmethod
    def analyze_data_question(question: str, data: dict) -> str:
        """分析数据相关问题"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        # 构建请求数据
        prompt = f"问题：{question}\n数据：{json.dumps(data, ensure_ascii=False)}\n请分析并回答："
        data_payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False  # 如果不需要流式输出
        }
        
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data_payload)
            response.raise_for_status()  # 检查请求是否成功
            
            result = response.json()
            # 确保解包的内容符合预期
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0]['message']['content']
                return answer
            else:
                raise ValueError("响应中没有可用的选择")
        except Exception as e:
            raise Exception(f"分析数据问题失败: {str(e)}")

    @staticmethod
    def _generate_analysis_prompt(prompt: str) -> str:
        """生成分析提示词"""
        return f"""请分析以下患者数据，生成一个详细的思维链分析：

1. **数据特点分析**：
   - 关键信息提取：请列出数据中的重要特征和指标。
   - 数据完整性评估：请评估数据的完整性和准确性。
   - 异常值识别：请识别数据中的异常值，并说明可能的原因。

2. **诊断思路**：
   - 主要问题识别：请指出患者的主要健康问题。
   - 相关因素分析：请分析可能影响患者健康的相关因素。
   - 诊断优先级排序：请根据分析结果对诊断进行优先级排序。

3. **治疗建议框架**：
   - 当前治疗方案评估：请评估现有治疗方案的有效性。
   - 潜在问题识别：请识别可能的潜在问题。
   - 建议方向确定：请提出进一步的治疗建议。

患者数据：
{prompt}"""

    @staticmethod
    def _generate_report_prompt(analysis_result: str) -> str:
        """生成报告提示词"""
        return f"""基于以下思维链分析，生成详细的诊断报告：

{analysis_result}

请按照以下结构组织报告：

1. **患者基本信息**：
   - 年龄、性别、基础疾病史
   - 主要症状和体征

2. **诊断分析**：
   - 主要诊断
   - 病理类型和分期
   - 转移情况
   - 合并症

3. **治疗历程**：
   - 手术情况
   - 化疗方案
   - 放疗/其他治疗
   - 治疗效果评估

4. **当前问题**：
   - 主要症状
   - 检查结果
   - 治疗反应
   - 当前问题

5. **下一步建议**：
   - 检查建议
   - 治疗建议
   - 随访计划

请使用清晰的标题层级和项目符号，确保报告结构清晰、内容完整。"""

    @staticmethod
    def _make_api_request(prompt: str, headers: dict, stream_callback: Optional[Callable] = None) -> str:
        """发送API请求"""
        data = {
            "model": "deepseek-chat",  # 确保使用正确的模型名称
            "messages": [{"role": "user", "content": prompt}],  # 确保消息格式正确
            "stream": True  # 如果支持流式输出
        }
        
        with requests.post(DEEPSEEK_API_URL, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # 检查请求是否成功
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line.decode('utf-8').replace('data: ', ''))
                        if 'choices' in json_response and len(json_response['choices']) > 0:
                            content = json_response['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                full_response += content
                                if stream_callback:
                                    stream_callback(content)
                    except json.JSONDecodeError:
                        continue
            
            return full_response