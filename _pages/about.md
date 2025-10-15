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
document.addEventListener("DOMContentLoaded", function() {
  const newsContainer = document.querySelector(".news-scroll");
  const newsList = document.querySelector(".news-list");
  const newsItems = document.querySelectorAll(".news-list li");
  const itemHeight = newsItems[0].offsetHeight;
  const totalHeight = newsItems.length * itemHeight;

  // 设置初始位置
  newsList.style.transform = "translateY(0)";

  // 每 30 秒滚动一次（与 CSS 动画同步）
  setInterval(() => {
    const currentY = parseInt(newsList.style.transform.replace(/[^-\d.]/g, '')) || 0;
    const newY = currentY - itemHeight;

    // 如果滚动到第二份内容的开头，跳回第一份内容的开头
    if (newY <= -totalHeight / 2) {
      newsList.style.transition = "none";
      newsList.style.transform = "translateY(0)";
      setTimeout(() => {
        newsList.style.transition = "transform 0.3s ease-out";
      }, 10);
    } else {
      newsList.style.transform = `translateY(${newY}px)`;
    }
  }, 30000 / newsItems.length); // 每条新闻滚动时间
});
</script>
