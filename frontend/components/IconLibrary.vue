<template>
  <view id="app">
    <!-- 使用 SVG 图标作为主要方案 -->
    <svg style="display: none;">
      <defs>
        <!-- 搜索图标 -->
        <symbol id="icon-search" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="2"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </symbol>
        
        <!-- 消息图标 -->
        <symbol id="icon-message" viewBox="0 0 24 24">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 首页图标 -->
        <symbol id="icon-home" viewBox="0 0 24 24">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" fill="none" stroke="currentColor" stroke-width="2"/>
          <polyline points="9 22 9 12 15 12 15 22" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 任务图标 -->
        <symbol id="icon-task" viewBox="0 0 24 24">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
          <line x1="9" y1="9" x2="15" y2="9" stroke="currentColor" stroke-width="2"/>
          <line x1="9" y1="13" x2="15" y2="13" stroke="currentColor" stroke-width="2"/>
          <line x1="9" y1="17" x2="12" y2="17" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 用户图标 -->
        <symbol id="icon-user" viewBox="0 0 24 24">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" fill="none" stroke="currentColor" stroke-width="2"/>
          <circle cx="12" cy="7" r="4" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 金钱图标 -->
        <symbol id="icon-money" viewBox="0 0 24 24">
          <line x1="12" y1="1" x2="12" y2="23" stroke="currentColor" stroke-width="2"/>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 时间图标 -->
        <symbol id="icon-time" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/>
          <polyline points="12 6 12 12 16 14" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 星星图标 -->
        <symbol id="icon-star" viewBox="0 0 24 24">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 设置图标 -->
        <symbol id="icon-settings" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        
        <!-- 更多图标 -->
        <symbol id="icon-more" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="1" fill="currentColor"/>
          <circle cx="19" cy="12" r="1" fill="currentColor"/>
          <circle cx="5" cy="12" r="1" fill="currentColor"/>
        </symbol>
        
        <!-- 添加图标 -->
        <symbol id="icon-add" viewBox="0 0 24 24">
          <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </symbol>
        
        <!-- 关闭图标 -->
        <symbol id="icon-close" viewBox="0 0 24 24">
          <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </symbol>
        
        <!-- 勾选图标 -->
        <symbol id="icon-check" viewBox="0 0 24 24">
          <polyline points="20 6 9 17 4 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </symbol>
        
        <!-- 微信图标 -->
        <symbol id="icon-wechat" viewBox="0 0 24 24">
          <path d="M8.5 11.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" fill="currentColor"/>
          <path d="M15.5 11.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" fill="currentColor"/>
          <path d="M21.5 5.5c-1.93 0-3.5 1.57-3.5 3.5 0 .77.26 1.48.69 2.06l-.42 1.47-1.46-.49c-.6.2-1.25.31-1.93.31-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5c.68 0 1.33.11 1.93.31l1.46.49.42-1.47c-.43-.58-.69-1.29-.69-2.06 0-1.93 1.57-3.5 3.5-3.5s3.5 1.57 3.5 3.5c0 .34-.05.67-.15.99L21.5 7.5l-1.06-.36c.09-.3.13-.61.13-.93 0-1.37-.68-2.58-1.74-3.34-.05-.03-.1-.07-.15-.1C18.12 2.23 17.5 2 16.79 2c-1.63 0-3.07.8-3.95 2.03L11.5 4l-.95-.32C9.75 2.75 7.98 2 6.06 2 4.03 2 2.33 3.23 1.63 4.96c-.02.06-.04.12-.07.18C.72 6.06.11 7.41.11 8.88c0 3.04 2.47 5.5 5.5 5.5 1.53 0 2.9-.62 3.86-1.62l.5.17.56-1.95c.17.03.35.06.53.06.96 0 1.82-.38 2.47-1.02l1.18 1.97c-.32.49-.51 1.07-.51 1.71 0 .34.07.67.2.98l-1.5.5-1.28-2.13c.1-.3.15-.62.15-.94 0-.87-.35-1.65-.91-2.22-.28-.28-.6-.5-.95-.67l1.14-1.14c.58.38 1.29.61 2.04.61.9 0 1.73-.31 2.38-.84l1.82 1.22c-.11.21-.19.44-.25.67l-1.88-.63.5-1.75c.37.28.86.44 1.37.44 1.24 0 2.25-1.01 2.25-2.25 0-.6-.24-1.14-.62-1.53-.19-.19-.41-.34-.66-.45z" fill="currentColor"/>
        </symbol>
      </defs>
    </svg>
  </view>
</template>

<script>
export default {
  name: 'IconLibrary'
}
</script>
