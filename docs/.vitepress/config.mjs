import { defineConfig } from 'vitepress'
import mathjax3 from 'markdown-it-mathjax3'
import { withMermaid } from 'vitepress-plugin-mermaid'

// https://vitepress.dev/reference/site-config
export default withMermaid(
  defineConfig({
    title: '游戏开发101',
    description: '游戏开发101 - 数值设计、规则与技术标准',
    lang: 'zh-CN',
    base: '/Game_Num_Basics_And_Calc/',

    // 最后更新时间
    lastUpdated: true,

    // Vue 编译器选项 - 忽略自定义元素
    vue: {
      template: {
        compilerOptions: {
          // 将以下标签视为自定义元素，不作为 Vue 组件解析
          isCustomElement: (tag) => {
            // 忽略自定义颜色标签 <c=xxx>, 链接标签 <l=xxx>, 精灵标签 <s=xxx> 等
            return /^[cls]=/.test(tag) || tag.startsWith('/c') || tag.startsWith('/l') || tag.startsWith('/s')
          }
        }
      }
    },

    // Markdown 配置
    markdown: {
      math: true,
      lineNumbers: true,
      config: (md) => {
        md.use(mathjax3)
      }
    },

    // 主题配置
    themeConfig: {
      logo: '/assets/favicon.png',
      
      // 搜索
      search: {
        provider: 'local',
        options: {
          translations: {
            button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
            modal: {
              noResultsText: '无法找到相关结果',
              resetButtonTitle: '清除查询条件',
              footer: { selectText: '选择', navigateText: '切换' }
            }
          }
        }
      },

      // 编辑此页
      editLink: {
        pattern: 'https://github.com/lsc1414/Game_Num_Basics_And_Calc/edit/vitepress/docs/:path',
        text: '在 GitHub 上编辑此页'
      },

      // 最后更新时间文本
      lastUpdatedText: '最后更新',

      // 社交链接
      socialLinks: [
        { icon: 'github', link: 'https://github.com/lsc1414/Game_Num_Basics_And_Calc' }
      ],

      // 页脚导航
      docFooter: {
        prev: '上一页',
        next: '下一页'
      },

      // 大纲配置
      outline: {
        level: [2, 3],
        label: '页面导航'
      },

      // 返回顶部
      returnToTopLabel: '返回顶部',

      // 侧边栏菜单标签
      sidebarMenuLabel: '菜单',

      // 深色模式切换标签
      darkModeSwitchLabel: '主题',

      // 顶部导航栏
      nav: [
        { text: '首页', link: '/' },
        { text: '新人上路', link: '/START_HERE' },
        { text: '全站索引', link: '/Full_Index' },
        {
          text: '核心文档',
          items: [
            { text: '📘 数值手册', link: '/Design/Numerical_Manual' },
            { text: '⚔️ 战斗系统', link: '/Design/Mechanics/Combat_System' },
            { text: '⚡ 性能预算', link: '/Tech/Performance_Budget' }
          ]
        }
      ],

      // 侧边栏
      sidebar: {
        '/': [
          {
            text: '🎮 开始',
            items: [
              { text: '游戏开发 101', link: '/' },
              { text: '🚀 新人上路指南', link: '/START_HERE' },
              { text: '📚 全站索引', link: '/Full_Index' }
            ]
          },
          {
            text: '🎨 Art',
            collapsed: true,
            items: [
              {
                text: 'Tech Art',
                collapsed: true,
                items: [
                  { text: '🌈 HDR 渲染深度研究', link: '/Art/Tech_Art/HDR_DeepDive' },
                  { text: '🌤️ Bloom 后处理深度研究', link: '/Art/Tech_Art/Bloom_PostProcessing_DeepDive' },
                  { text: '👮‍♂️ 美术警察：资源验证标准', link: '/Art/Tech_Art/Asset_Validation_Standards' }
                ]
              },
              {
                text: 'UI/UX',
                collapsed: true,
                items: [
                  { text: '🎨 UI/UX 设计与交互规范', link: '/Art/UI_UX/UI_UX_Guidelines' },
                  { text: '📐 UI 信息密度与技能描述设计', link: '/Art/UI_UX/UI_Info_Density_Guide' },
                  { text: '🔠 游戏字体排印指南', link: '/Art/UI_UX/Typography_And_Font_Guide' }
                ]
              },
              {
                text: 'VFX',
                collapsed: true,
                items: [
                  { text: '✨ 特效优化黑魔法', link: '/Art/VFX/VFX_Optimization_Guide' },
                  { text: '✨ 视觉特效设计与性能规范', link: '/Art/VFX/VFX_Standards' },
                  { text: '游戏手感与 Juice', link: '/Art/VFX/Game_Feel_And_Juice' },
                  { text: '🧙‍♂️ Unity 粒子系统深度研究', link: '/Art/VFX/Unity_Particle_System_DeepDive' },
                  { text: '🧙‍♂️ 特效与打击感深度研究', link: '/Art/VFX/VFX_And_Game_Feel' }
                ]
              },
              { text: '🎥 Unity URP 画面表现与镜头设计指南', link: '/Art/Visual_Quality_Guide' },
              { text: '🎥 摄像机设计深度指南', link: '/Art/Camera_DeepDive_And_Settings' },
              { text: '🎨 美术风格一致性指南', link: '/Art/Art_Direction_Guide' },
              { text: '👁️ 视觉层级：混乱中的秩序', link: '/Art/Visual_Hierarchy_In_Chaos' }
            ]
          },
          {
            text: '🎵 Audio',
            collapsed: true,
            items: [
              { text: '🎧 Wwise 音频中间件详解', link: '/Audio/Wwise_Middleware_Guide' },
              { text: '🎵 动态音乐系统深度研究', link: '/Audio/Adaptive_Music_System' },
              { text: '🎵 游戏音效设计', link: '/Audio/Audio_System_Design_and_Tricks' },
              { text: '👂 AudioListener 挂载策略', link: '/Audio/AudioListener_Placement_Guide' },
              { text: '🔊 游戏音效设计与实现实战指南', link: '/Audio/Practical_Guide' },
              { text: '🛠️ Unity 轻量级音频框架', link: '/Audio/Lightweight_Audio_Framework' }
            ]
          },
          {
            text: '📐 Design',
            collapsed: true,
            items: [
              { text: '📘 核心数值体系定义手册', link: '/Design/Numerical_Manual' },
              { text: '🧠 游戏心理学框架', link: '/Design/Game_Psychology_DeepDive' },
              { text: '🧙‍♂️ 游戏设计哲学与系统架构', link: '/Design/Philosophy_And_Systems' },
              {
                text: 'Mechanics',
                collapsed: true,
                items: [
                  { text: '⚔️ 战斗系统详解', link: '/Design/Mechanics/Combat_System' },
                  { text: '⚡ 元素反应与连携机制', link: '/Design/Mechanics/Elemental_Reaction_System' },
                  { text: '🎲 肉鸽强化系统', link: '/Design/Mechanics/Roguelike_Perks' },
                  { text: '🏰 塔防建筑机制设计', link: '/Design/Mechanics/Tower_Defense_System' },
                  { text: '💢 仇恨系统与 AI 目标选择', link: '/Design/Mechanics/Aggro_System' },
                  { text: '🧙‍♂️ 难度曲线与 DDA', link: '/Design/Mechanics/Difficulty_And_DDA_System' }
                ]
              },
              {
                text: 'Systems',
                collapsed: true,
                items: [
                  { text: '🛡️ 装备与物品化设计', link: '/Design/Systems/Itemization' },
                  { text: '💰 掉落规则与战利品系统', link: '/Design/Systems/Loot_Table_Rules' },
                  { text: '💰 经济系统与通胀控制', link: '/Design/Systems/Economy_And_Inflation_Model' },
                  { text: '🌲 局外成长系统', link: '/Design/Systems/Meta_Progression' },
                  { text: '📈 数值膨胀控制论', link: '/Design/Systems/Power_Creep_Management' },
                  { text: '🧙‍♂️ 技能树设计深度研究', link: '/Design/Systems/Skill_Tree_Design' }
                ]
              },
              {
                text: 'Content',
                collapsed: true,
                items: [
                  { text: '👹 怪物图鉴与AI行为', link: '/Design/Content/Enemy_Bestiary' },
                  { text: '🗺️ 关卡与波次设计指南', link: '/Design/Content/Level_Design_Guide' },
                  { text: '🗺️ 关卡设计理论', link: '/Design/Content/Level_Design_Theory' },
                  { text: '🧙‍♂️ Boss 战设计哲学', link: '/Design/Content/Boss_Design_Philosophy' }
                ]
              },
              {
                text: 'LiveOps',
                collapsed: true,
                items: [
                  { text: '🌟 业界优秀运营系统研究', link: '/Design/LiveOps/Advanced_LiveOps_Systems' },
                  { text: '🎫 通行证经济学', link: '/Design/LiveOps/Battle_Pass_Economy' },
                  { text: '📅 活动排期策略', link: '/Design/LiveOps/Event_Cadence_Strategy' }
                ]
              },
              {
                text: 'UX',
                collapsed: true,
                items: [
                  { text: '♿ 无障碍设计标准', link: '/Design/UX/Accessibility_Standards' },
                  { text: '👶 新手引导与首局体验', link: '/Design/UX/FTUE_Best_Practices' }
                ]
              }
            ]
          },
          {
            text: '⚙️ Tech',
            collapsed: true,
            items: [
              { text: '⚡ 性能预算与优化标准', link: '/Tech/Performance_Budget' },
              { text: '🤖 Utility AI 决策系统', link: '/Tech/AI_Utility_System' },
              { text: '🤖 有限状态机 FSM 设计', link: '/Tech/FSM_Design_Patterns' },
              { text: '⚔️ 技能系统 GAS 设计方案', link: '/Tech/Gameplay_Ability_System_Design' },
              { text: '🌐 网络架构与协议', link: '/Tech/Network_Architecture' },
              { text: '📱 移动端深度优化指南', link: '/Tech/Mobile_Optimization_Guide' },
              { text: '💾 存档与数据持久化架构', link: '/Tech/Save_System_Architecture' },
              { text: '🔄 热更新与资源管理', link: '/Tech/Hot_Update_And_Resources' },
              { text: '🛠️ Luban 配表实战', link: '/Tech/Luban_Config_Guide' },
              {
                text: 'Architecture',
                collapsed: true,
                items: [
                  { text: '🏗️ 游戏设计模式实战', link: '/Tech/Architecture/Game_Design_Patterns_Practice' },
                  { text: '🧠 通用加权决策系统', link: '/Tech/Architecture/Unified_Decision_System' },
                  { text: '🧩 ECS 理论与实践', link: '/Tech/Architecture/ECS_Theory_And_Practice' },
                  { text: '☠️ Unity 代码毒药', link: '/Tech/Architecture/Unity_Anti_Patterns' }
                ]
              },
              {
                text: 'Graphics',
                collapsed: true,
                items: [
                  { text: '🎨 Shader 核心数学模式', link: '/Tech/Graphics/Shader_Math_Patterns' },
                  { text: '🎨 Linear与Gamma渲染空间', link: '/Tech/Graphics/Linear_vs_Gamma_Rendering' },
                  { text: '🎨 Unity SpriteAtlas 优化', link: '/Tech/Graphics/Unity_SpriteAtlas_DeepDive' },
                  { text: '⚡ Compute Shader 移动端指南', link: '/Tech/Graphics/Compute_Shader_Mobile_Guide' },
                  { text: '🧙‍♂️ 粒子特效材质透明度混合', link: '/Tech/Graphics/Particle_Blending_Modes' }
                ]
              },
              {
                text: 'Mechanics',
                collapsed: true,
                items: [
                  { text: '🎯 索敌机制详解与实战', link: '/Tech/Mechanics/Targeting_System_DeepDive' },
                  { text: '🎯 索敌管道详解', link: '/Tech/Mechanics/Targeting_Pipeline_DeepDive' },
                  { text: '🏹 投射物系统深度解析', link: '/Tech/Mechanics/Projectile_System_DeepDive' },
                  { text: '📐 Unity Transform 数学变换', link: '/Tech/Mechanics/Unity_Transform_Math_Guide' },
                  { text: '📐 Unity RectTransform 深度解析', link: '/Tech/Mechanics/Unity_RectTransform_DeepDive' },
                  { text: '🧭 NavMesh 寻路与状态控制', link: '/Tech/Mechanics/NavMesh_Pathfinding_Guide' }
                ]
              },
              {
                text: 'Algorithms',
                collapsed: true,
                items: [
                  { text: '🎲 Roguelike 随机算法剖析', link: '/Tech/Algorithms/Roguelike_RNG_Systems' },
                  { text: '🧙‍♂️ 关卡生成算法 PCG', link: '/Tech/Algorithms/Procedural_Generation_Guide' },
                  { text: '🧙‍♂️ 游戏常用算法深度研究', link: '/Tech/Algorithms/Common_Game_Algorithms' }
                ]
              }
            ]
          },
          {
            text: '📖 Dev Guides',
            collapsed: true,
            items: [
              { text: '📜 全员速查表', link: '/Dev_Guides/Project_Cheat_Sheet' },
              { text: '🛠️ Unity 游戏开发实战锦囊', link: '/Dev_Guides/Unity_Practical_Tips' },
              { text: '💀 游戏开发血泪史', link: '/Dev_Guides/Production_Lessons' },
              {
                text: 'Tools',
                collapsed: true,
                items: [
                  { text: '⏱️ 性能监控脚本集', link: '/Dev_Guides/Tools/Performance_Monitoring_Scripts' },
                  { text: '⚔️ 战斗仿真系统', link: '/Dev_Guides/Tools/Combat_Simulation_System' },
                  { text: '🛠️ 游戏开发工具链指南', link: '/Dev_Guides/Tools/Game_Dev_Toolchain_Guide' },
                  { text: '🧮 数值计算器套装', link: '/Dev_Guides/Tools/Numerical_Calculator_Suite' }
                ]
              },
              {
                text: 'Publishing',
                collapsed: true,
                items: [
                  { text: '🚀 Steam Unity 独立游戏开发实战指南', link: '/Dev_Guides/Publishing/Steam_Unity_Indie_Game_Guide' },
                  { text: '🚀 发射前夜：上线前的生死清单', link: '/Dev_Guides/Publishing/Launch_Readiness_Checklist' },
                  { text: '🚂 Steam 发行策略研究', link: '/Dev_Guides/Publishing/Steam_Strategy' },
                  { text: '📱 TapTap 发行策略研究', link: '/Dev_Guides/Publishing/TapTap_Strategy' }
                ]
              },
              {
                text: 'Industry Cases',
                collapsed: true,
                items: [
                  { text: '🧛 Vampire Survivors 性能奇迹', link: '/Dev_Guides/Industry_Cases/Vampire_Survivors_Performance' },
                  { text: '🔱 Hades 构建多样性深度解析', link: '/Dev_Guides/Industry_Cases/Hades_Build_Diversity' },
                  { text: '🥔 Brotato 数值体系全解', link: '/Dev_Guides/Industry_Cases/Brotato_Numerical_Analysis' },
                  { text: '🏰 Kingdom Rush 数值模型分析', link: '/Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model' }
                ]
              },
              {
                text: 'Collaboration',
                collapsed: true,
                items: [
                  { text: '🐙 Git 版本管理与 Commit 规范', link: '/Dev_Guides/Collaboration/Git_Commit_Standards' },
                  { text: '🐙 GitHub 工作流与 PR 最佳实践', link: '/Dev_Guides/Collaboration/GitHub_PR_Workflow' },
                  { text: '🏃 独立游戏团队 Scrum 实施指南', link: '/Dev_Guides/Collaboration/Agile_For_Indie_Teams' }
                ]
              }
            ]
          },
          {
            text: '📋 Unity Standards',
            collapsed: true,
            items: [
              { text: 'Unity 资产命名规范与强制检查工具', link: '/Unity_Standards/Asset_Naming' },
              { text: '🏭 标准资源管理工业流程', link: '/Unity_Standards/Standard_Resource_Workflow' },
              { text: '📂 Unity 项目文件夹结构规范', link: '/Unity_Standards/Folder_Structure' },
              { text: '📦 Unity 资产管理实战指南', link: '/Unity_Standards/Asset_Management' }
            ]
          }
        ]
      }
    },

    // Mermaid 配置
    mermaid: {
      // 主题配置
    },
    mermaidPlugin: {
      class: 'mermaid'
    }
  })
)
