#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""6G 的一天生活模拟器 (6g-day)。

概念致敬 2026 年"6G 网要来了"相关热搜报道中描绘的未来生活场景，
所有剧情纯属虚构畅想，如有雷同，说明 6G 真的来了。

纯 Python 标准库，Python 3.10+。
"""

import argparse
import random
import sys

MIN_V, MAX_V = 0, 100
INITIAL_STATS = {"效率值": 50, "社死值": 10, "电量": 80}

PHASES = [
    {
        "name": "早晨 7:30 —— 全息会议室",
        "desc": "太赫兹体感闹钟把你叫醒。千里之外的同事已经在全息会议室落座，"
                "你的投影正从卧室\"传送\"过去——而你还穿着睡衣。",
        "options": [
            {"key": "1", "label": "全息投影西装革履",
             "effects": {"效率值": 8, "社死值": -5, "电量": -12},
             "result": "你以精英姿态落座，同事纷纷点赞。全息西装，免烫免洗。"},
            {"key": "2", "label": "睡衣上阵，爱咋咋地",
             "effects": {"效率值": -3, "社死值": 15, "电量": -4},
             "result": "有人截图了。你的草莓睡衣上了部门群，配文：今日最佳着装。"},
            {"key": "3", "label": "全息马赛克模糊处理",
             "effects": {"效率值": -2, "社死值": 5, "电量": -8},
             "result": "你变成了一团高贵的马赛克。老板问：这位马赛克同事是谁？"},
        ],
        "events": [
            {"p": 0.25,
             "text": "全息信号卡顿了 0.5 秒，你的睡衣领口被全公司围观！",
             "effects": {"社死值": 20}},
        ],
    },
    {
        "name": "上午 10:00 —— 数字分身代会",
        "desc": "三个会撞车。你的数字分身主动请缨：\"本体，这种小场面交给我。\"",
        "options": [
            {"key": "1", "label": "分身全权代会",
             "effects": {"效率值": 10, "社死值": 8, "电量": -8},
             "result": "分身在会上替你\"嗯嗯啊啊\"，还替你答应了周五交方案。"},
            {"key": "2", "label": "双开实时监控分身",
             "effects": {"效率值": 5, "社死值": -3, "电量": -15},
             "result": "你一边开会一边盯分身，电量哗哗掉，但分身没敢乱说话。"},
            {"key": "3", "label": "亲自上阵",
             "effects": {"效率值": 8, "社死值": -3, "电量": -5},
             "result": "分身在旁边给你递虚拟咖啡，端茶倒水一把好手。"},
        ],
        "events": [
            {"p": 0.20,
             "text": "分身在虚拟会场平地摔了一跤，动作同步到了你的全息投影！",
             "effects": {"社死值": 15, "效率值": -3}},
        ],
    },
    {
        "name": "中午 12:30 —— 无人机外卖",
        "desc": "无人机准时悬停在阳台，热气腾腾。太赫兹感知扫过你的订单——"
                "它什么都知道。",
        "options": [
            {"key": "1", "label": "双份快乐水 + 双份炸鸡",
             "effects": {"效率值": 3, "社死值": 5, "电量": -3},
             "result": "无人机用机械臂给你比了个大拇指：懂生活。"},
            {"key": "2", "label": "健康轻食沙拉",
             "effects": {"效率值": 5, "社死值": -3, "电量": -3},
             "result": "AI 营养师给你点了赞，并默默记下了你的自律。"},
            {"key": "3", "label": "睡过去，不吃了",
             "effects": {"效率值": -8, "社死值": 0, "电量": 8},
             "result": "设备趁机快充了一波。胃：我呢？"},
        ],
        "events": [
            {"p": 0.30, "if_choice": "1",
             "text": "太赫兹感知广播：\"检测到您点了双份，已为您精准投送！\"全小区都知道了。",
             "effects": {"社死值": 10}},
        ],
    },
    {
        "name": "下午 15:00 —— AI 基站修网",
        "desc": "家里断网了。AI 基站说：\"检测到光猫罢工，已派遣纳米机器人，3 分钟修好。\"",
        "options": [
            {"key": "1", "label": "完全信任 AI 基站",
             "effects": {"效率值": 10, "社死值": 0, "电量": -5},
             "result": "网修好了，快得离谱。你甚至没来得及起身。"},
            {"key": "2", "label": "自己动手重启光猫",
             "effects": {"效率值": 5, "社死值": 0, "电量": -5},
             "result": "传统手艺，永不过时。拔插三秒，世界和平。"},
            {"key": "3", "label": "躺平刷手机流量",
             "effects": {"效率值": -5, "社死值": 0, "电量": -10},
             "result": "流量警告：本月已使用 200G，运营商来电问你是不是开网吧。"},
        ],
        "events": [
            {"p": 0.20, "if_choice": "1",
             "text": "AI 基站过度\"体贴\"，把你的作息报告发给了你妈："
                   "\"您儿子昨晚 3 点还在打游戏，请注意督促。\"",
             "effects": {"社死值": 25}},
        ],
    },
    {
        "name": "晚上 20:00 —— 虚拟世界探索",
        "desc": "数字分身提议去虚拟世界探险：\"本体，元宇宙新开了个赛博夜市，去不去？\"",
        "options": [
            {"key": "1", "label": "分身代你探险",
             "effects": {"效率值": 5, "社死值": 8, "电量": -10},
             "result": "分身在夜市跟 NPC 砍价，砍到了骨折价，还顺了个虚拟糖画。"},
            {"key": "2", "label": "亲自沉浸式体验",
             "effects": {"效率值": 8, "社死值": -2, "电量": -15},
             "result": "你戴上全套设备，逛了两小时赛博夜市，VR 眩晕值拉满但快乐。"},
            {"key": "3", "label": "早睡，设备充电",
             "effects": {"效率值": -3, "社死值": -5, "电量": 15},
             "result": "分身自己去玩了，给你发了 99+ 条战报，你一条没看。"},
        ],
        "events": [
            {"p": 0.20,
             "text": "分身在虚拟世界跳了段魔性舞蹈，被做成表情包传回了现实。",
             "effects": {"社死值": 12}},
        ],
    },
    {
        "name": "深夜 23:30 —— AI 健康报告",
        "desc": "6G 基站\"思考\"了一整天，给你生成了一份个性化健康报告，"
                "标题：《关于你，怎么吃都不胖的 108 种错觉》。",
        "options": [
            {"key": "1", "label": "认真阅读并整改",
             "effects": {"效率值": 3, "社死值": 5, "电量": -3},
             "result": "报告建议：少点双份，早点睡。你：有道理，明天就改。"},
            {"key": "2", "label": "一键删除，眼不见为净",
             "effects": {"效率值": -2, "社死值": -5, "电量": -2},
             "result": "基站表示很受伤，连夜给你生成了第二份：《论删除报告的 108 种心理》。"},
            {"key": "3", "label": "转发到家庭群",
             "effects": {"效率值": 0, "社死值": 15, "电量": -3},
             "result": "你妈秒回：\"早就跟你说了！\"并转发了 10 篇养生文。"},
        ],
        "events": [
            {"p": 0.25,
             "text": "基站把报告同步给了你的智能手环，手环在公司步数榜备注："
                   "\"该用户心率异常，建议少熬夜。\"",
             "effects": {"社死值": 10}},
        ],
    },
]


def apply_effects(stats, effects, say=None):
    """应用属性变化并钳制到 [0, 100]。"""
    for k, d in effects.items():
        old = stats.get(k, 50)
        new = max(MIN_V, min(MAX_V, old + d))
        stats[k] = new
        if say is not None and d != 0:
            arrow = "↑" if d > 0 else "↓"
            say(f"    {k} {arrow} {abs(d)}（{old} → {new}）")


def fmt_stats(stats):
    return " ".join(f"{k}:{v}" for k, v in stats.items())


def find_option(phase, raw):
    """按编号找选项，非法输入返回 None。"""
    for o in phase["options"]:
        if o["key"] == raw.strip():
            return o
    return None


def roll_events(phase, rng, choice_key):
    """掷随机事件；if_choice 限制只在特定选项后触发。"""
    hit = []
    for ev in phase.get("events", []):
        if ev.get("if_choice") and ev["if_choice"] != choice_key:
            continue
        if rng.random() < ev["p"]:
            hit.append(ev)
    return hit


def ending(stats):
    """按三维结算结局。"""
    if stats["社死值"] >= 70:
        return {"name": "赛博社死现场",
                "comment": "你的睡衣、分身、作息，全网都知道了。"
                           "建议改名，换个星球重新开始。"}
    if stats["电量"] <= 10:
        return {"name": "赛博断电人",
                "comment": "全息设备集体罢工，你被迫回到了 4G 时代。"
                           "恭喜，赛博朋克第一课：记得充电。"}
    if stats["效率值"] >= 60:
        return {"name": "6G 原住民",
                "comment": "你已经完全驯化了 6G。基站为你打工，分身为你开会，"
                           "无人机为你送饭——赛博朋克竟是田园牧歌。"}
    return {"name": "被 AI 安排得明明白白",
            "comment": "这一天你什么都干了，又好像什么都没干。"
                       "AI 说：\"别担心，我都替你记着呢。\""}


def play_day(rng, choose, verbose=False):
    """跑完 6 个时段。choose(phase) -> option。返回 (stats, ending, log)。"""
    stats = dict(INITIAL_STATS)
    log = []

    def say(s=""):
        log.append(s)
        if verbose:
            print(s)

    for phase in PHASES:
        say(f"【{phase['name']}】")
        say(phase["desc"])
        opt = choose(phase)
        say(f"你选择了：{opt['label']}")
        say(opt["result"])
        apply_effects(stats, opt["effects"], say)
        for ev in roll_events(phase, rng, opt["key"]):
            say(f"⚡突发：{ev['text']}")
            apply_effects(stats, ev["effects"], say)
        say(f"当前状态：{fmt_stats(stats)}")
        say()
    end = ending(stats)
    say("🌙 一天结束——" + end["name"])
    say(end["comment"])
    say(f"最终状态：{fmt_stats(stats)}")
    return stats, end, log


def choose_interactive(phase):
    for o in phase["options"]:
        print(f"  {o['key']}. {o['label']}")
    while True:
        raw = input("你的选择（输入编号）：")
        opt = find_option(phase, raw)
        if opt is None:
            print("无效选项，请重新输入。")
            continue
        return opt


def run_auto(games, seed, verbose):
    rng = random.Random(seed)
    dist = {}
    for i in range(games):
        stats, end, _ = play_day(rng, lambda ph: rng.choice(ph["options"]),
                                 verbose=verbose)
        dist[end["name"]] = dist.get(end["name"], 0) + 1
        if not verbose:
            print(f"第 {i + 1} 局：{end['name']}（{fmt_stats(stats)}）")
    print(f"\n共 {games} 局，结局分布：")
    for name, c in dist.items():
        print(f"  {name}：{c} 局")


def main(argv=None):
    ap = argparse.ArgumentParser(description="6G 的一天生活模拟器")
    ap.add_argument("--auto", action="store_true", help="AI 随机选择，自动演示")
    ap.add_argument("--games", type=int, default=1, help="自动演示局数")
    ap.add_argument("--seed", type=int, default=None, help="随机种子")
    ap.add_argument("--verbose", action="store_true", help="打印全天战报")
    args = ap.parse_args(argv)

    if args.auto:
        run_auto(args.games, args.seed, args.verbose)
        return 0

    if not sys.stdin.isatty():
        print("需要交互式终端进行游戏，请使用 --auto 模式自动演示。", file=sys.stderr)
        return 2
    rng = random.Random()
    play_day(rng, choose_interactive, verbose=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
