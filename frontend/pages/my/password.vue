<template>
	<view class="change-password-container">
		<view class="form-section">
			<view class="form-item">
				<text class="label">原密码</text>
				<input 
					type="password" 
					v-model="formData.oldPassword" 
					placeholder="请输入原密码"
					class="input"
				/>
			</view>
			
			<view class="form-item">
				<text class="label">新密码</text>
				<input 
					type="password" 
					v-model="formData.newPassword" 
					placeholder="请输入新密码（6-20位）"
					class="input"
				/>
			</view>
			
			<view class="form-item">
				<text class="label">确认密码</text>
				<input 
					type="password" 
					v-model="formData.confirmPassword" 
					placeholder="请再次输入新密码"
					class="input"
				/>
			</view>
		</view>
		
		<view class="tips">
			<text class="tips-title">密码设置规则</text>
			<text class="tips-item">1. 密码长度6-20位</text>
			<text class="tips-item">2. 建议使用字母、数字组合</text>
			<text class="tips-item">3. 不要使用过于简单的密码</text>
		</view>
		
		<button class="submit-btn" @click="handleSubmit" :disabled="!canSubmit">
			确认修改
		</button>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			formData: {
				oldPassword: '',
				newPassword: '',
				confirmPassword: ''
			}
		}
	},
	computed: {
		canSubmit() {
			return this.formData.oldPassword.length >= 6 &&
			       this.formData.newPassword.length >= 6 &&
			       this.formData.newPassword === this.formData.confirmPassword
		}
	},
	methods: {
		async handleSubmit() {
			if (!this.canSubmit) {
				if (this.formData.newPassword !== this.formData.confirmPassword) {
					uni.showToast({ title: '两次密码不一致', icon: 'none' })
				} else if (this.formData.newPassword.length < 6) {
					uni.showToast({ title: '密码长度至少6位', icon: 'none' })
				}
				return
			}

			try {
				uni.showLoading({ title: '提交中...' })
				const res = await api.user.changePassword({
					old_password: this.formData.oldPassword,
					new_password: this.formData.newPassword
				})
				
				if (res.code === 1) {
					uni.showToast({
						title: '密码修改成功',
						icon: 'success'
					})
					setTimeout(() => {
						uni.navigateBack()
					}, 1500)
				}
			} catch (e) {
				console.error('修改失败:', e)
			} finally {
				uni.hideLoading()
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.change-password-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding: 20rpx;
}

.form-section {
	background: #fff;
	border-radius: 16rpx;
	padding: 0 30rpx;
	margin-bottom: 20rpx;
	
	.form-item {
		padding: 30rpx 0;
		border-bottom: 1rpx solid #f5f5f5;
		
		&:last-child {
			border-bottom: none;
		}
		
		.label {
			display: block;
			font-size: 28rpx;
			color: #333;
			margin-bottom: 16rpx;
		}
		
		.input {
			width: 100%;
			height: 80rpx;
			padding: 0 20rpx;
			border: 1rpx solid #ddd;
			border-radius: 12rpx;
			font-size: 28rpx;
		}
	}
}

.tips {
	background: #fff9e6;
	padding: 30rpx;
	border-radius: 16rpx;
	margin-bottom: 30rpx;
	
	.tips-title {
		display: block;
		font-size: 28rpx;
		font-weight: bold;
		color: #faad14;
		margin-bottom: 16rpx;
	}
	
	.tips-item {
		display: block;
		font-size: 24rpx;
		color: #8c6a1a;
		line-height: 1.8;
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
	
	&[disabled] {
		background: #ccc;
	}
}
</style>
