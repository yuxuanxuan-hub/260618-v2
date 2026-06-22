$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Out = Join-Path $Root "islandtrace-app.html"
$Utf8 = New-Object System.Text.UTF8Encoding $false

function Read-Utf8($path) {
    [System.IO.File]::ReadAllText($path, $Utf8)
}

function Get-Body($file) {
    $html = Read-Utf8 (Join-Path $Root $file)
    if ($html -match '(?s)<body[^>]*>(.*?)</body>') { return $Matches[1].Trim() }
    return ""
}

function Strip-NavFooter($body) {
    $body = $body -replace '(?s)<!--[^>]*NAV[^>]*-->\s*', ''
    $body = $body -replace '(?s)<nav[\s\S]*?</nav>', ''
    $body = $body -replace '(?s)<footer[\s\S]*?</footer>', ''
    return $body.Trim()
}

function Strip-Scripts($body) {
    while ($body -match '(?s)<script[\s\S]*?</script>') {
        $body = $body -replace '(?s)<script[\s\S]*?</script>', ''
    }
    return $body.Trim()
}

function Get-Script($file) {
    $html = Read-Utf8 (Join-Path $Root $file)
    if ($html -match '(?s)<script>(.*?)</script>') { return $Matches[1].Trim() }
    return ""
}

function Get-Style($file) {
    $html = Read-Utf8 (Join-Path $Root $file)
    if ($html -match '(?s)<style>(.*?)</style>') { return $Matches[1].Trim() }
    return ""
}

$indexCss = Get-Style "index.html"
$extraCss = Read-Utf8 (Join-Path $Root "app-extra.css")
$nav = (Read-Utf8 (Join-Path $Root "_nav.html")).Trim()
$footer = (Read-Utf8 (Join-Path $Root "_footer.html")).Trim()
$routerJs = Read-Utf8 (Join-Path $Root "app-router.js")

$indexBody = Strip-Scripts (Strip-NavFooter (Get-Body "index.html"))
$indexBody = $indexBody -replace 'class="view-all">', 'class="view-all" data-go="products">'
$indexBody = $indexBody -replace 'class="btn-outline">了解更多</button>', 'class="btn-outline" data-go="about">了解更多</button>'

$productsBody = Strip-Scripts (Strip-NavFooter (Get-Body "products.html")) -replace 'href="index\.html"', 'href="#" data-go="index"'
$aboutBody = Strip-Scripts (Strip-NavFooter (Get-Body "about.html")) -replace 'class="btn-primary">探索所有體驗</a>', 'class="btn-primary" data-go="products">探索所有體驗</a>'
$faqBody = Strip-Scripts (Strip-NavFooter (Get-Body "faq.html")) -replace '(?s)^\s*<main>\s*', '' -replace '(?s)\s*</main>\s*$', ''
$profileBody = Strip-Scripts (Strip-NavFooter (Get-Body "profile-1.html")) -replace 'switchTab\(', 'switchProfileTab('
$loginBody = Strip-Scripts (Strip-NavFooter (Get-Body "login.html"))
$detailBody = Strip-Scripts (Strip-NavFooter (Get-Body "product-detail.html")) -replace 'href="index\.html"', 'href="#" data-go="index"' -replace 'class="book-btn" onclick="bookNow\(\)"', 'class="book-btn" id="btn-book-now"'
$bookingBody = Strip-Scripts (Strip-NavFooter (Get-Body "booking.html"))
$bookingBody = $bookingBody -replace 'class="booking-body single"', 'class="booking-body"'
$bookingBody = $bookingBody -replace 'id="page-step1" class="page active"', 'id="page-step1" class="booking-page active"'
$bookingBody = $bookingBody -replace 'id="page-step2" class="page"', 'id="page-step2" class="booking-page"'
$bookingBody = $bookingBody -replace 'id="page-success" class="page"', 'id="page-success" class="booking-page"'
$bookingBody = $bookingBody -replace 'onclick="alert\(''返回首頁[^'']*''\)"', 'id="btn-success-home"'
$bookingBody = $bookingBody -replace 'onclick="alert\(''查看我的訂單[^'']*''\)"', 'id="btn-success-orders"'

# Rename booking step cards only (inside view-booking, first occurrence in step1)
$bookingBody = $bookingBody -replace '(?s)(<div id="page-step1"[\s\S]*?<div class="booking-body[\s\S]*?)class="booking-card"', '$1class="booking-card-inner"'
$bookingBody = $bookingBody -replace 'class="booking-card" style="margin-bottom: 20px;"', 'class="booking-card-inner" style="margin-bottom: 20px;"'
$bookingBody = $bookingBody -replace '(?s)(<div id="page-step2"[\s\S]*?)class="booking-card"', '$1class="booking-card-inner"'

$productsJs = (Get-Script "products.html") + "`nfunction applyThemeFilter(theme){document.querySelectorAll('#theme-tags .tag-btn').forEach(b=>b.classList.toggle('active',b.dataset.theme===theme));filterCards();}"
$detailJs = (Get-Script "product-detail.html") -replace 'function updateDisplay\(\)', 'function updateQtyDisplay()' -replace 'updateDisplay\(\)', 'updateQtyDisplay()' -replace '(?s)function bookNow\(\)[\s\S]*?\}\s*', ''
$bookingJs = (Get-Script "booking.html") -replace 'function showPage\(', 'function showBookingStep(' -replace 'showPage\(', 'showBookingStep(' -replace '(?s)\r?\n\s*/\* ---- Init ---- \*/[\s\S]*$', '' -replace "querySelectorAll\('\.page'\)", "querySelectorAll('.booking-page')"
$faqJs = Get-Script "faq.html"
$profileJs = (Get-Script "profile-1.html") -replace 'switchTab', 'switchProfileTab'
$loginJs = (Get-Script "login.html") -replace 'function switchTab\(', 'function switchLoginTab(' -replace 'switchTab\(', 'switchLoginTab('

$html = @"
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>島嶼旅跡 IslandTrace</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600;700;900&family=Noto+Sans+TC:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
$indexCss
$extraCss
  </style>
</head>
<body>
$nav
<div id="view-index" class="view active">$indexBody</div>
<div id="view-products" class="view">$productsBody</div>
<div id="view-about" class="view">$aboutBody</div>
<div id="view-faq" class="view">$faqBody</div>
<div id="view-profile" class="view">$profileBody</div>
<div id="view-login" class="view">$loginBody</div>
<div id="view-detail" class="view">$detailBody</div>
<div id="view-booking" class="view">$bookingBody</div>
$footer
<script>
$routerJs
$productsJs
$detailJs
$bookingJs
function initFaq(){document.querySelectorAll('#view-faq .tab-btn').forEach(btn=>{btn.onclick=()=>{document.querySelectorAll('#view-faq .tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('#view-faq .faq-section').forEach(s=>s.classList.remove('active'));btn.classList.add('active');document.getElementById(btn.dataset.target).classList.add('active');};});}
$faqJs
$profileJs
$loginJs
function initAboutReveal(){document.querySelectorAll('#view-about .reveal').forEach(el=>{const o=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');o.unobserve(e.target);}});},{threshold:.12});o.observe(el);});}
</script>
</body>
</html>
"@

$html = $html -replace 'href="index\.html"', 'href="#" data-go="index"'
$html = $html -replace '<a href="#">探索體驗</a>', '<a href="#" data-go="products">探索體驗</a>'

[System.IO.File]::WriteAllText($Out, $html, $Utf8)
Write-Host "Written $Out ($($html.Length) bytes)"
