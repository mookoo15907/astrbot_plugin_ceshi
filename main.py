from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import random
import json
from pathlib import Path
from datetime import datetime

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 数据持久化文件：插件同目录 data/xiaosui_state.json
        self._data_dir = Path(__file__).parent / "data"
        self._data_path = self._data_dir / "xiaosui_state.json"
        self._state = {"users": {, "sign_counts": {}}  # { user_id: {"favor": int, "marbles": int, "last_sign": "YYYY-MM-DD"} }

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        try:
            self._data_dir.mkdir(parents=True, exist_ok=True)
            if self._data_path.exists():
                self._state = json.loads(self._data_path.read_text(encoding="utf-8"))
                if "users" not in self._state:
                    self._state["users"] = {}
        if "sign_counts" not in self._state:
            self._state["sign_counts"] = {}
            logger.info("小碎数据已加载")
        except Exception as e:
            logger.error(f"加载数据失败：{e}")

    def _save_state(self):
        try:
            self._data_path.write_text(json.dumps(self._state, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"保存数据失败：{e}")

    def _get_user_id(self, event: AstrMessageEvent) -> str:
        """尽量稳妥地拿一个用户唯一标识"""
        for getter in ("get_sender_id", "get_user_id", "get_sender_qq"):
            fn = getattr(event, getter, None)
            if callable(fn):
                try:
                    uid = fn()
                    if uid:
                        return str(uid)
                except Exception:
                    pass
        try:
            sender = getattr(event, "sender", None)
            if sender and hasattr(sender, "id"):
                return str(sender.id)
            if sender and hasattr(sender, "user_id"):
                return str(sender.user_id)
        except Exception:
            pass
        return f"name::{event.get_sender_name()}"



    @filter.command("查询甜樱桃巧克力碎布朗尼")
    async def reply_查询甜樱桃巧克力碎布朗尼(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 五任")

    @filter.command("查询自给自足微波炉")
    async def reply_查询自给自足微波炉(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断")

    @filter.command("查询永远抽不到大奖的摇号机")
    async def reply_查询永远抽不到大奖的摇号机(self, event: AstrMessageEvent):
        yield event.plain_result("53 已买断")

    @filter.command("查询偷chi芒果蛋糕的女仆")
    async def reply_查询偷chi芒果蛋糕的女仆(self, event: AstrMessageEvent):
        yield event.plain_result("50 未买断")

    @filter.command("查询幸运值满格的书呆子")
    async def reply_查询幸运值满格的书呆子(self, event: AstrMessageEvent):
        yield event.plain_result("35 未买断")

    @filter.command("查询编织人类情感的缝纫师")
    async def reply_查询编织人类情感的缝纫师(self, event: AstrMessageEvent):
        yield event.plain_result("50 未买断")

    @filter.command("查询送信的云中信使")
    async def reply_查询送信的云中信使(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断")

    @filter.command("查询喜欢狗尾巴草的三花猫")
    async def reply_查询喜欢狗尾巴草的三花猫(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断 三任")

    @filter.command("查询被欺负的小孩子")
    async def reply_查询被欺负的小孩子(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断")

    @filter.command("查询童年的糖纸小狗")
    async def reply_查询童年的糖纸小狗(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断")

    @filter.command("查询初春时节的青团")
    async def reply_查询初春时节的青团(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询焦糖小熊饼干天使")
    async def reply_查询焦糖小熊饼干天使(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断 五任")

    @filter.command("查询晨露味道的花茶")
    async def reply_查询晨露味道的花茶(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断 二任")

    @filter.command("查询幽灵男孩和他的幽灵小狗")
    async def reply_查询幽灵男孩和他的幽灵小狗(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询海浪纹和鲤鱼旗")
    async def reply_查询海浪纹和鲤鱼旗(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 五任")

    @filter.command("查询薰衣草味威化饼干")
    async def reply_查询薰衣草味威化饼干(self, event: AstrMessageEvent):
        yield event.plain_result("97.5 已买断")

    @filter.command("查询阳光海盐柠檬汽水")
    async def reply_查询阳光海盐柠檬汽水(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 三任")

    @filter.command("查询桃子气泡酒")
    async def reply_查询桃子气泡酒(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询偷跑出来的熊猫")
    async def reply_查询偷跑出来的熊猫(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询破晓时分的城市天际线")
    async def reply_查询破晓时分的城市天际线(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 四任")

    @filter.command("查询奶油布丁和木勺子")
    async def reply_查询奶油布丁和木勺子(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 三任")

    @filter.command("查询甜滋滋的满杯桑椹")
    async def reply_查询甜滋滋的满杯桑椹(self, event: AstrMessageEvent):
        yield event.plain_result("38 未买断")

    @filter.command("查询灯会中的狐狸面具")
    async def reply_查询灯会中的狐狸面具(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询节日专供红豆汤圆")
    async def reply_查询节日专供红豆汤圆(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询松露巧克力侦探")
    async def reply_查询松露巧克力侦探(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 五任")

    @filter.command("查询味觉失衡的美食鉴赏家")
    async def reply_查询味觉失衡的美食鉴赏家(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询蓝莓果酱流心蛋挞")
    async def reply_查询蓝莓果酱流心蛋挞(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 三任")

    @filter.command("查询云端的摩天轮")
    async def reply_查询云端的摩天轮(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询牛油果纪律委员")
    async def reply_查询牛油果纪律委员(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询米饭爱好者")
    async def reply_查询米饭爱好者(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断 五任")

    @filter.command("查询苹果小画家")
    async def reply_查询苹果小画家(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询午餐肉三明治")
    async def reply_查询午餐肉三明治(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询蜜罐松饼小熊")
    async def reply_查询蜜罐松饼小熊(self, event: AstrMessageEvent):
        yield event.plain_result("67.5 已买断 三任")

    @filter.command("查询带有薄荷香气的马卡龙")
    async def reply_查询带有薄荷香气的马卡龙(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询永远找不齐拼图碎块的少女")
    async def reply_查询永远找不齐拼图碎块的少女(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断")

    @filter.command("查询只会做奥利奥大福的甜品社社长")
    async def reply_查询只会做奥利奥大福的甜品社社长(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询草莓冰沙小公主")
    async def reply_查询草莓冰沙小公主(self, event: AstrMessageEvent):
        yield event.plain_result("105 已买断")

    @filter.command("查询天然呆羊角恶魔")
    async def reply_查询天然呆羊角恶魔(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询海底鲸鱼和小气泡")
    async def reply_查询海底鲸鱼和小气泡(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 四任")

    @filter.command("查询夜间偷吃的小鼠")
    async def reply_查询夜间偷吃的小鼠(self, event: AstrMessageEvent):
        yield event.plain_result("67.5 已买断")

    @filter.command("查询玩滑板的黑猫")
    async def reply_查询玩滑板的黑猫(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询三色睡衣小兔")
    async def reply_查询三色睡衣小兔(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 四任")

    @filter.command("查询熊熊高中生")
    async def reply_查询熊熊高中生(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询小笼包中国娘")
    async def reply_查询小笼包中国娘(self, event: AstrMessageEvent):
        yield event.plain_result("63 已买断 三任")

    @filter.command("查询软面包女仆")
    async def reply_查询软面包女仆(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询浅蓝天使小兔")
    async def reply_查询浅蓝天使小兔(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询圣诞姜饼人小鹿")
    async def reply_查询圣诞姜饼人小鹿(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询糖果甜点烘焙师")
    async def reply_查询糖果甜点烘焙师(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询爱心章鱼烧")
    async def reply_查询爱心章鱼烧(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 三任")

    @filter.command("查询唱片面包熊熊")
    async def reply_查询唱片面包熊熊(self, event: AstrMessageEvent):
        yield event.plain_result("送设 二人共养中")

    @filter.command("查询珍珠椰果醇香奶茶")
    async def reply_查询珍珠椰果醇香奶茶(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 五任")

    @filter.command("查询夏日的三球冰淇淋")
    async def reply_查询夏日的三球冰淇淋(self, event: AstrMessageEvent):
        yield event.plain_result("55 未买断")

    @filter.command("查询元气莓果慕斯蛋糕")
    async def reply_查询元气莓果慕斯蛋糕(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询人缘很好的蛀牙小美女")
    async def reply_查询人缘很好的蛀牙小美女(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询菠萝圈和菠萝啤")
    async def reply_查询菠萝圈和菠萝啤(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断")

    @filter.command("查询命运蘑菇骰子")
    async def reply_查询命运蘑菇骰子(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断")

    @filter.command("查询企鹅棒冰")
    async def reply_查询企鹅棒冰(self, event: AstrMessageEvent):
        yield event.plain_result("67.5 已买断 二任")

    @filter.command("查询抹茶杏仁豆腐")
    async def reply_查询抹茶杏仁豆腐(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询热腾腾的炸虾天妇罗")
    async def reply_查询热腾腾的炸虾天妇罗(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询小行星与宇航员")
    async def reply_查询小行星与宇航员(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询24小时自动贩售机猫猫")
    async def reply_查询24小时自动贩售机猫猫(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询白色花束和旧邮差")
    async def reply_查询白色花束和旧邮差(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询电视机斑点小狗")
    async def reply_查询电视机斑点小狗(self, event: AstrMessageEvent):
        yield event.plain_result("55 未买断")

    @filter.command("查询变态痴汉少女")
    async def reply_查询变态痴汉少女(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询桃子口香糖粘液")
    async def reply_查询桃子口香糖粘液(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断 四任")

    @filter.command("查询绝对优等生")
    async def reply_查询绝对优等生(self, event: AstrMessageEvent):
        yield event.plain_result("55 未买断")

    @filter.command("查询美少女格斗家")
    async def reply_查询美少女格斗家(self, event: AstrMessageEvent):
        yield event.plain_result("35 未买断")

    @filter.command("查询冬日小松鼠")
    async def reply_查询冬日小松鼠(self, event: AstrMessageEvent):
        yield event.plain_result("52.5 已买断 四任")

    @filter.command("查询素食主义关东煮")
    async def reply_查询素食主义关东煮(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 三任")

    @filter.command("查询易碎玻璃杯/崩塌的情绪")
    async def reply_查询易碎玻璃杯_崩塌的情绪(self, event: AstrMessageEvent):
        yield event.plain_result("97.5 已买断 五任")

    @filter.command("查询日系阴郁系少女")
    async def reply_查询日系阴郁系少女(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 三任")

    @filter.command("查询恶龙公主")
    async def reply_查询恶龙公主(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询仙人球堕天使")
    async def reply_查询仙人球堕天使(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断 五任")

    @filter.command("查询寒冷地带的羊驼")
    async def reply_查询寒冷地带的羊驼(self, event: AstrMessageEvent):
        yield event.plain_result("135 已买断 三任 二人共养中")

    @filter.command("查询审美奇异的废宅少女")
    async def reply_查询审美奇异的废宅少女(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询永不停止的晚间噪音")
    async def reply_查询永不停止的晚间噪音(self, event: AstrMessageEvent):
        yield event.plain_result("50 已买断 五任")

    @filter.command("查询满腹心机的学生会会长")
    async def reply_查询满腹心机的学生会会长(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询存在于虚实之间的幽灵体")
    async def reply_查询存在于虚实之间的幽灵体(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询软软小仓鼠")
    async def reply_查询软软小仓鼠(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断")

    @filter.command("查询无处堆放的城市垃圾")
    async def reply_查询无处堆放的城市垃圾(self, event: AstrMessageEvent):
        yield event.plain_result("30 未买断")

    @filter.command("查询黑箱天使")
    async def reply_查询黑箱天使(self, event: AstrMessageEvent):
        yield event.plain_result("105 已买断 五任")

    @filter.command("查询新式洋馆鬼屋")
    async def reply_查询新式洋馆鬼屋(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询视线集中恶魔小姐")
    async def reply_查询视线集中恶魔小姐(self, event: AstrMessageEvent):
        yield event.plain_result("112.5 已买断")

    @filter.command("查询知书达礼外交官")
    async def reply_查询知书达礼外交官(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断")

    @filter.command("查询蔷薇花嫁1")
    async def reply_查询蔷薇花嫁1(self, event: AstrMessageEvent):
        yield event.plain_result("112.5 已买断 五任")

    @filter.command("查询百合花精灵")
    async def reply_查询百合花精灵(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 四任")

    @filter.command("查询薄荷馅冰皮月饼")
    async def reply_查询薄荷馅冰皮月饼(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询春季旅行者")
    async def reply_查询春季旅行者(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询小醒")
    async def reply_查询小醒(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 四任")

    @filter.command("查询悠长假日")
    async def reply_查询悠长假日(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 二任")

    @filter.command("查询蓝玫瑰小王子")
    async def reply_查询蓝玫瑰小王子(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询毛绒小熊学生妹")
    async def reply_查询毛绒小熊学生妹(self, event: AstrMessageEvent):
        yield event.plain_result("55 未买断 二任")

    @filter.command("查询面包店店员勤恳工作中")
    async def reply_查询面包店店员勤恳工作中(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 五任")

    @filter.command("查询小怕")
    async def reply_查询小怕(self, event: AstrMessageEvent):
        yield event.plain_result("125 未买断")

    @filter.command("查询春日的绿樱桃")
    async def reply_查询春日的绿樱桃(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断")

    @filter.command("查询美术生与三原色")
    async def reply_查询美术生与三原色(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询南瓜瑞士卷")
    async def reply_查询南瓜瑞士卷(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断")

    @filter.command("查询万福招财猫")
    async def reply_查询万福招财猫(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 三任")

    @filter.command("查询羊羊天使")
    async def reply_查询羊羊天使(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 五任")

    @filter.command("查询杀人兔")
    async def reply_查询杀人兔(self, event: AstrMessageEvent):
        yield event.plain_result("30 已买断")

    @filter.command("查询通灵少女")
    async def reply_查询通灵少女(self, event: AstrMessageEvent):
        yield event.plain_result("30 已买断")

    @filter.command("查询音乐极端分子")
    async def reply_查询音乐极端分子(self, event: AstrMessageEvent):
        yield event.plain_result("30 已买断 二任")

    @filter.command("查询三只眼恶魔")
    async def reply_查询三只眼恶魔(self, event: AstrMessageEvent):
        yield event.plain_result("20 未买断")

    @filter.command("查询小厨娘天使")
    async def reply_查询小厨娘天使(self, event: AstrMessageEvent):
        yield event.plain_result("20 未买断")

    @filter.command("查询心情外显")
    async def reply_查询心情外显(self, event: AstrMessageEvent):
        yield event.plain_result("20 未买断")

    @filter.command("查询流浪小狗")
    async def reply_查询流浪小狗(self, event: AstrMessageEvent):
        yield event.plain_result("20 未买断")

    @filter.command("查询新型AI机械姬")
    async def reply_查询新型AI机械姬(self, event: AstrMessageEvent):
        yield event.plain_result("30 已买断 二任")

    @filter.command("查询黑猫猫店长")
    async def reply_查询黑猫猫店长(self, event: AstrMessageEvent):
        yield event.plain_result("20 未买断")

    @filter.command("查询秋日落叶")
    async def reply_查询秋日落叶(self, event: AstrMessageEvent):
        yield event.plain_result("20 未买断")

    @filter.command("查询春日游园")
    async def reply_查询春日游园(self, event: AstrMessageEvent):
        yield event.plain_result("25 未买断")

    @filter.command("查询冰雪兔")
    async def reply_查询冰雪兔(self, event: AstrMessageEvent):
        yield event.plain_result("25 未买断")

    @filter.command("查询绿林精灵")
    async def reply_查询绿林精灵(self, event: AstrMessageEvent):
        yield event.plain_result("25 未买断")

    @filter.command("查询蛋黄猫猫")
    async def reply_查询蛋黄猫猫(self, event: AstrMessageEvent):
        yield event.plain_result("25 无psd 已买断 三任")

    @filter.command("查询巧克力甜甜圈")
    async def reply_查询巧克力甜甜圈(self, event: AstrMessageEvent):
        yield event.plain_result("37.5 已买断 三任")

    @filter.command("查询牧场花花")
    async def reply_查询牧场花花(self, event: AstrMessageEvent):
        yield event.plain_result("25 未买断")

    @filter.command("查询青苹果")
    async def reply_查询青苹果(self, event: AstrMessageEvent):
        yield event.plain_result("60 未买断")

    @filter.command("查询小老虎")
    async def reply_查询小老虎(self, event: AstrMessageEvent):
        yield event.plain_result("45 已买断")

    @filter.command("查询兔子玩偶祭品")
    async def reply_查询兔子玩偶祭品(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 四任")

    @filter.command("查询黄草莓酱烤猫咪")
    async def reply_查询黄草莓酱烤猫咪(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询天国花束")
    async def reply_查询天国花束(self, event: AstrMessageEvent):
        yield event.plain_result("130 未买断")

    @filter.command("查询日式酱油丸子")
    async def reply_查询日式酱油丸子(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询巫女纸人")
    async def reply_查询巫女纸人(self, event: AstrMessageEvent):
        yield event.plain_result("90 已买断 五任")

    @filter.command("查询柠檬片小鼠")
    async def reply_查询柠檬片小鼠(self, event: AstrMessageEvent):
        yield event.plain_result("45 已买断 二任")

    @filter.command("查询油菜花小羊")
    async def reply_查询油菜花小羊(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断")

    @filter.command("查询鲜奶华夫")
    async def reply_查询鲜奶华夫(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断")

    @filter.command("查询小狸猫")
    async def reply_查询小狸猫(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断 五任")

    @filter.command("查询田园少女和蛋黄小鸡")
    async def reply_查询田园少女和蛋黄小鸡(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询影楼模特")
    async def reply_查询影楼模特(self, event: AstrMessageEvent):
        yield event.plain_result("30 未买断")

    @filter.command("查询雪花雪花")
    async def reply_查询雪花雪花(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断")

    @filter.command("查询棕色小狗天使")
    async def reply_查询棕色小狗天使(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询猫猫酷妹")
    async def reply_查询猫猫酷妹(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断")

    @filter.command("查询酒心巧克力")
    async def reply_查询酒心巧克力(self, event: AstrMessageEvent):
        yield event.plain_result("70 未买断")

    @filter.command("查询雨衣小猫")
    async def reply_查询雨衣小猫(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断")

    @filter.command("查询音符鸟")
    async def reply_查询音符鸟(self, event: AstrMessageEvent):
        yield event.plain_result("40 未买断")

    @filter.command("查询鸭鸭")
    async def reply_查询鸭鸭(self, event: AstrMessageEvent):
        yield event.plain_result("40 未买断")

    @filter.command("查询体感缺失街头少女")
    async def reply_查询体感缺失街头少女(self, event: AstrMessageEvent):
        yield event.plain_result("97.5 已买断 三任")

    @filter.command("查询香蕉小猴炸弹")
    async def reply_查询香蕉小猴炸弹(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断 四任")

    @filter.command("查询薄荷漏斗巧克力")
    async def reply_查询薄荷漏斗巧克力(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询梦境寄信")
    async def reply_查询梦境寄信(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 四任")

    @filter.command("查询棉花娃娃")
    async def reply_查询棉花娃娃(self, event: AstrMessageEvent):
        yield event.plain_result("40 未买断")

    @filter.command("查询少女的布偶屋")
    async def reply_查询少女的布偶屋(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 三任")

    @filter.command("查询毛绒兔")
    async def reply_查询毛绒兔(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询致幻毒蘑菇")
    async def reply_查询致幻毒蘑菇(self, event: AstrMessageEvent):
        yield event.plain_result("40 未买断")

    @filter.command("查询炼乳草莓")
    async def reply_查询炼乳草莓(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询芝士猫薄荷")
    async def reply_查询芝士猫薄荷(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询拇指多肉")
    async def reply_查询拇指多肉(self, event: AstrMessageEvent):
        yield event.plain_result("40 未买断")

    @filter.command("查询日式清汤杯面")
    async def reply_查询日式清汤杯面(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询红苹果熊熊果冻")
    async def reply_查询红苹果熊熊果冻(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询小奶牛")
    async def reply_查询小奶牛(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 四任")

    @filter.command("查询骷髅小恶魔")
    async def reply_查询骷髅小恶魔(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询熊熊导游")
    async def reply_查询熊熊导游(self, event: AstrMessageEvent):
        yield event.plain_result("67.5 已买断 四任")

    @filter.command("查询海鲜寿司")
    async def reply_查询海鲜寿司(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询定制祈")
    async def reply_查询定制祈(self, event: AstrMessageEvent):
        yield event.plain_result("原设无身价 身价即稿价喔 二任")

    @filter.command("查询春天的和果子")
    async def reply_查询春天的和果子(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 三任")

    @filter.command("查询烤面包机")
    async def reply_查询烤面包机(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断 三任")

    @filter.command("查询独角兽小马")
    async def reply_查询独角兽小马(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询冰蓝小兔")
    async def reply_查询冰蓝小兔(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询学园荔枝")
    async def reply_查询学园荔枝(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 一任 共养中")

    @filter.command("查询婚礼与钻石")
    async def reply_查询婚礼与钻石(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询电子机械娘")
    async def reply_查询电子机械娘(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 四任")

    @filter.command("查询陶瓷猫")
    async def reply_查询陶瓷猫(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断")

    @filter.command("查询染血熊")
    async def reply_查询染血熊(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断 二任")

    @filter.command("查询茶道")
    async def reply_查询茶道(self, event: AstrMessageEvent):
        yield event.plain_result("60 已买断")

    @filter.command("查询魔法小兔")
    async def reply_查询魔法小兔(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 三任")

    @filter.command("查询荧光水母")
    async def reply_查询荧光水母(self, event: AstrMessageEvent):
        yield event.plain_result("67.5 已买断 三任")

    @filter.command("查询纯情魅魔")
    async def reply_查询纯情魅魔(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询家居狐狸")
    async def reply_查询家居狐狸(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询铃铛斑点鹿")
    async def reply_查询铃铛斑点鹿(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询章鱼寄生")
    async def reply_查询章鱼寄生(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询樱桃布丁小兔")
    async def reply_查询樱桃布丁小兔(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询新生代小偶像")
    async def reply_查询新生代小偶像(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询奶酪松鼠")
    async def reply_查询奶酪松鼠(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询蓝玫瑰庭园")
    async def reply_查询蓝玫瑰庭园(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询新手巫女")
    async def reply_查询新手巫女(self, event: AstrMessageEvent):
        yield event.plain_result("62.5 已买断 五任")

    @filter.command("查询蓝莓国的神")
    async def reply_查询蓝莓国的神(self, event: AstrMessageEvent):
        yield event.plain_result("67.5 已买断 二任")

    @filter.command("查询谋杀金鱼")
    async def reply_查询谋杀金鱼(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询猫咪甜心")
    async def reply_查询猫咪甜心(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询缝补小兔")
    async def reply_查询缝补小兔(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询非常像学生的掌管人间爱意的神")
    async def reply_查询非常像学生的掌管人间爱意的神(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询金钱豹辣妹")
    async def reply_查询金钱豹辣妹(self, event: AstrMessageEvent):
        yield event.plain_result("100 未买断")

    @filter.command("查询蓝色史莱姆果冻")
    async def reply_查询蓝色史莱姆果冻(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询蔷薇花嫁2")
    async def reply_查询蔷薇花嫁2(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询口蘑小花")
    async def reply_查询口蘑小花(self, event: AstrMessageEvent):
        yield event.plain_result("150 已买断 二任")

    @filter.command("查询水饺厨娘")
    async def reply_查询水饺厨娘(self, event: AstrMessageEvent):
        yield event.plain_result("45 未买断")

    @filter.command("查询潜在性死亡少女")
    async def reply_查询潜在性死亡少女(self, event: AstrMessageEvent):
        yield event.plain_result("62.5 已买断 三任")

    @filter.command("查询扑克垂耳兔")
    async def reply_查询扑克垂耳兔(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 三任")

    @filter.command("查询薄荷柠檬奶油兔")
    async def reply_查询薄荷柠檬奶油兔(self, event: AstrMessageEvent):
        yield event.plain_result("75 已买断 三任")

    @filter.command("查询星星猫头鹰")
    async def reply_查询星星猫头鹰(self, event: AstrMessageEvent):
        yield event.plain_result("200 未买断")

    @filter.command("查询曲奇小饼干")
    async def reply_查询曲奇小饼干(self, event: AstrMessageEvent):
        yield event.plain_result("210 已买断 共养中")

    @filter.command("查询波点宅宅猫")
    async def reply_查询波点宅宅猫(self, event: AstrMessageEvent):
        yield event.plain_result("375 已买断 二任")

    @filter.command("查询樱花白狐")
    async def reply_查询樱花白狐(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 五任")

    @filter.command("查询透明雨衣")
    async def reply_查询透明雨衣(self, event: AstrMessageEvent):
        yield event.plain_result("280 未买断")

    @filter.command("查询白蜡烛")
    async def reply_查询白蜡烛(self, event: AstrMessageEvent):
        yield event.plain_result("350 已买断 二任")

    @filter.command("查询红眼黑蛛")
    async def reply_查询红眼黑蛛(self, event: AstrMessageEvent):
        yield event.plain_result("100 未买断")

    @filter.command("查询闪闪蜻蜓")
    async def reply_查询闪闪蜻蜓(self, event: AstrMessageEvent):
        yield event.plain_result("187.5 已买断")

    @filter.command("查询小黄鸭")
    async def reply_查询小黄鸭(self, event: AstrMessageEvent):
        yield event.plain_result("150 已买断 三任")

    @filter.command("查询隐藏面布偶熊")
    async def reply_查询隐藏面布偶熊(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二任")

    @filter.command("查询定制护士小兔")
    async def reply_查询定制护士小兔(self, event: AstrMessageEvent):
        yield event.plain_result("230 不用买断")

    @filter.command("查询定制古风少年")
    async def reply_查询定制古风少年(self, event: AstrMessageEvent):
        yield event.plain_result("是送设哦＞＜")

    @filter.command("查询另类恶魔")
    async def reply_查询另类恶魔(self, event: AstrMessageEvent):
        yield event.plain_result("200 已买断 四任")

    @filter.command("查询幼稚园斑点狗")
    async def reply_查询幼稚园斑点狗(self, event: AstrMessageEvent):
        yield event.plain_result("240 已买断")

    @filter.command("查询糖果世界")
    async def reply_查询糖果世界(self, event: AstrMessageEvent):
        yield event.plain_result("67 未买断")

    @filter.command("查询无限生命药瓶")
    async def reply_查询无限生命药瓶(self, event: AstrMessageEvent):
        yield event.plain_result("220 已买断 四任")

    @filter.command("查询小女仆黑猫")
    async def reply_查询小女仆黑猫(self, event: AstrMessageEvent):
        yield event.plain_result("240 已买断 四任")

    @filter.command("查询北极熊玩偶")
    async def reply_查询北极熊玩偶(self, event: AstrMessageEvent):
        yield event.plain_result("400 已买断 三任")

    @filter.command("查询卡路里面包兔")
    async def reply_查询卡路里面包兔(self, event: AstrMessageEvent):
        yield event.plain_result("280 已买断 二任")

    @filter.command("查询小短腿柯基")
    async def reply_查询小短腿柯基(self, event: AstrMessageEvent):
        yield event.plain_result("设主是燕咪～抽送 原设无偿 不用买断")

    @filter.command("查询藤川碎")
    async def reply_查询藤川碎(self, event: AstrMessageEvent):
        yield event.plain_result("是我哦(*'▽'*)♪我现任设主：云云 已买断")

    @filter.command("查询苍白天国")
    async def reply_查询苍白天国(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 五任")

    @filter.command("查询定制紫色章鱼小花")
    async def reply_查询定制紫色章鱼小花(self, event: AstrMessageEvent):
        yield event.plain_result("135 无需买断")

    @filter.command("查询定制浪花彩虹")
    async def reply_查询定制浪花彩虹(self, event: AstrMessageEvent):
        yield event.plain_result("90 无需买断")

    @filter.command("查询定制中二龙")
    async def reply_查询定制中二龙(self, event: AstrMessageEvent):
        yield event.plain_result("90 无需买断")

    @filter.command("查询定制异瞳白猫")
    async def reply_查询定制异瞳白猫(self, event: AstrMessageEvent):
        yield event.plain_result("90 无需买断")

    @filter.command("查询陶瓷猫猫")
    async def reply_查询陶瓷猫猫(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断 二任")

    @filter.command("查询气球猫营业员")
    async def reply_查询气球猫营业员(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 五任")

    @filter.command("查询千原一")
    async def reply_查询千原一(self, event: AstrMessageEvent):
        yield event.plain_result("是俺之前的自设(｡ˇε ˇ｡）")

    @filter.command("查询骰子兔子小姐")
    async def reply_查询骰子兔子小姐(self, event: AstrMessageEvent):
        yield event.plain_result("80 未买断")

    @filter.command("查询草莓奶油小方")
    async def reply_查询草莓奶油小方(self, event: AstrMessageEvent):
        yield event.plain_result("设主是芝士～属于福利设哦(*'▽'*)♪")

    @filter.command("查询酸奶产出者")
    async def reply_查询酸奶产出者(self, event: AstrMessageEvent):
        yield event.plain_result("25 未买断")

    @filter.command("查询奶油面包")
    async def reply_查询奶油面包(self, event: AstrMessageEvent):
        yield event.plain_result("设主是芝士～是无偿赠送哦(*'▽'*)♪")

    @filter.command("查询校园第十三条怪谈")
    async def reply_查询校园第十三条怪谈(self, event: AstrMessageEvent):
        yield event.plain_result("350 已买断 四任")

    @filter.command("查询定制猫烤布丁")
    async def reply_查询定制猫烤布丁(self, event: AstrMessageEvent):
        yield event.plain_result("50 无需买断")

    @filter.command("查询定制绿毛白花少女")
    async def reply_查询定制绿毛白花少女(self, event: AstrMessageEvent):
        yield event.plain_result("90 无需买断")

    @filter.command("查询云际的丹顶鹤")
    async def reply_查询云际的丹顶鹤(self, event: AstrMessageEvent):
        yield event.plain_result("384 已买断 四任")

    @filter.command("查询樱花色富士山和猫")
    async def reply_查询樱花色富士山和猫(self, event: AstrMessageEvent):
        yield event.plain_result("570 已买断 三任")

    @filter.command("查询碎花白狼")
    async def reply_查询碎花白狼(self, event: AstrMessageEvent):
        yield event.plain_result("150 已买断 四任")

    @filter.command("查询定制网瘾企鹅少女")
    async def reply_查询定制网瘾企鹅少女(self, event: AstrMessageEvent):
        yield event.plain_result("50 无需买断 五任")

    @filter.command("查询干花水信玄饼")
    async def reply_查询干花水信玄饼(self, event: AstrMessageEvent):
        yield event.plain_result("535 已买断 五任")

    @filter.command("查询化学系医师")
    async def reply_查询化学系医师(self, event: AstrMessageEvent):
        yield event.plain_result("580 已买断 五任")

    @filter.command("查询堂食大阪烧")
    async def reply_查询堂食大阪烧(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 五任")

    @filter.command("查询网页访问出错喵")
    async def reply_查询网页访问出错喵(self, event: AstrMessageEvent):
        yield event.plain_result("510 已买断 五任")

    @filter.command("查询海水煎蛋")
    async def reply_查询海水煎蛋(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断")

    @filter.command("查询音乐社团吉他手")
    async def reply_查询音乐社团吉他手(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 四任")

    @filter.command("查询电波狐狸风纪委员")
    async def reply_查询电波狐狸风纪委员(self, event: AstrMessageEvent):
        yield event.plain_result("400 已买断 四任")

    @filter.command("查询四四四小兔")
    async def reply_查询四四四小兔(self, event: AstrMessageEvent):
        yield event.plain_result("是送设哦(๑°3°๑)")

    @filter.command("查询鲜虾乌冬")
    async def reply_查询鲜虾乌冬(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 五任")

    @filter.command("查询随机参数")
    async def reply_查询随机参数(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 三任")

    @filter.command("查询幻想的一天")
    async def reply_查询幻想的一天(self, event: AstrMessageEvent):
        yield event.plain_result("100 未买断")

    @filter.command("查询抹茶奶油猫猫")
    async def reply_查询抹茶奶油猫猫(self, event: AstrMessageEvent):
        yield event.plain_result("150 已买断")

    @filter.command("查询甜甜圈小狗")
    async def reply_查询甜甜圈小狗(self, event: AstrMessageEvent):
        yield event.plain_result("是送给城城的设～(๑°3°๑)")

    @filter.command("查询街边的塑料袋")
    async def reply_查询街边的塑料袋(self, event: AstrMessageEvent):
        yield event.plain_result("150 已买断 四任")

    @filter.command("查询灾厄社畜")
    async def reply_查询灾厄社畜(self, event: AstrMessageEvent):
        yield event.plain_result("120 已买断")

    @filter.command("查询海域行空")
    async def reply_查询海域行空(self, event: AstrMessageEvent):
        yield event.plain_result("470 已买断 四任")

    @filter.command("查询困困草莓")
    async def reply_查询困困草莓(self, event: AstrMessageEvent):
        yield event.plain_result("150 已买断 五任")

    @filter.command("查询恋爱乙女")
    async def reply_查询恋爱乙女(self, event: AstrMessageEvent):
        yield event.plain_result("是抽送设哦(*´﹃｀*)")

    @filter.command("查询普通人类女仆")
    async def reply_查询普通人类女仆(self, event: AstrMessageEvent):
        yield event.plain_result("430 已买断 三任")

    @filter.command("查询孕育兔苗")
    async def reply_查询孕育兔苗(self, event: AstrMessageEvent):
        yield event.plain_result("430 已买断 三任 小葵和修修共养中～")

    @filter.command("查询老式蟹黄汤包")
    async def reply_查询老式蟹黄汤包(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 二任")

    @filter.command("查询宝箱怪boss")
    async def reply_查询宝箱怪boss(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 三任")

    @filter.command("查询变质便当")
    async def reply_查询变质便当(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 三任")

    @filter.command("查询烘焙于我")
    async def reply_查询烘焙于我(self, event: AstrMessageEvent):
        yield event.plain_result("450 已买断 五任")

    @filter.command("查询雾气云")
    async def reply_查询雾气云(self, event: AstrMessageEvent):
        yield event.plain_result("120 未买断")

    @filter.command("查询炼狱草莓酒")
    async def reply_查询炼狱草莓酒(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 五任")

    @filter.command("查询桃浆制品")
    async def reply_查询桃浆制品(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 三任")

    @filter.command("查询病理之爱")
    async def reply_查询病理之爱(self, event: AstrMessageEvent):
        yield event.plain_result("700 已买断 四任")

    @filter.command("查询童心小熊")
    async def reply_查询童心小熊(self, event: AstrMessageEvent):
        yield event.plain_result("是送设哦(≧∇≦)")

    @filter.command("查询唯一的朋友")
    async def reply_查询唯一的朋友(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断")

    @filter.command("查询皮格马利翁之帽")
    async def reply_查询皮格马利翁之帽(self, event: AstrMessageEvent):
        yield event.plain_result("是群福利抽送设哦～")

    @filter.command("查询程序侵入")
    async def reply_查询程序侵入(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断")

    @filter.command("查询谜题猫猫")
    async def reply_查询谜题猫猫(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 四任")

    @filter.command("查询通勤瓢虫")
    async def reply_查询通勤瓢虫(self, event: AstrMessageEvent):
        yield event.plain_result("180 已买断 五任")

    @filter.command("查询噩梦小鬼")
    async def reply_查询噩梦小鬼(self, event: AstrMessageEvent):
        yield event.plain_result("600 已买断 三任")

    @filter.command("查询鲨鲨宅")
    async def reply_查询鲨鲨宅(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断")

    @filter.command("查询外星小兔")
    async def reply_查询外星小兔(self, event: AstrMessageEvent):
        yield event.plain_result("600 已买断 四任")

    @filter.command("查询幻想中的玫瑰花")
    async def reply_查询幻想中的玫瑰花(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 四任")

    @filter.command("查询棋局之间")
    async def reply_查询棋局之间(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询瓷")
    async def reply_查询瓷(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 三任")

    @filter.command("查询渐变云层小狐狸")
    async def reply_查询渐变云层小狐狸(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 二任")

    @filter.command("查询田园花圃")
    async def reply_查询田园花圃(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询哭泣小兔")
    async def reply_查询哭泣小兔(self, event: AstrMessageEvent):
        yield event.plain_result("37.5 已买断 二人共养中")

    @filter.command("查询认真的恶魔酱")
    async def reply_查询认真的恶魔酱(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 五任")

    @filter.command("查询电子彩虹猫")
    async def reply_查询电子彩虹猫(self, event: AstrMessageEvent):
        yield event.plain_result("520 已买断 三任")

    @filter.command("查询天空塔")
    async def reply_查询天空塔(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 五任")

    @filter.command("查询药物博士")
    async def reply_查询药物博士(self, event: AstrMessageEvent):
        yield event.plain_result("225 已买断 三任")

    @filter.command("查询莓果兔")
    async def reply_查询莓果兔(self, event: AstrMessageEvent):
        yield event.plain_result("是送设喔(*'▽'*)♪ 二任")

    @filter.command("查询缤纷下午茶")
    async def reply_查询缤纷下午茶(self, event: AstrMessageEvent):
        yield event.plain_result("240 已买断 四任 二人共养中")

    @filter.command("查询恶魔的注视")
    async def reply_查询恶魔的注视(self, event: AstrMessageEvent):
        yield event.plain_result("240 已买断 五任")

    @filter.command("查询融化飞蛾")
    async def reply_查询融化飞蛾(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 二任")

    @filter.command("查询霓虹日和")
    async def reply_查询霓虹日和(self, event: AstrMessageEvent):
        yield event.plain_result("240 已买断 三任")

    @filter.command("查询虚拟的歌唱家")
    async def reply_查询虚拟的歌唱家(self, event: AstrMessageEvent):
        yield event.plain_result("240 已买断 五任")

    @filter.command("查询鱼类真主")
    async def reply_查询鱼类真主(self, event: AstrMessageEvent):
        yield event.plain_result("160 未买断 在小葵那里～")

    @filter.command("查询卷卷毛绒")
    async def reply_查询卷卷毛绒(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 二任")

    @filter.command("查询失散银河")
    async def reply_查询失散银河(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 二人共养中")

    @filter.command("查询青绿")
    async def reply_查询青绿(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 三任")

    @filter.command("查询明令禁止")
    async def reply_查询明令禁止(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 三任")

    @filter.command("查询斑斑点点")
    async def reply_查询斑斑点点(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 五任")

    @filter.command("查询电子速成犬")
    async def reply_查询电子速成犬(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 二任")

    @filter.command("查询chi掉苹果")
    async def reply_查询chi掉苹果(self, event: AstrMessageEvent):
        yield event.plain_result("170 未买断 也是小葵的≥﹏≤我什么时候能p到葵设")

    @filter.command("查询BOBO")
    async def reply_查询BOBO(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 二任")

    @filter.command("查询餐盘与心脏")
    async def reply_查询餐盘与心脏(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 二任")

    @filter.command("查询非我所愿")
    async def reply_查询非我所愿(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 五任")

    @filter.command("查询街区之旅")
    async def reply_查询街区之旅(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 五任")

    @filter.command("查询怦怦巧克力")
    async def reply_查询怦怦巧克力(self, event: AstrMessageEvent):
        yield event.plain_result("255 已买断 三任")

    @filter.command("查询超时链接")
    async def reply_查询超时链接(self, event: AstrMessageEvent):
        yield event.plain_result("170 未买断")

    @filter.command("查询距离恒定")
    async def reply_查询距离恒定(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 三任")

    @filter.command("查询无效祷告")
    async def reply_查询无效祷告(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断")

    @filter.command("查询糖渍玻璃")
    async def reply_查询糖渍玻璃(self, event: AstrMessageEvent):
        yield event.plain_result("650 已买断")

    @filter.command("查询青橘狐狐")
    async def reply_查询青橘狐狐(self, event: AstrMessageEvent):
        yield event.plain_result("是送设喔～")

    @filter.command("查询恋爱感应器械")
    async def reply_查询恋爱感应器械(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断")

    @filter.command("查询枝桠缠绕")
    async def reply_查询枝桠缠绕(self, event: AstrMessageEvent):
        yield event.plain_result("180 未买断")

    @filter.command("查询脆脆竹")
    async def reply_查询脆脆竹(self, event: AstrMessageEvent):
        yield event.plain_result("180 未买断 在小葵家～下次就p到葵设！")

    @filter.command("查询定制文学少女")
    async def reply_查询定制文学少女(self, event: AstrMessageEvent):
        yield event.plain_result("300 是定制啦～！ 三任")

    @filter.command("查询定制纽扣垂耳兔")
    async def reply_查询定制纽扣垂耳兔(self, event: AstrMessageEvent):
        yield event.plain_result("250 是定制喔(〃ﾉωﾉ)")

    @filter.command("查询蜜糖红豆年糕")
    async def reply_查询蜜糖红豆年糕(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 三任")

    @filter.command("查询二象性猫猫")
    async def reply_查询二象性猫猫(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询枯萎蛙")
    async def reply_查询枯萎蛙(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 五任")

    @filter.command("查询灵光乍现")
    async def reply_查询灵光乍现(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询白化别西卜")
    async def reply_查询白化别西卜(self, event: AstrMessageEvent):
        yield event.plain_result("180 未买断 小葵的✧٩(ˊωˋ*)و✧明天我也p到！")

    @filter.command("查询炙烤虾饼")
    async def reply_查询炙烤虾饼(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 四任")

    @filter.command("查询飘飘")
    async def reply_查询飘飘(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 五任")

    @filter.command("查询逃逸的薄荷")
    async def reply_查询逃逸的薄荷(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断")

    @filter.command("查询期限红酒")
    async def reply_查询期限红酒(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询光藓净化")
    async def reply_查询光藓净化(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 五任")

    @filter.command("查询云际航行")
    async def reply_查询云际航行(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询无法治愈")
    async def reply_查询无法治愈(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 三任")

    @filter.command("查询四分之三的你和四分之一的我")
    async def reply_查询四分之三的你和四分之一的我(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询百分百天使")
    async def reply_查询百分百天使(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 五任")

    @filter.command("查询哩哩")
    async def reply_查询哩哩(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任 在小葵家～～")

    @filter.command("查询定制爱心小草莓")
    async def reply_查询定制爱心小草莓(self, event: AstrMessageEvent):
        yield event.plain_result("500 已买断 四任：是定制设喔")

    @filter.command("查询照烧鱼果")
    async def reply_查询照烧鱼果(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 三任")

    @filter.command("查询回转寿司日")
    async def reply_查询回转寿司日(self, event: AstrMessageEvent):
        yield event.plain_result("285 已买断 二任")

    @filter.command("查询赴约期限")
    async def reply_查询赴约期限(self, event: AstrMessageEvent):
        yield event.plain_result("270 已买断 二任")

    @filter.command("查询丘比特•七夕特别版")
    async def reply_查询丘比特_七夕特别版(self, event: AstrMessageEvent):
        yield event.plain_result("是送设喔～")

    @filter.command("查询青蛙青蛙•七夕特别版")
    async def reply_查询青蛙青蛙_七夕特别版(self, event: AstrMessageEvent):
        yield event.plain_result("也是送设喔～")

    @filter.command("查询罗宋汤与胡萝卜")
    async def reply_查询罗宋汤与胡萝卜(self, event: AstrMessageEvent):
        yield event.plain_result("180 未买断")

    @filter.command("查询定制bingo")
    async def reply_查询定制bingo(self, event: AstrMessageEvent):
        yield event.plain_result("230 定制设不用买断啦")

    @filter.command("查询某年某日")
    async def reply_查询某年某日(self, event: AstrMessageEvent):
        yield event.plain_result("200 未买断")

    @filter.command("查询不要熬夜")
    async def reply_查询不要熬夜(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 三任")

    @filter.command("查询沉默檀香")
    async def reply_查询沉默檀香(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断")

    @filter.command("查询好运上上签")
    async def reply_查询好运上上签(self, event: AstrMessageEvent):
        yield event.plain_result("200 未买断")

    @filter.command("查询心意红豆沙")
    async def reply_查询心意红豆沙(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二人共养中")

    @filter.command("查询万圣夜狂欢")
    async def reply_查询万圣夜狂欢(self, event: AstrMessageEvent):
        yield event.plain_result("是送设哦 目前是共养中～")

    @filter.command("查询Blinkblink")
    async def reply_查询Blinkblink(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二任")

    @filter.command("查询雪花手册")
    async def reply_查询雪花手册(self, event: AstrMessageEvent):
        yield event.plain_result("180 未买断")

    @filter.command("查询薄荷致幻")
    async def reply_查询薄荷致幻(self, event: AstrMessageEvent):
        yield event.plain_result("285 已买断 二任")

    @filter.command("查询烘焙童话")
    async def reply_查询烘焙童话(self, event: AstrMessageEvent):
        yield event.plain_result("190 未买断")

    @filter.command("查询前夕的花蕾")
    async def reply_查询前夕的花蕾(self, event: AstrMessageEvent):
        yield event.plain_result("285 已买断 二任")

    @filter.command("查询尘寰浪漫")
    async def reply_查询尘寰浪漫(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二任")

    @filter.command("查询日常与不可能的漩涡")
    async def reply_查询日常与不可能的漩涡(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 三任")

    @filter.command("查询月下葵")
    async def reply_查询月下葵(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断")

    @filter.command("查询存在性征缪斯")
    async def reply_查询存在性征缪斯(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 三任")

    @filter.command("查询闪光派激萌")
    async def reply_查询闪光派激萌(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 三任")

    @filter.command("查询四重维度")
    async def reply_查询四重维度(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 五任")

    @filter.command("查询夜幕绕行")
    async def reply_查询夜幕绕行(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 四任")

    @filter.command("查询一页软糖")
    async def reply_查询一页软糖(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 四任")

    @filter.command("查询才不是玩偶兔")
    async def reply_查询才不是玩偶兔(self, event: AstrMessageEvent):
        yield event.plain_result("200 未买断")

    @filter.command("查询美丽新世界")
    async def reply_查询美丽新世界(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二任")

    @filter.command("查询行走东京")
    async def reply_查询行走东京(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二任")

    @filter.command("查询糖色信仰")
    async def reply_查询糖色信仰(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 三任")

    @filter.command("查询恒温动物")
    async def reply_查询恒温动物(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断")

    @filter.command("查询冷血动物")
    async def reply_查询冷血动物(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 二任 二人共养中")

    @filter.command("查询人群叛离")
    async def reply_查询人群叛离(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 二任")

    @filter.command("查询崩塌的阈值与象限")
    async def reply_查询崩塌的阈值与象限(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断")

    @filter.command("查询春季与绿苹果")
    async def reply_查询春季与绿苹果(self, event: AstrMessageEvent):
        yield event.plain_result("300 已买断 四任")

    @filter.command("查询睡意西瓜糖")
    async def reply_查询睡意西瓜糖(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 三任")

    @filter.command("查询云层与梦境")
    async def reply_查询云层与梦境(self, event: AstrMessageEvent):
        yield event.plain_result("210 未买断")

    @filter.command("查询乐天派小狗")
    async def reply_查询乐天派小狗(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 二任")

    @filter.command("查询腐败果实之宴")
    async def reply_查询腐败果实之宴(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 二任")

    @filter.command("查询无法原谅的一切")
    async def reply_查询无法原谅的一切(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 二任")

    @filter.command("查询逆向心愿")
    async def reply_查询逆向心愿(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 二任")

    @filter.command("查询甜蜜冰霜")
    async def reply_查询甜蜜冰霜(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 四任")

    @filter.command("查询自我上帝")
    async def reply_查询自我上帝(self, event: AstrMessageEvent):
        yield event.plain_result("315 已买断 二任 二人共养中")

    @filter.command("查询独居动物")
    async def reply_查询独居动物(self, event: AstrMessageEvent):
        yield event.plain_result("700 已买断")

    @filter.command("查询群居动物")
    async def reply_查询群居动物(self, event: AstrMessageEvent):
        yield event.plain_result("800 已买断 四任")

    @filter.command("查询透明人间")
    async def reply_查询透明人间(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 三任 二人共养中")

    @filter.command("查询碱水困境")
    async def reply_查询碱水困境(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 二任 二人共养中")

    @filter.command("查询完美快消品")
    async def reply_查询完美快消品(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 五任")

    @filter.command("查询海底囚徒")
    async def reply_查询海底囚徒(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 五任")

    @filter.command("查询人间一日游指南")
    async def reply_查询人间一日游指南(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 四任")

    @filter.command("查询枕头里的小妖怪")
    async def reply_查询枕头里的小妖怪(self, event: AstrMessageEvent):
        yield event.plain_result("330 已买断 四任")

    @filter.command("查询烟花色与不存在")
    async def reply_查询烟花色与不存在(self, event: AstrMessageEvent):
        yield event.plain_result("230 未买断")

    @filter.command("查询异国来信")
    async def reply_查询异国来信(self, event: AstrMessageEvent):
        yield event.plain_result("1900 已买断 二任 二人共养中")

    @filter.command("查询滤镜失灵")
    async def reply_查询滤镜失灵(self, event: AstrMessageEvent):
        yield event.plain_result("2000 已买断 三任")

    @filter.command("查询谁")
    async def reply_查询谁(self, event: AstrMessageEvent):
        yield event.plain_result("345 已买断 三任")

    @filter.command("查询肉食动物")
    async def reply_查询肉食动物(self, event: AstrMessageEvent):
        yield event.plain_result("2300 已买断 二人共养中")

    @filter.command("查询朝闻道")
    async def reply_查询朝闻道(self, event: AstrMessageEvent):
        yield event.plain_result("3000 已买断 二人共养中")

    @filter.command("查询跃动喵喵")
    async def reply_查询跃动喵喵(self, event: AstrMessageEvent):
        yield event.plain_result("是送设哦～")

    @filter.command("查询樱桃关节")
    async def reply_查询樱桃关节(self, event: AstrMessageEvent):
        yield event.plain_result("2000 已买断")

    @filter.command("查询魔女的法则")
    async def reply_查询魔女的法则(self, event: AstrMessageEvent):
        yield event.plain_result("3200 已买断 三任")

    @filter.command("查询要爱情不要面包")
    async def reply_查询要爱情不要面包(self, event: AstrMessageEvent):
        yield event.plain_result("360 已买断 四任")

    @filter.command("查询要面包不要爱情")
    async def reply_查询要面包不要爱情(self, event: AstrMessageEvent):
        yield event.plain_result("360 已买断 三任")

    @filter.command("查询我与绽放")
    async def reply_查询我与绽放(self, event: AstrMessageEvent):
        yield event.plain_result("3000 已买断 二任")

    @filter.command("查询至高天的降临")
    async def reply_查询至高天的降临(self, event: AstrMessageEvent):
        yield event.plain_result("3600 已买断 二任")

    @filter.command("查询被消解的玫瑰")
    async def reply_查询被消解的玫瑰(self, event: AstrMessageEvent):
        yield event.plain_result("450 已买断 二任")

    @filter.command("查询理解人类")
    async def reply_查询理解人类(self, event: AstrMessageEvent):
        yield event.plain_result("450 已买断 二任")

    @filter.command("查询花束中的新生")
    async def reply_查询花束中的新生(self, event: AstrMessageEvent):
        yield event.plain_result("450 已买断 二任")

    @filter.command("查询亡者永生")
    async def reply_查询亡者永生(self, event: AstrMessageEvent):
        yield event.plain_result("450 已买断 二任")

    @filter.command("查询外物游离")
    async def reply_查询外物游离(self, event: AstrMessageEvent):
        yield event.plain_result("300 未买断")

    @filter.command("查询死生一线")
    async def reply_查询死生一线(self, event: AstrMessageEvent):
        yield event.plain_result("5000 已买断 五任")

    @filter.command("查询最终的du约")
    async def reply_查询最终的du约(self, event: AstrMessageEvent):
        yield event.plain_result("5800 已买断 二任")

    @filter.command("查询伯爵献礼")
    async def reply_查询伯爵献礼(self, event: AstrMessageEvent):
        yield event.plain_result("480 已买断")

    @filter.command("查询牛油果毒素")
    async def reply_查询牛油果毒素(self, event: AstrMessageEvent):
        yield event.plain_result("480 已买断 三任")

    @filter.command("查询黑桃戏法")
    async def reply_查询黑桃戏法(self, event: AstrMessageEvent):
        yield event.plain_result("600 已买断 三任")

    @filter.command("查询双倍好运")
    async def reply_查询双倍好运(self, event: AstrMessageEvent):
        yield event.plain_result("540 已买断")

    @filter.command("查询木头生姜")
    async def reply_查询木头生姜(self, event: AstrMessageEvent):
        yield event.plain_result("400 未买断")

    @filter.command("查询神的欺诈")
    async def reply_查询神的欺诈(self, event: AstrMessageEvent):
        yield event.plain_result("400 未买断")

    @filter.command("查询果壳枣")
    async def reply_查询果壳枣(self, event: AstrMessageEvent):
        yield event.plain_result("630 已买断")

    @filter.command("查询萤火雨季")
    async def reply_查询萤火雨季(self, event: AstrMessageEvent):
        yield event.plain_result("600 已买断 三任")

    @filter.command("查询逃亡花园中")
    async def reply_查询逃亡花园中(self, event: AstrMessageEvent):
        yield event.plain_result("2000 已买断 二任")

    @filter.command("查询低温的星星")
    async def reply_查询低温的星星(self, event: AstrMessageEvent):
        yield event.plain_result("450 未买断")

    @filter.command("查询宇宙徊")
    async def reply_查询宇宙徊(self, event: AstrMessageEvent):
        yield event.plain_result("630 已买断")

    @filter.command("查询YEAH")
    async def reply_查询YEAH(self, event: AstrMessageEvent):
        yield event.plain_result("420 未买断")

    @filter.command("查询卷毛咖啡yin")
    async def reply_查询卷毛咖啡yin(self, event: AstrMessageEvent):
        yield event.plain_result("645 已买断 三任")

    @filter.command("查询幸福过敏")
    async def reply_查询幸福过敏(self, event: AstrMessageEvent):
        yield event.plain_result("420 未买断")

    @filter.command("查询雪国往事")
    async def reply_查询雪国往事(self, event: AstrMessageEvent):
        yield event.plain_result("430 未买断")

    @filter.command("查询定制爱意复写")
    async def reply_查询定制爱意复写(self, event: AstrMessageEvent):
        yield event.plain_result("设主是酒酒咪～")

    @filter.command("查询定制怀旧映像")
    async def reply_查询定制怀旧映像(self, event: AstrMessageEvent):
        yield event.plain_result("设主是雾凇咪～")

    @filter.command("查询定制概率游戏")
    async def reply_查询定制概率游戏(self, event: AstrMessageEvent):
        yield event.plain_result("设主是阿鹤咪～")

    @filter.command("查询彩虹糖时间")
    async def reply_查询彩虹糖时间(self, event: AstrMessageEvent):
        yield event.plain_result("430 未买断")

    @filter.command("查询白鸟停滞")
    async def reply_查询白鸟停滞(self, event: AstrMessageEvent):
        yield event.plain_result("3250 已买断 四任")

    @filter.command("查询子午线神游")
    async def reply_查询子午线神游(self, event: AstrMessageEvent):
        yield event.plain_result("1000 已买断 三任")

    @filter.command("查询定制人类失重")
    async def reply_查询定制人类失重(self, event: AstrMessageEvent):
        yield event.plain_result("设主是小飒～")

    @filter.command("查询定制唯")
    async def reply_查询定制唯(self, event: AstrMessageEvent):
        yield event.plain_result("设主是浮元子～")

    @filter.command("查询定制赫利俄斯之下")
    async def reply_查询定制赫利俄斯之下(self, event: AstrMessageEvent):
        yield event.plain_result("设主是芷阳～")

    @filter.command("查询美子的果实")
    async def reply_查询美子的果实(self, event: AstrMessageEvent):
        yield event.plain_result("1200 已买断")

    @filter.command("查询定制遐迩之月")
    async def reply_查询定制遐迩之月(self, event: AstrMessageEvent):
        yield event.plain_result("设主是池上月～")

    @filter.command("查询零点一冰室")
    async def reply_查询零点一冰室(self, event: AstrMessageEvent):
        yield event.plain_result("720 已买断 二任")

    @filter.command("查询乌鸦的权杖")
    async def reply_查询乌鸦的权杖(self, event: AstrMessageEvent):
        yield event.plain_result("750 已买断")

    @filter.command("查询簌簌")
    async def reply_查询簌簌(self, event: AstrMessageEvent):
        yield event.plain_result("720 已买断 三任")

    @filter.command("查询芭比巴卜")
    async def reply_查询芭比巴卜(self, event: AstrMessageEvent):
        yield event.plain_result("500 未买断")

    @filter.command("查询冷冷的夏天")
    async def reply_查询冷冷的夏天(self, event: AstrMessageEvent):
        yield event.plain_result("780 已买断 二任")

    @filter.command("查询三只猎犬")
    async def reply_查询三只猎犬(self, event: AstrMessageEvent):
        yield event.plain_result("800 已买断")

    @filter.command("查询BLUES")
    async def reply_查询BLUES(self, event: AstrMessageEvent):
        yield event.plain_result("800 已买断 二任")

    @filter.command("查询北芪与白山")
    async def reply_查询北芪与白山(self, event: AstrMessageEvent):
        yield event.plain_result("500 未买断")

    @filter.command("查询浴室里的啵帕")
    async def reply_查询浴室里的啵帕(self, event: AstrMessageEvent):
        yield event.plain_result("520 未买断")

    @filter.command("查询红苹果之森")
    async def reply_查询红苹果之森(self, event: AstrMessageEvent):
        yield event.plain_result("500 未买断")

    @filter.command("查询青苹果之塔")
    async def reply_查询青苹果之塔(self, event: AstrMessageEvent):
        yield event.plain_result("520 未买断")

    @filter.command("查询金苹果之谜")
    async def reply_查询金苹果之谜(self, event: AstrMessageEvent):
        yield event.plain_result("780 已买断 三任")

    @filter.command("查询紫苹果之药")
    async def reply_查询紫苹果之药(self, event: AstrMessageEvent):
        yield event.plain_result("780 已买断 二任")

    @filter.command("查询七月流火")
    async def reply_查询七月流火(self, event: AstrMessageEvent):
        yield event.plain_result("850 已买断")

    @filter.command("查询安娜苏的日记簿")
    async def reply_查询安娜苏的日记簿(self, event: AstrMessageEvent):
        yield event.plain_result("850 已买断 二任")

    @filter.command("查询CANDY")
    async def reply_查询CANDY(self, event: AstrMessageEvent):
        yield event.plain_result("850 已买断")

    @filter.command("查询墨鱼的论坛")
    async def reply_查询墨鱼的论坛(self, event: AstrMessageEvent):
        yield event.plain_result("850 已买断 三任")

    @filter.command("查询山莓会社")
    async def reply_查询山莓会社(self, event: AstrMessageEvent):
        yield event.plain_result("780 已买断 二任")

    @filter.command("查询天使城邀约")
    async def reply_查询天使城邀约(self, event: AstrMessageEvent):
        yield event.plain_result("780 已买断")

    @filter.command("查询都市恶灵废墟")
    async def reply_查询都市恶灵废墟(self, event: AstrMessageEvent):
        yield event.plain_result("1200 已买断 二任")

    @filter.command("查询定制雾镜迷城")
    async def reply_查询定制雾镜迷城(self, event: AstrMessageEvent):
        yield event.plain_result("设主是雾凇咪～")

    @filter.command("查询定制命运长街")
    async def reply_查询定制命运长街(self, event: AstrMessageEvent):
        yield event.plain_result("设主是雾凇咪～")

    @filter.command("查询POPO")
    async def reply_查询POPO(self, event: AstrMessageEvent):
        yield event.plain_result("2400 已买断 二任")

    @filter.command("一共有多少个云设")
    async def reply_一共有多少个云设(self, event: AstrMessageEvent):
        yield event.plain_result("到目前为止，录入bot的设定一共有439个哦✧٩(ˊωˋ*)و✧")





    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        self._save_state()

    def _time_period(self) -> str:
        """根据本地时间返回时段标签"""
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "morning"
        if 11 <= hour < 14:
            return "noon"
        if 14 <= hour < 18:
            return "afternoon"
        if 18 <= hour < 24:
            return "evening"
        return "midnight"
