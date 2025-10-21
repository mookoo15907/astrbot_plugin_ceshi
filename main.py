from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import random
import json
from pathlib import Path
from datetime import datetime

    # ---- 新增指令：占卜 ----
    @filter.command("占卜")
    async def divination(self, event: AstrMessageEvent):
        """
        随机抽取一张 22 大阿卡那（正/逆），
        先收取 20 玻璃珠占卜费；根据牌面评级决定玻璃珠增减（±266 封顶），
        好感度额外 +0~50；若为“特别棒”(SSS) 有 10% 概率额外 +999。
        """
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)
        user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

        # 1) 扣占卜费
        fee = 20
        user["marbles"] = user.get("marbles", 0) - fee

        # 2) 随机牌与正逆
        card_name = random.choice(list(MAJOR_ARCANA.keys()))
        upright = random.choice([True, False])
        orient = "upright" if upright else "reversed"
        m: ArcMeaning = MAJOR_ARCANA[card_name][orient]
        orient_cn = "正位" if upright else "逆位"

        # 3) 计算玻璃珠增减（按评级区间）与好感度
        rmin, rmax = MARBLE_RANGE[m.type]
        marble_delta = random.randint(rmin, rmax)
        # clip 到 ±266
        marble_delta = max(-266, min(266, marble_delta))

        favor_inc = random.randint(0, 50)

        # 4) SSS 额外 10% 中奖 +999
        bonus_text = ""
        bonus_delta = 0
        if m.type == "SSS" and random.random() < 0.10:
            bonus_delta = 999
            bonus_text = "\n🎉 中奖时刻！群星垂青，额外获得 **999** 颗玻璃珠！"

        # 5) 更新背包
        user["favor"] = user.get("favor", 0) + favor_inc
        user["marbles"] = user.get("marbles", 0) + marble_delta + bonus_delta
        self._save_state()

        # 6) 展示用的符号
        def fmt_signed(n: int) -> str:
            return f"+{n}" if n >= 0 else f"{n}"

        rating_word = RATING_WORD[m.type]
        keywords = "、".join(m.keywords[:6])

        reply = (
            f"🔮 我收取了 **{fee}** 枚玻璃珠作为占卜费用……\n"
            f"✨ 本次是 **{card_name}·{orient_cn}**\n"
            f"核心：**{m.core}**｜其它：{keywords}\n"
            f"🔎 解析：{m.interp}\n"
            f"这是一张**{rating_word}**牌呢。\n"
            f"💗 小碎好感度 {fmt_signed(favor_inc)}，"
            f"🫧 玻璃珠 {fmt_signed(marble_delta + bonus_delta)}{bonus_text}\n"
            f"📦 当前背包｜好感度：{user['favor']}｜玻璃珠：{user['marbles']}"
        )

        yield event.plain_result(reply)


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 数据持久化文件：插件同目录 data/xiaosui_state.json
        self._data_dir = Path(__file__).parent / "data"
        self._data_path = self._data_dir / "xiaosui_state.json"
        self._state = {"users": {}}  # { user_id: {"favor": int, "marbles": int, "last_sign": "YYYY-MM-DD"} }

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        try:
            self._data_dir.mkdir(parents=True, exist_ok=True)
            if self._data_path.exists():
                self._state = json.loads(self._data_path.read_text(encoding="utf-8"))
                if "users" not in self._state:
                    self._state["users"] = {}
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

    def _time_period(self, now: datetime | None = None) -> str:
        """按小时划分时间段：早上/中午/下午/晚上/半夜"""
        h = (now or datetime.now()).hour
        if 5 <= h <= 10:
            return "morning"
        if 11 <= h <= 13:
            return "noon"
        if 14 <= h <= 17:
            return "afternoon"
        if 18 <= h <= 22:
            return "evening"
        return "midnight"  # 23~4

    # ---- 已有指令：小碎（保留随机多语气） ----
    @filter.command("小碎")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令"""
        user_name = event.get_sender_name()
        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)

        replies = [
            f"你好呀，{user_name}，小碎在这里～",
            f"{user_name}，找我有什么事吗？",
            f"在呢在呢～{user_name}，小碎随时待命！",
            f"怎么了吗？",
            f"我在(*'▽'*)♪",
            f"嗨——"
        ]
        yield event.plain_result(random.choice(replies))

    # ---- 新增指令：签到（已加“每日一次”限制） ----
    @filter.command("签到")
    async def sign_in(self, event: AstrMessageEvent):
        """根据时间段打招呼 + 随机获得好感度与玻璃珠，并记录到背包；每日仅可签到一次"""
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)

        # ——【新增：每天只能签到一次的校验】——
        today = datetime.now().date().isoformat()
        user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})
        if user.get("last_sign") == today:
            yield event.plain_result(
                f"{user_name}，今天已经签过到啦～\n当前好感度：{user['favor']}｜玻璃珠：{user['marbles']}"
            )
            return
        # ——【新增结束】——

        period = self._time_period()
        pool = {
            "morning": [
                f"早安，{user_name}！小碎为你点亮新的一天～",
                f"{user_name} 早呀！今天也一起加油！",
                f"清晨好，{user_name}～来摸摸小碎提提神！",
                f"小碎送来一杯热可可，{user_name} 早上好！",
                f"新的一天，从和小碎说早安开始吧，{user_name}～",
                f"晨光正好，{user_name}～"
            ],
            "noon": [
                f"午间好，{user_name}～记得补充能量哦！",
                f"{user_name} 午好！小碎给你加点效率 BUFF～",
                f"小憩一下吧，{user_name}～小碎守着你！",
                f"咕噜咕噜～午饭好吃吗 {user_name}？",
                f"精神满满的下午从饱饱的中午开始！{user_name}～",
                f"午安～{user_name}，小碎在线待命！"
            ],
            "afternoon": [
                f"下午好，{user_name}～小碎陪你继续冲刺！",
                f"{user_name}，下午的太阳刚刚好～",
                f"来点小甜点如何？小碎请你～",
                f"保持专注，{user_name}～小碎给你打气！",
                f"嗷嗷～{user_name}，小碎在这儿守护你！",
                f"下午茶时间到～{user_name} 要不要来一口？"
            ],
            "evening": [
                f"晚上好，{user_name}～要不要一起放松下？",
                f"{user_name} 辛苦啦！小碎给你舒缓一下～",
                f"夜色真美，{user_name}～小碎也在！",
                f"来听会儿歌吧，{user_name}～小碎陪你～",
                f"收工快乐，{user_name}！小碎为你点亮小灯灯～",
                f"晚风轻拂～{user_name}，小碎在这儿～"
            ],
            "midnight": [
                f"半夜啦，{user_name}～注意休息哦，小碎抱抱～",
                f"{user_name} 还没睡呀？小碎小声陪你～",
                f"夜深了，{user_name}～要不要喝点热牛奶？",
                f"小碎给你盖小被子～{user_name} 晚安前的签到也很可爱！",
                f"星星眨眼睛～{user_name}，小碎悄悄上线～",
                f"夜猫子小队集合！{user_name}～小碎打卡到！"
            ],
        }

        greet = random.choice(pool[period])

        favor_inc = random.randint(0, 30)
        marbles_inc = random.randint(0, 30)

        # 此处直接使用上面已获取/创建的 user
        user["favor"] += favor_inc
        user["marbles"] += marbles_inc
        user["last_sign"] = today  # 记录今天已签到
        self._save_state()

        reply = (
            f"{greet}\n"
            f"签到成功啦～小碎好感度 +{favor_inc}，小碎赠予你 {marbles_inc} 颗玻璃珠。\n"
            f"当前好感度：{user['favor']}｜玻璃珠：{user['marbles']}"
        )
        yield event.plain_result(reply)

    # ---- 新增指令：我的背包 ----
    @filter.command("我的背包")
    async def my_bag(self, event: AstrMessageEvent):
        """查看当前用户累计的好感度与玻璃珠"""
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)
        info = self._state["users"].get(user_id, {"favor": 0, "marbles": 0})
        yield event.plain_result(
            f"{user_name} 的背包：\n好感度：{info['favor']}\n玻璃珠：{info['marbles']}"
        )

        # ---- 新增指令：占卜 ----
    @filter.command("占卜")
    async def divination(self, event: AstrMessageEvent):
        """
        随机抽取一张 22 大阿卡那（正/逆），
        先收取 20 玻璃珠占卜费；根据牌面评级决定玻璃珠增减（±266 封顶），
        好感度额外 +0~50；若为“特别棒”(SSS) 有 10% 概率额外 +999。
        """
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)
        user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

        # 1) 扣占卜费
        fee = 20
        user["marbles"] = user.get("marbles", 0) - fee

        # 2) 随机牌与正逆
        card_name = random.choice(list(MAJOR_ARCANA.keys()))
        upright = random.choice([True, False])
        orient = "upright" if upright else "reversed"
        m: ArcMeaning = MAJOR_ARCANA[card_name][orient]
        orient_cn = "正位" if upright else "逆位"

        # 3) 计算玻璃珠增减（按评级区间）与好感度
        rmin, rmax = MARBLE_RANGE[m.type]
        marble_delta = random.randint(rmin, rmax)
        # clip 到 ±266
        marble_delta = max(-266, min(266, marble_delta))

        favor_inc = random.randint(0, 50)

        # 4) SSS 额外 10% 中奖 +999
        bonus_text = ""
        bonus_delta = 0
        if m.type == "SSS" and random.random() < 0.10:
            bonus_delta = 999
            bonus_text = "\n🎉 中奖时刻！群星垂青，额外获得 **999** 颗玻璃珠！"

        # 5) 更新背包
        user["favor"] = user.get("favor", 0) + favor_inc
        user["marbles"] = user.get("marbles", 0) + marble_delta + bonus_delta
        self._save_state()

        # 6) 展示用的符号
        def fmt_signed(n: int) -> str:
            return f"+{n}" if n >= 0 else f"{n}"

        rating_word = RATING_WORD[m.type]
        keywords = "、".join(m.keywords[:6])

        reply = (
            f"🔮 我收取了 **{fee}** 枚玻璃珠作为占卜费用……\n"
            f"✨ 本次是 **{card_name}·{orient_cn}**\n"
            f"核心：**{m.core}**｜其它：{keywords}\n"
            f"🔎 解析：{m.interp}\n"
            f"这是一张**{rating_word}**牌呢。\n"
            f"💗 小碎好感度 {fmt_signed(favor_inc)}，"
            f"🫧 玻璃珠 {fmt_signed(marble_delta + bonus_delta)}{bonus_text}\n"
            f"📦 当前背包｜好感度：{user['favor']}｜玻璃珠：{user['marbles']}"
        )

        yield event.plain_result(reply)


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        self._save_state()
