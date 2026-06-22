# Implementation Plan - IslandTrace Single HTML App Bundling & Polish

This plan outlines the changes required to bundle all pages of the IslandTrace app into a single HTML file (`islandtrace-app.html`) with cohesive routing, layout fixes, and dynamic features (favorites, booking step linkage, and back history navigation).

## User Review Required

> [!IMPORTANT]
> The single-page application (SPA) shell uses custom DOM routing to hide/show views. All pages (except `login`) will share the standard Navigation and Footer templates unified with `index.html`.

## Proposed Changes

### [Shared Layouts]

#### [MODIFY] [_nav.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/_nav.html)
- Ensure all navigation buttons point to the correct routes:
  - "探索體驗" -> `products` (`data-go="products"`)
  - "關於我們" -> `about` (`data-go="about"`)
  - "常見問題" -> `faq` (`data-go="faq"`)
  - "我的訂單" -> `profile-1` (`data-go="profile-1"`)
  - "登入/註冊" -> `login` (`data-go="login"`)

#### [MODIFY] [_footer.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/_footer.html)
- Update footer link targets:
  - "所有體驗" -> `products` (`data-go="products"`)
  - "戶外冒險" -> `products` with "戶外" filter (`data-go="products" data-theme="戶外"`)
  - "手作工藝" -> `products` with "手作" filter (`data-go="products" data-theme="手作"`)
  - "美食料理" -> `products` with "美食" filter (`data-go="products" data-theme="美食"`)
  - "文化歷史" -> `products` with "文化" filter (`data-go="products" data-theme="文化"`)
  - "關於我們" -> `about` (`data-go="about"`)
  - "常見問答" -> `faq` (`data-go="faq"`)
  - "查看訂單" -> `profile-1` (`data-go="profile-1"`)
  - Other generic footer links -> `index` (`data-go="index"`)

---

### [Homepage]

#### [MODIFY] [index.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/index.html)
- Change `<div class="card-fav">` elements to `<button class="card-fav">` tags.
- Bind the heart button to add the experience to "我的收藏" (My Favorites) in `profile-1`.
- Ensure clicking on a card navigates to `product-detail` (`data-go="product-detail"`).

---

### [Products Page]

#### [MODIFY] [products.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/products.html)
- Bind the heart/favorite icon click event to add the experience to "我的收藏" in `profile-1`.
- Ensure clicking on a card navigates to `product-detail`.

---

### [Product Detail Page]

#### [MODIFY] [product-detail.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/product-detail.html)
- Pass the selected "參加人數" (participant count) and "總金額" (total price) to the booking page when clicking "立刻預定".
- Ensure "立刻預定" navigates to the booking view.

---

### [Booking Page]

#### [MODIFY] [booking.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/booking.html)
- Fix the calendar date grid layout by replacing responsive flex rules with stable, fixed sizing (e.g., `width: 36px; height: 36px; line-height: 36px;`) so the grid remains aligned.
- In Step 2, add a "← 返回上一步" (Back to Step 1) button to navigate back to Step 1.
- In Step 1, add a "← 返回商品詳情" (Back to Product Detail) button to navigate back to `product-detail`.
- Synchronize participant count and total amount in Step 2 summary card and Success page based on data passed from `product-detail`.

---

### [About Us Page]

#### [MODIFY] [about.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/about.html)
- Ensure the "探索所有體驗" button navigates to the `products` view (`data-go="products"`).

---

### [Profile Page]

#### [MODIFY] [profile-1.html](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/profile-1.html)
- Create a container element inside the "我的收藏" panel to display favorited items dynamically.
- Implement JavaScript logic to render cards of favorited items with links to `product-detail`.
- Hide the default "還沒有收藏的體驗..." message when there is at least one favorited item.

---

### [App Router & Bundle Script]

#### [MODIFY] [app-router.js](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/app-router.js)
- Update page routing identifiers: rename `profile` to `profile-1` and `detail` to `product-detail`.
- Store routing history to support returning to previous views.
- Provide a global state object `App.state` to hold favorites data and booking details.

#### [MODIFY] [build_app.py](file:///c:/Users/H310/OneDrive/文件/GitHub/260618-v2/build_app.py)
- Update code injection to align with the new requirements:
  - Inject unified `_nav.html` and `_footer.html` into the bundle.
  - Exclude Nav/Footer from `login` view.
  - Implement full layout/CSS replacements.
  - Integrate global script handlers for favorites and page state sync.

## Verification Plan

### Automated Tests
- Run `python build_app.py` to compile `islandtrace-app.html`.
- Run local check scripts to verify file sizes and contents.

### Manual Verification
- Open the compiled page in the browser.
- Verify Nav & Footer display correctly on all pages except `login`.
- Click nav links to ensure page transitions (`index` -> `products` -> `about` -> `faq` -> `profile-1` -> `login`).
- Verify favoriting a card on index/products page dynamically adds it to "我的收藏" panel and toggles heart states.
- Click a card, select a quantity and verify correct price totals are propagated to booking step 2 and success screens.
- Test step 2 -> step 1 -> product detail back buttons.
- Confirm calendar date picker renders correctly and dates align cleanly with columns.
