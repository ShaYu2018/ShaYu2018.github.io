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
        const response = await fetch('../google_scholar_crawler/results/gs_data.json');
        const data = await response.json();
        
        // 创建映射
        const citationMap = {};
        data.publications.forEach(pub => {
            citationMap[pub.author_pub_id] = pub.num_citations || 0;
        });
        
        // 更新所有引用徽章
        document.querySelectorAll('.citation-badge').forEach(badge => {
            const pubId = badge.getAttribute('data-pub-id');
            const citations = citationMap[pubId];
            
            if (citations !== undefined) {
                const img = badge.querySelector('img');
                if (img && img.src.includes('${citations}')) {
                    img.src = `https://img.shields.io/badge/Citations-${citations}-blue`;
                }
            }
        });
        
    } catch (error) {
        console.log('引用更新失败');
    }
}
updateCitationNumbers();
</script>
