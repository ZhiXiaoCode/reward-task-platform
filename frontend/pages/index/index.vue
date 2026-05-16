<template>
	<view class="index-container">
		<!-- 顶部搜索区域 -->
		<view class="search-bar">
			<view class="search-box" @click="goToSearch">
				<text class="iconfont icon-search"></text>
				<text class="placeholder">搜索任务</text>
			</view>
			<text class="message-icon iconfont icon-message" @click="goToMessage"></text>
		</view>

		<!-- 用户信息卡片 -->
		<view class="user-card" v-if="userInfo">
			<view class="user-info">
				<image :src="userInfo.avatar || '/static/default-avatar.png'" class="avatar"></image>
				<view class="info">
					<text class="nickname">{{ userInfo.nickname }}</text>
					<text class="balance">余额: ¥{{ userInfo.balance || 0 }}</text>
				</view>
			</view>
			<button class="publish-btn" @click="goToPublish">发布任务</button>
		</view>

		<!-- 任务分类 -->
		<view class="category-section">
			<view class="section-title">
				<text>任务分类</text>
				<text class="more" @click="goToTaskList">更多 ></text>
			</view>
			<scroll-view class="category-scroll" scroll-x>
				<view 
					class="category-item" 
					v-for="item in categories" 
					:key="item.id"
					@click="goToCategory(item.id)"
				>
					<image :src="item.icon" class="category-icon"></image>
					<text class="category-name">{{ item.name }}</text>
					<text class="task-count">{{ item.task_count }}个任务</text>
				</view>
			</scroll-view>
		</view>

		<!-- 推荐任务 -->
		<view class="task-section">
			<view class="section-title">
				<text>推荐任务</text>
				<text class="more" @click="goToTaskList">更多 ></text>
			</view>
			
			<view class="task-list">
				<view 
					class="task-item" 
					v-for="task in tasks" 
					:key="task.id"
					@click="goToTaskDetail(task.id)"
				>
					<view class="task-header">
						<text class="task-title">{{ task.title }}</text>
						<view class="task-reward">
							<text class="money">+{{ task.reward }}</text>
							<text class="unit">元</text>
						</view>
					</view>
					<view class="task-body">
						<text class="task-desc">{{ task.description }}</text>
					</view>
					<view class="task-footer">
						<view class="task-info">
							<text class="category-tag">{{ task.category_name }}</text>
							<text class="views">{{ task.views }}人浏览</text>
						</view>
						<button class="accept-btn">立即接单</button>
					</view>
				</view>
			</view>

			<view class="loading-more" v-if="loading">
				<text>加载中...</text>
			</view>
			<view class="no-more" v-if="!hasMore && tasks.length > 0">
				<text>没有更多了</text>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			userInfo: null,
			categories: [],
			tasks: [],
			page: 1,
			pageSize: 10,
			hasMore: true,
			loading: false
		}
	},
	onLoad() {
		this.checkLogin()
		this.loadCategories()
		this.loadTasks()
	},
	onShow() {
		this.getUserInfo()
	},
	onReachBottom() {
		if (this.hasMore && !this.loading) {
			this.loadMore()
		}
	},
	methods: {
		checkLogin() {
			const userInfo = uni.getStorageSync('user_info')
			if (!userInfo) {
				uni.reLaunch({
					url: '/pages/login/login'
				})
			} else {
				this.userInfo = userInfo
			}
		},
		async getUserInfo() {
			try {
				const res = await api.user.getProfile()
				if (res.code === 1) {
					this.userInfo = res.data
					uni.setStorageSync('user_info', res.data)
				}
			} catch (e) {
				console.error('获取用户信息失败:', e)
			}
		},
		async loadCategories() {
			try {
				const res = await api.task.getCategories()
				if (res.code === 1) {
					this.categories = res.data.categories || []
				}
			} catch (e) {
				console.error('获取分类失败:', e)
			}
		},
		async loadTasks() {
			try {
				this.loading = true
				const res = await api.task.getList({
					page: this.page,
					page_size: this.pageSize
				})
				if (res.code === 1) {
					this.tasks = res.data.items || []
					this.hasMore = res.data.items.length >= this.pageSize
				}
			} catch (e) {
				console.error('获取任务列表失败:', e)
			} finally {
				this.loading = false
			}
		},
		async loadMore() {
			this.page++
			this.loading = true
			try {
				const res = await api.task.getList({
					page: this.page,
					page_size: this.pageSize
				})
				if (res.code === 1) {
					this.tasks = [...this.tasks, ...(res.data.items || [])]
					this.hasMore = res.data.items.length >= this.pageSize
				}
			} catch (e) {
				console.error('加载更多失败:', e)
			} finally {
				this.loading = false
			}
		},
		goToSearch() {
			uni.navigateTo({
				url: '/pages/task/search'
			})
		},
		goToMessage() {
			uni.navigateTo({
				url: '/pages/my/messages'
			})
		},
		goToPublish() {
			uni.navigateTo({
				url: '/pages/task/create'
			})
		},
		goToCategory(categoryId) {
			uni.navigateTo({
				url: `/pages/task/list?category_id=${categoryId}`
			})
		},
		goToTaskList() {
			uni.switchTab({
				url: '/pages/task/list'
			})
		},
		goToTaskDetail(taskId) {
			uni.navigateTo({
				url: `/pages/task/detail?id=${taskId}`
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.index-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.search-bar {
	display: flex;
	align-items: center;
	padding: 20rpx 30rpx;
	background: #fff;
	
	.search-box {
		flex: 1;
		display: flex;
		align-items: center;
		height: 70rpx;
		padding: 0 30rpx;
		background: #f5f5f5;
		border-radius: 35rpx;
		
		.icon-search {
			color: #999;
			margin-right: 10rpx;
		}
		
		.placeholder {
			color: #999;
			font-size: 28rpx;
		}
	}
	
	.message-icon {
		margin-left: 30rpx;
		font-size: 48rpx;
		color: #666;
	}
}

.user-card {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 30rpx;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	margin: 20rpx;
	border-radius: 20rpx;
	
	.user-info {
		display: flex;
		align-items: center;
		
		.avatar {
			width: 100rpx;
			height: 100rpx;
			border-radius: 50%;
			margin-right: 20rpx;
		}
		
		.info {
			display: flex;
			flex-direction: column;
			
			.nickname {
				font-size: 32rpx;
				font-weight: bold;
				color: #fff;
				margin-bottom: 10rpx;
			}
			
			.balance {
				font-size: 26rpx;
				color: rgba(255, 255, 255, 0.8);
			}
		}
	}
	
	.publish-btn {
		padding: 16rpx 30rpx;
		background: #fff;
		color: #667eea;
		font-size: 28rpx;
		border-radius: 30rpx;
	}
}

.category-section {
	padding: 20rpx;
	background: #fff;
	margin-bottom: 20rpx;
	
	.section-title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx 0;
		
		text:first-child {
			font-size: 32rpx;
			font-weight: bold;
		}
		
		.more {
			font-size: 26rpx;
			color: #999;
		}
	}
	
	.category-scroll {
		white-space: nowrap;
	}
	
	.category-item {
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		width: 180rpx;
		margin-right: 20rpx;
		padding: 20rpx;
		background: #f5f5f5;
		border-radius: 16rpx;
		
		.category-icon {
			width: 80rpx;
			height: 80rpx;
			margin-bottom: 10rpx;
		}
		
		.category-name {
			font-size: 28rpx;
			font-weight: bold;
			margin-bottom: 8rpx;
		}
		
		.task-count {
			font-size: 22rpx;
			color: #999;
		}
	}
}

.task-section {
	padding: 20rpx;
	background: #fff;
	
	.section-title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx 0;
		
		text:first-child {
			font-size: 32rpx;
			font-weight: bold;
		}
		
		.more {
			font-size: 26rpx;
			color: #999;
		}
	}
	
	.task-list {
		.task-item {
			padding: 30rpx;
			background: #f9f9f9;
			border-radius: 16rpx;
			margin-bottom: 20rpx;
			
			.task-header {
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
				margin-bottom: 16rpx;
				
				.task-title {
					flex: 1;
					font-size: 30rpx;
					font-weight: bold;
					margin-right: 20rpx;
				}
				
				.task-reward {
					display: flex;
					align-items: baseline;
					
					.money {
						font-size: 40rpx;
						font-weight: bold;
						color: #ff6b6b;
					}
					
					.unit {
						font-size: 24rpx;
						color: #ff6b6b;
						margin-left: 5rpx;
					}
				}
			}
			
			.task-body {
				margin-bottom: 16rpx;
				
				.task-desc {
					font-size: 26rpx;
					color: #666;
					line-height: 1.5;
				}
			}
			
			.task-footer {
				display: flex;
				justify-content: space-between;
				align-items: center;
				
				.task-info {
					display: flex;
					align-items: center;
					
					.category-tag {
						padding: 8rpx 16rpx;
						background: #667eea;
						color: #fff;
						font-size: 22rpx;
						border-radius: 8rpx;
						margin-right: 16rpx;
					}
					
					.views {
						font-size: 24rpx;
						color: #999;
					}
				}
				
				.accept-btn {
					padding: 16rpx 40rpx;
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: #fff;
					font-size: 28rpx;
					border-radius: 30rpx;
				}
			}
		}
	}
	
	.loading-more, .no-more {
		text-align: center;
		padding: 30rpx;
		color: #999;
		font-size: 26rpx;
	}
}
</style>
