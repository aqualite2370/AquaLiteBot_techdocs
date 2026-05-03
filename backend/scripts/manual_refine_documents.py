from __future__ import annotations

import json
import re
from pathlib import Path


BACKUP_PATH = Path("backend/data/documents.pre_rewrite_backup.json")
TARGET_PATH = Path("backend/data/documents.json")


MANUAL_REFINES: dict[str, dict[str, list]] = {
    "定时禁言群员": {
        "desc": [
            "用于在群内创建查看和取消定时禁言任务",
        ],
        "commands": [
            ("创建定时禁言任务", "/mute 小时:分钟 分钟 QQ"),
            ("取消指定成员的任务", "/unmute QQ"),
            ("查看当前禁言任务列表", "/list_mute"),
        ],
        "notes": [
            "仅群主和管理员可创建或删除任务",
        ],
    },
    "JmComic演下载": {
        "desc": [
            "用于?ID 下载 JmComic 资源并返回结果",
            "模块已加入开关项，便于按吁",
        ],
        "commands": [
            ("?ID 下载演资源", "jm[id]"),
        ],
        "links": [
            "https://github.com/hect0x7/JMComic-Crawler-Python",
        ],
    },
    "相关信息": {
        "desc": [
            "发联系方式：奶茶sama（QQ?259891410）",
            "群聊丽站：775402634",
            "?2/3/4 群已解散，以中轾兑为准",
        ],
    },
    "B站频解": {
        "desc": [
            "用于解析 B 站分亓接并?QQ 丛接播放",
            "请先?B 站频页点击“分亝，再制链接作为参数",
        ],
        "commands": [
            ("解析 B 站分亓接", "bili [分享链接]"),
            ("使用同义前缀触发解析", "bili / b站解?/ B站解?[分享链接]"),
        ],
    },
    "表情包制": {
        "desc": [
            "攌按关锯忟生成或调用表情包模板",
            "叟看表情参数明与预图",
        ],
        "commands": [
            ("按模板则生成表情", "关键?+ 图片/文字/@某人"),
            ("查看关键词应的表情参数与览", "表情详情 + 关键"),
            ("忟打功能说明入口", "表情包制"),
        ],
    },
    "活字印刷": {
        "desc": [
            "用于生成活字印刷风格的文朕果",
        ],
        "commands": [
            ("查看该功能的参数与帮助", "hzys -h"),
        ],
    },
    "用前必！！": {
        "desc": [
            "拉群前先加入中轾?75402634，并根据群公告提供目标群信息",
            "如有或反馈，叁系奶茶sama（QQ?259891410）",
        ],
        "notes": [
            "请严格注意命令中的空格与参数格式，[] 内常表示“需要替捸实际参数”",
            "命令长时间无响应时，请先核示例图输入格式，再发送你好?Bot 在线状",
        ],
    },
    "MaimaiDX（舞萌）模块": {
        "desc": [
            "攌查 MaimaiDX 为佳成绩（Best40 / Best50）",
        ],
        "commands": [
            ("查为 Best40", "/mai b40"),
            ("查为 Best50", "/mai b50"),
        ],
        "notes": [
            "首使用前需先在外部站点完成账号绑定，并在个人信恸绑定 QQ",
        ],
        "links": [
            "https://www.diving-fish.com/maimaidx/prober/",
        ],
    },
    "🌩": {
        "desc": [
            "娱乐互动功能，可领取随机小礼包",
        ],
        "commands": [
            ("触发闔互动事件", "劈我"),
        ],
        "notes": [
            "?Bot 具有管理权限且目标为群员时，參随机触发 1-300 秒",
        ],
    },
    "舞萌小黑": {
        "desc": [
            "舞萌相关娱乐功能，具体效果参示例图",
        ],
    },
    "Valorant模块": {
        "desc": [
            "该模块依赖网环境，国内网络下可能无法稳定使用",
            "攌绑定账号并查询商店轮捿",
        ],
        "commands": [
            ("绑定账号（建聊使甼", "/valbind[账户名]#[密码]"),
            ("查当前商店轍", "/val shop"),
            ("世刐触发商店查", "瓦商"),
        ],
        "notes": [
            "若账号开吺次验证，參导致绑定失败",
            "请勿在公群聊丏送敏感账号信",
        ],
    },
    "在线运代码": {
        "desc": [
            "用于在线调试小型算法或代码片段，返回标准输出结果",
        ],
        "commands": [
            ("按执代码块", "code c/cpp/c#/py/php/go/java/js"),
        ],
        "notes": [
            "首指定诨，后细容为代码主体",
        ],
    },
    "奶茶抽": {
        "desc": [
            "群内互动抽功能，可按数连经与",
        ],
        "commands": [
            ("参与次抽奖", "抽奶"),
            ("按指定数连绊奖", "抽奶茶[次数]"),
        ],
        "notes": [
            "发起抽前至少需要两来茶",
        ],
    },
    "OSU！模": {
        "desc": [
            "攌 OSU 谱面搜索与下载推送",
        ],
        "commands": [
            ("按关锯搜索谱面", "/osu mapsec[关键词]"),
            ("?SID 下载并推送谱面文件", "/osudl [sid]"),
        ],
    },
    "Furry?随机": {
        "desc": [
            "基于 e621 的搜紸随机图功能，攌多标签组合",
        ],
        "commands": [
            ("按关锯搜索", "/e621 sec[搜索词]"),
            ("?ID 获取指定图片", "/e621 get[图片id]"),
            ("按关锯随机返回图片", "/e621 rand[搜索词]"),
            ("写随机搜", "er[关键词]"),
            ("全随机模式", "er"),
        ],
        "notes": [
            "多标签可使用 # 分隔，例如：dragon#strong",
            "使用 @ 全展示模式时返回条数会减少",
        ],
    },
    "奶茶酱陪": {
        "desc": [
            "基于小爱 API 的聊天模块，叿行日常话",
        ],
        "commands": [
            ("艾特 Bot 并发送句进行话", "@Bot + 诏"),
        ],
    },
    "游戏黑摇人模": {
        "desc": [
            "用于管理黑游戏列表和发起摇人提醒",
        ],
        "commands": [
            ("查看当前黑游戏列表", "游戏列表"),
            ("发起某游戏的摇人", "玩不游戏名] / 打不打[游戏名]"),
            ("加入黑列表", "加入游戏列表[游戏名]"),
            ("出开黑列表", "出游戏列表[游戏名]"),
        ],
    },
    "世界计划pjsk表情包制": {
        "desc": [
            "用于生成世界计划（PJSK）格文朡情图",
        ],
        "commands": [
            ("按文朆容生成图片", "pjsk[文本内]"),
        ],
        "notes": [
            "文本业空格会处理为换行",
        ],
    },
    "ACC计算": {
        "desc": [
            "用于计算游玩成绩相关 ACC 数据",
        ],
        "commands": [
            ("进入 ACC 计算流程", "/acc"),
        ],
        "notes": [
            "按提示骤依次输入参数即",
        ],
    },
    "奶茶排": {
        "desc": [
            "查看群内奶茶数量排",
        ],
        "commands": [
            ("获取奶茶排榜", "奶茶排"),
        ],
    },
    "戳一?拍一": {
        "desc": [
            "娱乐互动功能，直接戳奶茶酱即叧发",
        ],
    },
    "图片鉴赏分析": {
        "desc": [
            "用于对图片进行鉴赏或分析输出",
        ],
        "commands": [
            ("分析图片内", "/分析 + 图片"),
            ("鉴赏图片风格", "/鉴赏 + 图片"),
        ],
    },
    "Arcaea模块（已不可甼": {
        "desc": [
            "该模块当前已停运，暂不可使用",
        ],
        "notes": [
            "上游服务不可用致功能下线",
        ],
    },
    "工作性价比算器": {
        "desc": [
            "用于评估工作收益与投入的性价比",
        ],
        "commands": [
            ("吊工作性价比算流程", "工作性价"),
        ],
    },
    "舞立方模": {
        "desc": [
            "提供舞立方账号绑定与成绩查能力",
        ],
        "commands": [
            ("绑定账号（建聊进行）", "/wlf bind"),
            ("完成扠后进行二次确认", "/wlf bindsec"),
            ("查账号基信息", "/wlf"),
            ("按曲名搜", "/wlf sec[歌曲名]"),
            ("按谱?ID 搜索", "/wlf secid[谱面id]"),
            ("查指定成绩", "/wlf 查分[类型][曲名]"),
            ("模糊查成绩", "/wlf 模糊查分[类型][曲名]"),
            ("查看佳成绩前 20", "/wlf best"),
            ("查看新曲盈绩", "/wlf 新曲成绩"),
        ],
        "notes": [
            "推荐使用徿扠，不建使用舞立?App 扠",
            "/wlf best 受消恺件限制，私聊丏能无法使用",
        ],
    },
    "Phigros模块": {
        "desc": [
            "攌 Phigros 曲目信息查与技巧提示",
        ],
        "commands": [
            ("按曲名精硟", "/phi song[曲目名]"),
            ("按关锯模糊搜索", "/phi sec[关键词]"),
            ("查看玩法提示", "/phi tip"),
        ],
        "notes": [
            "数据内来源于萌娘百科",
        ],
    },
    "帽作择": {
        "desc": [
            "用于在丙项丿速随机决策",
        ],
        "commands": [
            ("在三项业机给出结果", "/师选择[选项1]或[选项2]..."),
        ],
    },
    "今日人品": {
        "desc": [
            "每日娱乐功能，返回当前人品",
        ],
        "commands": [
            ("查今日人品", "今日人品"),
        ],
    },
    "图片二元化": {
        "desc": [
            "将输入图片转捸二元格效果",
        ],
        "commands": [
            ("提交图片进二元化", "/二元化 + 图片"),
        ],
    },
    "签到": {
        "desc": [
            "提供每日签到和奶茶数量查",
        ],
        "commands": [
            ("完成每日签到", "签到 /sign"),
            ("查看为奶茶持有数量", "!mm / 我的奶茶"),
        ],
    },
    "Emoji合成": {
        "desc": [
            "将两?Emoji 合成为新的表情结果",
        ],
        "commands": [
            ("输入两个 Emoji 进合成", "emoji + emoji"),
        ],
        "notes": [
            "暂不攌识别 QQ 专有表情",
        ],
    },
    "点歌": {
        "desc": [
            "攌多平台关锯点歌",
        ],
        "commands": [
            ("QQ 音乐点歌", "/qq点歌 [关键词]"),
            ("网易云点歌", "/网易点歌 [关键词]"),
            ("酷我点歌", "/酷我点歌 [关键词]"),
            ("酷狗点歌", "/酷狗点歌 [关键词]"),
            ("咒点歌", "/咒点歌 [关键词]"),
            ("B 站点歌", "/b站点?[关键词]"),
        ],
        "notes": [
            "命令前缀包含 / ",
        ],
    },
    "EPIC每日免费游戏推": {
        "desc": [
            "用于查 EPIC 当前免费游戏信息",
        ],
        "commands": [
            ("获取每日免费游戏推", "喜加"),
        ],
    },
    "奶茶酱的过去": {
        "desc": [
            "历史文档归档页，记录旧版朵料入口与迁移说明",
        ],
        "links": [
            "https://www.showdoc.com.cn/ncj114514/8843059108042576",
            "https://note.youdao.com/ynoteshare1/index.html?id=31dc3ca4d79fdcc36240e95d4de06198&type=note",
        ],
    },
}


def extract_images(content: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\([^)]+\)", content or "")


def extract_links(content: str) -> list[str]:
    urls = re.findall(r"https?://[^\s)]+", content or "")
    out = []
    for u in urls:
        if "note.youdao.com/yws/public/resource" in u:
            continue
        if u not in out:
            out.append(u)
    return out


def build_markdown(title: str, source_content: str, spec: dict[str, list]) -> str:
    desc = spec.get("desc", [])
    commands = spec.get("commands", [])
    notes = spec.get("notes", [])

    links = []
    for u in spec.get("links", []):
        if u not in links:
            links.append(u)
    for u in extract_links(source_content):
        if u not in links:
            links.append(u)

    images = extract_images(source_content)

    parts: list[str] = [f"# {title}", "", "## 描述"]
    if desc:
        parts.extend([f"- {item}" for item in desc])
    else:
        parts.append("- 请参考下方功能明与示例")

    if commands:
        parts.extend(["", "## 使用"])
        for feature, command in commands:
            parts.append("```")
            parts.append(f"功能说明: {feature}")
            parts.append(f"触发命令: {command}")
            parts.append("```")
            parts.append("")
        if parts[-1] == "":
            parts.pop()

    if notes:
        parts.extend(["", "## 注意"])
        parts.extend([f"- {item}" for item in notes])

    if links:
        parts.extend(["", "## 参链"])
        parts.extend([f"- {u}" for u in links])

    if images:
        parts.extend(["", "## 示例", ""])
        for img in images:
            parts.append(img)
            parts.append("")
        if parts[-1] == "":
            parts.pop()

    return "\n".join(parts).strip() + "\n"


def main() -> None:
    source_payload = json.loads(BACKUP_PATH.read_text(encoding="utf-8"))
    target_payload = json.loads(TARGET_PATH.read_text(encoding="utf-8"))

    source_by_id = {d["id"]: d for d in source_payload.get("documents", [])}

    rewritten = 0
    for doc in target_payload.get("documents", []):
        source_doc = source_by_id.get(doc["id"], doc)
        title = source_doc.get("title", doc.get("title", "朑名文"))
        spec = MANUAL_REFINES.get(title, {})
        new_content = build_markdown(title, source_doc.get("content", ""), spec)
        if doc.get("content") != new_content:
            doc["content"] = new_content
            rewritten += 1

    TARGET_PATH.write_text(json.dumps(target_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manually_refined_docs={rewritten}")


if __name__ == "__main__":
    main()

