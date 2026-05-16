<template>
	<view class="my-tasks-container">
		<!-- 任务类型切换 -->
		<view class="tab-bar">
			<view 
				class="tab-item" 
				:class="{active: currentType === 'accepted'}"
				@click="changeType('accepted')"
			>
				我接的任务
			</view>
			<view 
				class="tab-item" 
				:class="{active: currentType === 'published'}"
				@click="changeType('published')"
			>
				我发布的
			</view>
		</view>

		<!-- 任务列表 -->
		<scroll-view class="task-scroll" scroll-y @scrolltolower="loadMore">
			<view class="task-list">
				<view 
					class="task-item" 
					v-for="task in tasks" 
					:key="task.id"
					@click="goToDetail(task.id)"
				>
					<view class="task-header">
						<text class="task-title">{{ task.title }}</text>
						<view class="task-status" :class="'status-' + task.status">
							{{ getStatusText(task.status) }}
						</view>
					</view>
					
					<view class="task-info">
						<view class="info-row">
							<text class="label">分类：</text>
							<text class="value">{{ task.category_name }}</text>
						</view>
						<view class="info-row">
							<text class="label">奖励：</text>
							<text class="value reward">¥{{ task.reward }}</text>
						</view>
						<view class="info-row" v-if="task.worker_nickname && currentType === 'published'">
							<text class="label">接单人：</text>
							<text class="value">{{ task.worker_nickname }}</text>
						</view>
						<view class="info-row">
							<text class="label">发布时间：</text>
							<text class="value">{{ formatTime(task.created_at) }}</text>
						</view>
					</view>

					<!-- 操作按钮 -->
					<view class="task-actions" v-if="task.status === 'submitted' && currentType === 'published'">
						<button class="action-btn pass" @click.stop="verifyTask(task.id, true)">通过</button>
						<button class="action-btn reject" @click.stop="verifyTask(task.id, false)">拒绝</button>
					</view>
				</view>
			</view>

			<!-- 加载状态 -->
			<view class="loading-more" v-if="loading">
				<text>加载中...</text>
			</view>
			<view class="no-more" v-if="!hasMore && tasks.length > 0">
				<text>没有更多了</text>
			</view>
			<view class="empty-state" v-if="!loading && tasks.length === 0">
				<text class="empty-text">暂无任务</text>
				<button class="go-publish-btn" @click="goToPublish" v-if="currentType === 'published'">
					去发布任务
				</button>
			</view>
		</scroll-view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			currentType: 'accepted',
			tasks: [],
			page: 1,
			pageSize: 10,
			hasMore: true,
			loading: false
		}
	},
	onLoad(options) {
		if (options.type) {
			this.currentType = options.type
		}
		this.loadTasks()
	},
	methods: {
		async loadTasks() {
			if (this.loading) return
			
			try {
				this.loading = true
				let res
				if (this.currentType === 'published') {
					res = await api.task.getMyPublished({
						page: this.page,
						page_size: this.pageSize
					})
				} else {
					res = await api.task.getMyAccepted({
						page: this.page,
						page_size: this.pageSize
					})
				}
				
				if (res.code === 1) {
					if (this.page === 1) {
						this.tasks = res.data.items || []
					} else {
						this.tasks = [...this.tasks, ...(res.data.items || [])]
					}
					this.hasMore = res.data.items && res.data.items.length >= this.pageSize
				}
			} catch (e) {
				console.error('获取任务失败:', e)
			} finally {
				this.loading = false
			}
		},
		loadMore() {
			if (this.hasMore && !this.loading) {
				this.page++
				this.loadTasks()
			}
		},
		changeType(type) {
			this.currentType = type
			this.page = 1
			this.hasMore = true
			this.loadTasks()
		},
		getStatusText(status) {
			const statusMap = {
				'pending': '待接单',
				'in_progress': '进行中',
				'submitted': '待审核',
				'completed': '已完成',
				'rejected': '已拒绝',
				'cancelled': '已取消'
			}
			return statusMap[status] || status
		},
		formatTime(timeStr) {
			if (!timeStr) return ''
			const date = new Date(timeStr)
			return `${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
		},
		goToDetail(taskId) {
			uni.navigateTo({
				url: `/pages/task/detail?id=${taskId}`
			})
		},
		goToPublish() {
			uni.navigateTo({
				url: '/pages/task/create'
			})
		},
		async verifyTask(taskId, approved) {
			try {
				const res = await api.task.verify(taskId, {
					approved: approved,
					comment: approved ? '审核通过' : '不符合要求'
				})
				if (res.code === 1) {
					uni.showToast({
						title: approved ? '已通过' : '已拒绝',
						icon: 'success'
					})
					setTimeout(() => {
						this.refreshTasks()
					}, 1500)
				}
			} catch (e) {
				console.error('审核失败:', e)
			}
		},
		async refreshTasks() {
			this.page = 1
			this.hasMore = true
			await this.loadTasks()
		}
	}
}
</script>

<style lang="scss" scoped>
.my-tasks-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.tab-bar {
	display: flex;
	background: #fff;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #eee;
	
	.tab-item {
		flex: 1;
		text-align: center;
		font-size: 28rpx;
		color: #666;
		padding: 16rpx 0;
		position: relative;
		
		&.active {
			color: #667eea;
			font-weight: bold;
			
			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 50%;
				transform: translateX(-50%);
				width: 60rpx;
				height: 6rpx;
				background: #667eea;
				border-radius: 3rpx;
			}
		}
	}
}

.task-scroll {
	height: calc(100vh - 100rpx);
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
		
		.task-title {
			flex: 1;
			font-size: 30rpx;
			font-weight: bold;
			color: #333;
			margin-right: 20rpx;
		}
		
		.task-status {
			padding: 8rpx 16rpx;
			font-size: 22rpx;
			border-radius: 8rpx;
			
			&.status-pending { background: #f0f0f0; color: #666; }
			&.status-in_progress { background: #e6f7ff; color: #1890ff; }
			&.status-submitted { background: #fff7e6; color: #faad14; }
			&.status-completed { background: #f6ffed; color: #52c41a; }
			&.status-rejected { background: #fff1f0; color: #ff4d4f; }
		}
	}
	
	.task-info {
		.info-row {
			display: flex;
			padding: 8rpx 0;
			
			.label {
				font-size: 26rpx;
				color: #999;
				width: 140rpx;
			}
			
			.value {
				font-size: 26rpx;
				color: #333;
				
				&.reward {
					color: #ff6b6b;
					font-weight: bold;
				}
			}
		}
	}
	
	.task-actions {
		display: flex;
		gap: 20rpx;
		margin-top: 20rpx;
		padding-top: 20rpx;
		border-top: 1rpx solid #f0f0f0;
		
		.action-btn {
			flex: 1;
			height: 64rpx;
			line-height: 64rpx;
			font-size: 26rpx;
			border-radius: 32rpx;
			border: none;
			
			&.pass {
				background: #52c41a;
				color: #fff;
			}
			
			&.reject {
				background: #ff4d4f;
				color: #fff;
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

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 100rpx 0;
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
		margin-bottom: 40rpx;
	}
	
	.go-publish-btn {
		padding: 20rpx 60rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #fff;
		font-size: 28rpx;
		border-radius: 40rpx;
		border: none;
	}
}
</style>
