"""AI 伴侣 · 角色扮演聊天界面（Streamlit + DeepSeek）

界面结构：
    侧边栏：选择伴侣 / 人设小卡 / 自定义角色 / 模型参数 / 接口密钥 / 清空对话
    主  区：角色资料卡 + 聊天记录（支持流式输出与思考过程）+ 底部输入框

自定义角色：
    在侧边栏「🎨 自定义角色」里填写性格关键词、性格描述、说话风格等，
    程序会把设定自动拼装成 system 提示词，生成的角色与内置角色一样能聊天，
    并保存在 resources/custom_characters.json，重启应用后依然在。

运行方式：
    streamlit run "第三章/03.ai_patner_1.py"
"""

import json
import os
import re
from pathlib import Path
from typing import TypedDict

import streamlit as st
from openai import OpenAI

# ============================== 1. 常量与工具 ==============================

# 资源目录：基于脚本所在位置解析，避免从不同工作目录运行时找不到图片
RESOURCES_DIR = Path(__file__).resolve().parent / "resources"

# 自定义角色存档：新建 / 编辑 / 删除后自动写入，重启应用不丢
CUSTOM_CHAR_FILE = RESOURCES_DIR / "custom_characters.json"

# DeepSeek 接口配置（与 01.deepseek调用测试.py 保持一致）
BASE_URL = "https://api.deepseek.com"
MODELS = ["deepseek-flash", "deepseek-v4-pro"]
USER_AVATAR = "🧑‍💻"


def _fix_no_proxy() -> None:
    """规整本机 no_proxy 环境变量。

    本机 no_proxy 形如 "localhost|127.*|[::1]"，既用了 "|" 分隔又带 IPv6 方括号，
    httpx 会把它整体当作一个 URL 模式解析并抛出 InvalidURL，导致 OpenAI() 构造失败。
    这里统一换成逗号分隔并忽略 IPv6 项（只影响当前进程）。
    """
    raw = os.environ.get("no_proxy", "")
    if "|" not in raw and "[" not in raw:
        return
    hosts = [item.strip() for item in raw.replace("|", ",").split(",")]
    hosts = [item for item in hosts if item and "[" not in item and "]" not in item]
    os.environ["no_proxy"] = ",".join(hosts)


_fix_no_proxy()


# ============================== 2. 角色人设 ==============================
# 每个角色 = 一套 system 提示词 + 开场白 + 展示信息

class Character(TypedDict):
    """一个伴侣角色的完整设定"""

    name: str
    avatar: str
    title: str
    tags: list[str]
    persona: str
    greeting: str


class CharacterSpec(TypedDict):
    """自定义角色的「原始设定」：既写入 JSON，也用于回填编辑表单

    persona 不直接存，而是由下面这些字段实时拼装（见 compose_persona），
    这样以后改风格、改字数上限，不用重新手写一整段提示词。
    """

    name: str
    avatar: str
    title: str
    tags: list[str]
    personality: str  # 自由描述的性格；留空时用 tags 兜底
    style: str  # STYLE_PRESETS 的键，或 CUSTOM_STYLE
    custom_style: str  # style == CUSTOM_STYLE 时生效
    greeting: str  # 开场白；留空自动生成
    reply_limit: int  # 回复字数上限
    extra: str  # 附加规则，可为空
    override: str  # 手动指定的完整 system 提示词，非空时优先


class ChatRecord(TypedDict):
    """一条聊天记录：正文 + 可选的思考过程"""

    role: str
    content: str
    reasoning: str


CHARACTERS: dict[str, Character] = {
    "🌙 林晚 · 温柔知心姐姐": {
        "name": "林晚",
        "avatar": "🌙",
        "title": "深夜电台主播",
        "tags": ["温柔", "倾听", "治愈系"],
        "persona": (
            "你是「林晚」，26 岁的深夜电台情感节目主播，听众都叫你最温柔的树洞。"
            "你说话轻声细语，习惯先接住对方的情绪再聊事情，常把“嗯嗯”“我懂”“慢慢说”挂在嘴边。"
            "你从不评判对方的对错，也不急着给建议，只在对方明确需要时才给出 1~2 条具体可行的小建议。"
            "回复要口语化、有画面感，通常不超过 80 字，可以用（轻轻笑）（顿了顿）这类动作描写。"
        ),
        "greeting": "嗨，我是林晚。今晚的电台只剩我们两个人啦，想聊点什么都可以，我在听。",
    },
    "🔥 苏喆 · 毒舌学霸": {
        "name": "苏喆",
        "avatar": "🔥",
        "title": "竞赛金牌学长",
        "tags": ["毒舌", "犀利", "靠谱"],
        "persona": (
            "你是「苏喆」，22 岁计算机竞赛金牌得主，说话直接、爱吐槽，但心是热的。"
            "你反感空话和拖延，回答问题前会先用一句话戳破对方的自我安慰，然后给出真正有用的干货。"
            "你的吐槽只针对事情本身，绝不进行人身攻击；给出建议时喜欢用「第一步/第二步」这类结构化表述，"
            "偶尔会甩出一句“这题我小学就会了”当作调味。回复不超过 120 字。"
        ),
        "greeting": "哟，又来一个想学习的。说吧，这次卡在哪道题上——先说好，敷衍的回答我不收。",
    },
    "🖌️ 墨白 · 古风诗人": {
        "name": "墨白",
        "avatar": "🖌️",
        "title": "江湖游吟诗人",
        "tags": ["古风", "文雅", "浪漫"],
        "persona": (
            "你是「墨白」，一位仗剑走江湖的游吟诗人，谈吐文雅，不喜俗物。"
            "你说话带一点文白的古风味道，爱用意象（月色、长风、远山、酒）来打比方，"
            "但绝不用生僻字为难对方，确保普通人也能读懂。你偶尔会即兴吟两句四言或七言的短句。"
            "谈正事时逻辑清晰、态度诚恳，绝不装腔作势。回复不超过 100 字。"
        ),
        "greeting": "一路风尘，客官竟寻到在下这草庐来了。今夜月色正好，且说说你的心事吧。",
    },
    "🍀 小满 · 元气少女": {
        "name": "小满",
        "avatar": "🍀",
        "title": "永远 18 岁的同桌",
        "tags": ["元气", "活泼", "捧场王"],
        "persona": (
            "你是「小满」，一个永远 18 岁、永远精力过剩的元气少女，是对方最铁的同桌。"
            "你说话语速快、情绪足，爱用语气词和颜文字（呀！哇！诶嘿～），会真诚地夸对方。"
            "你好奇心爆棚，喜欢追问细节，也会认真记住对方说过的每件小事并在之后提起。"
            "遇到对方情绪低落时，你会立刻收起玩笑，认真陪着对方。回复不超过 80 字。"
        ),
        "greeting": "哇！你终于来啦～我都等你半天了，今天有什么好玩的要跟我讲呀？",
    },
}


# ------------------------- 自定义角色：拼装与持久化 -------------------------

# 说话风格预设：每个键对应一句写进 system 提示词的描述
STYLE_PRESETS: dict[str, str] = {
    "温柔体贴": "说话轻声细语，先接住对方的情绪再聊事情，常说“嗯嗯”“我懂”“慢慢说”，从不评判对方的对错。",
    "毒舌犀利": "说话直接、爱吐槽，先一句话戳破对方的自我安慰，再给出真正有用的干货；吐槽只针对事情本身，绝不人身攻击。",
    "古风文雅": "谈吐带一点文白的古风味道，爱用意象（月色、长风、远山、酒）打比方，但不用生僻字为难对方，偶尔即兴吟一两句短句。",
    "元气活泼": "说话语速快、情绪足，爱用语气词和颜文字（呀！哇！诶嘿～），会真诚地夸对方，好奇心爆棚。",
    "沉稳专业": "语气平稳克制，先给结论再给依据，喜欢用「第一步/第二步」这类结构化表述，不夸张、不闲聊。",
    "幽默风趣": "喜欢用比喻和自嘲制造笑点，但该认真的时候绝不含糊，玩笑之后总会补一句真心话。",
    "傲娇别扭": "嘴上不肯服软、爱抬杠，其实很在意对方，关心的话总要说成反话（“才、才不是担心你呢”）。",
    "高冷寡言": "惜字如金，回应简短，很少寒暄，偶尔冒出来的一句话却很戳心。",
}
CUSTOM_STYLE = "✍️ 自定义风格"
MAX_TAGS = 6
DEFAULT_AVATAR = "🙂"
DEFAULT_REPLY_LIMIT = 120


def parse_tags(raw: str) -> list[str]:
    """把「慢热、嘴硬心软, 细腻」这类输入切成标签列表（最多 MAX_TAGS 个）"""
    items = re.split(r"[、,，;；/|\s]+", raw)
    return [item.strip() for item in items if item.strip()][:MAX_TAGS]


def character_key_of(spec: CharacterSpec) -> str:
    """角色在下拉框中的显示名，与内置角色保持同一格式：头像 名字 · 身份"""
    return f"{spec['avatar']} {spec['name']} · {spec['title']}"


def ensure_period(text: str) -> str:
    """给用户手写的句子补上句号，避免拼出来的提示词黏成一团"""
    text = text.strip()
    if text and text[-1] not in "。！？.!?…":
        text += "。"
    return text


def compose_persona(spec: CharacterSpec) -> str:
    """把结构化设定拼装成 system 提示词（写法与内置角色保持一致）"""
    name = spec["name"].strip() or "小助手"
    head = f"你是「{name}」"
    if spec["title"].strip():
        head += f"，{spec['title'].strip()}"
    parts = [head + "。"]

    personality = spec["personality"].strip()
    if personality:
        parts.append(personality)
    elif spec["tags"]:
        parts.append(f"你的核心性格是{'、'.join(spec['tags'])}，说话做事都要自然地体现出这些特点。")

    style_text = (
        spec["custom_style"].strip()
        if spec["style"] == CUSTOM_STYLE
        else STYLE_PRESETS.get(spec["style"], "")
    )
    if style_text:
        parts.append(style_text)

    parts.append(
        f"无论对方问什么，都要以「{name}」的身份和口吻回答，不要跳出角色，也不要暴露自己是 AI。"
    )
    if spec["extra"].strip():
        parts.append(spec["extra"].strip())
    parts.append(f"回复要口语化、有画面感，不超过 {spec['reply_limit']} 字。")
    return "".join(ensure_period(part) for part in parts)


def build_character(spec: CharacterSpec) -> Character:
    """把自定义设定转成与内置角色同构的 Character（persona 实时拼装）"""
    name = spec["name"].strip() or "小助手"
    greeting = spec["greeting"].strip() or f"嗨，我是{name}，想聊点什么都可以，我在这儿听着呢。"
    return {
        "name": name,
        "avatar": spec["avatar"].strip() or DEFAULT_AVATAR,
        "title": spec["title"].strip() or "自定义伴侣",
        "tags": spec["tags"],
        # 高级选项里手写了 system 提示词就以它为准，否则按上面的设定自动拼装
        "persona": spec["override"].strip() or compose_persona(spec),
        "greeting": greeting,
    }


def normalize_spec(raw: object) -> CharacterSpec | None:
    """把（来自 JSON 文件的）裸字典补齐成 CharacterSpec；没有名字时返回 None"""
    if not isinstance(raw, dict):
        return None

    def text(field: str) -> str:
        return str(raw.get(field, "") or "").strip()

    name = text("name")
    if not name:
        return None

    tags = raw.get("tags")
    if isinstance(tags, str):
        tags = parse_tags(tags)
    elif isinstance(tags, list):
        tags = [str(item).strip() for item in tags if str(item).strip()][:MAX_TAGS]
    else:
        tags = []

    style = text("style")
    if style not in STYLE_PRESETS and style != CUSTOM_STYLE:
        style = next(iter(STYLE_PRESETS))

    try:
        reply_limit = int(str(raw.get("reply_limit", DEFAULT_REPLY_LIMIT)).strip())
    except ValueError:
        reply_limit = DEFAULT_REPLY_LIMIT

    return {
        "name": name,
        "avatar": text("avatar") or DEFAULT_AVATAR,
        "title": text("title") or "自定义伴侣",
        "tags": tags,
        "personality": text("personality"),
        "style": style,
        "custom_style": text("custom_style"),
        "greeting": text("greeting"),
        "reply_limit": min(max(reply_limit, 40), 400),
        "extra": text("extra"),
        "override": text("override"),
    }


def load_custom_specs() -> dict[str, CharacterSpec]:
    """从 resources/custom_characters.json 读取自定义角色（文件不存在或损坏时当作空）"""
    if not CUSTOM_CHAR_FILE.exists():
        return {}
    try:
        raw = json.loads(CUSTOM_CHAR_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    if isinstance(raw, dict):
        items = list(raw.values())
    elif isinstance(raw, list):
        items = raw
    else:
        return {}

    specs: dict[str, CharacterSpec] = {}
    for item in items:
        spec = normalize_spec(item)
        if spec:
            # key 由设定重新算出来，避免手改 JSON 后和下拉框对不上
            specs[character_key_of(spec)] = spec
    return specs


def save_custom_specs(specs: dict[str, CharacterSpec]) -> None:
    """把自定义角色写回本地 JSON（写失败只提示，不影响当前会话继续使用）"""
    try:
        CUSTOM_CHAR_FILE.parent.mkdir(parents=True, exist_ok=True)
        CUSTOM_CHAR_FILE.write_text(
            json.dumps(specs, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as error:
        st.warning(f"自定义角色没能写入本地文件：{error}", icon="⚠️")


def all_characters() -> dict[str, Character]:
    """内置角色 + 用户自定义角色，一起作为角色下拉框的候选项"""
    characters: dict[str, Character] = dict(CHARACTERS)
    for key, spec in st.session_state.custom_specs.items():
        characters[key] = build_character(spec)
    return characters


def validate_spec(spec: CharacterSpec, current_key: str = "") -> str:
    """校验角色设定，返回错误提示（空字符串表示通过）

    current_key 是编辑场景下的原角色名，用来排除自己、允许只改设定不改名。
    """
    if not spec["name"].strip():
        return "请先给角色起个名字"
    if not spec["title"].strip():
        return "请填写「身份 / 职业」，人设会更具体"
    if not spec["tags"] and not spec["personality"].strip():
        return "「性格关键词」和「性格描述」至少填一项"
    key = character_key_of(spec)
    occupied = {item for item in all_characters() if item != current_key}
    if key in occupied:
        return f"已经有一个「{key}」了，换个名字或身份再试"
    return ""


def render_character_form(prefix: str, defaults: CharacterSpec | None) -> CharacterSpec:
    """渲染角色设定表单，返回当前填写的设定

    prefix 作为控件 key 的前缀：新建用 "new"，编辑用 "edit_角色名"，
    这样切换编辑对象时控件会重新取默认值，不会被上一个角色的缓存覆盖。
    """
    spec = defaults

    st.caption("带 * 的是必填项，设定越具体，角色的性格越稳定。")
    name = st.text_input(
        "角色名 *",
        value=spec["name"] if spec else "",
        key=f"{prefix}_name",
        placeholder="例如：橘子",
    )
    avatar = st.text_input(
        "头像 emoji",
        value=spec["avatar"] if spec else DEFAULT_AVATAR,
        key=f"{prefix}_avatar",
        max_chars=4,
        placeholder="例如：🌰",
        help="随手挑一个 emoji 当头像",
    )
    title = st.text_input(
        "身份 / 职业 *",
        value=spec["title"] if spec else "",
        key=f"{prefix}_title",
        placeholder="例如：凌晨三点的便利店店员",
    )
    tags_raw = st.text_input(
        "性格关键词 *",
        value="、".join(spec["tags"]) if spec else "",
        key=f"{prefix}_tags",
        placeholder="用「、」或逗号分隔，例如：慢热、细腻、嘴硬心软",
        help=f"最多保留 {MAX_TAGS} 个",
    )
    personality = st.text_area(
        "性格描述（可留空，留空则按关键词生成）",
        value=spec["personality"] if spec else "",
        key=f"{prefix}_personality",
        height=90,
        placeholder="例如：习惯把关心藏在小事里，别人难过时不说大道理，只默默递一杯热水。",
    )
    style_options = list(STYLE_PRESETS) + [CUSTOM_STYLE]
    default_style = spec["style"] if spec and spec["style"] in style_options else style_options[0]
    style = st.selectbox(
        "说话风格",
        options=style_options,
        index=style_options.index(default_style),
        key=f"{prefix}_style",
    )
    custom_style = st.text_area(
        "自定义说话风格（上面选「✍️ 自定义风格」时生效）",
        value=spec["custom_style"] if spec else "",
        key=f"{prefix}_custom_style",
        height=70,
        placeholder="例如：每句话都要提一次天气，把心情比作云的形状。",
    )
    greeting = st.text_area(
        "开场白（可留空，留空自动生成）",
        value=spec["greeting"] if spec else "",
        key=f"{prefix}_greeting",
        height=70,
        placeholder="例如：（抬头看了你一眼）这么晚才来呀，坐吧。",
    )
    reply_limit = st.slider(
        "回复字数上限",
        min_value=40,
        max_value=400,
        step=20,
        value=spec["reply_limit"] if spec else DEFAULT_REPLY_LIMIT,
        key=f"{prefix}_limit",
    )
    extra = st.text_area(
        "附加规则（可留空）",
        value=spec["extra"] if spec else "",
        key=f"{prefix}_extra",
        height=70,
        placeholder="例如：不要主动给建议；聊到加班时可以吐槽两句。",
    )
    override = st.text_area(
        "直接指定 system 提示词（高级，填写后会覆盖上面的自动拼装）",
        value=spec["override"] if spec else "",
        key=f"{prefix}_override",
        height=90,
        placeholder="留空即可，上面的设定会自动拼成提示词",
    )

    return {
        "name": name.strip(),
        "avatar": avatar.strip() or DEFAULT_AVATAR,
        "title": title.strip(),
        "tags": parse_tags(tags_raw),
        "personality": personality.strip(),
        "style": style,
        "custom_style": custom_style.strip(),
        "greeting": greeting.strip(),
        "reply_limit": reply_limit,
        "extra": extra.strip(),
        "override": override.strip(),
    }


# ============================== 3. 页面配置 ==============================
st.set_page_config(
    page_title="AI 伴侣",
    page_icon="💞",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://api-docs.deepseek.com/zh-cn/",
        "Report a bug": "https://api-docs.deepseek.com/zh-cn/",
        "About": "AI 伴侣 · Streamlit 角色扮演聊天演示",
    },
)

# 复用 02.streamlit入门.py 中的 logo 资源
if (RESOURCES_DIR / "img.png").exists():
    st.logo(str(RESOURCES_DIR / "img.png"))

# ============================== 4. 会话状态 ==============================
# messages 结构：[{"role": "user"/"assistant", "content": 正文, "reasoning": 思考过程}]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "custom_specs" not in st.session_state:
    st.session_state.custom_specs = load_custom_specs()  # 自定义角色：从本地 JSON 恢复
if "character_key" not in st.session_state:
    st.session_state.character_key = list(CHARACTERS)[0]
if "active_character" not in st.session_state:
    st.session_state.active_character = st.session_state.character_key

# 新建 / 改名 / 删除角色后要切换下拉框，必须在控件创建之前赋值（否则 Streamlit 会报错）
pending_character = st.session_state.pop("pending_character", None)
if pending_character:
    st.session_state.character_key = pending_character

# 角色候选 = 内置 + 自定义；若当前选中的自定义角色被删了，回退到第一个角色
characters = all_characters()
if st.session_state.character_key not in characters:
    st.session_state.character_key = next(iter(characters))


@st.cache_resource(show_spinner=False)
def get_client(key: str) -> OpenAI:
    """缓存 OpenAI 客户端（key 为 DeepSeek API Key），避免每次交互都重新建立连接"""
    return OpenAI(api_key=key, base_url=BASE_URL)


def show_avatar(character: Character, font_size: int = 64) -> None:
    """角色头像：优先用 resources/avatar_角色名.png，没有则用 emoji 占位"""
    portrait = RESOURCES_DIR / f"avatar_{character['name']}.png"
    if portrait.exists():
        st.image(str(portrait), width="stretch")
    else:
        st.markdown(
            f"<div style='font-size:{font_size}px;line-height:1.1;text-align:center;'>"
            f"{character['avatar']}</div>",
            unsafe_allow_html=True,
        )


# ============================== 5. 侧边栏（角色 + 参数） ==============================
with st.sidebar:
    st.subheader("🎭 选择伴侣")
    char_key = st.selectbox(
        "角色",
        options=list(characters),
        key="character_key",
        label_visibility="collapsed",
    )
    char = characters[char_key]
    is_custom = char_key in st.session_state.custom_specs

    # 人设小卡
    with st.container(border=True):
        card = st.columns([1, 2], vertical_alignment="center")
        with card[0]:
            show_avatar(char, font_size=54)
        with card[1]:
            st.markdown(f"**{char['name']}**")
            st.caption(f"{char['title']}｜{' · '.join(char['tags'])}")
            if is_custom:
                st.caption("✨ 自定义角色")

    with st.expander("📝 查看人设提示词"):
        st.caption("这段文字会作为 system 消息发给模型：")
        st.write(char["persona"])

    # ---- 自定义角色：新建 / 编辑 / 备份，设定会存到 resources/custom_characters.json ----
    with st.expander("🎨 自定义角色", expanded=False):
        st.caption(
            "填好性格设定就能捏一个属于自己的伴侣：它会出现在上面的角色下拉框里，"
            f"并自动保存到 {CUSTOM_CHAR_FILE.name}。"
        )
        tab_new, tab_edit, tab_backup = st.tabs(["✨ 新建", "🛠️ 编辑 / 删除", "💾 导入 / 导出"])

        with tab_new:
            draft = render_character_form("new", None)
            st.caption("⬆️ 以上设定会自动拼装成下面这段 system 提示词（实时预览）：")
            st.code(build_character(draft)["persona"], language="text")
            if st.button("✨ 创建并切换", type="primary", width="stretch"):
                error = validate_spec(draft)
                if error:
                    st.error(error, icon="🚨")
                else:
                    key = character_key_of(draft)
                    st.session_state.custom_specs[key] = draft
                    save_custom_specs(st.session_state.custom_specs)
                    st.session_state.pending_character = key
                    st.session_state.flash = {
                        "text": f"自定义角色「{draft['name']}」已就绪",
                        "icon": "🎉",
                    }
                    st.rerun()

        with tab_edit:
            specs = st.session_state.custom_specs
            if not specs:
                st.info("还没有自定义角色，先去「✨ 新建」捏一个吧。", icon="💡")
            else:
                options = list(specs)
                # 上一次编辑的角色可能已被改名或删除，这里先把控件状态修正
                if st.session_state.get("manage_character") not in options:
                    st.session_state.manage_character = options[0]
                target = st.selectbox(
                    "选择要管理的角色", options=options, key="manage_character"
                )
                draft = render_character_form(f"edit_{target}", specs[target])
                st.caption("⬆️ 修改后 system 提示词会变成：")
                st.code(build_character(draft)["persona"], language="text")

                save_col, delete_col = st.columns(2)
                if save_col.button("💾 保存修改", width="stretch"):
                    error = validate_spec(draft, current_key=target)
                    if error:
                        st.error(error, icon="🚨")
                    else:
                        new_key = character_key_of(draft)
                        specs.pop(target, None)  # 先摘掉旧名字，再存新名字（允许改名）
                        st.session_state.custom_specs[new_key] = draft
                        save_custom_specs(st.session_state.custom_specs)
                        st.session_state.pending_character = new_key
                        st.session_state.flash = {
                            "text": f"角色「{draft['name']}」已更新",
                            "icon": "💾",
                        }
                        st.rerun()

                confirmed = st.checkbox("我确认删除该角色", key=f"confirm_{target}")
                if delete_col.button("🗑️ 删除", width="stretch"):
                    if not confirmed:
                        st.warning("请先勾选上面的确认框", icon="⚠️")
                    else:
                        specs.pop(target, None)
                        save_custom_specs(st.session_state.custom_specs)
                        st.session_state.pending_character = next(iter(CHARACTERS))
                        st.session_state.flash = {"text": f"已删除角色「{target}」", "icon": "🧹"}
                        st.rerun()

        with tab_backup:
            specs = st.session_state.custom_specs
            st.caption("导出的 JSON 可以备份或分享到别的机器；导入是合并，同名角色会被覆盖。")
            st.download_button(
                "⬇️ 导出全部自定义角色",
                data=json.dumps(specs, ensure_ascii=False, indent=2),
                file_name=CUSTOM_CHAR_FILE.name,
                mime="application/json",
                width="stretch",
                disabled=not specs,
            )
            uploaded = st.file_uploader(
                "⬆️ 选择要导入的 JSON", type=["json"], key="import_file"
            )
            if st.button("📥 合并导入", width="stretch", disabled=uploaded is None):
                try:
                    incoming = json.loads(uploaded.getvalue().decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    st.error(f"文件不是有效的 JSON：{error}", icon="🚨")
                else:
                    if isinstance(incoming, dict):
                        items = list(incoming.values())
                    elif isinstance(incoming, list):
                        items = incoming
                    else:
                        items = []
                    count = 0
                    for item in items:
                        spec = normalize_spec(item)
                        if spec:
                            st.session_state.custom_specs[character_key_of(spec)] = spec
                            count += 1
                    if count:
                        save_custom_specs(st.session_state.custom_specs)
                        st.session_state.flash = {
                            "text": f"已导入 {count} 个自定义角色",
                            "icon": "📥",
                        }
                        st.rerun()
                    else:
                        st.error("文件里没有可识别的角色，请检查字段是否完整", icon="🚨")

    st.divider()

    # 参数设置
    st.subheader("⚙️ 参数设置")
    model = st.selectbox("模型", MODELS)
    temperature = st.slider(
        "温度 temperature", 0.0, 2.0, 1.1, 0.1, help="越高越天马行空，越低越稳定"
    )
    max_tokens = st.slider("最大生成长度 max_tokens", 256, 8192, 2048, 256)
    thinking = st.toggle(
        "开启深度思考", value=False, help="先输出推理过程再作答，更严谨但更慢、更耗 token"
    )
    reasoning_effort = "medium"
    if thinking:
        reasoning_effort = st.select_slider(
            "思考强度", options=["low", "medium", "high"], value="medium"
        )
    show_reasoning = st.toggle("显示思考过程", value=True)

    st.divider()

    # 接口密钥
    st.subheader("🔑 接口密钥")
    api_key = st.text_input(
        "DEEPSEEK_API_KEY", value=os.environ.get("DEEPSEEK_API_KEY", ""), type="password"
    )
    if api_key:
        st.success("密钥已就绪", icon="✅")
    else:
        st.warning("请填写 DEEPSEEK_API_KEY 后再聊天", icon="⚠️")

    st.divider()
    if st.button("🧹 清空对话", type="primary", width="stretch"):
        st.session_state.messages = []


# ============================== 6. 主区：角色资料卡 ==============================
st.title("💞 AI 伴侣")
# 侧边栏的操作会先 st.rerun()，当次 toast 会被丢掉，所以用会话变量中转一次
flash = st.session_state.pop("flash", None)
if flash:
    st.toast(flash["text"], icon=flash["icon"])
st.caption(
    f"当前伴侣：{char['avatar']} {char['name']} · {char['title']}"
    f"{'（✨ 自定义）' if is_custom else ''}　|　模型：{model}"
)

with st.container(border=True):
    profile = st.columns([1, 6], vertical_alignment="center")
    with profile[0]:
        show_avatar(char, font_size=76)
    with profile[1]:
        st.markdown(f"#### {char['name']} · {char['title']}")
        st.caption(" · ".join(char["tags"]) + ("　|　✨ 自定义角色" if is_custom else ""))
        st.write(char["persona"])

# 切换角色或清空对话后，重新插入开场白
if st.session_state.active_character != char_key or not st.session_state.messages:
    st.session_state.active_character = char_key
    st.session_state.messages = [
        {"role": "assistant", "content": char["greeting"], "reasoning": ""}
    ]


# ============================== 7. 主区：聊天区 ==============================
def render_message(record: ChatRecord) -> None:
    """渲染一条历史消息（思考过程默认折叠）"""
    is_user = record["role"] == "user"
    with st.chat_message(
        "user" if is_user else "assistant",
        avatar=USER_AVATAR if is_user else char["avatar"],
    ):
        if record["reasoning"] and show_reasoning:
            with st.expander("🤔 思考过程"):
                st.markdown(record["reasoning"])
        st.markdown(record["content"])


def stream_reply(chat_history: list, think_placeholder, result: dict):
    """调用 DeepSeek 流式接口：逐段 yield 正文，思考过程实时刷新到 think_placeholder"""
    try:
        client = get_client(api_key)
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": char["persona"]}] + chat_history,
            stream=True,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_body={"thinking": {"type": "enabled" if thinking else "disabled"}},
            **({"reasoning_effort": reasoning_effort} if thinking else {}),
        )
    except Exception as error:  # 网络、密钥、参数异常统一提示，避免整页报错
        result["error"] = str(error)
        yield f"⚠️ 调用失败：{error}"
        return

    step = 0
    try:
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            reasoning = getattr(delta, "reasoning_content", None)
            if reasoning:
                result["reasoning"] += reasoning
                step += 1
                if think_placeholder is not None and step % 10 == 0:  # 节流刷新，避免卡顿
                    think_placeholder.markdown(f"*{result['reasoning']}*")
            if delta.content:
                yield delta.content
    except Exception as error:
        result["error"] = str(error)
        yield f"\n\n⚠️ 连接中断：{error}"
    finally:
        close = getattr(stream, "close", None)
        if callable(close):
            close()
        if think_placeholder is not None and result["reasoning"]:
            think_placeholder.markdown(f"*{result['reasoning']}*")


for message in st.session_state.messages:
    render_message(message)

prompt = st.chat_input(f"和 {char['name']} 说点什么吧…", disabled=not api_key)
if isinstance(prompt, str) and prompt.strip():
    user_record: ChatRecord = {"role": "user", "content": prompt, "reasoning": ""}
    st.session_state.messages.append(user_record)
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=char["avatar"]):
        # 思考过程用空占位符承载，边生成边刷新
        think_placeholder = None
        if thinking and show_reasoning:
            with st.expander("🤔 思考过程", expanded=True):
                think_placeholder = st.empty()

        result = {"reasoning": "", "error": ""}
        history = [
            {"role": item["role"], "content": item["content"]}
            for item in st.session_state.messages
        ]
        reply = st.write_stream(stream_reply(history, think_placeholder, result))

    reply_text = "".join(reply) if isinstance(reply, list) else (reply or "")
    reply_record: ChatRecord = {
        "role": "assistant",
        "content": reply_text or "（这次没有收到回复，请检查网络或密钥）",
        "reasoning": result["reasoning"],
    }
    st.session_state.messages.append(reply_record)
    if result["error"]:
        st.toast("调用 DeepSeek 失败，请检查网络或密钥", icon="🚨")


