import json

INPUT = "{\"code\":200,\"msg\":\"success\",\"result\":{\"curpage\":1,\"allnum\":10,\"newslist\":[{\"id\":\"a45c630578ac6e1855b4d0756fc69033\",\"ctime\":\"2024-06-13 10:40\",\"title\":\"美联储维持利率不变 预计年内最多降息一次\",\"description\":\"这是美联储自去年9月以来连续第七次会议维持利率不变。2024-06-1310:40\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a5c75a3109f7844fef6df.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a5c75a3109f7860de1a76.html\"},{\"id\":\"778b3939b067a4e95ef21104e490d444\",\"ctime\":\"2024-06-13 10:38\",\"title\":\"保障性住房再贷款落地进程加快\",\"description\":\"2024-06-1310:38\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a5ce8a3109f7844fef71b.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a5c8ca3109f7860de1a7a.html\"},{\"id\":\"41555a48592e530645b0fd58f0aad101\",\"ctime\":\"2024-06-13 10:39\",\"title\":\"促投资稳增长 超长期特别国债有序发行\",\"description\":\"2024-06-1310:39\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a5c8da3109f7844fef6f1.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a5c8da3109f7860de1a7b.html\"},{\"id\":\"ca10e3775a495fc92e130b1fc839b4c0\",\"ctime\":\"2024-06-13 10:40\",\"title\":\"如何享受减半征收“六税两费”政策？收好这张图\",\"description\":\"2024-06-1310:40\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a5c92a3109f7844fef6f4.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a5c92a3109f7860de1a7c.html\"},{\"id\":\"ea5da9879b02661c23e61a3b5a726f5e\",\"ctime\":\"2024-06-13 10:41\",\"title\":\"不顾多方反对 欧盟拟对中国电动汽车征收临时反补贴税\",\"description\":\"2024-06-1310:41\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a5c92a3109f7844fef6f7.png\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a5c92a3109f7860de1a7d.html\"},{\"id\":\"1320a66ed1130a4e5b0d6d29d0d08470\",\"ctime\":\"2024-06-13 10:41\",\"title\":\"种粮有了“双保险”，农民如何“旱涝保收”？\",\"description\":\"2024-06-1310:41\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a5c99a3109f7844fef6fa.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a5c99a3109f7860de1a7e.html\"},{\"id\":\"5538c3e1f74f519f8ed49827bc628739\",\"ctime\":\"2024-06-13 11:10\",\"title\":\"【全球市场早报】6月13日\",\"description\":\"2024-06-1311:10\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/13\\/666a6314a3109f7844fef728.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/13\\/WS666a6314a3109f7860de1a8e.html\"},{\"id\":\"6ccec8811908f92d84452595e516fed4\",\"ctime\":\"2024-06-12 18:40\",\"title\":\"【全球市场晚报】6月12日\",\"description\":\"2024-06-1218:40\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/12\\/66697b22a3109f7844fef48d.jpeg\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/12\\/WS66697b22a3109f7860de19ed.html\"},{\"id\":\"a06228c9da5f4a82b29d1813d5aea439\",\"ctime\":\"2024-06-07 15:47\",\"title\":\"【推动高质量发展】内蒙古发展跑出加速度 经济增速连续两年进入全国第一方阵\",\"description\":\"去年，内蒙古地方生产总值、固定资产投资和进出口总额这三个指标的增速都居全国前三，规模以上工业增加值的增速也排在全国第7，一批惠及长远的一些大项目、好项目纷纷落地。2024-06-0715:47\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/07\\/6662bb4ba3109f7844feceb6.png\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/07\\/WS6662baf5a3109f7860de100b.html\"},{\"id\":\"d0cccfb82ed7bdd0e7ea5f106a96a47c\",\"ctime\":\"2024-06-07 15:47\",\"title\":\"【推动高质量发展】内蒙古：打好“三北”工程攻坚战 实现生态、生产、生活“三赢”\",\"description\":\"内蒙古是我国治理荒漠化的主战场，也是“三北”防护林体系工程建设的重要地区。记者今日从国新办举行的“推动高质量发展”系列主题新闻发布会上了解到，国家“三北”工程沙化土地治理最大的任务量在内蒙古。2024-06-0715:47\",\"source\":\"中国日报财经\",\"picUrl\":\"\\/\\/img3.chinadaily.com.cn\\/images\\/202406\\/07\\/6662baf7a3109f7844feceae.png\",\"url\":\"\\/\\/caijing.chinadaily.com.cn\\/a\\/202406\\/07\\/WS6662baf7a3109f7860de100e.html\"}]}}"


def main(data: str) -> dict:
    data = json.loads(data)
    news_list = data["result"]["newslist"]
    markdown_links = []
    for news in news_list:
        title = news["title"]
        url = news["url"]
        markdown_link = f"[{title}]({url})"
        markdown_links.append(markdown_link)

    return {
        "result": "\n".join(markdown_links),
    }


if __name__ == '__main__':
    json_str = INPUT
    result = main(json_str)
    print(result)
