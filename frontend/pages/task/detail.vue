<template>
	<view class="task-detail-container">
		<!-- 任务基本信息 -->
		<view class="task-header">
			<view class="task-title-section">
				<text class="task-title">{{ taskDetail.title }}</text>
				<view class="task-reward">
					<text class="money">+{{ taskDetail.reward }}</text>
					<text class="unit">元</text>
				</view>
			</view>
			
			<view class="task-meta">
				<text class="category-tag">{{ taskDetail.category_name }}</text>
				<text class="views">{{ taskDetail.views }}人浏览</text>
				<text class="status-tag" :class="'status-' + taskDetail.status">
					{{ getStatusText(taskDetail.status) }}
				</text>
			</view>
		</view>

		<!-- 任务详情 -->
		<view class="task-section">
			<view class="section-title">
				<text>任务详情</text>
			</view>
			<view class="section-content">
				<text class="description">{{ taskDetail.description }}</text>
			</view>
		</view>

		<!-- 任务要求 -->
		<view class="task-section" v-if="taskDetail.requirements">
			<view class="section-title">
				<text>任务要求</text>
			</view>
			<view class="section-content">
				<text class="requirements">{{ taskDetail.requirements }}</text>
			</view>
		</view>

		<!-- 任务信息 -->
		<view class="task-section">
			<view class="section-title">
				<text>任务信息</text>
			</view>
			<view class="info-list">
				<view class="info-item">
					<text class="info-label">发布时间</text>
					<text class="info-value">{{ formatDateTime(taskDetail.created_at) }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">发布者</text>
					<text class="info-value">{{ taskDetail.publisher_nickname }}</text>
				</view>
				<view class="info-item" v-if="taskDetail.deadline">
					<text class="info-label">截止时间</text>
					<text class="info-value">{{ formatDateTime(taskDetail.deadline) }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">参与人数</text>
					<text class="info-value">{{ taskDetail.current_participants }}/{{ taskDetail.participant_limit }}</text>
				</view>
			</view>
		</view>

		<!-- 提交内容（如果已提交） -->
		<view class="task-section" v-if="taskDetail.submit_content">
			<view class="section-title">
				<text>我的提交</text>
			</view>
			<view class="section-content submit-content">
				<text>{{ taskDetail.submit_content }}</text>
				<text class="submit-time">提交时间：{{ formatDateTime(taskDetail.submit_time) }}</text>
			</view>
		</view>

		<!-- 审核结果（如果有） -->
		<view class="task-section" v-if="taskDetail.verify_comment">
			<view class="section-title">
				<text>审核结果</text>
			</view>
			<view class="section-content verify-content">
				<text class="verify-comment">{{ taskDetail.verify_comment }}</text>
				<text class="verify-time">审核时间：{{ formatDateTime(taskDetail.verify_time) }}</text>
			</view>
		</view>

		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="action-buttons" v-if="taskDetail.status === 'pending'">
				<button class="accept-btn" @click="acceptTask">立即接单</button>
			</view>
			<view class="action-buttons" v-else-if="taskDetail.status === 'in_progress' && isMyTask">
				<button class="submit-btn" @click="showSubmitModal">提交任务</button>
			</view>
			<view class="action-buttons" v-else-if="taskDetail.status === 'submitted' && isPublisher">
				<button class="verify-btn pass" @click="verifyTask(true)">通过</button>
				<button class="verify-btn reject" @click="verifyTask(false)">拒绝</button>
			</view>
			<view class="action-buttons" v-else>
				<text class="status-text">{{ getStatusText(taskDetail.status) }}</text>
			</view>
		</view>

		<!-- 提交任务弹窗 -->
		<view class="modal" v-if="showSubmitModal" @click="showSubmitModal = false">
			<view class="modal-content" @click.stop>
				<view class="modal-header">
					<text>提交任务</text>
					<text class="close-btn" @click="showSubmitModal = false">×</text>
				</view>
				<view class="modal-body">
					<textarea 
						v-model="submitContent" 
						placeholder="请输入任务完成说明..."
						class="submit-input"
					></textarea>
				</view>
				<view class="modal-footer">
					<button class="confirm-btn" @click="confirmSubmit">确认提交</button>
				</view>
			</view>
		</view>

		<!-- 审核弹窗 -->
		<view class="modal" v-if="showVerifyModal" @click="showVerifyModal = false">
			<view class="modal-content" @click.stop>
				<view class="modal-header">
					<text>{{ verifyAction === 'pass' ? '通过审核' : '拒绝审核' }}</text>
					<text class="close-btn" @click="showVerifyModal = false">×</text>
				</view>
				<view class="modal-body">
					<textarea 
						v-model="verifyComment" 
						:placeholder="verifyAction === 'pass' ? '请输入审核备注（可选）' : '请输入拒绝原因'"
						class="verify-input"
					></textarea>
				</view>
				<view class="modal-footer">
					<button class="confirm-btn" @click="confirmVerify">确认</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			taskId: null,
			taskDetail: {
				title: '',
				description: '',
				requirements: '',
				category_name: '',
				reward: 0,
				status: '',
				views: 0,
				participant_limit: 1,
				current_participants: 0,
				publisher_id: 0,
				publisher_nickname: '',
				worker_id: null,
				submit_content: '',
				submit_time: null,
				verify_comment: '',
				verify_time: null,
				deadline: null,
				created_at: ''
			},
			showSubmitModal: false,
			showVerifyModal: false,
			submitContent: '',
			verifyComment: '',
			verifyAction: '',
			userInfo: null
		}
	},
	computed: {
		isMyTask() {
			return this.userInfo && this.taskDetail.worker_id === this.userInfo.id
		},
		isPublisher() {
			return this.userInfo && this.taskDetail.publisher_id === this.userInfo.id
		}
	},
	onLoad(options) {
		if (options.id) {
			this.taskId = options.id
			this.loadTaskDetail()
		}
		this.loadUserInfo()
	},
	methods: {
		async loadTaskDetail() {
			try {
				uni.showLoading({ title: '加载中...' })
				const res = await api.task.getDetail(this.taskId)
				if (res.code === 1) {
					this.taskDetail = res.data
				}
			} catch (e) {
				console.error('获取任务详情失败:', e)
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			} finally {
				uni.hideLoading()
			}
		},
		loadUserInfo() {
			const info = uni.getStorageSync('user_info')
			if (info) {
				this.userInfo = info
			}
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
		formatDateTime(dateStr) {
			if (!dateStr) return ''
			const date = new Date(dateStr)
			return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
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
		async acceptTask() {
			if (!this.checkLogin()) return
			
			try {
				const res = await api.task.accept(this.taskId)
				if (res.code === 1) {
					uni.showToast({
						title: '接单成功',
						icon: 'success'
					})
					setTimeout(() => {
						this.loadTaskDetail()
					}, 1500)
				}
			} catch (e) {
				console.error('接单失败:', e)
			}
		},
		showSubmitModalF() {
			if (!this.checkLogin()) return
			this.showSubmitModal = true
		},
		async confirmSubmit() {
			if (!this.submitContent.trim()) {
				uni.showToast({
					title: '请输入完成说明',
					icon: 'none'
				})
				return
			}
			
			try {
				const res = await api.task.submit(this.taskId, {
					content: this.submitContent
				})
				if (res.code === 1) {
					uni.showToast({
						title: '提交成功',
						icon: 'success'
					})
					this.showSubmitModal = false
					this.submitContent = ''
					setTimeout(() => {
						this.loadTaskDetail()
					}, 1500)
				}
			} catch (e) {
				console.error('提交失败:', e)
			}
		},
		verifyTask(approved) {
			this.verifyAction = approved ? 'pass' : 'reject'
			this.showVerifyModal = true
		},
		async confirmVerify() {
			if (this.verifyAction === 'reject' && !this.verifyComment.trim()) {
				uni.showToast({
					title: '请输入拒绝原因',
					icon: 'none'
				})
				return
			}
			
			try {
				const res = await api.task.verify(this.taskId, {
					approved: this.verifyAction === 'pass',
					comment: this.verifyComment
				})
				if (res.code === 1) {
					uni.showToast({
						title: '审核完成',
						icon: 'success'
					})
					this.showVerifyModal = false
					this.verifyComment = ''
					setTimeout(() => {
						this.loadTaskDetail()
					}, 1500)
				}
			} catch (e) {
				console.error('审核失败:', e)
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.task-detail-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.task-header {
	background: #fff;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.task-title-section {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 20rpx;
		
		.task-title {
			flex: 1;
			font-size: 36rpx;
			font-weight: bold;
			color: #333;
			margin-right: 20rpx;
		}
		
		.task-reward {
			display: flex;
			align-items: baseline;
			
			.money {
				font-size: 48rpx;
				font-weight: bold;
				color: #ff6b6b;
			}
			
			.unit {
				font-size: 26rpx;
				color: #ff6b6b;
				margin-left: 4rpx;
			}
		}
	}
	
	.task-meta {
		display: flex;
		align-items: center;
		gap: 20rpx;
		
		.category-tag {
			padding: 8rpx 20rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #fff;
			font-size: 24rpx;
			border-radius: 8rpx;
		}
		
		.views {
			font-size: 24rpx;
			color: #999;
		}
		
		.status-tag {
			padding: 8rpx 20rpx;
			font-size: 24rpx;
			border-radius: 8rpx;
			
			&.status-pending {
				background: #f0f0f0;
				color: #666;
			}
			&.status-in_progress {
				background: #e6f7ff;
				color: #1890ff;
			}
			&.status-submitted {
				background: #fff7e6;
				color: #faad14;
			}
			&.status-completed {
				background: #f6ffed;
				color: #52c41a;
			}
			&.status-rejected {
				background: #fff1f0;
				color: #ff4d4f;
			}
		}
	}
}

.task-section {
	background: #fff;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
		padding-left: 20rpx;
		border-left: 6rpx solid #667eea;
	}
	
	.section-content {
		font-size: 28rpx;
		color: #666;
		line-height: 1.8;
		
		&.submit-content, &.verify-content {
			background: #f9f9f9;
			padding: 20rpx;
			border-radius: 12rpx;
			
			.submit-time, .verify-time {
				display: block;
				margin-top: 16rpx;
				font-size: 24rpx;
				color: #999;
			}
		}
	}
	
	.info-list {
		.info-item {
			display: flex;
			justify-content: space-between;
			padding: 20rpx 0;
			border-bottom: 1rpx solid #f0f0f0;
			
			&:last-child {
				border-bottom: none;
			}
			
			.info-label {
				font-size: 28rpx;
				color: #999;
			}
			
			.info-value {
				font-size: 28rpx;
				color: #333;
			}
		}
	}
}

.bottom-bar {
	position: fixed;
	left: 0;
	right: 0;
	bottom: 0;
	background: #fff;
	padding: 20rpx 30rpx;
	padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
	
	.action-buttons {
		display: flex;
		gap: 20rpx;
		
		button, .verify-btn {
			flex: 1;
			height: 88rpx;
			line-height: 88rpx;
			text-align: center;
			border-radius: 44rpx;
			font-size: 32rpx;
			border: none;
		}
		
		.accept-btn, .submit-btn, .pass {
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #fff;
		}
		
		.verify-btn.pass {
			background: #52c41a;
			color: #fff;
		}
		
		.verify-btn.reject {
			background: #ff4d4f;
			color: #fff;
		}
		
		.status-text {
			flex: 1;
			text-align: center;
			line-height: 88rpx;
			font-size: 28rpx;
			color: #999;
		}
	}
}

.modal {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 999;
	
	.modal-content {
		width: 90%;
		background: #fff;
		border-radius: 20rpx;
		overflow: hidden;
		
		.modal-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			font-size: 32rpx;
			font-weight: bold;
			border-bottom: 1rpx solid #f0f0f0;
			
			.close-btn {
				font-size: 48rpx;
				color: #999;
			}
		}
		
		.modal-body {
			padding: 30rpx;
			
			textarea {
				width: 100%;
				min-height: 200rpx;
				padding: 20rpx;
				border: 1rpx solid #ddd;
				border-radius: 12rpx;
				font-size: 28rpx;
				line-height: 1.6;
			}
		}
		
		.modal-footer {
			padding: 0 30rpx 30rpx;
			
			.confirm-btn {
				width: 100%;
				height: 88rpx;
				line-height: 88rpx;
				background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
				color: #fff;
				font-size: 32rpx;
				border-radius: 44rpx;
				border: none;
			}
		}
	}
}
</style>
