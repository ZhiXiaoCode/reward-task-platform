<template>
	<view class="task-list-container">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-box" @click="goToSearch">
				<text class="iconfont icon-search"></text>
				<text class="placeholder">搜索任务</text>
			</view>
		</view>

		<!-- 分类标签 -->
		<view class="category-tabs">
			<scroll-view class="tabs-scroll" scroll-x>
				<view 
					class="tab-item" 
					:class="{active: currentCategory === 0}"
					@click="changeCategory(0)"
				>
					全部
				</view>
				<view 
					class="tab-item" 
					v-for="cat in categories" 
					:key="cat.id"
					:class="{active: currentCategory === cat.id}"
					@click="changeCategory(cat.id)"
				>
					{{ cat.name }}
				</view>
			</scroll-view>
		</view>

		<!-- 任务列表 -->
		<scroll-view 
			class="task-scroll" 
			scroll-y 
			@scrolltolower="loadMore"
		>
			<view class="task-list">
				<view 
					class="task-item" 
					v-for="task in tasks" 
					:key="task.id"
					@click="goToDetail(task.id)"
				>
					<view class="task-header">
						<view class="task-info">
							<text class="task-title">{{ task.title }}</text>
							<view class="task-tags">
								<text class="category-tag">{{ task.category_name }}</text>
								<text class="views-tag">{{ task.views }}人浏览</text>
							</view>
						</view>
						<view class="task-reward">
							<text class="money">+{{ task.reward }}</text>
							<text class="unit">元</text>
						</view>
					</view>
					
					<view class="task-desc">
						<text>{{ task.description }}</text>
					</view>
					
					<view class="task-footer">
						<view class="task-meta">
							<text class="publisher">发布者：{{ task.publisher_nickname }}</text>
							<text class="time">{{ formatTime(task.created_at) }}</text>
						</view>
						<button class="accept-btn" @click.stop="acceptTask(task.id)">
							立即接单
						</button>
					</view>
				</view>
			</view>

			<!-- 加载状态 -->
			<view class="loading-more" v-if="loading">
				<text>加载中...</text>
			</view>
			<view class="no-more" v-if="!hasMore && tasks.length > 0">
				<text>没有更多任务了</text>
			</view>
			<view class="empty-state" v-if="!loading && tasks.length === 0">
				<text class="iconfont icon-empty"></text>
				<text class="empty-text">暂无任务</text>
				<button class="refresh-btn" @click="loadTasks">刷新试试</button>
			</view>
		</scroll-view>

		<!-- 发布任务按钮 -->
		<view class="publish-btn-fixed" @click="goToPublish">
			<text class="iconfont icon-add"></text>
			<text>发布任务</text>
		</view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			categories: [],
			tasks: [],
			currentCategory: 0,
			page: 1,
			pageSize: 10,
			hasMore: true,
			loading: false
		}
	},
	onLoad() {
		this.loadCategories()
		this.loadTasks()
	},
	onShow() {
		this.refreshTasks()
	},
	methods: {
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
			if (this.loading) return
			
			try {
				this.loading = true
				const params = {
					page: this.page,
					page_size: this.pageSize
				}
				
				if (this.currentCategory > 0) {
					params.category_id = this.currentCategory
				}
				
				const res = await api.task.getList(params)
				if (res.code === 1) {
					if (this.page === 1) {
						this.tasks = res.data.items || []
					} else {
						this.tasks = [...this.tasks, ...(res.data.items || [])]
					}
					this.hasMore = res.data.items && res.data.items.length >= this.pageSize
				}
			} catch (e) {
				console.error('获取任务列表失败:', e)
			} finally {
				this.loading = false
			}
		},
		async refreshTasks() {
			this.page = 1
			this.hasMore = true
			await this.loadTasks()
		},
		loadMore() {
			if (this.hasMore && !this.loading) {
				this.page++
				this.loadTasks()
			}
		},
		changeCategory(categoryId) {
			this.currentCategory = categoryId
			this.refreshTasks()
		},
		goToSearch() {
			uni.navigateTo({
				url: '/pages/task/search'
			})
		},
		goToDetail(taskId) {
			uni.navigateTo({
				url: `/pages/task/detail?id=${taskId}`
			})
		},
		goToPublish() {
			this.checkLoginAndNavigate('/pages/task/create')
		},
		async acceptTask(taskId) {
			if (!this.checkLogin()) {
				return
			}
			
			try {
				const res = await api.task.accept(taskId)
				if (res.code === 1) {
					uni.showToast({
						title: '接单成功',
						icon: 'success'
					})
					setTimeout(() => {
						this.goToDetail(taskId)
					}, 1500)
				}
			} catch (e) {
				console.error('接单失败:', e)
			}
		},
		checkLogin() {
			const token = uni.getStorageSync('access_token')
			if (!token) {
				uni.showToast({
					title: '请先登录',
					icon: 'none'
				})
				setTimeout(() => {
					uni.navigateTo({
						url: '/pages/login/login'
					})
				}, 1500)
				return false
			}
			return true
		},
		checkLoginAndNavigate(url) {
			if (this.checkLogin()) {
				uni.navigateTo({ url })
			}
		},
		formatTime(timeStr) {
			if (!timeStr) return ''
			const date = new Date(timeStr)
			const now = new Date()
			const diff = now - date
			
			if (diff < 60000) return '刚刚'
			if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
			if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
			if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
			
			return `${date.getMonth() + 1}-${date.getDate()}`
		}
	}
}
</script>

<style lang="scss" scoped>
.task-list-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.search-bar {
	padding: 20rpx 30rpx;
	background: #fff;
	
	.search-box {
		display: flex;
		align-items: center;
		height: 70rpx;
		padding: 0 30rpx;
		background: #f5f5f5;
		border-radius: 35rpx;
		
		.iconfont {
			color: #999;
			margin-right: 10rpx;
		}
		
		.placeholder {
			color: #999;
			font-size: 28rpx;
		}
	}
}

.category-tabs {
	background: #fff;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #eee;
	
	.tabs-scroll {
		white-space: nowrap;
	}
	
	.tab-item {
		display: inline-block;
		padding: 16rpx 30rpx;
		margin: 0 10rpx;
		font-size: 28rpx;
		color: #666;
		background: #f5f5f5;
		border-radius: 30rpx;
		
		&.active {
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #fff;
		}
	}
}

.task-scroll {
	height: calc(100vh - 280rpx);
}

.task-list {
	padding: 20rpx;
}

.task-item {
	background: #fff;
	border-radius: 16rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.task-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 20rpx;
		
		.task-info {
			flex: 1;
			margin-right: 20rpx;
			
			.task-title {
				font-size: 32rpx;
				font-weight: bold;
				color: #333;
				display: block;
				margin-bottom: 12rpx;
			}
			
			.task-tags {
				display: flex;
				align-items: center;
				
				.category-tag {
					padding: 6rpx 16rpx;
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: #fff;
					font-size: 22rpx;
					border-radius: 6rpx;
					margin-right: 12rpx;
				}
				
				.views-tag {
					font-size: 24rpx;
					color: #999;
				}
			}
		}
		
		.task-reward {
			display: flex;
			align-items: baseline;
			
			.money {
				font-size: 44rpx;
				font-weight: bold;
				color: #ff6b6b;
			}
			
			.unit {
				font-size: 24rpx;
				color: #ff6b6b;
				margin-left: 4rpx;
			}
		}
	}
	
	.task-desc {
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
		margin-bottom: 20rpx;
		
		text {
			display: -webkit-box;
			-webkit-line-clamp: 2;
			-webkit-box-orient: vertical;
			overflow: hidden;
		}
	}
	
	.task-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		
		.task-meta {
			display: flex;
			flex-direction: column;
			
			.publisher {
				font-size: 24rpx;
				color: #999;
				margin-bottom: 6rpx;
			}
			
			.time {
				font-size: 22rpx;
				color: #ccc;
			}
		}
		
		.accept-btn {
			padding: 16rpx 40rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #fff;
			font-size: 28rpx;
			border-radius: 30rpx;
			border: none;
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
		margin-bottom: 40rpx;
	}
	
	.refresh-btn {
		padding: 20rpx 60rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #fff;
		font-size: 28rpx;
		border-radius: 40rpx;
	}
}

.publish-btn-fixed {
	position: fixed;
	right: 30rpx;
	bottom: 150rpx;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 24rpx 30rpx;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: #fff;
	border-radius: 50rpx;
	box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.3);
	
	.iconfont {
		font-size: 48rpx;
		margin-bottom: 8rpx;
	}
	
	text {
		font-size: 24rpx;
	}
}
</style>
