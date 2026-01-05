using UnityEditor;
using UnityEngine;
using System.Collections.Generic;
using System.IO;

public class AssetNamingValidator : AssetPostprocessor
{
    // 核心配置：什么类型 -> 对应什么前缀
    private static readonly Dictionary<System.Type, string> _prefixRules = new Dictionary<System.Type, string>()
    {
        { typeof(Material), "M_" },
        { typeof(GameObject), "P_" }, // 预制体
        { typeof(Texture2D), "T_" },  // 基础纹理
        { typeof(Sprite), "UI_" },    // 精灵/UI (需要额外判断)
        { typeof(AudioClip), "SFX_" }, // 默认音效 (BGM_ 需手动例外)
        { typeof(Shader), "Sh_" },
    };

    static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths)
    {
        foreach (string path in importedAssets) CheckAsset(path);
        foreach (string path in movedAssets) CheckAsset(path);
    }

    static void CheckAsset(string path)
    {
        // 1. 忽略非 Assets 目录或系统包
        if (!path.StartsWith("Assets/") || path.Contains("Packages/") || path.Contains("/Plugins/")) return;

        // 2. 忽略 Editor 脚本和 Meta 文件
        if (path.Contains("/Editor/") || path.EndsWith(".cs") || path.EndsWith(".meta")) return;

        string fileName = Path.GetFileNameWithoutExtension(path);
        Object asset = AssetDatabase.LoadAssetAtPath<Object>(path);
        if (asset == null) return;

        System.Type type = asset.GetType();

        // 3. 特殊处理：Prefab vs Model
        if (asset is GameObject)
        {
            // 如果是 FBX 模型，前缀应为 SK_ 或 SM_，这里简化检查
            // 真实项目中可通过 AssetImporter 判断是 Model 还是 Prefab
            return; 
        }

        // 4. 检查前缀
        if (_prefixRules.TryGetValue(type, out string expectedPrefix))
        {
            // 特殊处理：UI 图片
            if (type == typeof(Texture2D))
            {
                TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer != null && importer.textureType == TextureImporterType.Sprite)
                {
                    expectedPrefix = "UI_";
                }
            }

            if (!fileName.StartsWith(expectedPrefix))
            {
                Debug.LogWarning($"⚠️ [Naming Violation] Asset '{{fileName}}' should start with '{{expectedPrefix}}'\nPath: {{path}}");
            }
        }
    }
}