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








    # ---- 新增指令：投喂（42条候选，含特殊食物，3分钟冷却）----
    @filter.command("投喂")
    async def feed_xiaosui(self, event: AstrMessageEvent):
        """给小碎投喂；每次好感度+0~10，命中特殊食物额外+5~20；冷却3分钟"""
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)
        user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

        now_ts = int(datetime.now().timestamp())
        cd = 180  # 3分钟
        last_ts = int(user.get("last_feed_ts", 0))
        remain = cd - (now_ts - last_ts)
        if remain > 0:
            mm, ss = divmod(remain, 60)
            wait_str = f"{mm}分{ss}秒" if mm else f"{ss}秒"
            yield event.plain_result(
                f"⌛ {user_name}，小碎还在消化中～请再等 {wait_str} 再投喂。\n"
                f"💗 当前好感度：{user.get('favor',0)}"
            )
            return

        # 结构：(一句话情景文本, 是否特殊)
        pool = []

        # --- 星露谷物语 ×10（新增2条：生鱼片、幸运午餐） ---
        pool += [
            ("小碎接过星露谷的披萨，边吹边咬一口，芝士拉出细细长丝。", False),
            ("粉红蛋糕香气扑鼻，小碎小口啃着，脸颊鼓鼓的。", False),
            ("星露谷的咖啡刚冲好，小碎捧着杯子深吸一口气再轻抿。", False),
            ("鲑鱼晚餐摆上桌，小碎认真地把柠檬挤在鱼排上。", False),
            ("巧克力蛋糕切下一角，小碎把叉子立正地插好再优雅送入口。", False),
            ("龙虾浓汤热气氤氲，小碎端稳碗边吹边喝。", False),
            ("香辣鳗鱼一上来，小碎眯起眼睛说：这股劲儿正合适。", True),          # 特殊
            ("金星南瓜派切面细腻，小碎晃晃叉子：今天也会很顺利。", True),        # 特殊
            ("生鱼片切得晶莹，小碎蘸了一点酱油，满足地眯起眼。", False),           # 新增
            ("幸运午餐端到面前，小碎认真默念：今天要抓住好时机。", True),         # 新增/特殊
        ]

        # --- 饥荒 ×5 ---
        pool += [
            ("小碎把饥荒的肉丸倒进碗里，用小勺一下一下地舀。", False),
            ("太妃糖甜意蔓延，小碎舔了舔指尖上的糖霜。", False),
            ("培根煎蛋滋滋作响，小碎把蛋黄轻轻戳破配着培根吞下。", True),       # 特殊
            ("饕餮馅饼切开冒着热气，小碎吹了两口才敢咬。", True),                  # 特殊
            ("波兰饺子皮薄馅足，小碎夹起一个蘸了点酱再吃。", False),
        ]

        # --- 泰拉瑞亚 ×5 ---
        pool += [
            ("熟鱼肉质紧实，小碎顺着鱼刺细细拆开吃得很认真。", False),
            ("南瓜派切成扇形，小碎数了数层次才下口。", False),
            ("一碗热汤端上来，小碎先试探地抿了一口再点头。", False),
            ("苹果派略带肉桂香，小碎把边缘的酥皮先掰掉吃。", False),
            ("至尊培根油亮喷香，小碎一口下去精神都跟着抖擞起来。", True),       # 特殊
        ]

        # --- 通用可爱互动 ×22 ---
        pool += [
            ("热可可送到手心，小碎呼一口热气暖暖指尖。", False),
            ("草莓牛奶冰凉顺喉，小碎在吸管里发出小小的咕噜声。", False),
            ("抹茶曲奇咔哧一声，小碎认真数着碎屑别让它们逃跑。", False),
            ("蜜瓜面包外脆内软，小碎把顶上的格子一块块掰开。", False),
            ("薄荷冰淇淋化得很快，小碎飞快地转着杯子防止滴落。", False),
            ("芝士汉堡层层叠，小碎从侧面小心翼翼地咬第一口。", False),
            ("蜂蜜柚子茶微苦回甘，小碎捧杯看着浮起的柚皮条发呆。", False),
            ("可丽饼卷着奶油，小碎先舔了一下边缘确认不会沾鼻尖。", False),
            ("彩虹果冻在盘里抖动，小碎用勺背轻轻按了按。", True),                # 特殊
            ("焦糖布蕾敲开脆皮，小碎满意地点点头。", False),
            ("焗土豆牵丝拉长，小碎把丝绕在叉子上慢慢卷。", False),
            ("乌龙奶盖茶入口绵密，小碎把奶盖胡子抹掉后偷笑。", False),
            ("樱花团子软糯弹牙，小碎一串一串地分给大家。", False),
            ("海盐美式醒脑一击，小碎眨眨眼决定开始干活。", False),
            ("松饼塔叠得高高的，小碎担心倒塌先抽走最顶上一片。", False),
            ("柠檬塔酸甜对撞，小碎被刺激得肩膀一抖又想再来一口。", False),
            ("巧克力豆在掌心融化，小碎赶紧一颗颗送进嘴里。", False),
            ("蜜桃乌龙果香四溢，小碎把漂浮的果肉捞起来慢慢嚼。", False),
            ("星光糖在舌尖噼啪作响，小碎被惊到笑出声。", True),                 # 特殊
            ("小熊软糖排成方阵，小碎宣布开饭仪式并迅速解散队伍。", False),
            ("玉米棒刷了黄油，小碎顺着纹路一排排地啃。", False),
            ("椰子布丁轻轻晃动，小碎叮嘱自己这次一定不要打翻。", False),
        ]

        # 安全兜底
        if not pool:
            pool = [("小饼干一块，小碎眯起眼心情变好。", False)]

        # --- 随机抽取 ---
        text, is_special = random.choice(pool)

        # --- 基础好感 +0~10 ---
        favor_inc = random.randint(0, 10)
        bonus_inc = 0
        bonus_text = ""
        if is_special:
            bonus_inc = random.randint(5, 20)
            bonus_text = f"\n诶，吃到了特别的食物！小碎好感度额外增加 {bonus_inc}"

        # --- 更新与落盘（记录冷却时间戳）---
        user["favor"] += favor_inc + bonus_inc
        user["last_feed_ts"] = now_ts
        self._save_state()

        # --- 回复 ---
        def fmt_plus(n: int) -> str:
            return f"+{n}" if n >= 0 else f"{n}"

        reply = (
            f"{user_name} 投喂：{text}\n"
            f"好感度 {fmt_plus(favor_inc)}{bonus_text}\n"
            f"💗 当前好感度：{user['favor']}"
        )
        yield event.plain_result(reply)

# ---- 新增指令：运势（0与100有特殊奖励）----
@filter.command("运势")
async def fortune(self, event: AstrMessageEvent):
    """
    随机给出 0~100 的当下运势值。
    - 运势=0：安慰并赠送 3 颗玻璃珠（含鼓励话术）
    - 运势=100：+10 好感度，+50 玻璃珠（含祝福话术）
    """
    user_name = event.get_sender_name()
    user_id = self._get_user_id(event)
    user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

    FACES = [
        "(๑•̀ㅂ•́)و✧", "(つ´ω`)つ", "(*/ω＼*)", "(๑ᵔ⤙ᵔ๑)", "(=^･ω･^=)",
        "( ੭ ˙ᗜ˙ )੭", "(≧▽≦)/", "ヾ(•ω•`)o", "(｡•̀ᴗ-)✧", "(ง •̀_•́)ง",
        "(˶ᵔ ᵕ ᵔ˶)", "(•̀ᴗ•́)و ̑̑", "(*´∀`*)", "(｡˃ ᵕ ˂ )b", "(　＾∀＾)"
    ]
    face = random.choice(FACES)

    x = random.randint(0, 100)

    base_line = f"你当下的运势是 {x}，顺带一提，运势是百分制的哦~ {face}"

    # 特殊分支：0 与 100
    if x == 0:
        user["marbles"] += 3
        encourage_pool = [
            "低谷是弹射的起点，慢慢来会好起来的～",
            "别担心，休整一下再出发，风会转向你这边。",
            "把情绪放下半步，路就会出现。加油！"
        ]
        reply = (
            f"{base_line}\n"
            f"🫧 小碎送你 3 颗玻璃珠以示安慰。\n"
            f"📣 {random.choice(encourage_pool)}\n"
            f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
        )
        self._save_state()
        yield event.plain_result(reply)
        return

    if x == 100:
        user["favor"] += 10
        user["marbles"] += 50
        bless_pool = [
            "愿你所想皆如愿、所行皆坦途！",
            "万事顺遂，灵感与好运一起到访～",
            "今天你发光，世界都在为你让路！"
        ]
        reply = (
            f"{base_line}\n"
            f"🎉 满分好运！小碎为你提升好感度 +10，并赠送 50 颗玻璃珠！\n"
            f"🌟 {random.choice(bless_pool)}\n"
            f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
        )
        self._save_state()
        yield event.plain_result(reply)
        return

    # 常规分支：1~99
    reply = f"{base_line}\n📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
    yield event.plain_result(reply)



# ---- 新增指令：我还要签到（九段运势，仅玻璃珠变动，不加好感）----
@filter.command("我还要签到")
async def extra_sign_in(self, event: AstrMessageEvent):
    """
    规则：
    - 每日一次（与“签到”互不影响），记录到 user['last_extra_sign']
    - 随机给出九段运势：大吉/吉/中吉/小吉/平/小凶/中凶/凶/大凶
    - 仅根据运势增减玻璃珠，不增加好感度
    - 运势好→祝福；运势差→鼓励；平→中性提示
    """
    user_name = event.get_sender_name()
    user_id = self._get_user_id(event)
    user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

    today = datetime.now().date().isoformat()
    if user.get("last_extra_sign") == today:
        yield event.plain_result(
            f"🔒 {user_name}，今天已经进行过【勤勉签到】啦～\n"
            f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
        )
        return

    diligent_lines = [
        "今天也是勤勉的一天～",
        "记录一下扎实的努力！",
        "稳步前进就是胜利～",
        "打卡！小目标正在靠近你～",
        "勤能补拙，今天也很棒！",
        "有在认真生活的味道～",
        "努力被宇宙看见啦！",
        "悄悄耕耘，静待花开～",
        "积跬步以至千里！",
        "继续保持，好状态在线～",
        "今日功课√ 给自己点个赞！",
        "进度条+1，能量值+1！",
        "你在变好，小碎看得见～",
        "认真这件事，你赢麻了～",
        "坚持的人自带光～"
    ]
    diligent_text = random.choice(diligent_lines)

    # 九段日式运势
    luck_levels = ["大吉", "吉", "中吉", "小吉", "平", "小凶", "中凶", "凶", "大凶"]
    level = random.choice(luck_levels)

    # 对应玻璃珠区间
    marble_ranges = {
        "大吉": (180, 266),
        "吉": (120, 200),
        "中吉": (80, 160),
        "小吉": (40, 100),
        "平": (0, 60),
        "小凶": (-20, 20),
        "中凶": (-60, 0),
        "凶": (-120, -40),
        "大凶": (-200, -100),
    }
    desc = {
        "大吉": "群星加护",
        "吉": "好运相随",
        "中吉": "顺水顺心",
        "小吉": "稳步向前",
        "平": "风平浪静",
        "小凶": "略有波折",
        "中凶": "阴云未散",
        "凶": "注意节奏",
        "大凶": "谨慎行事",
    }

    rmin, rmax = marble_ranges[level]
    delta = random.randint(rmin, rmax)
    delta = max(-266, min(266, delta))
    user["marbles"] = user.get("marbles", 0) + delta

    # 祝福 / 中性 / 鼓励
    bless_pool = [
        "好运加身，今天注定闪闪发光～",
        "顺风顺水，连星星都在帮你许愿！",
        "阳光正好，心想事成～"
    ]
    neutral_pool = [
        "平稳是另一种幸福，慢慢走也能到达。",
        "不焦不躁，保持节奏就是好兆头。",
        "静水流深，平日的积累最可贵。"
    ]
    encourage_pool = [
        "乌云只是暂时的，下一刻就是晴天。",
        "先休息一下，明天会更顺。",
        "困难是运气积蓄的前奏，撑一撑就见光。"
    ]

    if level in ("大吉", "吉", "中吉", "小吉"):
        mood_line = f"🌟 {random.choice(bless_pool)}"
    elif level == "平":
        mood_line = f"🧭 {random.choice(neutral_pool)}"
    else:
        mood_line = f"🛡️ {random.choice(encourage_pool)}"

    user["last_extra_sign"] = today
    self._save_state()

    def fmt_signed(n: int) -> str:
        return f"+{n}" if n >= 0 else f"{n}"

    reply = (
        f"{diligent_text}\n"
        f"📅 今日运势：**{level}（{desc[level]}）**\n"
        f"🫧 玻璃珠变动：{fmt_signed(delta)}（不增加好感度）\n"
        f"{mood_line}\n"
        f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
    )
    yield event.plain_result(reply)

    # ==== 内部：初始化彩蛋系统结构（必须有） ====
    def _ensure_egg_state(self):
        """确保彩蛋系统的状态结构存在"""
        if "egg_system" not in self._state:
            self._state["egg_system"] = {}
        if "users" not in self._state:
            self._state["users"] = {}
        es = self._state["egg_system"]
        # 彩蛋数量配置
        es.setdefault("catalog", {"N": 25, "R": 10, "UR": 5, "SP": 10})
        # “最难超稀有彩蛋”的标记（用于0.5%掉落判定）
        es.setdefault("mythic_id", {"cat": "UR", "id": 5})


# ==== 彩蛋系统（掉落、去重、成就、图鉴）========================================
# 用法建议：
# 1) 在你的「签到」「我还要签到」「占卜」「投喂」等指令的尾部调用：
#       await self._try_drop_easter_egg(event, is_interaction=True)
#    这些“日常互动”每次将有 15% 概率掉落彩蛋（并自动处理奖励与成就）。
# 2) 若你在「任何群内消息」的入口处（如全局 on_message 钩子）也想掉落彩蛋，可调用：
#       await self._try_drop_easter_egg(event, is_interaction=False)
#    这类“日常聊天”将有 5% 概率掉落彩蛋。
#
# 说明：
# - 总计 50 个彩蛋：普通 25、稀有 10、超稀有 5、特别 10（与星露谷/饥荒/泰拉瑞亚相关）
# - 特别彩蛋：每次掉落判定中有固定 10% 机会指定为“特别”
# - 稀有度权重（在非特别时）：普通≈80%、稀有≈19%、超稀有≈1%
# - 不会重复获得相同彩蛋
# - 超稀有中存在“最难”的唯一彩蛋（全 50 个中最难触发）：全局 0.5% 掉落概率，
#   奖励为好感 +300、玻璃珠 +999（其它超稀有不会奖励这么多）
# - 每个彩蛋都有独立的奖励区间，稀有度越高，奖励越多
# - 成就（共 6 个）：1/10/25/40/全收集（50）/特别全收集（10）
#   奖励：见 ACHIEVEMENTS_REWARD
#
# 你可以用下方“彩蛋图鉴”指令查看进度。

# —— 内部：初始化彩蛋相关状态结构 —— #
def _ensure_egg_state(self):
    if "egg_system" not in self._state:
        self._state["egg_system"] = {}
    if "users" not in self._state:
        self._state["users"] = {}
    es = self._state["egg_system"]
    # 目录配置（只记录数量，不记录文案；文案由模板生成）
    es.setdefault("catalog", {"N": 25, "R": 10, "UR": 5, "SP": 10})
    # 保留“最难超稀有”的唯一编号（UR 的最后一个）
    es.setdefault("mythic_id", {"cat": "UR", "id": 5})

# —— 内部：格式化奖励显示（带正负号） —— #
def _fmt_signed(self, n: int) -> str:
    return f"+{n}" if n >= 0 else f"{n}"

# —— 内部：根据稀有度与编号，生成稳定的彩蛋标题与内容（不随时间改变） —— #
# ==== 改进版：逻辑式彩蛋文本 + 奖励关联 =======================================

def _egg_text(self, cat: str, idx: int) -> tuple[str, str, int, int]:
    """
    返回 (标题, 内容, favor_inc, marble_inc)
    每个编号对应一个固定的故事与奖励逻辑。
    """
    # 普通彩蛋（25）
    normal_eggs = [
        ("【甜甜圈店的奇遇】",
         "和小碎一起吃到了超棒的草莓燕麦脆珠甜甜圈，意外地在甜甜圈上发现了玻璃珠点缀！",
         5, 30),
        ("【便利店的幸运签】",
         "小碎在发票上刮出了‘再来一瓶’的幸运字样，两人都笑了。",
         8, 20),
        ("【邮筒下的信封】",
         "风吹起的信封里掉出一枚亮晶晶的珠子，小碎帮忙捡了起来。",
         10, 15),
        ("【路边的猫】",
         "小碎蹲下摸了摸那只橘猫，猫打了个滚，露出一个闪光的小球。",
         12, 25),
        ("【掉落的糖纸】",
         "糖纸背后写着‘今天会有好事’，结果你脚边真的滚来一颗玻璃珠。",
         8, 18),
        ("【泡泡机的故障】",
         "泡泡里飞出一颗小珠子，小碎忙着追，结果你们都笑翻了。",
         10, 20),
        ("【夜晚的便利店灯】",
         "灯光闪了三下，柜台边反光的不是零钱，而是一颗漂亮的珠子。",
         6, 25),
        ("【公交卡的反面】",
         "小碎贴贴公交卡背面，发现印着一颗笑脸玻璃珠的图案，感觉被祝福了。",
         15, 10),
        ("【角落的糖果罐】",
         "最后一颗玻璃糖是心形的，小碎说：‘这是今天的好运！’",
         10, 30),
        ("【图书馆的回音】",
         "小碎在书页间发现一张旧书签，上面粘着一颗迷你珠子。",
         6, 18),
        ("【海边的贝壳】",
         "贝壳打开，里面藏着一颗像月亮一样的玻璃珠。",
         15, 25),
        ("【风车转动的瞬间】",
         "小碎拍下的照片里，多出了一道光点，那正是玻璃珠的倒影。",
         12, 20),
        ("【废弃游乐场】",
         "旋转木马启动了一下，地上掉出一个粉色珠子。",
         8, 28),
        ("【天台的风筝】",
         "线断了，但风筝带回一条缎带，上面缠着珠光。",
         10, 25),
        ("【午后的柠檬水】",
         "酸酸甜甜，小碎喝完一整杯，发现杯底的冰块里冻着颗玻璃珠！",
         8, 35),
        ("【路灯下的影子】",
         "两道影子交叠时，地上闪了下光，小碎惊呼：‘它在动！’",
         5, 20),
        ("【天桥上的彩带】",
         "风吹落的彩带挂在你手臂上，系着一颗蓝色小珠子。",
         10, 30),
        ("【车站的留言墙】",
         "‘要一起努力哦’，小碎指着那条留言笑了，旁边是一个闪亮标记。",
         15, 15),
        ("【海洋的声音】",
         "和小碎一起到海滩，听到人鱼们在歌唱，他们的眼泪化作了玻璃珠滚到脚边。",
         12, 20),
        ("【蛋糕店的点心】",
         "抹茶蛋糕上插着小碎做的旗子，下面藏了两颗玻璃珠。",
         8, 40),
        ("【自动售货机】",
         "买饮料多吐了一颗珠珠糖，味道居然是薄荷运气味。",
         10, 15),
        ("【街角旧相机】",
         "冲洗出的照片上闪着彩色反光，小碎说那是‘情绪的珠子’。",
         10, 25),
        ("【山丘上的风】",
         "风吹乱了头发，也吹来一颗珠子，小碎伸手接住。",
         5, 35),
        ("【纸飞机的终点】",
         "飞机降落在你的脚边，小碎在上面画了个笑脸。",
         12, 20),
        ("【猫头鹰的信】",
         "夜空里传来一声咕咕，信封掉落，里面是小碎画的珠子贴纸。",
         15, 25),
    ]

    # 稀有彩蛋（10）
    rare_eggs = [
        ("【流星下的约定】",
         "小碎许愿：‘如果有星星掉下来，就分你一半好运！’第二天地上真多了几颗珠子。",
         20, 80),
        ("【梦中的旋律】",
         "梦里小碎弹钢琴，音符变成闪光的玻璃珠飘起。",
         25, 60),
        ("【钟楼的碎片】",
         "钟声敲响时，掉下一片刻着花纹的玻璃片，光从中透出彩虹。",
         15, 100),
        ("【湖面的倒影】",
         "你与小碎低头看湖，水中星光汇成一颗大珠子。",
         30, 70),
        ("【雪天的手套】",
         "雪地里摸到小碎丢的手套，里面藏着一颗温热的珠子。",
         20, 90),
        ("【风铃的共鸣】",
         "小碎挂起的风铃在风中共振，风声带来了好运。",
         25, 75),
        ("【夜市的奖券】",
         "小碎抽中了‘特等奖’，奖品是一瓶装满玻璃珠的罐子！",
         15, 120),
        ("【旧车站的时刻表】",
         "上面手写着‘等好运的列车’，角落贴着一颗珠子。",
         20, 90),
        ("【烟花的残光】",
         "烟花散尽，‘每一次闪烁，都是你的一颗幸运珠。’",
         25, 100),
        ("【风中的回信】",
         "寄出的信没有名字，但回信附了一颗发光珠。",
         30, 80),
    ]

    # 超稀有彩蛋（5）
    ur_eggs = [
        ("【星辉折射镜】",
         "小碎用镜子对准夜空，所有星光都汇聚成你的名字。",
         60, 200),
        ("【时间夹缝票根】",
         "旧电影院的票根突然发光，时光倒流回最初的那天。",
         100, 150),
        ("【彩色万花筒】",
         "透过万花筒看世界，小碎发现每个图案中心都有颗珠子。",
         50, 250),
        ("【空中花园门票】",
         "风带来一张写着‘限时入场’的门票，小碎带你飞了上去。",
         120, 120),
        ("【群星玻璃匣】",
         "（恭喜达成最稀有彩蛋~！）小碎打开匣子，所有星星一齐闪烁——玻璃珠飞舞成环。",
         300, 999),
    ]

    # 特别彩蛋（10）
    sp_eggs = [
        # 星露谷 6
        ("【星露谷·金星南瓜派】",
         "小碎帮忙烤南瓜派，结果烤盘里多了闪亮的珠子。",
         25, 150),
        ("【星露谷·幸运午餐】",
         "午餐香气扑鼻，小碎咬下一口后：‘今天会超顺利的！’",
         20, 100),
        ("【星露谷·古代水果酒】",
         "酒香飘满农场，瓶底藏着一颗古老的珠子。",
         15, 200),
        ("【星露谷·火山地牢】",
         "熔岩菇闪着红光，小碎摘下最大的一颗递给你。",
         30, 120),
        ("【星露谷·春】",
         "春天里花瓣徐徐飘落，小碎从风中捞到一颗玻璃珠。",
         25, 130),
        ("【星露谷·流星田边】",
         "夜里的农田被流星照亮，一颗珠子嵌在土里发光。",
         20, 160),
        # 饥荒 2
        ("【饥荒·猪王的馈赠】",
         "猪王开心地丢出三颗珠子，小碎接得飞快。",
         15, 180),
        ("【饥荒·舞台剧】",
         "影子伸手递来礼物，小碎微笑着收下。",
         25, 150),
        # 泰拉瑞亚 2
        ("【泰拉瑞亚·红心水晶】",
         "砸碎红心后，小碎心跳了一下，地上出现两颗珠子。",
         20, 200),
        ("【泰拉瑞亚·月总的余晖】",
         "月亮领主化作光，化成珠雨落下。",
         40, 250),
    ]

    pools = {"N": normal_eggs, "R": rare_eggs, "UR": ur_eggs, "SP": sp_eggs}
    if cat not in pools or idx > len(pools[cat]):
        return "【未知彩蛋】", "神秘的数据碎片在闪光。", 0, 0
    return pools[cat][idx - 1]

# —— 奖励部分由 _egg_text 自带，因此 _roll_rewards 不再使用 —— #
def _roll_rewards(self, cat: str, is_mythic: bool):
    return 0, 0  # 保留空壳防兼容

# —— 内部：选择一个尚未获得的彩蛋（按类别与编号池），失败返回 None —— #
def _pick_uncollected(self, user, cat: str):
    total = self._state["egg_system"]["catalog"][cat]
    owned = set(user.setdefault("eggs", {}).setdefault(cat, []))
    candidates = [i for i in range(1, total + 1) if i not in owned]
    if not candidates:
        return None
    return random.choice(candidates)

# —— 内部：尝试掉落（核心逻辑） —— #
async def _try_drop_easter_egg(self, event: AstrMessageEvent, *, is_interaction: bool):
    """
    is_interaction=True  → 15% 掉落
    is_interaction=False →  5% 掉落
    包含：
      - 特别彩蛋 10% 固定概率
      - 最难超稀有（0.5% 全局几率）
      - 稀有度权重：普通/稀有/超稀有 ≈ 80/19/1（当未命中特别/最难时）
      - 去重、发放奖励、成就判定
    """
    self._ensure_egg_state()
    user_id = self._get_user_id(event)
    user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})
    user.setdefault("eggs", {"N": [], "R": [], "UR": [], "SP": []})
    user.setdefault("egg_total", 0)
    user.setdefault("egg_achievements", [])  # 存储已解锁成就 key

    # 掉落判定
    p = 0.15 if is_interaction else 0.05
    if random.random() >= p:
        return  # 没掉落就静默

    # —— 0.5%：最难超稀有 —— #
    myth = self._state["egg_system"]["mythic_id"]
    if random.random() < 0.005:
        # 仅当未拥有
        if myth["id"] not in user["eggs"]["UR"]:
            cat, idx, is_mythic = myth["cat"], myth["id"], True
        else:
            cat, idx, is_mythic = None, None, False
    else:
        cat, idx, is_mythic = None, None, False

    # —— 10%：特别彩蛋 —— #
    if cat is None:
        if random.random() < 0.10:
            pick = self._pick_uncollected(user, "SP")
            if pick:
                cat, idx = "SP", pick

    # —— 常规权重（普通/稀有/超稀有） —— #
    if cat is None:
        # 近似 80/19/1
        r = random.random()
        order = [("N", 0.80), ("R", 0.99), ("UR", 1.00)]
        chosen = None
        for c, th in order:
            if r <= th:
                chosen = c
                break
        # 如果该类已满，按 N→R→UR→SP 轮询找可用（SP 作为兜底）
        for c in [chosen, "N", "R", "UR", "SP"]:
            pick = self._pick_uncollected(user, c)
            if pick:
                cat, idx = c, pick
                break

    # 没有任何可选（可能已全收集）
    if cat is None or idx is None:
        return

    # —— 生成文本与奖励 —— #
    title, content = self._egg_text(cat, idx)
    favor_inc, marble_inc = self._roll_rewards(cat, is_mythic)
    user["favor"] += favor_inc
    user["marbles"] += marble_inc

    # 记录收藏
    user["eggs"][cat].append(idx)
    user["egg_total"] = sum(len(v) for v in user["eggs"].values())

    # 彩蛋稀有度中文名
    cat_name = {"N": "普通彩蛋", "R": "稀有彩蛋", "UR": "超稀有彩蛋", "SP": "特别彩蛋"}[cat]

    # 输出文本（遵循格式：【彩蛋描述】（彩蛋内容）+奖励）
    lines = []
    prefix = "（最难！）" if is_mythic else ""
    lines.append(f"{cat_name}*{title}{prefix}{content}")
    lines.append(f"小碎好感{self._fmt_signed(favor_inc)}，玻璃珠{self._fmt_signed(marble_inc)}。")

    # —— 成就判定 —— #
    ach_lines = self._check_and_grant_achievements(event, user)

    self._save_state()
    # 发送合并结果
    reply = "\n".join(lines + ach_lines + [
        f"📦 当前背包｜好感度：{user['favor']}｜玻璃珠：{user['marbles']}"])
    yield event.plain_result(reply)

# —— 内部：成就系统 —— #
def _check_and_grant_achievements(self, event: AstrMessageEvent, user) -> list[str]:
    """
    返回需要追加展示的成就文本数组
    """
    user_name = event.get_sender_name()
    owned_sp = len(user["eggs"]["SP"])
    total = user["egg_total"]

    ACHIEVEMENTS = [
        ("EGG_1",      total >= 1,   "「小碎的第一颗蛋」 —— 小碎开心地举起它，眼睛闪闪发光。"),
        ("EGG_10",     total >= 10,  "「彩蛋连连看」 —— 你的篮子叮叮当当，越来越重啦～"),
        ("EGG_25",     total >= 25,  "「珍重的回忆」 —— 旅程已经过了一半。"),
        ("EGG_40",     total >= 40,  " 叮咚！小碎的惊喜仓库」 —— 彩蛋多到小碎要数不过来了！"),
        ("EGG_ALL",    total >= 50,  "「小碎的终极闪闪收藏」 —— 全部集齐，连星星都在鼓掌～"),
        ("EGG_SP_ALL", owned_sp >= 10, "「特别蛋大冒险！」 —— 小碎和你跑遍世界，收集到了所有的奇迹！"),
    ]
    ACHIEVEMENTS_REWARD = {
        "EGG_1":      (3, 20),
        "EGG_10":     (10, 80),
        "EGG_25":     (20, 150),
        "EGG_40":     (40, 300),
        "EGG_ALL":    (120, 800),   # 全收集最多
        "EGG_SP_ALL": (60, 400),    # 特别全收集也很香
    }
    WOW = [
        "这运气太会挑时机啦！",
        "小碎眼睛都亮了！",
        "鼓掌到手心红彤彤～",
        "概率亲了你一下！",
    ]


    out = []
    unlocked = set(user.setdefault("egg_achievements", []))
    for key, cond, name in ACHIEVEMENTS:
        if cond and key not in unlocked:
            unlocked.add(key)
            user["egg_achievements"] = list(unlocked)
            f_inc, m_inc = ACHIEVEMENTS_REWARD[key]
            user["favor"] += f_inc
            user["marbles"] += m_inc
            out.append(
                f"🎖️ {random.choice(WOW)} {user_name}，恭喜你触发了【{name}】成就，小碎送你"
                f" 好感{self._fmt_signed(f_inc)}、玻璃珠{self._fmt_signed(m_inc)}～"
            )
    return out

# —— 指令：彩蛋图鉴（查看进度与成就） —— #
@filter.command("彩蛋图鉴")
async def eggdex(self, event: AstrMessageEvent):
    self._ensure_egg_state()
    user_id = self._get_user_id(event)
    user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})
    user.setdefault("eggs", {"N": [], "R": [], "UR": [], "SP": []})
    user.setdefault("egg_total", 0)
    user.setdefault("egg_achievements", [])

    N, R, UR, SP = (len(user["eggs"]["N"]), len(user["eggs"]["R"]),
                    len(user["eggs"]["UR"]), len(user["eggs"]["SP"]))
    total = user["egg_total"]
    ach = user["egg_achievements"]

    # 进度条文本
    bar = lambda got, all_: "█" * min(10, round(got / all_ * 10)) + "░" * max(0, 10 - round(got / all_ * 10))

    catalog = self._state["egg_system"]["catalog"]
    reply = (
        "📖 小碎的彩蛋图鉴\n"
        f"普通：{N}/{catalog['N']}  [{bar(N, catalog['N'])}]\n"
        f"稀有：{R}/{catalog['R']}  [{bar(R, catalog['R'])}]\n"
        f"超稀有：{UR}/{catalog['UR']}  [{bar(UR, catalog['UR'])}]\n"
        f"特别：{SP}/{catalog['SP']}  [{bar(SP, catalog['SP'])}]\n"
        f"总计：{total}/50\n"
        f"成就：{len(ach)} 个（已解锁：{', '.join(ach) if ach else '暂无'}）\n"
        f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
    )
    yield event.plain_result(reply)

    # ---- 新增指令：彩蛋详情（查看某一类彩蛋的已收集故事）----
@filter.command("彩蛋详情")
async def egg_detail(self, event: AstrMessageEvent):
    """
    用法：
    - 发送 “彩蛋详情 普通” 或 “彩蛋详情 稀有/超稀有/特别”
    - 显示已收集彩蛋的标题与故事。
    - 若未指定类别，则默认展示全部分类的简要摘要。
    """
    self._ensure_egg_state()
    user_id = self._get_user_id(event)
    user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})
    user.setdefault("eggs", {"N": [], "R": [], "UR": [], "SP": []})

    args = event.message_str.strip().split()
    query = args[1] if len(args) > 1 else None

    cat_map = {
        "普通": "N", "稀有": "R", "超稀有": "UR", "特别": "SP",
    }

    # 无参数时输出收集进度摘要
    if query is None:
        summary = (
            f"📔 小碎的彩蛋详情索引\n"
            f"可以发送：彩蛋详情 普通｜稀有｜超稀有｜特别\n"
            f"已收集：普通 {len(user['eggs']['N'])}/25，稀有 {len(user['eggs']['R'])}/10，"
            f"超稀有 {len(user['eggs']['UR'])}/5，特别 {len(user['eggs']['SP'])}/10"
        )
        yield event.plain_result(summary)
        return

    if query not in cat_map:
        yield event.plain_result("❓ 类别无效哦～请输入 普通 / 稀有 / 超稀有 / 特别")
        return

    cat = cat_map[query]
    collected = user["eggs"].get(cat, [])
    if not collected:
        yield event.plain_result(f"📭 {query}彩蛋还没有收集到哦～快去多和小碎玩玩吧！")
        return

    reply_lines = [f"🎀 你已收集的 {query}彩蛋："]
    for idx in sorted(collected):
        title, content, favor, marbles = self._egg_text(cat, idx)
        reply_lines.append(
            f"{title}\n{content}\n💗 好感+{favor}｜🫧 玻璃珠+{marbles}\n"
        )

    # 分隔符让内容阅读更舒适
    result = "\n".join(reply_lines)
    yield event.plain_result(result)

    

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        self._save_state()


