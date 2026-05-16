<template>
	<view class="my-container">
		<!-- 用户信息卡片 -->
		<view class="user-card">
			<view class="user-info" @click="goToProfile">
				<image :src="userInfo.avatar || '/static/default-avatar.png'" class="avatar"></image>
				<view class="info">
					<text class="nickname">{{ userInfo.nickname || '未登录' }}</text>
					<text class="phone">{{ userInfo.phone || '点击登录' }}</text>
				</view>
				<text class="iconfont icon-arrow-right arrow"></text>
			</view>
			
			<view class="balance-card" v-if="userInfo.id">
				<view class="balance-item">
					<text class="balance-label">账户余额</text>
					<text class="balance-value">¥{{ userInfo.balance || 0 }}</text>
				</view>
				<view class="balance-buttons">
					<button class="balance-btn" @click="goToBalance">充值</button>
					<button class="balance-btn outline" @click="goToWithdraw">提现</button>
				</view>
			</view>
		</view>

		<!-- 我的任务 -->
		<view class="menu-section">
			<view class="section-title">我的任务</view>
			<view class="menu-grid">
				<view class="menu-item" @click="goToMyTasks('published')">
					<text class="iconfont icon-edit"></text>
					<text class="menu-text">我发布的</text>
				</view>
				<view class="menu-item" @click="goToMyTasks('accepted')">
					<text class="iconfont icon-task"></text>
					<text class="menu-text">我接的</text>
				</view>
			</view>
		</view>

		<!-- 功能菜单 -->
		<view class="menu-section">
			<view class="menu-list">
				<view class="menu-item-row" @click="goToBalance">
					<view class="menu-left">
						<text class="iconfont icon-wallet"></text>
						<text class="menu-label">我的余额</text>
					</view>
					<view class="menu-right">
						<text class="menu-value">¥{{ userInfo.balance || 0 }}</text>
						<text class="iconfont icon-arrow-right"></text>
					</view>
				</view>
				
				<view class="menu-item-row" @click="goToTransaction">
					<view class="menu-left">
						<text class="iconfont icon-list"></text>
						<text class="menu-label">交易记录</text>
					</view>
					<text class="iconfont icon-arrow-right"></text>
				</view>
				
				<view class="menu-item-row" @click="goToNotifications">
					<view class="menu-left">
						<text class="iconfont icon-bell"></text>
						<text class="menu-label">消息通知</text>
					</view>
					<view class="menu-right">
						<view class="badge" v-if="unreadCount > 0">{{ unreadCount > 99 ? '99+' : unreadCount }}</view>
						<text class="iconfont icon-arrow-right"></text>
					</view>
				</view>
			</view>
		</view>

		<!-- 设置菜单 -->
		<view class="menu-section">
			<view class="menu-list">
				<view class="menu-item-row" @click="goToProfile">
					<view class="menu-left">
						<text class="iconfont icon-user"></text>
						<text class="menu-label">个人资料</text>
					</view>
					<text class="iconfont icon-arrow-right"></text>
				</view>
				
				<view class="menu-item-row" @click="goToPassword">
					<view class="menu-left">
						<text class="iconfont icon-lock"></text>
						<text class="menu-label">修改密码</text>
					</view>
					<text class="iconfont icon-arrow-right"></text>
				</view>
				
				<view class="menu-item-row" @click="showAbout">
					<view class="menu-left">
						<text class="iconfont icon-info"></text>
						<text class="menu-label">关于我们</text>
					</view>
					<text class="iconfont icon-arrow-right"></text>
				</view>
				
				<view class="menu-item-row" @click="goToHelp">
					<view class="menu-left">
						<text class="iconfont icon-question"></text>
						<text class="menu-label">帮助与反馈</text>
					</view>
					<text class="iconfont icon-arrow-right"></text>
				</view>
			</view>
		</view>

		<!-- 退出登录 -->
		<view class="logout-section" v-if="userInfo.id">
			<button class="logout-btn" @click="handleLogout">退出登录</button>
		</view>

		<!-- 登录按钮 -->
		<view class="login-section" v-else>
			<button class="login-btn" @click="goToLogin">登录 / 注册</button>
		</view>

		<!-- 底部安全区 -->
		<view class="safe-area-bottom"></view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			userInfo: {},
			unreadCount: 0
		}
	},
	onShow() {
		this.loadUserInfo()
		this.loadUnreadCount()
	},
	methods: {
		loadUserInfo() {
			const info = uni.getStorageSync('user_info')
			if (info) {
				this.userInfo = info
			} else {
				this.userInfo = {}
			}
		},
		async loadUnreadCount() {
			if (!this.userInfo.id) return
			
			try {
				const res = await api.notification.getUnreadCount()
				if (res.code === 1) {
					this.unreadCount = res.data.count
				}
			} catch (e) {
				console.error('获取未读数失败:', e)
			}
		},
		goToLogin() {
			uni.navigateTo({
				url: '/pages/login/login'
			})
		},
		goToProfile() {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: '/pages/my/profile'
			})
		},
		goToBalance() {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: '/pages/my/balance'
			})
		},
		goToWithdraw() {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: '/pages/my/withdraw'
			})
		},
		goToMyTasks(type) {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: `/pages/my/tasks?type=${type}`
			})
		},
		goToTransaction() {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: '/pages/my/transactions'
			})
		},
		goToNotifications() {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: '/pages/my/notifications'
			})
		},
		goToPassword() {
			if (!this.checkLogin()) return
			uni.navigateTo({
				url: '/pages/my/password'
			})
		},
		showAbout() {
			uni.showModal({
				title: '关于我们',
				content: '悬赏任务平台 v3.0\n\n一个安全可靠的悬赏任务交易平台',
				showCancel: false
			})
		},
		goToHelp() {
			uni.showModal({
				title: '帮助与反馈',
				content: '客服电话：400-888-8888\n工作时间：9:00-18:00',
				showCancel: false
			})
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
		async handleLogout() {
			try {
				await api.auth.logout()
			} catch (e) {
				console.log('登出请求失败', e)
			}
			
			uni.clearStorageSync()
			this.userInfo = {}
			this.unreadCount = 0
			
			uni.showToast({
				title: '已退出登录',
				icon: 'success'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.my-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

.user-card {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 40rpx 30rpx;
	
	.user-info {
		display: flex;
		align-items: center;
		margin-bottom: 30rpx;
		
		.avatar {
			width: 120rpx;
			height: 120rpx;
			border-radius: 60rpx;
			margin-right: 24rpx;
			background: #fff;
		}
		
		.info {
			flex: 1;
			
			.nickname {
				display: block;
				font-size: 36rpx;
				font-weight: bold;
				color: #fff;
				margin-bottom: 10rpx;
			}
			
			.phone {
				font-size: 26rpx;
				color: rgba(255, 255, 255, 0.8);
			}
		}
		
		.arrow {
			font-size: 32rpx;
			color: rgba(255, 255, 255, 0.8);
		}
	}
	
	.balance-card {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 16rpx;
		padding: 30rpx;
		
		.balance-item {
			text-align: center;
			margin-bottom: 24rpx;
			
			.balance-label {
				display: block;
				font-size: 26rpx;
				color: rgba(255, 255, 255, 0.8);
				margin-bottom: 10rpx;
			}
			
			.balance-value {
				font-size: 56rpx;
				font-weight: bold;
				color: #fff;
			}
		}
		
		.balance-buttons {
			display: flex;
			gap: 20rpx;
			
			.balance-btn {
				flex: 1;
				height: 72rpx;
				line-height: 72rpx;
				background: #fff;
				color: #667eea;
				font-size: 30rpx;
				border-radius: 36rpx;
				border: none;
				
				&.outline {
					background: transparent;
					border: 2rpx solid #fff;
					color: #fff;
				}
			}
		}
	}
}

.menu-section {
	margin: 20rpx;
	
	.section-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
		padding-left: 10rpx;
		border-left: 6rpx solid #667eea;
	}
	
	.menu-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 20rpx;
		background: #fff;
		padding: 30rpx;
		border-radius: 16rpx;
		
		.menu-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			padding: 30rpx;
			background: #f9f9f9;
			border-radius: 12rpx;
			
			.iconfont {
				font-size: 56rpx;
				color: #667eea;
				margin-bottom: 16rpx;
			}
			
			.menu-text {
				font-size: 26rpx;
				color: #333;
			}
		}
	}
	
	.menu-list {
		background: #fff;
		border-radius: 16rpx;
		overflow: hidden;
		
		.menu-item-row {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			border-bottom: 1rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.menu-left {
				display: flex;
				align-items: center;
				
				.iconfont {
					font-size: 40rpx;
					color: #667eea;
					margin-right: 20rpx;
				}
				
				.menu-label {
					font-size: 28rpx;
					color: #333;
				}
			}
			
			.menu-right {
				display: flex;
				align-items: center;
				
				.menu-value {
					font-size: 28rpx;
					color: #ff6b6b;
					margin-right: 10rpx;
				}
				
				.iconfont {
					font-size: 28rpx;
					color: #ccc;
				}
				
				.badge {
					padding: 4rpx 12rpx;
					background: #ff4d4f;
					color: #fff;
					font-size: 22rpx;
					border-radius: 20rpx;
					margin-right: 10rpx;
				}
			}
		}
	}
}

.logout-section, .login-section {
	padding: 40rpx 20rpx;
	
	.logout-btn, .login-btn {
		width: 100%;
		height: 88rpx;
		line-height: 88rpx;
		background: #fff;
		color: #666;
		font-size: 32rpx;
		border-radius: 44rpx;
		border: none;
	}
	
	.login-btn {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #fff;
	}
}

.safe-area-bottom {
	height: env(safe-area-inset-bottom);
}
</style>
