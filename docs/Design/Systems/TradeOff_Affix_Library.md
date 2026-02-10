---
sidebarTitle: "权衡词条库"
---

# ⚖️ 权衡词条库

> **文档目标 (Goal)**：提供 150 个“有代价的强力词条”灵感，用于构建 Roguelike、装备或天赋系统。
> **核心逻辑 (Core Logic)**：**缺陷即特色 (Flaw is Feature)**。通过剥夺玩家的一部分能力，迫使玩家走上极端的流派构建之路。

---

## ⚔️ 玻璃大炮 (Glass Cannon) - 攻防置换
*用生存换取极致输出 (Trade Survival for Extreme Damage).*

1.  **😡 狂暴姿态 (Berserker Stance)**：造成的伤害 +100%，受到的伤害 +100%。 (Damage Dealt +100%, Damage Taken +100%)
2.  **🗡️ 玻璃匕首 (Glass Dagger)**：暴击率 +50%，生命上限 -60%。 (Crit Chance +50%, Max HP -60%)

3.  **⚔️ 鲁莽进攻 (Reckless Attack)**：攻击速度 +40%，护甲 -10。 (Attack Speed +40%, Armor -10)

4.  **🩸 鲜血渴望 (Bloodlust)**：击杀敌人回复 1% 生命，但无法自然回血。 (Heal 1% HP on Kill, No Natural Regen)

5.  **🎲 孤注一掷 (All In)**：伤害 +30%，闪避率归零。 (Damage +30%, Dodge Chance becomes 0)

6.  **🦖 巨大化 (Gigantism)**：攻击范围 +50%，受击判定体积 +50%。 (Attack Range +50%, Hitbox Size +50%)

7.  **💉 肾上腺素 (Adrenaline)**：生命值越低，攻击速度越快（最高 +100%），但最大生命值 -20%。 (Attack Speed increases as HP drops, Max HP -20%)

8.  **👻 无形之刃 (Spectral Blade)**：穿透 +2，但最大生命值固定为 1。 (Pierce +2, Max HP fixed at 1)

9.  **🔨 沉重打击 (Heavy Blow)**：击退效果 +200%，移动速度 -30%。 (Knockback +200%, Move Speed -30%)

10. **👁️ 弱点识破 (Expose Weakness)**：暴击伤害 +100%，但非暴击攻击伤害 -50%。 (Crit Dmg +100%, Non-Crit Dmg -50%)

11. **☠️ 诅咒之剑 (Cursed Sword)**：攻击力 +300%，但受到任何伤害立即死亡。 (Damage +300%, Die on any hit taken)

12. **🔥 狂热信徒 (Zealot)**：每秒流失 1% 生命值，伤害 +50%。 (Lose 1% HP/sec, Damage +50%)

13. **🔄 痛苦转化 (Pain Conversion)**：受到伤害时，下一次攻击伤害 +200%。 (On Hit Taken: Next Attack deals +200% Dmg)

14. **🛡️ 护盾过载 (Shield Overload)**：护盾上限 +100%，但生命上限变为 1。 (Max Shield +100%, Max HP becomes 1)

15. **🪓 双刃斧 (Double-Edged Axe)**：攻击有 10% 几率对自己造成 10% 攻击力的伤害，伤害 +40%。 (10% chance to self-damage on attack, Damage +40%)

16. **🛑 静止射击 (Stationary Shooter)**：站立不动时伤害 +50%，移动时伤害 -50%。 (Damage +50% while standing still, -50% while moving)

17. **👓 近视眼 (Nearsighted)**：近战伤害 +50%，远程伤害 -50%。 (Melee Dmg +50%, Ranged Dmg -50%)

18. **🔭 远视眼 (Farsighted)**：远程伤害 +50%，近战伤害 -50%。 (Ranged Dmg +50%, Melee Dmg -50%)

19. **💔 脆弱核心 (Fragile Core)**：核心（基地）血量 -80%，所有防御塔伤害 +30%。 (Base HP -80%, Tower Damage +30%)

20. **🏳️ 背水一战 (Last Stand)**：当生命值低于 20% 时，无敌 5 秒（冷却 60秒），但最大生命值 -30%。 (Invulnerable for 5s when HP < 20%, Max HP -30%)

---

## 🎯 专精特化 (Specialist) - 属性置换
*用一种属性换取另一种属性，塑造极端流派 (Trade one stat for another to specialize).*

21. **🔫 重型枪管 (Heavy Barrel)**：伤害 +50%，攻击速度 -30%。 (Damage +50%, Attack Speed -30%)

22. **🪶 轻量化 (Lightweight)**：移动速度 +30%，击退抗性 -50%。 (Move Speed +30%, Knockback Resistance -50%)

23. **🔫 多重枪管 (Multi-Barrel)**：投射物数量 +2，伤害 -40%。 (Projectiles +2, Damage -40%)

24. **🎯 狙击镜头 (Sniper Scope)**：射程 +100%，攻击速度 -50%。 (Range +100%, Attack Speed -50%)

25. **💥 霰弹模式 (Shotgun Mode)**：投射物数量 +4，射程 -60%，散布 +30度。 (Projectiles +4, Range -60%, Spread +30 deg)

26. **🐢 龟壳 (Turtle Shell)**：护甲 +20，移动速度 -20%。 (Armor +20, Move Speed -20%)

27. **🦔 刺猬 (Hedgehog)**：反伤 +50%，攻击力 -20%。 (Thorns damage +50%, Attack Damage -20%)

28. **🧙‍♂️ 法师思维 (Mage Mind)**：元素伤害 +50%，物理伤害 -50%。 (Elemental Dmg +50%, Physical Dmg -50%)

29. **🩸 蛮族血统 (Barbarian Blood)**：物理伤害 +50%，无法造成元素伤害。 (Physical Dmg +50%, Cannot deal Elemental Dmg)

30. **🎯 精准打击 (Precise Strike)**：暴击率 100%，暴击伤害固定为 150%（无法提升）。 (Crit Chance 100%, Crit Dmg fixed at 150%)

31. **🌪️ 乱射 (Spray and Pray)**：攻击速度 +100%，精准度 -50%（子弹乱飞）。 (Attack Speed +100%, Accuracy -50%)

32. **🪨 巨石投掷 (Boulder Toss)**：投射物不再穿透，但爆炸范围 +100%。 (Projectiles no longer pierce, Explosion Area +100%)

33. **🩸 流血专精 (Bleed Specialist)**：流血伤害 +100%，直击伤害 -30%。 (Bleed Dmg +100%, Hit Dmg -30%)

34. **🧪 毒素扩散 (Poison Proliferation)**：中毒层数上限 +5，单层毒素伤害 -10%。 (Max Poison Stacks +5, Poison Dmg per stack -10%)

35. **🐌 缓慢投射 (Slow Projectiles)**：投射物速度 -50%，投射物持续时间 +100%。 (Projectile Speed -50%, Duration +100%)

36. **🚀 快速投射 (Fast Projectiles)**：投射物速度 +100%，伤害 -10%。 (Projectile Speed +100%, Damage -10%)

37. **👻 以太行者 (Ethereal Walker)**：闪避率 +30%，护甲 -30。 (Dodge +30%, Armor -30)

38. **🗿 钢铁意志 (Iron Will)**：免疫控制，但移动速度 -20%。 (Immune to CC, Move Speed -20%)

39. **🛡️ 魔法护盾 (Mana Shield)**：受到伤害优先扣除法力值，法力值归零时受到 200% 伤害。 (Damage taken from Mana before HP, take 200% dmg if Mana is 0)

40. **👻 异灵之体 (Eldritch Body)**：免疫物理伤害，受到的魔法伤害 +200%。 (Immune to Physical, +200% Magic Dmg taken)

---

## 💰 贪婪经济 (Economy) - 资源置换
*用战斗力换取发育，或用未来换取现在 (Trade power for economy, or future for present).*

41. **💰 贪婪之手 (Greed)**：金币获取 +50%，敌人血量 +20%。 (Gold Gain +50%, Enemy HP +20%)

42. **⚗️ 点金术 (Alchemy)**：击杀敌人 10% 几率掉落金币，伤害 -10%。 (10% chance to drop Gold on kill, Damage -10%)

43. **💸 高利贷 (Usury)**：立即获得 1000 金币，之后每波扣除 100 金币，直到还清 1500 金币。 (Gain 1000 Gold now, pay back 100/wave until 1500 paid)

44. **📈 投资 (Investment)**：每波结束获得 10% 当前金币的利息，但商店价格 +20%。 (Gain 10% interest per wave, Shop Prices +20%)

45. **🗑️ 拾荒者 (Scavenger)**：拾取范围 +100%，伤害 -5%。 (Pickup Range +100%, Damage -5%)

46. **💎 昂贵品味 (Expensive Taste)**：商店刷新出的物品品质更高，但价格 +50%。 (Higher Item Quality in Shop, Prices +50%)

47. **♻️ 回收利用 (Recycling)**：出售物品获得 100% 原价，但无法获得战斗掉落金币。 (Sell items for 100% value, No Gold drops from enemies)

48. **🤠 赏金猎人 (Bounty Hunter)**：精英怪掉落双倍奖励，精英怪伤害 +50%。 (Elite drops x2, Elite Damage +50%)

49. **🎲 赌徒 (Gambler)**：宝箱有 50% 几率开出双倍物品，50% 几率为空。 (Chests: 50% double loot, 50% empty)

50. **📜 契约 (Contract)**：每波开始时获得一件随机物品，但每波敌人数量 +10%。 (Gain random item per wave, Enemy Count +10%)

51. **💳 透支 (Overdraft)**：技能无冷却，但每次释放消耗 10 金币（金币不足无法释放）。 (No Cooldowns, Skills cost 10 Gold)

52. **🥇 黄金甲 (Gold Plating)**：每拥有 100 金币，护甲 +1，但受到伤害时掉落金币。 (+1 Armor per 100 Gold, Drop Gold on hit)

53. **💸 挥霍 (Splurge)**：伤害提升（当前金币 * 0.1%），每秒流失 1 金币。 (Damage +0.1% per Gold, Lose 1 Gold/sec)

54. **🏭 廉价制造 (Cheap Construction)**：建造费用 -30%，建筑血量 -50%。 (Build Cost -30%, Building HP -50%)

55. **🚀 未来科技 (Future Tech)**：立即解锁所有科技，但每波敌人血量 +50%。 (Unlock all tech, Enemy HP +50%)

56. **🩸 血汗钱 (Blood Money)**：拾取金币时受到 1 点伤害，金币价值 +100%。 (Take 1 dmg on Gold pickup, Gold Value +100%)

57. **🎈 通货膨胀 (Inflation)**：金币获取 +100%，商店价格 +150%。 (Gold Gain +100%, Shop Prices +150%)

58. **🌟 稀有收集 (Collector)**：稀有度高的物品掉率 +50%，普通物品掉率 -50%。 (Rare Drop Rate +50%, Common Drop Rate -50%)

59. **⚰️ 买命 (Life Insurance)**：受到致命伤害时消耗 50% 金币复活，若金币不足则死亡。 (Revive on death costing 50% Gold)

60. **🤲 捐赠 (Donation)**：将所有金币捐赠，每捐赠 100 金币，伤害永久 +1%。 (Donate all Gold, +1% Damage per 100 Gold donated)

---

## ⚙️ 机制异化 (Mechanic Shift) - 规则改变
*改变游戏的基础规则，创造全新的玩法体验 (Change base rules for unique gameplay).*

61. **🔋 异能电池 (Eldritch Battery)**：技能冷却时间 -50%，但无法造成暴击。 (Cooldowns -50%, Cannot Crit)

62. **🩸 鲜血魔法 (Blood Magic)**：技能不再消耗法力，改为消耗生命值。 (Skills cost HP instead of Mana)

63. **🛡️ 能量护盾 (Chaos Inoculation)**：生命值变为 1，护盾值变为原来的生命值上限，护盾脱战后极速回复。 (HP becomes 1, Shield = Max HP, Fast Shield Regen)

64. **🔫 双发 (Double Tap)**：每次攻击射出两发子弹，但只能造成 60% 伤害。 (Fire 2 shots, deal 60% damage each)

65. **⏱️ 蓄力爆发 (Charge Shot)**：攻击需要蓄力 1秒，伤害 +300%。 (1s Charge time, Damage +300%)

66. **🤖 自动炮台 (Auto Turret)**：无法手动攻击，攻击变为自动索敌，攻速 -20%。 (Auto-attack only, Attack Speed -20%)

67. **🗡️ 近战法师 (Battlemage)**：法术射程变为近战范围，法术伤害 +100%。 (Spells become Melee range, Spell Dmg +100%)

68. **🎱 弹射 (Ricochet)**：子弹在敌人间弹射 3 次，对单体伤害 -30%。 (Chain +3, Single Target Dmg -30%)

69. **🏹 穿透 (Pierce)**：子弹穿透所有敌人，每穿透一个敌人伤害递减 20%。 (Pierce All, -20% Dmg per pierce)

70. **🪃 回旋镖 (Boomerang)**：子弹会飞回，造成两次伤害，射程 -30%。 (Projectiles return, Range -30%)

71. **🧛 吸血鬼 (Vampire)**：无法使用血瓶，只能通过吸血回复。 (No Potions, Leech only)

72. **🕊️ 和平主义 (Pacifist)**：无法造成伤害，但召唤物/防御塔伤害 +100%。 (Deal 0 Damage, Summon/Tower Dmg +100%)

73. **🐺 独狼 (Lone Wolf)**：无法召唤/建造，自身属性 +100%。 (Cannot Summon/Build, Stats +100%)

74. **🧟 人海战术 (Zerg Rush)**：召唤物上限 +100%，召唤物生命值 -50%。 (Summon Limit +100%, Summon HP -50%)

75. **🔥 献祭 (Immolation)**：每秒对周围敌人造成高额伤害，但每秒对自己造成伤害。 (Burn enemies nearby, Burn self)

76. **⏳ 时间停滞 (Time Stop)**：受到伤害时触发时停 2秒，冷却 30秒，期间无法移动。 (Stop time for 2s on hit, Cooldown 30s, Rooted)

77. **🔗 量子纠缠 (Quantum Entanglement)**：受到的伤害由所有友方单位分摊。 (Damage shared among all allies)

78. **⛓️ 灵魂链接 (Soul Link)**：造成的伤害 30% 转化为对自己的治疗，受到的伤害 30% 转化为对敌人的治疗（资敌）。 (Lifesteal 30%, Enemies Lifesteal 30% from you)

79. **🩸 狂战士之血 (Berserker's Blood)**：每损失 1% 生命，攻击力 +1%。 (+1% Damage per 1% HP lost)

80. **☠️ 处决 (Execution)**：对生命值低于 20% 的敌人造成 10 倍伤害，对高于 20% 的敌人伤害 -20%。 (10x Damage to Low HP enemies, -20% Dmg otherwise)

---

## 💀 诅咒与混沌 (Cursed & Chaos) - 混乱中立
*引入随机性或极端的环境改变 (Randomness and Chaos).*

81. **🌀 混乱之触 (Chaos Touch)**：攻击造成随机元素效果（火/冰/电/毒），伤害浮动范围变为 1%~200%。 (Random Element, Dmg Range 1-200%)

82. **🐱 薛定谔的猫 (Schrodinger's Cat)**：每 10 秒，有 50% 几率无敌 5 秒，50% 几率受到双倍伤害。 (50% Invincible / 50% Double Dmg Taken)

83. **👹 巨大化敌人 (Giant Enemies)**：敌人体型 +50%，血量 +50%，移动速度 -30%。 (Enemy Size/HP +50%, Speed -30%)

84. **🐜 微缩化敌人 (Tiny Enemies)**：敌人体型 -50%，血量 -30%，移动速度 +50%，闪避率 +20%。 (Enemy Size -50%, HP -30%, Speed +50%, Dodge +20%)

85. **🏆 精英挑战 (Elite Challenge)**：不再刷新普通怪，全部刷新精英怪，数量 -80%。 (All enemies are Elites, Count -80%)

86. **🌑 黑暗降临 (Darkness Falls)**：视野范围 -50%，伤害 +50%。 (Vision Range -50%, Damage +50%)

87. **🌫️ 迷雾 (Fog)**：地图被迷雾覆盖，无法看到远处敌人，近战伤害 +50%。 (Fog of War, Melee Dmg +50%)

88. **🧲 重力反转 (Reverse Gravity)**：击退效果变为吸引效果。 (Knockback becomes Pull)

89. **🔪 友军伤害 (Friendly Fire)**：攻击会伤害友军，伤害 +100%。 (Friendly Fire ON, Damage +100%)

90. **⚡ 过载 (Overload)**：技能效果 +200%，但有 20% 几率释放失败并对自己造成伤害。 (Skill Effect +200%, 20% Fail Chance & Self Dmg)

91. **🌌 随机传送 (Random Blink)**：受到伤害时随机传送到屏幕任意位置。 (Teleport randomly on hit)

92. **⏩ 时间加速 (Time Acceleration)**：游戏整体速度（敌我） +50%。 (Game Speed +50%)

93. **🪞 镜像世界 (Mirror World)**：左右操作反向，伤害 +50%。 (Controls Inverted, Damage +50%)

94. **💀 一击必杀 (One Hit Kill)**：敌人和自己，任何一方受到伤害即死（Superhot 模式）。 (Everything dies in 1 hit)

95. **💣 战利品炸弹 (Loot Bomb)**：掉落物拾取时会小范围爆炸，造成伤害。 (Loot explodes on pickup)

96. **👻 幽灵模式 (Ghost Mode)**：穿墙，但受到的伤害 +50%。 (Noclip, Damage Taken +50%)

97. **📏 尺寸混乱 (Size Chaos)**：每隔 10 秒，随机改变自身大小（影响属性）。 (Random Size change every 10s)

98. **🔫 武器卡壳 (Jamming)**：攻击有 10% 几率卡壳（停顿 1秒），伤害 +30%。 (10% Jam chance, Damage +30%)

99. **🍀 幸运儿 (Lucky One)**：所有概率触发事件的几率翻倍，但敌人暴击率也翻倍。 (Proc Rates x2, Enemy Crit x2)

100. **🎰 终极赌注 (Final Wager)**：通关奖励翻倍，但如果死亡，删除存档。 (Double Rewards, Permadeath)

---

## 🔮 奇术与异能 (Thaumaturgy & Anomalies) - 新增机制
*更多改变游戏底层逻辑的词条 (More mechanics-altering affixes).*

101. **🔄 逆行投射 (Retrograde)**: 投射物向反方向发射，但速度 +200%。 (Projectiles fire backwards, Speed +200%)

102. **🛰️ 轨道轰炸 (Orbital Strike)**: 站立不动时，每秒召唤一次天基炮击，但射击时无法移动。 (Call down strikes while standing, cannot move while shooting)

103. **🔗 生命链接 (Life Link)**: 你受到的伤害由所有召唤物分摊。 (Damage taken is split among summons)

104. **🛡️ 法力护盾 (Mana Guard)**: 受到伤害的 30% 由法力值扣除。 (30% of damage taken from Mana)

105. **🍖 血肉献祭 (Flesh Sacrifice)**: 召唤物死亡时爆炸，造成高额范围伤害。 (Summons explode on death)

106. **👻 灵魂收割 (Soul Harvest)**: 每击杀一个敌人，伤害 +1%（无限叠加），受到伤害时清零。 (Damage +1% per kill, resets on hit)

107. **⚡ 相位移动 (Phase Shift)**: 冲刺/翻滚时无敌，但冲刺结束后 1秒内无法攻击。 (Invulnerable during dash, Disarmed for 1s after)

108. **⏪ 时间回溯 (Rewind)**: 受到致命伤害时，时间倒流 3秒（冷却 120秒）。 (Rewind 3s on death, 120s CD)

109. **🕳️ 重力井 (Gravity Well)**: 你的投射物会产生微型黑洞，吸附周围敌人。 (Projectiles pull enemies in)

110. **⚡ 连锁反应 (Chain Lightning)**: 所有伤害转化为闪电伤害，并获得 +2 弹射次数。 (All Dmg converts to Lightning, Chain +2)

111. **🧊 极寒领域 (Arctic Aura)**: 周围敌人移动速度 -50%，但你无法造成远程伤害。 (Nearby enemies slowed 50%, No Ranged Dmg)

112. **🔥 烈火战车 (Chariot of Fire)**: 移动时在身后留下火焰路径，但停止移动时每秒受到伤害。 (Leave fire trail, burn self when stopped)

113. **🩸 鲜血契约 (Blood Pact)**: 召唤物不再消耗法力，改为消耗你的生命值上限（保留生命）。 (Summons reserve Max HP instead of Mana)

114. **👻 亡灵大军 (Army of the Dead)**: 每击杀一个敌人，有 20% 几率将其复活为友军，持续 10秒。 (20% chance to resurrect enemy as ally for 10s)

115. **🛡️ 荆棘护甲 (Spiked Carapace)**: 护甲值的 100% 转化为攻击力，但护甲值归零。 (Armor converts to Damage, Armor becomes 0)

116. **🎯 弱点锁定 (Target Lock)**: 只能攻击离你最近的敌人，但伤害 +100%。 (Can only attack nearest enemy, Damage +100%)

117. **💣 爆破专家 (Demolitionist)**: 攻击不再造成直接伤害，而是附着炸弹，3秒后爆炸。 (Attacks attach bombs, explode after 3s)

118. **🌪️ 旋风斩 (Whirlwind)**: 攻击变为以自身为中心的持续旋转，移动速度 -20%。 (Spin to win, Move Speed -20%)

119. **🏹 箭雨 (Arrow Rain)**: 攻击变为从天而降的箭雨，有延迟但范围极大。 (Attacks fall from sky, delayed but huge AoE)

120. **👻 幽灵击 (Ghost Strike)**: 攻击无视墙壁和障碍物，但射程 -30%。 (Attacks ignore walls, Range -30%)

121. **🔄 转换者 (Shapeshifter)**: 每使用一次技能，随机切换武器/形态。 (Random weapon swap on skill use)

122. **⚖️ 业报 (Karma)**: 造成的伤害越高，受到的伤害越高（每 1000 Dps +1% 易伤）。 (More DPS = More Damage Taken)

123. **🎲 命运之轮 (Wheel of Fortune)**: 伤害在 0% 到 300% 之间随机浮动。 (Damage rolls 0-300%)

124. **🔋 能量过载 (Energy Overload)**: 满蓝时伤害 +100%，空蓝时伤害 -50%。 (Full Mana: Dmg +100%, Empty: Dmg -50%)

125. **🩸 嗜血狂魔 (Bloodseeker)**: 攻速无上限，但每秒消耗生命值随攻速增加。 (Uncapped Attack Speed, HP drain scales with AS)

126. **🛡️ 绝对防御 (Absolute Defense)**: 免疫所有伤害，但无法移动和攻击（持续 5秒，冷却 30秒）。 (Invulnerable but stunned for 5s)

127. **👻 灵魂出窍 (Astral Projection)**: 本体无敌且无法移动，控制灵魂进行战斗，灵魂死亡则本体死亡。 (Control invincible ghost, body vulnerable)

128. **💣 自爆卡车 (Kamikaze)**: 冲刺撞击敌人造成巨额伤害，并对自己造成 50% 伤害。 (Dash deals huge dmg, self-dmg 50%)

129. **🌪️ 风怒 (Windfury)**: 每次攻击有 20% 几率触发 3 次额外攻击。 (20% chance for 3 extra hits)

130. **🧊 冰霜新星 (Frost Nova)**: 暴击时释放冰霜新星，冻结周围敌人。 (Crit triggers Frost Nova)

131. **🔥 炎爆术 (Pyroblast)**: 攻击变为巨大的火球，飞行极慢但伤害极高。 (Huge slow fireball, massive damage)

132. **⚡ 闪电传送 (Lightning Warp)**: 移动变为瞬移，并在起点和终点造成闪电伤害。 (Movement becomes teleport + dmg)

133. **🩸 鲜血护盾 (Blood Shield)**: 溢出的治疗量转化为护盾，护盾每秒衰减。 (Overheal becomes Shield, decays over time)

134. **👻 亡语者 (Deathspeaker)**: 附近的尸体每秒对周围敌人造成伤害。 (Corpses deal AoE damage)

135. **🛡️ 坚如磐石 (Solid Rock)**: 无法被击退，受到的伤害减少 20%，但无法跳跃/冲刺。 (Immune to Knockback, Dmg Red 20%, No Dash)

136. **🎯 致命节奏 (Lethal Tempo)**: 每次攻击增加 10% 攻速，停止攻击时重置。 (Stacking AS on hit, resets on stop)

137. **💣 连环爆破 (Chain Reaction)**: 敌人死亡时爆炸，如果炸死其他敌人则继续爆炸。 (Enemy death explosion chains)

138. **🌪️ 飓风护体 (Hurricane)**: 投射物会被身边的飓风偏转，但无法精准瞄准。 (Projectiles deflected, Accuracy -50%)

139. **🏹 弹药限制 (Ammo Limit)**: 攻击力 +200%，但需要换弹（有装填时间）。 (Damage +200%, requires Reload)

140. **👻 影子武士 (Shadow Clone)**: 召唤一个模仿你动作的影子，造成 50% 伤害。 (Clone mimics actions, 50% dmg)

141. **⚖️ 等价交换 (Equivalent Exchange)**: 拾取回血道具时扣除金币，拾取金币时扣除生命。 (Health costs Gold, Gold costs Health)

142. **🎲 随机附魔 (Random Enchant)**: 每次进入房间，武器获得随机元素附魔。 (Random weapon element per room)

143. **🔋 电池包 (Battery Pack)**: 移动积攒电荷，停止移动时释放电荷造成伤害。 (Move to charge, Stop to discharge)

144. **🛡️ 反应装甲 (Reactive Armor)**: 受到伤害时，护甲 +100%，持续 3秒。 (Armor +100% after taking hit)

145. **🩸 痛苦羁绊 (Pain Bond)**: 链接最近的敌人，你受到的伤害他也受到。 (Link to enemy, share damage taken)

146. **👻 虚空行走 (Void Walk)**: 不攻击时隐身，攻击破隐并必暴。 (Invisible when idle, Crit on break)

147. **💣 定时炸弹 (Time Bomb)**: 身上被安装炸弹，必须在 10秒内击杀敌人重置倒计时，否则爆炸。 (Kill to reset bomb timer or die)

148. **🌪️ 元素混乱 (Elemental Chaos)**: 你的抗性每秒随机变化（-50% 到 +50%）。 (Resistances fluctuate randomly)

149. **🏹 巨弓 (Greatbow)**: 射程无限，但近身无法攻击（最小射程限制）。 (Infinite Range, Min Range limit)

150. **🃏 命运之手 (Hand of Fate)**: 你的技能由系统随机释放，无消耗，冷却 -50%。 (Random skills cast automatically, CD -50%)

---

## 📚 来源参考 (References)
*   **Brotato / Vampire Survivors**: 大量数值权衡设计的来源。
*   **Path of Exile (PoE)**: 核心天赋 (Keystone) 提供了极佳的机制置换灵感（如 CI, Blood Magic）。
*   **Risk of Rain 2**: 道具叠加与副作用（如 Shaped Glass）。
*   **Binding of Isaac**: 极端的角色形态变化（如 The Lost）。
*   **Dota 2**: 装备的主动/被动副作用（如 臂章, 疯狂面具）。
*   **Hades**: 混沌恩赐 (Chaos Boons) 与双重恩赐。
*   **Noita**: 魔杖编辑与法术修正。
