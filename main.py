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


# ==== 彩蛋系统（被动触发 + 成就）========================================
# 用法（请在以下指令最后面各加一行调用）：
#   - 在“签到”、“我还要签到”、“占卜”、“投喂”的回复 yield 之后，追加：
#       res = await self._try_drop_egg(event, is_interaction=True)
#       if res: yield res
#   - 若你有一个“群内任意消息入口”（如总 on_message/默认回调），在合适位置追加：
#       res = await self._try_drop_egg(event, is_interaction=False)
#       if res: yield res
#
# 说明：
# - 群内任意消息：5% 掉落概率
# - 日常互动（两个签到、占卜、投喂）：15% 掉落概率
# - 特别彩蛋：固定每次 10% 概率独立判定（若命中则直接掉落特别彩蛋）
# - 超稀有中有一个“传说彩蛋”全局 0.5% 概率（独立判定），奖励 300 好感 + 999 玻璃珠
# - 不会掉重复彩蛋；若该稀有度已集齐，会自动回落/上浮到可用的稀有度
# - 成就：集齐 1/10/25/40/50（全收集）、特别彩蛋全收集；触发即发放奖励
# ======================================================================

# （放在类里）
async def _try_drop_egg(self, event: AstrMessageEvent, is_interaction: bool) -> MessageEventResult | None:
    user_name = event.get_sender_name()
    user_id = self._get_user_id(event)
    user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

    # ── 初始化彩蛋/成就存档 ─────────────────────────────────────────────
    store = self._state.setdefault("eggs", {})
    u = store.setdefault(user_id, {
        "collected": [],            # 存放 egg_id 列表（不重复）
        "achievements": [],         # 已达成成就 key 列表
        "special_collected": [],    # 已收集的“特别彩蛋” egg_id
    })

    # ── 定义彩蛋池（每种先给 3 个示例，其余你可继续补充到目标数量）────────
    # 结构：("id", "标题", "正文内容（不含结尾奖励提示）", favor_delta, marbles_delta)
    NORMAL_EGGS = [
        ("n01", "【甜甜圈店的奇遇】", "和小碎一起吃到了超棒的草莓燕麦脆珠甜甜圈，意外地在甜甜圈上发现了玻璃珠点缀！", 5, 30),
        ("n02", "【落叶捡到信封】", "风把一封未寄出的感谢信吹到你脚边，小碎帮你把它妥帖转交。", 4, 20),
        ("n03", "【图书角的便签】", "角落里的书页间夹着温柔的提醒：补水、休息、继续出发。", 3, 15),
        # TODO: 补充至 25 个普通彩蛋
    ]
    RARE_EGGS = [
        ("r01", "【月光茶会】", "与小碎在露台泡了一壶月见乌龙，茶香里藏着一点点好运。", 12, 60),
        ("r02", "【旧相机咔嚓】", "你和小碎的合影被冲洗出来，照片边缘泛着温暖的光晕。", 15, 80),
        ("r03", "【流星备忘录】", "数到第七颗流星时，小碎递来一张写着“保持热爱”的小纸条。", 18, 90),
        # TODO: 补充至 10 个稀有彩蛋
    ]
    # 超稀有里包含一个“传说彩蛋”（id = u00），全局 0.5% 概率；其余奖励为两位/三位量级
    ULTRA_EGGS = [
        ("u00", "【星海的奇迹】", "星河旋转落在你掌心，小碎惊叹得说不出话。", 300, 999),   # 传说彩蛋（最难）
        ("u01", "【时间的裂缝】", "你和小碎在钟表店里看见秒针倒转了一小格。", 40, 150),
        ("u02", "【七色玻璃室】", "阳光穿过彩窗，小碎替你接住了最亮的一束。", 90, 60),
        # TODO: 补充至 5 个超稀有彩蛋（含 u00 在内）
    ]
    # 特别彩蛋（与星露谷、饥荒、泰拉瑞亚相关）——固定 10% 独立概率
    SPECIAL_EGGS = [
        # 星露谷
        ("s-sdv-01", "【星露谷·金星南瓜】", "秋收节的瓜香甜到小碎眯起了眼：今天一定会很顺。", 16, 120),
        # 饥荒
        ("s-dst-01", "【饥荒·远古火焰】", "营地重燃，小碎在火光里认真烤好了第一块培根煎蛋。", 20, 100),
        # 泰拉瑞亚
        ("s-ter-01", "【泰拉瑞亚·陨星之夜】", "划破天际的光砸在远处，小碎把你往更安全的方向拉。", 22, 110),
        # TODO: 补充至 10 个特别彩蛋（可按三作继续扩展）
    ]

    # 快速索引：已拥有
    owned = set(u["collected"])
    owned_special = set(u["special_collected"])

    # ── 概率设定 ──────────────────────────────────────────────────────
    # 基础掉落概率：互动 15%，普通消息 5%
    base_p = 0.15 if is_interaction else 0.05

    # 特别彩蛋：固定 10% 独立判定（若命中则直接走特别彩蛋逻辑）
    from random import random, choice

    # 1) 先判定特别彩蛋（独立）
    if random() < 0.10:
        # 可选的特别彩蛋（去重）
        avail = [e for e in SPECIAL_EGGS if e[0] not in owned_special]
        if not avail:
            # 特别彩蛋已集齐，继续进入普通概率流
            pass
        else:
            egg = choice(avail)
            return await self._award_egg_and_achievements(event, user_name, user_id, user, u, egg, rarity_tag="特别彩蛋")

    # 2) 然后判定基础掉落
    if random() >= base_p:
        return None

    # 3) 传说彩蛋全局 0.5% 独立触发（若未获得）
    mythic = next((e for e in ULTRA_EGGS if e[0] == "u00"), None)
    if mythic and mythic[0] not in owned and random() < 0.005:
        return await self._award_egg_and_achievements(event, user_name, user_id, user, u, mythic, rarity_tag="超稀有彩蛋")

    # 4) 稀有度权重抽取（可按需微调）
    #    普通 82%，稀有 17%，超稀有 1%
    roll = random()
    if roll < 0.82:
        pool, tag = NORMAL_EGGS, "普通彩蛋"
    elif roll < 0.99:
        pool, tag = RARE_EGGS, "稀有彩蛋"
    else:
        pool, tag = ULTRA_EGGS, "超稀有彩蛋"

    # 按稀有度挑未拥有
    avail = [e for e in pool if e[0] not in owned]
    # 若该池已空，则尝试回落/上浮寻找可用彩蛋
    if not avail:
        fallback_order = [NORMAL_EGGS, RARE_EGGS, ULTRA_EGGS]
        for p in fallback_order:
            cand = [e for e in p if e[0] not in owned]
            if cand:
                avail = cand
                tag = "普通彩蛋" if p is NORMAL_EGGS else ("稀有彩蛋" if p is RARE_EGGS else "超稀有彩蛋")
                break
    if not avail:
        # 全部收集完毕则不给重复；可以在此提示“已全收集”
        return None

    egg = choice(avail)
    return await self._award_egg_and_achievements(event, user_name, user_id, user, u, egg, rarity_tag=tag)

# 负责发放奖励 + 成就检测 + 文案输出
async def _award_egg_and_achievements(self, event: AstrMessageEvent, user_name: str, user_id: str,
                                      user: dict, ustate: dict, egg_tuple: tuple, rarity_tag: str) -> MessageEventResult:
    egg_id, title, body, f_inc, m_inc = egg_tuple

    # 写入收集
    if rarity_tag == "特别彩蛋":
        if egg_id not in ustate["special_collected"]:
            ustate["special_collected"].append(egg_id)
    if egg_id not in ustate["collected"]:
        ustate["collected"].append(egg_id)

    # 发奖励
    user["favor"] += int(f_inc)
    user["marbles"] += int(m_inc)

    # 成就检查
    achieve_msgs = self._check_and_award_achievements(user_name, user_id, user, ustate)

    # 落盘
    self._save_state()

    # 文案（与示例格式一致）
    reply = (
        f"{rarity_tag}*{title}{body} 小碎好感+{f_inc}，玻璃珠+{m_inc}。\n"
        + ("\n".join(achieve_msgs) + ("\n" if achieve_msgs else ""))
        + f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
    )
    return event.plain_result(reply)

def _check_and_award_achievements(self, user_name: str, user_id: str, user: dict, ustate: dict) -> list[str]:
    msgs = []
    owned = set(ustate.get("collected", []))
    owned_special = set(ustate.get("special_collected", []))
    done = set(ustate.get("achievements", []))

    # 成就定义（key, 触发条件函数, 奖励favor, 奖励marbles, 展示名）
    ACHIEVEMENTS = [
        ("a01_any_1",    lambda: len(owned) >= 1,   2,   5,   "第一次发现彩蛋"),
        ("a02_any_10",   lambda: len(owned) >= 10, 10,  30,   "彩蛋猎人·入门"),
        ("a03_any_25",   lambda: len(owned) >= 25, 20,  80,   "彩蛋猎人·进阶"),
        ("a04_any_40",   lambda: len(owned) >= 40, 40, 150,   "彩蛋收藏家"),
        ("a05_all_50",   lambda: len(owned) >= 50, 100, 500,  "全收集·群星加冕"),
        ("a06_sp_all",   lambda: len(owned_special) >= 10, 60, 300, "特别彩蛋·全收集"),
    ]

    for key, cond, fav, marb, title in ACHIEVEMENTS:
        if key not in done and cond():
            done.add(key)
            ustate["achievements"] = list(done)
            user["favor"] += fav
            user["marbles"] += marb
            # 小碎恭喜语（全收集与特别全收集更激动一些）
            if key in ("a05_all_50", "a06_sp_all"):
                exclaim = "哇——太厉害了！" if key == "a06_sp_all" else "天哪，了不起！"
                msgs.append(
                    f"🎖️ {user_name}，恭喜你触发了【{title}】成就！{exclaim}小碎送你 好感+{fav}、玻璃珠+{marb}～"
                )
            else:
                msgs.append(
                    f"🏅 {user_name}，恭喜你触发了【{title}】成就！小碎送你 好感+{fav}、玻璃珠+{marb}～"
                )

    return msgs




    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        self._save_state()
