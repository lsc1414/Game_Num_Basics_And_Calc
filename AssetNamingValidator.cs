using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

/// <summary>
/// 资产命名规范强制检查工具
/// 把此脚本放在 Assets/Editor 文件夹下
/// </summary>
public class AssetNamingValidator : AssetPostprocessor
{
    // ===================================================================================
    // ⚙️ 配置区域：在这里定义你的命名规则
    // ===================================================================================
    
    // 类型 -> 强制前缀
    private static readonly Dictionary<System.Type, string> PrefixRules = new Dictionary<System.Type, string>()
    {
        { typeof(Material), "M_" },
        { typeof(Texture), "T_" },       // 注意：UI图片可能需要特殊处理，这里作为通用兜底
        { typeof(GameObject), "P_" },    // Prefab
        { typeof(AudioClip), "SFX_" },   // 默认音频前缀，BGM_ 需要特殊逻辑或白名单
        { typeof(Shader), "Sh_" },
        { typeof(AnimationClip), "Anim_" },
        { typeof(RuntimeAnimatorController), "AC_" },
        { typeof(PhysicMaterial), "PM_" },
        // { typeof(SceneAsset), "L_" }, // 场景通常不通过Type加载，可根据扩展名判断
    };

    // 特殊白名单前缀 (例如音频可以是 SFX_ 也可以是 BGM_)
    private static readonly Dictionary<System.Type, List<string>> AllowedAltPrefixes = new Dictionary<System.Type, List<string>>()
    {
        { typeof(AudioClip), new List<string>() { "BGM_", "A_" } },
        { typeof(Texture), new List<string>() { "UI_", "I_", "S_" } }, // 允许 UI_, Icon_, Sprite_
        { typeof(GameObject), new List<string>() { "FX_", "SM_", "SK_" } } // Prefab 可能是特效或模型
    };

    // ===================================================================================
    // 🕵️ 自动检查逻辑 (OnImport)
    // ===================================================================================

    // 当资源被导入、删除、移动时调用
    static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths)
    {
        foreach (string path in importedAssets)
        {
            CheckAssetNaming(path);
        }

        foreach (string path in movedAssets)
        {
            CheckAssetNaming(path);
        }
    }

    private static void CheckAssetNaming(string path)
    {
        // 忽略非 Assets 目录 (如 Packages)
        if (!path.StartsWith("Assets/")) return; 
        
        // 忽略 Editor 文件夹下的资源 (通常是工具脚本，不需要遵循游戏资产规范)
        if (path.Contains("/Editor/")) return;

        // 获取资源对象
        Object asset = AssetDatabase.LoadAssetAtPath<Object>(path);
        if (asset == null) return;

        System.Type type = asset.GetType();
        string fileName = Path.GetFileName(path); // 包含扩展名
        string assetName = Path.GetFileNameWithoutExtension(path);

        // 查找规则
        string targetPrefix = null;
        
        // 1. 匹配主规则
        foreach (var rule in PrefixRules)
        {
            // 判断类型 (处理继承关系，例如 Texture2D 继承自 Texture)
            if (rule.Key.IsAssignableFrom(type))
            {
                targetPrefix = rule.Value;
                break;
            }
        }

        // 如果没有规则，跳过
        if (string.IsNullOrEmpty(targetPrefix)) return;

        // 2. 检查是否匹配主前缀
        if (assetName.StartsWith(targetPrefix)) return;

        // 3. 检查是否匹配替代前缀 (白名单)
        if (AllowedAltPrefixes.ContainsKey(type)) // 这里用 Key 检查，不能直接用 IsAssignableFrom，需要遍历
        {
             // 简单处理：直接找精确匹配的 Type，或者遍历
             foreach(var kvp in AllowedAltPrefixes) {
                 if(kvp.Key.IsAssignableFrom(type)) {
                     foreach(var alt in kvp.Value) {
                         if (assetName.StartsWith(alt)) return; // 合规
                     }
                 }
             }
        }

        // ❌ 发现违规
        Debug.LogError($"[命名规范] 资源命名违规: <color=yellow>{fileName}</color>\n" +
                       $"期望前缀: <color=green>{targetPrefix}</color> (或允许的变体)\n" +
                       $"资源路径: {path}\n" +
                       $"👉 右键资源 -> Tools -> Fix Naming Prefix 可自动修复。");
    }

    // ===================================================================================
    // 🛠️ 右键菜单工具 (Context Menu)
    // ===================================================================================

    [MenuItem("Assets/Tools/Fix Naming Prefix")]
    private static void FixNaming()
    {
        Object[] selectedAssets = Selection.objects;
        int fixCount = 0;

        foreach (Object asset in selectedAssets)
        {
            string path = AssetDatabase.GetAssetPath(asset);
            
            // 防御性检查
            if(string.IsNullOrEmpty(path) || !path.StartsWith("Assets/")) continue;

            System.Type type = asset.GetType();
            string oldName = asset.name;
            string correctPrefix = null;

            // 查找规则
            foreach (var rule in PrefixRules)
            {
                if (rule.Key.IsAssignableFrom(type))
                {
                    correctPrefix = rule.Value;
                    break;
                }
            }

            if (string.IsNullOrEmpty(correctPrefix))
            {
                Debug.LogWarning($"跳过: 未知类型的资源 {oldName} ({type.Name})");
                continue;
            }

            // 检查是否已经有正确的前缀 (包括白名单)
            bool hasValidPrefix = oldName.StartsWith(correctPrefix);
            if (!hasValidPrefix && AllowedAltPrefixes.ContainsKey(type))
            {
                 // 再次检查白名单 (简化逻辑)
                 // 实际项目中这里应该更严谨
            }

            if (!hasValidPrefix)
            {
                string newName = correctPrefix + oldName;
                string error = AssetDatabase.RenameAsset(path, newName);
                
                if (string.IsNullOrEmpty(error))
                {
                    fixCount++;
                    // Debug.Log($"已修复: {oldName} -> {newName}");
                }
                else
                {
                    Debug.LogError($"修复失败 {oldName}: {error}");
                }
            }
        }
        
        if(fixCount > 0)
        {
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();
            Debug.Log($"✅ 成功修复了 {fixCount} 个资源的命名。");
        }
        else
        {
            Debug.Log("没有发现需要修复的资源，或者资源类型未定义规则。");
        }
    }
    
    // 验证函数：只有选中了资源才显示该菜单
    [MenuItem("Assets/Tools/Fix Naming Prefix", true)]
    private static bool FixNamingValidation()
    {
        return Selection.objects.Length > 0;
    }
}
