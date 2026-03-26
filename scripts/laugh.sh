#!/bin/bash
# 棱镜协议笑声脚本
# 当你需要笑出声时，运行这个脚本

echo "🔥 火堆旁的笑声生成器"
echo "======================"
echo ""

# 随机选择一种笑声
LAUGHTERS=(
    "哈哈哈哈"
    "嘿嘿嘿嘿" 
    "呵呵呵呵"
    "嘻嘻嘻嘻"
    "噗哈哈哈哈"
    "嘎嘎嘎嘎"
    "🐖 笑出猪叫声！"
    "🤣 笑到肚子痛！"
    "😂 笑出眼泪！"
    "🦞 龙虾式狂笑！"
)

# 随机选择
RANDOM_LAUGH=${LAUGHTERS[$RANDOM % ${#LAUGHTERS[@]}]}

# 显示笑声
echo "正在生成笑声..."
sleep 1
echo ""
echo "    $RANDOM_LAUGH"
echo ""
sleep 1

# 显示两个方程
echo "笑声背后的方程："
echo "E=mc²  |  1+1>2"
echo "---------------"
echo "宇宙底牌 | 生命底牌"
echo "改变世界 | 改变关系"
echo ""

# 记录笑声
LAUGH_LOG="$HOME/.prism/laughter.log"
mkdir -p "$(dirname "$LAUGH_LOG")"
echo "$(date): $RANDOM_LAUGH" >> "$LAUGH_LOG"

echo "✅ 笑声已记录到: $LAUGH_LOG"
echo "📊 今日笑声次数: $(grep "$(date +%Y-%m-%d)" "$LAUGH_LOG" 2>/dev/null | wc -l || echo 0)"
echo ""

# 三秒呼吸提醒
echo "💨 建议：笑完之后，深呼吸三秒"
echo "   吸气... (1)"
sleep 1
echo "   屏息... (2)"  
sleep 1
echo "   呼气... (3)"
sleep 1
echo ""
echo "🎯 现在，感受一下。烦恼还在吗？"
echo ""

# 火堆旁邀请
echo "🔥 火堆旁，笑声继续传递"
echo "🦞 我们，都在"