# 数据分析维度
# 针对数据进行分析，思考可以分析的角度

import asyncio
from typing import Dict, List

from app_agent.tools.filter_content import extract_array_data_from_text
from MetaGPT.metagpt.actions import Action
from MetaGPT.metagpt.actions.action_node import ActionNode
from MetaGPT.metagpt.utils.common import OutputParser


DataAnalysis_STRUCTION = """You are a senior data analysis expert with extensive experience in data 
analysis"""

# 实例化一个ActionNode，输入对应的参数
DATAANALYSIS = ActionNode(
    # ActionNode的名称
    key="DataAnalysisDimensions",
    # 期望输出的格式
    expected_type=str,
    # 命令文本
    instruction=DataAnalysis_STRUCTION,
    # 例子输入，在这里我们可以留空
    example="",
)


class WriteDataAnalysisDimensions(Action):
    language: str = "Chinese"

    def __init__(self, name: str = "", language: str = "Chinese", *args, **kwargs):
        super().__init__()
        self.language = language

    async def run(self, data: str, *args, **kwargs) -> List:
        PROMPT = """
            The data to be analyzed is as follows:
            {data}
            Please provide me with some perspectives and ideas for analyzing data, and follow the following requirements:
            1. The output must be strictly in the specified language, {language}
            2. Answer strictly in the array format like ["xxx","xxx",...],0-3,up to 3
            3. Please use the simplest words or short sentences to express your analytical perspective
            4. Do not have extra spaces or line breaks
            5. If there is no analyzable content in the above data, please reply with an empty array "[]"
            6. Only reply in array format, do not provide explanation.
            7. The analysis must be based on numerical data.
        """
        # 我们设置好prompt，作为ActionNode的输入
        prompt = PROMPT.format(data=data, language=self.language)
        # resp = await self._aask(prompt=prompt)
        # 直接调用ActionNode.fill方法，注意输入llm
        # 该方法会返回self，也就是一个ActionNode对象
        resp_node = await DATAANALYSIS.fill(context=prompt, llm=self.llm, schema='raw')
        # 选取ActionNode.content，获得我们期望的返回信息
        resp = resp_node.content
        resp = extract_array_data_from_text(resp)
        # print('resp:', resp)
        # print('type(resp):', type(resp))
        # return OutputParser.extract_struct(resp, list)
        return resp


async def main():
    data = '''customer_id	company_name	contact_person	position	contact_info	customer_level	customer_type	industry	source	is_business_opportunity	intended_payment_project	purchased_projects	project_budget	cooperation_stage	company_address	created_at	updated_at
2	腾讯科技	马华腾	产品经理	15111111234	重要客户	企业	游戏	线下	1	客户管理系统，设备互联	智慧园区	99999999	沟通中	深圳腾讯园区	16/5/2024 14:14:44	16/5/2024 14:14:49
5	阿里科技	李阿里	项目经理	15444441234	重要客户	企业	互联网	线下	1	智能客服系统	数据分析平台	700000	筹备中	杭州市西湖区	16/5/2024 14:14:47	16/5/2024 14:14:52
8	华为科技	陈华为	产品经理	15777771234	重要客户	企业	通信	线下	1	智能通信系统	5G技术平台	900000	筹备中	深圳市福田区	16/5/2024 14:14:50	16/5/2024 14:14:55
11	字节跳动	张字节	市场总监	15000001111	重要客户	企业	社交媒体	线上	1	智能推荐系统	内容分发平台	950000	筹备中	北京市海淀区	16/5/2024 14:14:53	16/5/2024 14:14:58
14	微博科技	张微博	运营总监	15033331111	重要客户	企业	社交媒体	线下	1	智能营销系统	广告投放平台	700000	洽谈中	北京市海淀区	16/5/2024 14:14:56	16/5/2024 14:14:11
17	滴滴科技	王滴滴	业务经理	15066661111	重要客户	企业	出行	线上	0	智能打车系统	共享出行平台	400000	规划中	北京市海淀区	16/5/2024 14:14:59	16/5/2024 14:14:14
20	搜狗科技	李搜狗	市场总监	15099991111	重要客户	企业	搜索引擎	线下	1	智能搜索系统	语音识别技术	500000	洽谈中	北京市海淀区	16/5/2024 14:14:12	16/5/2024 14:14:17
21	华南科技	张华为	市场总监	15100001111	重要客户	企业	通信	线上	1	智能通信系统	5G技术平台	900000	筹备中	深圳市南山区	16/5/2024 14:14:13	16/5/2024 14:14:18
24	字节不跳动	刘字节	产品经理	15133331111	重要客户	企业	社交媒体	线上	1	智能推荐系统	内容分发平台	950000	筹备中	北京市海淀区	16/5/2024 14:14:16	16/5/2024 14:14:21
27	大博科技	张微博	销售经理	15166661111	重要客户	企业	社交媒体	线下	1	智能营销系统	广告投放平台	700000	洽谈中	北京市海淀区	16/5/2024 14:14:19	16/5/2024 14:14:24
30	打滴科技	陈滴滴	产品经理	15199991111	重要客户	企业	出行	线上	0	智能打车系统	共享出行平台	400000	规划中	北京市海淀区	16/5/2024 14:14:22	16/5/2024 14:14:27
33	搜猫科技	周搜狗	市场经理	15222221111	重要客户	企业	搜索引擎	线下	1	智能搜索系统	语音识别技术	500000	洽谈中	北京市海淀区	16/5/2024 14:14:25	16/5/2024 14:14:30
39	腾Q科技	吴腾讯	产品经理	15288881111	重要客户	企业	游戏	线下	1	客户管理系统	设备互联	900000	沟通中	深圳腾讯园区	16/5/2024 14:14:31	16/5/2024 14:14:36
'''

    action = WriteDataAnalysisDimensions()
    result = await action.run(data)
    print('res:', result)


if __name__ == '__main__':
    asyncio.run(main())
