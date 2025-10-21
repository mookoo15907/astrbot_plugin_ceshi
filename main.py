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

    # ---- 新增指令：占卜（每日一次）----
    @filter.command("占卜")
    async def divination(self, event: AstrMessageEvent):
        """
        每日仅可占卜一次：
        - 扣 20 玻璃珠占卜费（仅在今日首次占卜时扣）
        - 抽 22 大阿卡那（正/逆）
        - 展示牌面等级（SSS/SS/S/B/C/D/F）与中文形容词
        - 好牌给祝福、坏牌给安慰；玻璃珠变动受牌面影响（±266 封顶）
        - SSS 牌 10% 中奖 +999 玻璃珠
        - 好感度 +0~50，与牌面无关
        """
        user_name = event.get_sender_name()
        user_id = self._get_user_id(event)
        user = self._state["users"].setdefault(user_id, {"favor": 0, "marbles": 0})

        today = datetime.now().date().isoformat()
        if user.get("last_divine") == today:
            # 今日已占卜，直接提示冷却；不扣费不改数值
            yield event.plain_result(
                f"🔒 {user_name}，今天已经占卜过啦～明天再来试试命运之轮吧！\n"
                f"📦 当前背包｜好感度：{user.get('favor',0)}｜玻璃珠：{user.get('marbles',0)}"
            )
            return

        # -- 首次占卜：扣占卜费 --
        fee = 20
        user["marbles"] = user.get("marbles", 0) - fee

        # -- 随机牌面 --
        cards = self._get_arcana_data()
        card_name = random.choice(list(cards.keys()))
        upright = random.choice([True, False])
        orient = "upright" if upright else "reversed"
        m = cards[card_name][orient]  # dict: core/type/keywords/interp
        orient_cn = "正位" if upright else "逆位"

        # -- 牌面等级与玻璃珠变化 --
        rating = m["type"]  # SSS/SS/S/B/C/D/F
        ranges = self._get_marble_range()
        rmin, rmax = ranges[rating]
        marble_delta = random.randint(rmin, rmax)
        marble_delta = max(-266, min(266, marble_delta))  # clip 到 ±266

        # -- 好感度独立增长 --
        favor_inc = random.randint(0, 50)

        # -- 特别棒（SSS）10% 中奖 +999 --
        bonus = 0
        bonus_text = ""
        if rating == "SSS" and random.random() < 0.10:
            bonus = 999
            bonus_text = "\n🎉 中奖时刻！群星垂青，额外获得 **999** 颗玻璃珠！"

        # -- 祝福/安慰语 --
        bucket = self._rating_bucket(rating)  # 'good' | 'swing' | 'bad'
        mood_line = self._bless_or_comfort(bucket)

        # -- 更新数据并标记今日已占卜 --
        user["favor"] = user.get("favor", 0) + favor_inc
        user["marbles"] = user.get("marbles", 0) + marble_delta + bonus
        user["last_divine"] = today
        self._save_state()

        # -- 展示 --
        def fmt_signed(n: int) -> str:
            return f"+{n}" if n >= 0 else f"{n}"

        rating_word = self._get_rating_word()[rating]  # 例如 “特别棒的”
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

        def _rating_bucket(self, rating: str) -> str:
        """
        把七档等级映射为三种语气：
        - good: SSS/SS/S
        - swing: B（有波动）
        - bad: C/D/F
        """
        if rating in ("SSS", "SS", "S"):
            return "good"
        if rating == "B":
            return "swing"
        return "bad"

    def _bless_or_comfort(self, bucket: str) -> str:
        """根据档位给祝福/安慰/建议文案（随机取一句）"""
        if bucket == "good":
            pool = [
                "🕊️ 祝福送达：顺风顺水、步步开花！",
                "🌟 愿你保持清澈与专注，好运与成果相互奔赴。",
                "🚀 保持节奏与信心，今天的舞台灯正亮着。",
                "💫 把灵感落地成行动，宇宙会给出回应。",
            ]
        elif bucket == "swing":
            pool = [
                "🌗 提醒：形势有波动，收束变量、稳步推进。",
                "🧭 先把小目标拿下，趋势自然会转向你。",
                "⚖️ 管住节奏与边界，少量正确比大量盲冲更强。",
            ]
        else:  # bad
            pool = [
                "🫧 别怕，今天先把自己安顿好，路会在脚下重新出现。",
                "🌧️ 暂避锋芒也算前进，先修复能量再出发。",
                "🛡️ 把风险写出来就降级一半，慢慢来，一切都会过去。",
            ]
        return random.choice(pool)



    # ====== 以下是占卜数据的延迟加载方法们 ======

    def _get_rating_word(self):
        return {
            "SSS": "特别棒的",
            "SS": "很好的",
            "S": "不错的",
            "B": "有波动的",
            "C": "不太顺的",
            "D": "糟心的",
            "F": "相当危险的",
        }

    def _get_marble_range(self):
        return {
            "SSS": (200, 266),
            "SS": (120, 220),
            "S": (40, 160),
            "B": (-60, 120),
            "C": (-160, 40),
            "D": (-220, -40),
            "F": (-266, -120),
        }

    def _get_arcana_data(self):
        """返回22张大阿卡那及正逆含义"""
        return {
            "愚者": {
                "upright": {"core": "自由", "type": "SS", "keywords": ["起点","冒险","单纯","信任","未知","旅途"], "interp": "拥抱未知，轻装上路会带来新鲜突破。"},
                "reversed": {"core": "鲁莽", "type": "C", "keywords": ["冲动","迷路","逃避","风险","幼稚","分心"], "interp": "先看脚下再跳，边界与计划缺一不可。"},
            },
            "魔术师": {
                "upright": {"core": "创造", "type": "SSS", "keywords": ["专注","沟通","资源","技巧","显化","机会"], "interp": "心之所向可被实现，主动出手就是魔法。"},
                "reversed": {"core": "失衡", "type": "D", "keywords": ["欺骗","分神","虚张","失控","散漫","反复"], "interp": "谨防口惠而实不至，把能量收束回到行动。"},
            },
            "女祭司": {
                "upright": {"core": "直觉", "type": "S", "keywords": ["潜意识","静观","神秘","梦境","洞察","沉默"], "interp": "答案在心底，给直觉一点安静的空间。"},
                "reversed": {"core": "压抑", "type": "C", "keywords": ["怀疑","迟疑","隔阂","隐瞒","自我否定","迷雾"], "interp": "过度压抑会遮蔽线索，承认感受即是起点。"},
            },
            "女皇": {
            "upright": {"core": "丰盛", "type": "SS",  "keywords": ["滋养","艺术","美感","安全","享受","生长"], "interp": "宽松与滋养让事物自然成熟。"},
            "reversed":{"core": "滞养", "type": "C",   "keywords": ["懒散","依赖","过度","窒息","空虚","拖延"], "interp": "爱与边界并重，别用纵容替代成长。"},
            },
           "皇帝": {
            "upright": {"core": "秩序", "type": "SS",  "keywords": ["结构","权威","规则","担当","稳固","治理"], "interp": "立规矩、定节奏，力量在于可持续的秩序。"},
            "reversed":{"core": "强控", "type": "D",   "keywords": ["僵化","独断","控制","硬碰","压制","冷硬"], "interp": "别让控制欲反噬结果，学会授权与倾听。"},
            },
           "教皇": {
            "upright": {"core": "传承", "type": "S",   "keywords": ["规范","学习","导师","体系","礼仪","社群"], "interp": "回到传统或向导师求助，走正道事半功倍。"},
            "reversed":{"core": "僵套", "type": "C",   "keywords": ["形式","教条","束缚","盲从","评判","停滞"], "interp": "打破过时规范，保留核心精神即可。"},
            },
           "恋人": {
            "upright": {"core": "选择", "type": "SS",  "keywords": ["连接","价值","吸引","坦诚","契合","合一"], "interp": "出于价值一致的选择，会让关系与项目共振。"},
            "reversed":{"core": "分岔", "type": "D",   "keywords": ["犹豫","错配","逃避","摇摆","分裂","矛盾"], "interp": "先对齐自我价值，再谈承诺与合作。"},
            },
           "战车": {
            "upright": {"core": "掌控", "type": "SS",  "keywords": ["推进","胜利","纪律","意志","速度","聚焦"], "interp": "握紧缰绳直面阻力，胜利来自持续推进。"},
            "reversed":{"core": "失控", "type": "D",   "keywords": ["偏航","内耗","拖延","分散","冲撞","放纵"], "interp": "收窄目标，先稳住方向再提速。"},
            },
           "力量": {
            "upright": {"core": "勇毅", "type": "SS",  "keywords": ["温柔","自律","驯服","耐心","治愈","自信"], "interp": "以温柔而坚定之力，化解粗暴的对抗。"},
            "reversed":{"core": "脆弱", "type": "C",   "keywords": ["自卑","急躁","压抑","失衡","逃避","怯场"], "interp": "照看脆弱面，练习稳定而非强撑。"},
            },
           "隐者": {
            "upright": {"core": "独省", "type": "S",   "keywords": ["内观","独处","导师","灯塔","专研","简化"], "interp": "退一步看全局，答案在寂静里亮起。"},
            "reversed":{"core": "闭塞", "type": "C",   "keywords": ["孤立","躲避","空转","迟缓","拒绝","狭隘"], "interp": "别把独处变成逃避，适度连结会解锁路径。"},
            },
           "命运之轮": {
            "upright": {"core": "转机", "type": "SS",  "keywords": ["周期","机缘","上升","变化","同步","幸运"], "interp": "顺势而为，抓住轮转中的上升窗口。"},
            "reversed":{"core": "逆风", "type": "B",   "keywords": ["延迟","反复","卡点","外因","停滞","错过"], "interp": "承认周期低谷，调整节奏等风向。"},
            },
           "正义": {
            "upright": {"core": "公正", "type": "S",   "keywords": ["因果","平衡","契约","选择","透明","责任"], "interp": "以事实与原则决断，你会获得清明的结果。"},
            "reversed":{"core": "失衡", "type": "C",   "keywords": ["偏颇","不公","拖延","误判","隐情","反噬"], "interp": "补充证据与视角，避免情绪化裁决。"},
            },
           "倒吊人": {
            "upright": {"core": "悬思", "type": "S",   "keywords": ["暂停","换位","牺牲","洞见","重置","等待"], "interp": "短暂停顿换来视角跃迁。"},
            "reversed":{"core": "僵滞", "type": "C",   "keywords": ["拖延","停摆","怨怼","固执","内耗","错位"], "interp": "把‘等’变成‘选’，主动定义牺牲的意义。"},
            },
           "死神": {
            "upright": {"core": "更迭", "type": "SS",  "keywords": ["终结","更新","断舍","再生","替换","清理"], "interp": "果断收尾为新生腾位。"},
            "reversed":{"core": "拒变", "type": "D",   "keywords": ["拖延","回头","依恋","冗余","旧习","惧怕"], "interp": "停止无效维持，给变化让路。"},
            },
            "节制": {
            "upright": {"core": "调和", "type": "SS",  "keywords": ["节律","配比","耐心","整合","中道","疗愈"], "interp": "在流动中寻均衡，小步慢跑更长久。"},
            "reversed":{"core": "失调", "type": "B",   "keywords": ["过度","失衡","忽冷忽热","碎片","焦躁","溢出"], "interp": "收束变量，回到可持续的节律。"},
            },
           "恶魔": {
            "upright": {"core": "欲念", "type": "B",   "keywords": ["绑定","诱惑","执念","物欲","依赖","影子"], "interp": "看见枷锁就能松开一环，自由从自知开始。"},
            "reversed":{"core": "解脱", "type": "S",   "keywords": ["觉醒","松绑","复元","止损","断链","净化"], "interp": "认清代价后抽身即自由。"},
            },
           "塔": {
            "upright": {"core": "崩解", "type": "F",   "keywords": ["突变","瓦解","震荡","清算","暴露","冲击"], "interp": "虚假结构会倒塌，但废墟里藏着蓝图。"},
            "reversed":{"core": "余震", "type": "D",   "keywords": ["拖延崩塌","否认","裂缝","补漏","侥幸","反复"], "interp": "与其补裂缝不如重构地基。"},
            },
           "星星": {
            "upright": {"core": "希望", "type": "SSS", "keywords": ["灵感","疗愈","宁静","远景","指引","信念"], "interp": "保持清澈与耐心，愿景会被星光照亮。"},
            "reversed":{"core": "失望", "type": "C",   "keywords": ["怀疑","黯淡","迟疑","能量低","灰心","散失"], "interp": "先修复自我，再点亮小目标重拾光感。"},
            },
           "月亮": {
            "upright": {"core": "潜影", "type": "B",   "keywords": ["直觉","不安","幻象","循环","想象","夜行"], "interp": "穿过情绪的潮汐，别急着下结论。"},
            "reversed":{"core": "澄清", "type": "S",   "keywords": ["解谜","真相","落地","收束","排雷","整理"], "interp": "迷雾散开，事实比恐惧更温和。"},
            },
           "太阳": {
            "upright": {"core": "喜悦", "type": "SSS", "keywords": ["成功","童真","能量","清晰","庆祝","丰收"], "interp": "全速前进，舞台灯正亮着。"},
            "reversed":{"core": "过曝", "type": "B",   "keywords": ["浮夸","急躁","骄矜","热度降","注意力","偏差"], "interp": "把热情落地到可验证的成果。"},
            },
           "审判": {
            "upright": {"core": "觉醒", "type": "SS",  "keywords": ["召回","复盘","重启","赎回","抉择","复活"], "interp": "回应内在召唤，一锤定音。"},
            "reversed":{"core": "犹疑", "type": "C",   "keywords": ["拖延","错过","逃避","自责","反刍","滞后"], "interp": "停止自我审判，把行动交给现在。"},
            },
           "世界": {
            "upright": {"core": "完成", "type": "SS",  "keywords": ["闭环","整合","里程","里程碑","联结","自由行"], "interp": "阶段性圆满，准备迎接新的层级。"},
            "reversed":{"core": "未竟", "type": "B",   "keywords": ["差一步","拼图缺","拖尾","松散","跳级","循环"], "interp": "把尾巴收好，再开启下一段航程。"},
            },
        }


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        self._save_state()
