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

    # ---- 新版：占卜（每日一次，内联数据，仅三组牌）----
    @filter.command("占卜")
    async def divination(self, event: AstrMessageEvent):
        """
        每日仅可占卜一次：
        - 首次占卜扣 20 玻璃珠
        - 随机抽取 22 大阿卡那中的前三组（愚者/魔术师/女祭司，含正逆）
        - 展示等级（SSS/SS/S/B/C/D/F）和中文形容，并根据好/波动/坏给祝福或安慰
        - 玻璃珠增减区间受等级影响（最终裁切到 ±266）
        - 好感度 +0~50，与牌面无关
        - SSS 牌有 10% 额外 +999 玻璃珠奖励
        """
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)
        user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

        # 每日一次
        today = datetime.now().date().isoformat()
        if user.get("last_divine") == today:
            yield event.plain_result(
                f"🔒 {user_name}，今天已经占卜过啦～明天再来试试命运之轮吧！\n"
                f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
            )
            return

        # 占卜费用（仅首次）
        fee = 20
        user["marbles"] = user.get("marbles", 0) - fee

        # 等级 -> 形容词 & 玻璃珠区间（最终会裁切到 ±266）
        RATING_WORD = {
            "SSS": "特别棒的",
            "SS":  "很好的",
            "S":   "不错的",
            "B":   "有波动的",
            "C":   "不太顺的",
            "D":   "糟心的",
            "F":   "相当危险的",
        }
        MARBLE_RANGE = {
            "SSS": (200, 266),
            "SS":  (120, 220),
            "S":   (40, 160),
            "B":   (-60, 120),
            "C":   (-160, 40),
            "D":   (-220, -40),
            "F":   (-266, -120),
        }

        # 仅前三组牌（正/逆）
        CARDS = {
            "愚者": {
                "upright":  {"core": "自由", "type": "SS",  "keywords": ["起点","冒险","单纯","信任","未知","旅途"], "interp": "拥抱未知，轻装上路会带来新鲜突破。"},
                "reversed": {"core": "鲁莽", "type": "C",   "keywords": ["冲动","迷路","逃避","风险","幼稚","分心"], "interp": "先看脚下再跳，边界与计划缺一不可。"},
            },
            "魔术师": {
                "upright":  {"core": "创造", "type": "SSS", "keywords": ["专注","沟通","资源","技巧","显化","机会"], "interp": "心之所向可被实现，主动出手就是魔法。"},
                "reversed": {"core": "失衡", "type": "D",   "keywords": ["欺骗","分神","虚张","失控","散漫","反复"], "interp": "谨防口惠而实不至，把能量收束回到行动。"},
            },
            "女祭司": {
                "upright":  {"core": "直觉", "type": "S",   "keywords": ["潜意识","静观","神秘","梦境","洞察","沉默"], "interp": "答案在心底，给直觉一点安静的空间。"},
                "reversed": {"core": "压抑", "type": "C",   "keywords": ["怀疑","迟疑","隔阂","隐瞒","自我否定","迷雾"], "interp": "过度压抑会遮蔽线索，承认感受即是起点。"},
            },
        }

        # 随机抽牌与正逆
        card_name = random.choice(list(CARDS.keys()))
        upright = random.choice([True, False])
        orient = "upright" if upright else "reversed"
        m = CARDS[card_name][orient]
        orient_cn = "正位" if upright else "逆位"
        rating = m["type"]

        # 玻璃珠增减（按等级），并裁切到 ±266
        rmin, rmax = MARBLE_RANGE[rating]
        marble_delta = random.randint(rmin, rmax)
        marble_delta = max(-266, min(266, marble_delta))

        # 好感度独立 +0~50
        favor_inc = random.randint(0, 50)

        # SSS 10% 额外奖励
        bonus = 0
        bonus_text = ""
        if rating == "SSS" and random.random() < 0.10:
            bonus = 999
            bonus_text = "\n🎉 中奖时刻！群星垂青，额外获得 **999** 颗玻璃珠！"

        # 好/波动/坏 -> 祝福/安慰
        if rating in ("SSS", "SS", "S"):
            mood_pool = [
                "🕊️ 祝福送达：顺风顺水、步步开花！",
                "🌟 保持清澈与专注，好运与成果相互奔赴。",
                "🚀 节奏对了就别停，今天的舞台灯正亮着。",
            ]
        elif rating == "B":
            mood_pool = [
                "🌗 形势有波动，收束变量稳稳推进。",
                "🧭 先拿下一个小目标，趋势自然会靠拢你。",
                "⚖️ 少量正确比大量盲冲更强。",
            ]
        else:
            mood_pool = [
                "🫧 别怕，先安顿好自己，路会在脚下重新出现。",
                "🌧️ 暂避锋芒也算前进，修复能量再出发。",
                "🛡️ 把风险写出来就降级一半，慢慢来，一切都会过去。",
            ]
        mood_line = random.choice(mood_pool)

        # 更新状态并标记今日已占卜
        user["favor"] += favor_inc
        user["marbles"] += marble_delta + bonus
        user["last_divine"] = today
        self._save_state()

        # 输出
        def fmt_signed(n: int) -> str:
            return f"+{n}" if n >= 0 else f"{n}"
        rating_word = RATING_WORD[rating]
        keywords = "、".join(m["keywords"][:6])

        reply = (
            f"🔮 我收取了 **{fee}** 枚玻璃珠作为占卜费用……\n"
            f"✨ 本次是 **{card_name}·{orient_cn}**\n"
            f"等级：**{rating}（{rating_word}）**\n"
            f"核心：**{m['core']}**｜其它：{keywords}\n"
            f"🔎 解析：{m['interp']}\n"
            f"{mood_line}\n"
            f"💗 小碎好感度 {fmt_signed(favor_inc)}，"
            f"🫧 玻璃珠 {fmt_signed(marble_delta + bonus)}{bonus_text}\n"
            f"📦 当前背包｜好感度：{user['favor']}｜玻璃珠：{user['marbles']}"
        )
        yield event.plain_result(reply)



    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        self._save_state()
