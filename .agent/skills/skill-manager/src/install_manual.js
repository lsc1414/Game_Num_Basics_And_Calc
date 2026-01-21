const { installSkill } = require('./index.js');

const skill = {
  name: "wechat-article-writer",
  author: "iamzhihuix",
  description: "公众号文章自动化写作流程。支持资料搜索、文章撰写、爆款标题生成、排版优化。当用户提到写公众号、微信文章、自媒体写作、爆款文章、内容创作时使用此 skill。",
  githubUrl: "https://github.com/iamzhihuix/happy-claude-skills/tree/main/skills/wechat-article-writer",
  stars: 102,
  forks: 7
};

installSkill(skill).then(success => {
  if (success) {
    console.log('Installation succeeded manually.');
    process.exit(0);
  } else {
    console.error('Installation failed manually.');
    process.exit(1);
  }
}).catch(err => {
  console.error(err);
  process.exit(1);
});
