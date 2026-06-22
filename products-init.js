<!-- 在products.html的<head>中添加utils.js引用 -->
<script src="utils.js"></script>
<script>
  // 页面加载后自动应用category过滤
  document.addEventListener('DOMContentLoaded', function() {
    const categoryParam = getUrlParam('category');
    if (categoryParam) {
      // 找到对应的分类按钮并点击
      const buttons = document.querySelectorAll('#theme-tags .tag-btn');
      buttons.forEach(btn => {
        if (btn.dataset.theme === categoryParam) {
          btn.classList.add('active');
        }
      });
      filterCards();
    }
    
    // 为每个卡片添加click事件导航到product-detail
    attachCardClickHandlers();
    
    // 为心形按钮添加收藏功能
    attachFavoriteHandlers();
  });
  
  // 为卡片添加点击事件
  function attachCardClickHandlers() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
      const titleElement = card.querySelector('.card-title');
      const cardBody = card.querySelector('.card-body');
      
      // 点击卡片（除了心形按钮外）导航到product-detail
      cardBody.style.cursor = 'pointer';
      cardBody.addEventListener('click', function(e) {
        // 确保点击的不是心形按钮
        if (!e.target.classList.contains('card-fav')) {
          window.location.href = `product-detail.html?productId=product-${index + 1}`;
        }
      });
      
      // 卡片图片区域也可点击
      const cardImg = card.querySelector('.card-img');
      cardImg.style.cursor = 'pointer';
      cardImg.addEventListener('click', function(e) {
        if (!e.target.classList.contains('card-fav')) {
          window.location.href = `product-detail.html?productId=product-${index + 1}`;
        }
      });
    });
  }
  
  // 为心形按钮添加收藏功能
  function attachFavoriteHandlers() {
    const favButtons = document.querySelectorAll('.card-fav');
    favButtons.forEach((btn, index) => {
      const card = btn.closest('.card');
      const productId = `product-${index + 1}`;
      const productName = card.querySelector('.card-title').textContent;
      const productImage = card.querySelector('.card-img img').src;
      const productPrice = card.querySelector('.card-price').textContent;
      const productLocation = card.querySelector('.card-meta span:first-child').textContent;
      
      // 检查是否已收藏
      if (isFavorited(productId)) {
        btn.classList.add('liked');
        btn.textContent = '♥';
      }
      
      // 点击心形按钮的处理
      btn.addEventListener('click', function(e) {
        e.stopPropagation(); // 阻止冒泡到卡片click事件
        
        const isFav = toggleFavorite(productId, productName, productImage, productPrice, productLocation);
        if (isFav) {
          btn.classList.add('liked');
          btn.textContent = '♥';
        } else {
          btn.classList.remove('liked');
          btn.textContent = '♡';
        }
      });
    });
  }
</script>
