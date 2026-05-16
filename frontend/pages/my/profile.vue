<template>
	<view class="profile-container">
		<view class="form-list">
			<view class="form-item">
				<text class="label">头像</text>
				<view class="value avatar-value" @click="chooseAvatar">
					<image :src="profile.avatar || '/static/default-avatar.png'" class="avatar"></image>
					<text class="iconfont icon-arrow-right"></text>
				</view>
			</view>
			
			<view class="form-item">
				<text class="label">昵称</text>
				<input 
					type="text" 
					v-model="profile.nickname" 
					placeholder="请输入昵称"
					class="input"
					@blur="updateProfile"
				/>
			</view>
			
			<view class="form-item">
				<text class="label">手机号</text>
				<text class="value-text">{{ profile.phone || '未绑定' }}</text>
			</view>
			
			<view class="form-item">
				<text class="label">注册时间</text>
				<text class="value-text">{{ profile.created_at || '-' }}</text>
			</view>
		</view>
		
		<view class="action-section">
			<button class="logout-btn" @click="handleLogout">退出登录</button>
		</view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			profile: {
				nickname: '',
				avatar: '',
				phone: '',
				created_at: ''
			}
		}
	},
	onShow() {
		this.loadProfile()
	},
	methods: {
		async loadProfile() {
			try {
				const res = await api.user.getProfile()
				if (res.code === 1) {
					this.profile = res.data
					uni.setStorageSync('user_info', res.data)
				}
			} catch (e) {
				console.error('获取资料失败:', e)
			}
		},
		async updateProfile() {
			try {
				const res = await api.user.updateProfile({
					nickname: this.profile.nickname,
					avatar: this.profile.avatar
				})
				if (res.code === 1) {
					uni.showToast({
						title: '保存成功',
						icon: 'success'
					})
				}
			} catch (e) {
				console.error('保存失败:', e)
			}
		},
		chooseAvatar() {
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					this.profile.avatar = res.tempFilePaths[0]
					this.updateProfile()
				}
			})
		},
		async handleLogout() {
			try {
				await api.auth.logout()
			} catch (e) {
				console.log('登出请求失败', e)
			}
			
			uni.clearStorageSync()
			uni.showToast({
				title: '已退出登录',
				icon: 'success'
			})
			setTimeout(() => {
				uni.reLaunch({
					url: '/pages/login/login'
				})
			}, 1500)
		}
	}
}
</script>

<style lang="scss" scoped>
.profile-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.form-list {
	background: #fff;
	margin: 20rpx;
	border-radius: 16rpx;
	padding: 0 30rpx;
	
	.form-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 30rpx 0;
		border-bottom: 1rpx solid #f5f5f5;
		
		&:last-child {
			border-bottom: none;
		}
		
		.label {
			font-size: 28rpx;
			color: #333;
		}
		
		.avatar-value {
			display: flex;
			align-items: center;
			
			.avatar {
				width: 80rpx;
				height: 80rpx;
				border-radius: 50%;
				margin-right: 10rpx;
			}
			
			.iconfont {
				font-size: 28rpx;
				color: #ccc;
			}
		}
		
		.input {
			flex: 1;
			text-align: right;
			font-size: 28rpx;
			color: #333;
		}
		
		.value-text {
			font-size: 28rpx;
			color: #999;
		}
	}
}

.action-section {
	padding: 40rpx 20rpx;
	
	.logout-btn {
		width: 100%;
		height: 88rpx;
		line-height: 88rpx;
		background: #fff;
		color: #ff4d4f;
		font-size: 32rpx;
		border-radius: 44rpx;
		border: none;
	}
}
</style>
