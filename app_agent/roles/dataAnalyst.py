import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from app_agent.actions.DataAnalysisDimensions import WriteDataAnalysisDimensions
from app_agent.actions.DataAnalysisInterpretation import WriteDataAnalysisInterpretation
from MetaGPT.metagpt.const import TUTORIAL_PATH

from MetaGPT.metagpt.logs import logger
from MetaGPT.metagpt.roles import Role
from MetaGPT.metagpt.schema import Message
from MetaGPT.metagpt.utils.file import File


# 数据分析助手
class DataAnalystAssistant(Role):
    data: str = ""
    language: str = "Chinese"
    resList: List = []

    def __init__(
            self,
            name: str = "hong",
            profile: str = "DataAnalyst Assistant",
            goal: str = "数据分析助手",
            data: str = "",
            # constraints则是我们期望对输出内容的约束
            language: str = "Chinese",
    ):
        super().__init__()
        self.set_actions([WriteDataAnalysisDimensions(language=language)])
        self.data = data
        self.language = language

    # 处理不同角度的数据分析
    async def _handle_dimensions(self, dimensions: List) -> Message:
        actions = list()
        for k in range(len(dimensions)):
            actions.append(WriteDataAnalysisInterpretation(
                data=self.data, dimension=dimensions[k], language=self.language))

        self.set_actions(actions)
        self.rc.todo = None
        return Message(content=str(dimensions))

    async def act(self) -> Message:
        """Perform an action as determined by the role.

        Returns:
            A message containing the result of the action.
        """
        todo = self.rc.todo

        #  分析维度
        if type(todo) is WriteDataAnalysisDimensions:
            msg = self.rc.memory.get(k=1)[0]
            self.data = msg.content
            resp = await todo.run(msg.content)
            # logger.info(resp)
            await self._handle_dimensions(resp)
            return Message(content='Done', role=self.profile)
        time.sleep(1)
        resp = await todo.run()
        # logger.info(resp)
        self.resList.append(resp)
        return Message(content=resp, role=self.profile)

    async def _think(self) -> None:
        """Determine the next action to be taken by the role."""
        # logger.info(self.rc.state)
        # logger.info(self, )
        if self.rc.todo is None:
            self._set_state(0)
            return

        if self.rc.state + 1 < len(self.states):
            self._set_state(self.rc.state + 1)
        else:
            self.rc.todo = None

    async def _react(self) -> Message:
        """Execute the assistant's think and actions.

        Returns:
            A message containing the final result of the assistant's actions.
        """
        msg = None
        while True:
            await self._think()
            if self.rc.todo is None:
                break
            msg = await self.act()

        # for res in self.resList:
        #     print('res:', res)

        res_list_text = json.dumps(self.resList)
        # print('res_list_text:')
        # print(res_list_text)

        root_path = Path("workspace") / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        await File.write(root_path, "data.md", res_list_text.encode("utf-8"))
        return msg


async def main():
    data = '''
    customer_id	company_name	contact_person	position	contact_info	customer_level	customer_type	industry	source	is_business_opportunity	intended_payment_project	purchased_projects	project_budget	cooperation_stage	company_address	created_at	updated_at
    2	腾讯科技	马华腾	产品经理	15111111234	重要客户	企业	游戏	线下	1	客户管理系统，设备互联	智慧园区	900000	沟通中	深圳腾讯园区	16/5/2024 14:14:44	16/5/2024 14:14:49
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

    role = DataAnalystAssistant()
    logger.info(data)
    result = await role.run(data)
    logger.info(result)


if __name__ == '__main__':
    asyncio.run(main())


async def start_data_analyst(data: str = ''):
    print('start data_analyst:', data)
    role = DataAnalystAssistant()
    logger.info(data)
    result = await role.run(data)
    logger.info(result)
