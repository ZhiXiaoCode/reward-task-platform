<template>
	<view class="notifications-container">
		<scroll-view class="list-scroll" scroll-y @scrolltolower="loadMore">
			<view class="notification-list">
				<view 
					class="notification-item" 
					v-for="item in notifications" 
					:key="item.id"
					:class="{unread: !item.is_read}"
					@click="markAsRead(item)"
				>
					<view class="notification-icon">
						<text class="iconfont icon-bell"></text>
					</view>
					<view class="notification-content">
						<view class="notification-header">
							<text class="notification-title">{{ item.title }}</text>
							<text class="notification-time">{{ formatTime(item.created_at) }}</text>
						</view>
						<text class="notification-body">{{ item.content }}</text>
						<view class="unread-dot" v-if="!item.is_read"></view>
					</view>
				</view>
			</view>

			<view class="loading-more" v-if="loading">
				<text>加载中...</text>
			</view>
			<view class="no-more" v-if="!hasMore && notifications.length > 0">
				<text>没有更多了</text>
			</view>
			<view class="empty-state" v-if="!loading && notifications.length === 0">
				<text class="iconfont icon-empty"></text>
				<text class="empty-text">暂无通知</text>
			</view>
		</scroll-view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			notifications: [],
			page: 1,
			pageSize: 20,
			hasMore: true,
			loading: false
		}
	},
	onLoad() {
		this.loadNotifications()
	},
	onShow() {
		this.refreshNotifications()
	},
	methods: {
		async loadNotifications() {
			if (this.loading) return
			
			try {
				this.loading = true
				const res = await api.notification.getList({
					page: this.page,
					page_size: this.pageSize
				})
				if (res.code === 1) {
					if (this.page === 1) {
						this.notifications = res.data.items || []
					} else {
						this.notifications = [...this.notifications, ...(res.data.items || [])]
					}
					this.hasMore = res.data.items && res.data.items.length >= this.pageSize
				}
			} catch (e) {
				console.error('获取通知失败:', e)
			} finally {
				this.loading = false
			}
		},
		async refreshNotifications() {
			this.page = 1
			this.hasMore = true
			await this.loadNotifications()
		},
		loadMore() {
			if (this.hasMore && !this.loading) {
				this.page++
				this.loadNotifications()
			}
		},
		async markAsRead(item) {
			if (item.is_read) return
			
			try {
				await api.notification.markAsRead(item.id)
				item.is_read = true
			} catch (e) {
				console.error('标记已读失败:', e)
			}
		},
		formatTime(timeStr) {
			if (!timeStr) return ''
			const date = new Date(timeStr)
			return `${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
		}
	}
}
</script>

<style lang="scss" scoped>
.notifications-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.list-scroll {
	height: 100vh;
}

.notification-list {
	padding: 20rpx;
}

.notification-item {
	display: flex;
	background: #fff;
	border-radius: 16rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	position: relative;
	
	&.unread {
		background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
	}
	
	.notification-icon {
		width: 80rpx;
		height: 80rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 20rpx;
		
		.iconfont {
			font-size: 36rpx;
			color: #fff;
		}
	}
	
	.notification-content {
		flex: 1;
		
		.notification-header {
			display: flex;
			justify-content: space-between;
			margin-bottom: 12rpx;
			
			.notification-title {
				font-size: 28rpx;
				font-weight: bold;
				color: #333;
			}
			
			.notification-time {
				font-size: 22rpx;
				color: #999;
			}
		}
		
		.notification-body {
			font-size: 26rpx;
			color: #666;
			line-height: 1.5;
		}
		
		.unread-dot {
			position: absolute;
			top: 30rpx;
			right: 30rpx;
			width: 16rpx;
			height: 16rpx;
			background: #ff4d4f;
			border-radius: 50%;
		}
	}
}

.loading-more, .no-more {
	text-align: center;
	padding: 30rpx;
	color: #999;
	font-size: 26rpx;
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 100rpx 0;
	
	.iconfont {
		font-size: 120rpx;
		color: #ddd;
		margin-bottom: 30rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}
</style>
