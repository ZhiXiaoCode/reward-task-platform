<template>
	<view class="create-task-container">
		<view class="form-container">
			<!-- 任务标题 -->
			<view class="form-item">
				<view class="form-label">
					<text class="required">*</text>
					<text>任务标题</text>
				</view>
				<input 
					type="text" 
					v-model="formData.title" 
					placeholder="请输入任务标题（5-50字）"
					maxlength="50"
					class="form-input"
				/>
			</view>

			<!-- 任务分类 -->
			<view class="form-item">
				<view class="form-label">
					<text class="required">*</text>
					<text>任务分类</text>
				</view>
				<picker 
					:range="categories" 
					range-key="name"
					@change="onCategoryChange"
				>
					<view class="picker-value">
						<text :class="{placeholder: !formData.category_id}">
							{{ selectedCategoryName || '请选择任务分类' }}
						</text>
						<text class="iconfont icon-arrow-right"></text>
					</view>
				</picker>
			</view>

			<!-- 任务奖励 -->
			<view class="form-item">
				<view class="form-label">
					<text class="required">*</text>
					<text>任务奖励</text>
				</view>
				<view class="reward-input">
					<input 
						type="digit" 
						v-model="formData.reward" 
						placeholder="请输入奖励金额"
						class="form-input"
					/>
					<text class="unit">元</text>
				</view>
				<text class="tips">奖励金额将直接从您的账户余额中扣除</text>
			</view>

			<!-- 任务描述 -->
			<view class="form-item">
				<view class="form-label">
					<text class="required">*</text>
					<text>任务描述</text>
				</view>
				<textarea 
					v-model="formData.description" 
					placeholder="请详细描述任务内容、步骤和要求（至少20字）"
					class="form-textarea"
					maxlength="2000"
				></textarea>
				<text class="char-count">{{ formData.description.length }}/2000</text>
			</view>

			<!-- 任务要求 -->
			<view class="form-item">
				<view class="form-label">
					<text>额外要求</text>
				</view>
				<textarea 
					v-model="formData.requirements" 
					placeholder="如有额外要求，请在此说明"
					class="form-textarea"
					maxlength="1000"
				></textarea>
			</view>

			<!-- 参与人数 -->
			<view class="form-item">
				<view class="form-label">
					<text>参与人数</text>
				</view>
				<view class="limit-selector">
					<view 
						class="limit-item" 
						v-for="n in 5" 
						:key="n"
						:class="{active: formData.participant_limit === n}"
						@click="formData.participant_limit = n"
					>
						{{ n }}人
					</view>
				</view>
			</view>

			<!-- 截止时间 -->
			<view class="form-item">
				<view class="form-label">
					<text>截止时间</text>
				</view>
				<picker 
					mode="date" 
					:value="formData.deadline" 
					:start="minDeadline"
					@change="onDeadlineChange"
				>
					<view class="picker-value">
						<text :class="{placeholder: !formData.deadline}">
							{{ formData.deadline || '不设置截止时间' }}
						</text>
						<text class="iconfont icon-arrow-right"></text>
					</view>
				</picker>
			</view>

			<!-- 费用说明 -->
			<view class="fee-section">
				<view class="fee-title">费用说明</view>
				<view class="fee-item">
					<text>任务奖励</text>
					<text class="fee-value">¥{{ formData.reward || 0 }}</text>
				</view>
				<view class="fee-item">
					<text>平台服务费</text>
					<text class="fee-value">¥0</text>
				</view>
				<view class="fee-item total">
					<text>总计</text>
					<text class="fee-value">¥{{ formData.reward || 0 }}</text>
				</view>
			</view>

			<!-- 提交按钮 -->
			<button class="submit-btn" @click="handleSubmit" :disabled="!canSubmit">
				发布任务
			</button>

			<!-- 注意事项 -->
			<view class="notice">
				<view class="notice-title">注意事项</view>
				<view class="notice-item">1. 请确保任务内容合法合规</view>
				<view class="notice-item">2. 任务奖励将直接从余额中扣除</view>
				<view class="notice-item">3. 审核通过后，奖励将发放给完成任务的用户</view>
				<view class="notice-item">4. 请确保任务描述清晰明确</view>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			categories: [],
			formData: {
				title: '',
				category_id: null,
				reward: '',
				description: '',
				requirements: '',
				participant_limit: 1,
				deadline: ''
			},
			minDeadline: ''
		}
	},
	computed: {
		selectedCategoryName() {
			if (!this.formData.category_id) return ''
			const cat = this.categories.find(c => c.id === this.formData.category_id)
			return cat ? cat.name : ''
		},
		canSubmit() {
			return this.formData.title.trim().length >= 5 &&
			       this.formData.category_id &&
			       parseFloat(this.formData.reward) > 0 &&
			       this.formData.description.trim().length >= 20
		}
	},
	onLoad() {
		this.loadCategories()
		this.setMinDeadline()
	},
	methods: {
		setMinDeadline() {
			const date = new Date()
			date.setDate(date.getDate() + 1)
			this.minDeadline = date.toISOString().split('T')[0]
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
		onCategoryChange(e) {
			const index = e.detail.value
			this.formData.category_id = this.categories[index].id
		},
		onDeadlineChange(e) {
			this.formData.deadline = e.detail.value
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
		async handleSubmit() {
			if (!this.checkLogin()) return
			
			if (!this.canSubmit) {
				uni.showToast({
					title: '请完善任务信息',
					icon: 'none'
				})
				return
			}

			try {
				uni.showLoading({ title: '发布中...' })
				
				const res = await api.task.create({
					title: this.formData.title,
					category_id: this.formData.category_id,
					reward: parseFloat(this.formData.reward),
					description: this.formData.description,
					requirements: this.formData.requirements,
					participant_limit: this.formData.participant_limit,
					deadline: this.formData.deadline || null
				})
				
				if (res.code === 1) {
					uni.showToast({
						title: '发布成功',
						icon: 'success'
					})
					setTimeout(() => {
						uni.navigateBack()
					}, 1500)
				}
			} catch (e) {
				console.error('发布失败:', e)
			} finally {
				uni.hideLoading()
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.create-task-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding: 20rpx;
}

.form-container {
	.form-item {
		background: #fff;
		padding: 30rpx;
		margin-bottom: 20rpx;
		border-radius: 16rpx;
		
		.form-label {
			font-size: 28rpx;
			color: #333;
			margin-bottom: 20rpx;
			
			.required {
				color: #ff4d4f;
				margin-right: 8rpx;
			}
		}
		
		.form-input {
			width: 100%;
			height: 80rpx;
			padding: 0 20rpx;
			border: 1rpx solid #ddd;
			border-radius: 12rpx;
			font-size: 28rpx;
		}
		
		.form-textarea {
			width: 100%;
			min-height: 200rpx;
			padding: 20rpx;
			border: 1rpx solid #ddd;
			border-radius: 12rpx;
			font-size: 28rpx;
			line-height: 1.6;
			box-sizing: border-box;
		}
		
		.char-count {
			display: block;
			text-align: right;
			font-size: 24rpx;
			color: #999;
			margin-top: 10rpx;
		}
		
		.tips {
			display: block;
			font-size: 24rpx;
			color: #999;
			margin-top: 10rpx;
		}
		
		.reward-input {
			display: flex;
			align-items: center;
			
			.unit {
				margin-left: 16rpx;
				font-size: 28rpx;
				color: #333;
			}
		}
		
		.picker-value {
			display: flex;
			justify-content: space-between;
			align-items: center;
			height: 80rpx;
			padding: 0 20rpx;
			border: 1rpx solid #ddd;
			border-radius: 12rpx;
			
			text:first-child {
				font-size: 28rpx;
				color: #333;
				
				&.placeholder {
					color: #999;
				}
			}
			
			.iconfont {
				color: #999;
			}
		}
		
		.limit-selector {
			display: flex;
			gap: 20rpx;
			
			.limit-item {
				padding: 16rpx 30rpx;
				border: 1rpx solid #ddd;
				border-radius: 8rpx;
				font-size: 28rpx;
				color: #666;
				
				&.active {
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: #fff;
					border-color: transparent;
				}
			}
		}
	}
	
	.fee-section {
		background: #fff;
		padding: 30rpx;
		margin-bottom: 20rpx;
		border-radius: 16rpx;
		
		.fee-title {
			font-size: 28rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 20rpx;
		}
		
		.fee-item {
			display: flex;
			justify-content: space-between;
			padding: 16rpx 0;
			font-size: 26rpx;
			color: #666;
			
			&.total {
				border-top: 1rpx solid #f0f0f0;
				margin-top: 10rpx;
				padding-top: 26rpx;
				font-weight: bold;
				color: #333;
			}
			
			.fee-value {
				color: #ff6b6b;
			}
		}
	}
	
	.submit-btn {
		width: 100%;
		height: 88rpx;
		line-height: 88rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #fff;
		font-size: 32rpx;
		border-radius: 44rpx;
		border: none;
		margin-bottom: 30rpx;
		
		&[disabled] {
			background: #ccc;
		}
	}
	
	.notice {
		background: #fff9e6;
		padding: 30rpx;
		border-radius: 16rpx;
		margin-bottom: 40rpx;
		
		.notice-title {
			font-size: 28rpx;
			font-weight: bold;
			color: #faad14;
			margin-bottom: 16rpx;
		}
		
		.notice-item {
			font-size: 24rpx;
			color: #8c6a1a;
			line-height: 1.8;
			margin-bottom: 8rpx;
		}
	}
}
</style>
