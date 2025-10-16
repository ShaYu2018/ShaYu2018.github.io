---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<span class='anchor' id='about-me'></span>
{% include_relative includes/intro.md %}

{% include_relative includes/news.md %}

{% include_relative includes/researches.md %}

{% include_relative includes/experiences.md %}

{% include_relative includes/educations.md %}

{% include_relative includes/publications.md %}

{% include_relative includes/projects.md %}

{% include_relative includes/honers.md %}

{% include_relative includes/talks.md %}


<script>
document.addEventListener("DOMContentLoaded", function() {
    const papers = document.querySelectorAll(".paper-box-text"); 
    let num = 1; // 从1开始
    papers.forEach(paper => {
        // 在第一个子元素前插入序号（数字和一个点）
        const firstChild = paper.firstElementChild;
        if (firstChild) {
            // 创建一个 span 来显示编号
            const numSpan = document.createElement("span");
            numSpan.textContent = num + ". ";
            numSpan.style.fontWeight = "bold";
            firstChild.insertAdjacentElement("afterbegin", numSpan);
            num++;
        }
    });
});
</script>



<script>
async function updateCitationNumbers() {
    try {
        console.log('开始加载引用数据...');
        
        // 使用绝对路径
        const response = await fetch('/google_scholar_crawler/results/gs_data.json');
        if (!response.ok) {
            throw new Error('无法加载数据文件');
        }
        
        const data = await response.json();
        console.log('成功加载数据，文章数量:', data.publications.length);
        
        // 创建 pub_id 到引用数的映射
        const citationMap = {};
        data.publications.forEach(pub => {
            citationMap[pub.author_pub_id] = pub.num_citations || 0;
        });
        
        console.log('创建映射表:', citationMap);
        
        // 为每个徽章创建图片
        const badges = document.querySelectorAll('.citation-badge');
        console.log('找到徽章数量:', badges.length);
        
        badges.forEach((badge, index) => {
            const pubId = badge.getAttribute('data-pub-id');
            const citations = citationMap[pubId];
            
            console.log(`处理第${index + 1}个徽章:`, pubId, '引用数:', citations);
            
            if (citations !== undefined) {
                const link = badge.querySelector('a');
                if (link) {
                    // 清空链接内容（移除任何现有内容）
                    link.innerHTML = '';
                    
                    // 创建图片
                    const img = document.createElement('img');
                    img.src = `https://img.shields.io/badge/Citations-${citations}-blue`;
                    img.alt = `Citations: ${citations}`;
                    img.style.verticalAlign = 'middle';
                    
                    link.appendChild(img);
                    console.log(`✅ 为 ${pubId} 设置引用数: ${citations}`);
                }
            } else {
                console.log(`❌ 未找到 ${pubId} 的引用数据`);
            }
        });
        
        console.log('🎉 引用数字更新完成');
        
    } catch (error) {
        console.log('引用数字更新失败:', error);
    }
}

// 确保页面完全加载后执行
document.addEventListener('DOMContentLoaded', updateCitationNumbers);
</script>
