// ==================== 收藏管理系統 ====================

// 初始化收藏數據（從localStorage讀取，如果沒有則使用空數組）
function initFavorites() {
  if (!localStorage.getItem('favorites')) {
    localStorage.setItem('favorites', JSON.stringify([]));
  }
}

// 獲取所有收藏
function getFavorites() {
  initFavorites();
  return JSON.parse(localStorage.getItem('favorites')) || [];
}

// 添加收藏
function addFavorite(productId, productName, productImage, productPrice, productLocation) {
  const favorites = getFavorites();
  
  // 檢查是否已存在
  const exists = favorites.find(fav => fav.id === productId);
  if (!exists) {
    favorites.push({
      id: productId,
      name: productName,
      image: productImage,
      price: productPrice,
      location: productLocation,
      addedDate: new Date().toISOString()
    });
    localStorage.setItem('favorites', JSON.stringify(favorites));
    return true;
  }
  return false;
}

// 移除收藏
function removeFavorite(productId) {
  const favorites = getFavorites();
  const filtered = favorites.filter(fav => fav.id !== productId);
  localStorage.setItem('favorites', JSON.stringify(filtered));
}

// 檢查是否已收藏
function isFavorited(productId) {
  const favorites = getFavorites();
  return favorites.some(fav => fav.id === productId);
}

// 切換收藏狀態
function toggleFavorite(productId, productName, productImage, productPrice, productLocation) {
  if (isFavorited(productId)) {
    removeFavorite(productId);
    return false;
  } else {
    addFavorite(productId, productName, productImage, productPrice, productLocation);
    return true;
  }
}

// ==================== 產品數據 ====================

const productsData = [
  {
    id: 'product-1',
    name: '清水斷崖獨木舟探險',
    category: '戶外',
    location: '花蓮',
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=75',
    price: 1800,
    time: '半天',
    rating: 5,
    reviews: 312
  },
  {
    id: 'product-2',
    name: '九份老街手捏陶藝體驗',
    category: '手作',
    location: '新北',
    image: 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=600&q=75',
    price: 980,
    time: '3小時',
    rating: 4.5,
    reviews: 205
  },
  {
    id: 'product-3',
    name: '台中市場私廚料理課',
    category: '美食',
    location: '台中',
    image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=75',
    price: 1500,
    time: '4小時',
    rating: 4.5,
    reviews: 189
  },
  {
    id: 'product-4',
    name: '阿里山日出觀星嚮導',
    category: '戶外',
    location: '嘉義',
    image: 'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600&q=75',
    price: 2200,
    time: '全天',
    rating: 5,
    reviews: 98
  },
  {
    id: 'product-5',
    name: '淡水老街藍染拼布工作坊',
    category: '手作',
    location: '新北',
    image: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600&q=75',
    price: 1200,
    time: '3小時',
    rating: 4.5,
    reviews: 147
  },
  {
    id: 'product-6',
    name: '台南府城古蹟深度導覽',
    category: '文化',
    location: '台南',
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=75',
    price: 800,
    time: '半天',
    rating: 4.5,
    reviews: 261
  },
  {
    id: 'product-7',
    name: '宜蘭梯田生態農場體驗',
    category: '戶外',
    location: '宜蘭',
    image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=75',
    price: 1100,
    time: '半天',
    rating: 4.5,
    reviews: 173
  },
  {
    id: 'product-8',
    name: '高雄漁港老漁料理日',
    category: '美食',
    location: '高雄',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=75',
    price: 1350,
    time: '4小時',
    rating: 5,
    reviews: 142
  },
  {
    id: 'product-9',
    name: '太魯閣峽谷健行之旅',
    category: '戶外',
    location: '花蓮',
    image: 'https://images.unsplash.com/photo-1434725039720-aaad6dd32dfe?w=600&q=75',
    price: 2500,
    time: '全天',
    rating: 4.5,
    reviews: 287
  },
  {
    id: 'product-10',
    name: '彰化扇形車庫鐵道文化探索',
    category: '文化',
    location: '彰化',
    image: 'https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=600&q=75',
    price: 700,
    time: '2小時',
    rating: 4.5,
    reviews: 118
  },
  {
    id: 'product-11',
    name: '墾丁珊瑚礁浮潛體驗',
    category: '戶外',
    location: '屏東',
    image: 'https://images.unsplash.com/photo-1682686580391-615b1f28e5ee?w=600&q=75',
    price: 1650,
    time: '半天',
    rating: 4.5,
    reviews: 234
  },
  {
    id: 'product-12',
    name: '台北茶道文化靜心體驗',
    category: '文化',
    location: '台北',
    image: 'https://images.unsplash.com/photo-1545315003-c5ad6226c272?w=600&q=75',
    price: 1200,
    time: '2小時',
    rating: 4.5,
    reviews: 196
  }
];

// 根據ID獲取產品
function getProductById(productId) {
  return productsData.find(p => p.id === productId);
}

// 根據分類過濾產品
function getProductsByCategory(category) {
  if (!category) return productsData;
  return productsData.filter(p => p.category === category);
}

// ==================== URL 參數管理 ====================

function getUrlParam(paramName) {
  const params = new URLSearchParams(window.location.search);
  return params.get(paramName);
}

function setUrlParam(paramName, value) {
  const params = new URLSearchParams(window.location.search);
  params.set(paramName, value);
  window.history.replaceState({}, '', `?${params.toString()}`);
}
