document.addEventListener("DOMContentLoaded", function() {
  if (typeof mermaid !== "undefined") {
    mermaid.initialize({ 
        startOnLoad: true,
        theme: 'dark' // 我们可以默认使用暗色，或者根据主题切换
    });
  }
});

// 支持 MkDocs Material 的即时加载 (instant loading)
if (typeof document.subscribe === "function") {
  document.subscribe(function() {
    if (typeof mermaid !== "undefined") {
      mermaid.initialize({ startOnLoad: true });
      mermaid.contentLoaded();
    }
  });
}
