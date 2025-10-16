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
// 使用CSS样式创建徽章
fetch('/google_scholar_crawler/results/gs_data.json')
    .then(r => r.json())
    .then(data => {
        const map = {};
        data.publications.forEach(pub => map[pub.author_pub_id] = pub.num_citations || 0);
        
        document.querySelectorAll('[data-pub-id]').forEach(badge => {
            const pubId = badge.getAttribute('data-pub-id');
            const citations = map[pubId];
            if (citations !== undefined) {
                const link = badge.querySelector('a');
                if (link) {
                    link.className = 'citation-badge-link';
                    link.innerHTML = `Citations: ${citations}`;
                }
            }
        });
    });

// 添加CSS样式
const style = document.createElement('style');
style.textContent = `
    .citation-badge-link {
        display: inline-block;
        background: linear-gradient(45deg, #007acc, #005a9e);
        color: white !important;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        text-decoration: none;
        margin-left: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .citation-badge-link:hover {
        background: linear-gradient(45deg, #005a9e, #004080);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
`;
document.head.appendChild(style);
</script>
