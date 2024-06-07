# 数据分析解读
# 针对数据进行分析，对特定的分析角度完成数据分析

import asyncio

from app_agent.actions.DataAnalysisDimensions import DataAnalysis_STRUCTION
from app_agent.tools.filter_content import extract_json_from_text
from MetaGPT.metagpt.actions import Action
from MetaGPT.metagpt.actions.action_node import ActionNode

# 实例化一个ActionNode，输入对应的参数
DATAANALYSIS = ActionNode(
    # ActionNode的名称
    key="DataAnalysisInterpretation",
    # 期望输出的格式
    expected_type=str,
    # 命令文本
    instruction=DataAnalysis_STRUCTION,
    # 例子输入，在这里我们可以留空
    example="",
)


class WriteDataAnalysisInterpretation(Action):
    data: str = ''
    dimension: str = ''
    language: str = "Chinese"

    def __init__(self, name: str = "", data: str = "", dimension: str = "", language: str = "Chinese", *args, **kwargs):
        super().__init__()
        self.data = data
        self.dimension = dimension
        self.language = language

    async def run(self, *args, **kwargs) -> dict:
        PROMPT = """
            The data to be analyzed is as follows:
            {data}
            Please analyze the above data according to the {dimension} dimension for me and follow the following requirements:
            1. The output must strictly use the specified language,{language}
            2. Do not have extra spaces or line breaks
            3. Answer strictly in the following Json format
            {{
                "dimension": "{dimension}",
                "analysis_conclusion": "Write the conclusion and analysis process here",
                "type": "Choose a suitable representation from 'line pie or bar', only one can be selected",
                # Pie:Suitable for displaying the proportion of different parts that make up the whole
                # Line:Suitable for displaying the trend of continuous data changing with another variable (such as time).Especially suitable for depicting the changes of time series data over time
                # Bar:Suitable for comparing numerical data from different categories/groups.

                "xAxis": "[
                    {{
                        "name":"",
                         "data":"[value1, value2,...]"
                    }}
                    # only one
                ]" ,
                "yAxis": "[
                    {{
                        "name":"",
                         "data":"[value1, value2,...]"
                    }}
                    
                ]"                 
                # xAxis or yAxis is a json list 
                # xAxis can only have one set of data as the horizontal axis
                # yAxis can have one or two sets of data as vertical coordinates
                # The value of the yAxis must be  integers or  floating-point numbers
                # the number of elements in xAxis and yAxis must be the same
                # xAxis and yAxis must be data that has been analyzed and statistically analyzed by you, rather than raw data
                # xAxis and yAxis can be used for displaying data charts 
                }}
                4. Only reply in Json format, do not provide explanation
                """
        # 我们设置好prompt，作为ActionNode的输入
        prompt = PROMPT.format(data=self.data, dimension=self.dimension, language=self.language)
        # resp = await self._aask(prompt=prompt)
        # 直接调用ActionNode.fill方法，注意输入llm
        # 该方法会返回self，也就是一个ActionNode对象
        resp_node = await DATAANALYSIS.fill(context=prompt, llm=self.llm, schema='raw')
        # 选取ActionNode.content，获得我们期望的返回信息
        resp = resp_node.content
        resp = extract_json_from_text(resp)
        # print('resp:', resp)
        return resp


async def main():
    data = '''
    customer_id	company_name	contact_person	position	contact_info	customer_level	customer_type	industry	source	is_business_opportunity	intended_payment_project	purchased_projects	project_budget	cooperation_stage	company_address	created_at	updated_at
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
    dimension = '评估线上与线下来源的商机转化率'
    action = WriteDataAnalysisInterpretation(data=data, dimension=dimension)

    result = await action.run()
    print('res:', result)


if __name__ == '__main__':
    asyncio.run(main())
