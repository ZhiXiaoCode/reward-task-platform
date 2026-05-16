<template>
	<view class="login-container">
		<view class="login-header">
			<image src="/static/logo.png" mode="aspectFit" class="logo"></image>
			<text class="title">悬赏任务平台</text>
			<text class="subtitle">轻松赚钱，快乐生活</text>
		</view>

		<view class="login-form">
			<view class="form-item">
				<text class="iconfont icon-phone"></text>
				<input 
					type="number" 
					v-model="formData.phone" 
					placeholder="请输入手机号"
					maxlength="11"
				/>
			</view>

			<view class="form-item">
				<text class="iconfont icon-password"></text>
				<input 
					:type="showPassword ? 'text' : 'password'"
					v-model="formData.password" 
					placeholder="请输入密码"
				/>
				<text 
					class="iconfont toggle-password"
					:class="showPassword ? 'icon-eye' : 'icon-eye-close'"
					@click="showPassword = !showPassword"
				></text>
			</view>

			<view class="forgot-password">
				<text @click="goToRegister">忘记密码？</text>
			</view>

			<button 
				class="login-btn" 
				:disabled="!canLogin"
				@click="handleLogin"
			>
				登录
			</button>

			<view class="register-link">
				<text>还没有账号？</text>
				<text class="link" @click="goToRegister">立即注册</text>
			</view>
		</view>

		<view class="agreement">
			<checkbox-group @change="onAgreementChange">
				<label>
					<checkbox :checked="agreed" color="#346DF0"/>
					<text>我已阅读并同意</text>
				</label>
			</checkbox-group>
			<text class="link" @click="showAgreement">《用户协议》</text>
			<text>和</text>
			<text class="link" @click="showPrivacy">《隐私政策》</text>
		</view>
	</view>
</template>

<script>
import api from '@/api/index.js'
import { setToken } from '@/utils/http.js'

export default {
	data() {
		return {
			formData: {
				phone: '',
				password: ''
			},
			showPassword: false,
			agreed: false
		}
	},
	computed: {
		canLogin() {
			return this.formData.phone.length === 11 && 
			       this.formData.password.length >= 6 &&
			       this.agreed
		}
	},
	methods: {
		async handleLogin() {
			if (!this.canLogin) {
				uni.showToast({
					title: '请填写完整信息',
					icon: 'none'
				})
				return
			}

			try {
				const res = await api.auth.login(this.formData)
				
				if (res.code === 1) {
					setToken(res.data.access_token)
					uni.setStorageSync('user_info', res.data.user)
					
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					})
					
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1500)
				}
			} catch (e) {
				console.error('登录失败:', e)
			}
		},
		onAgreementChange(e) {
			this.agreed = e.detail.value.length > 0
		},
		goToRegister() {
			uni.navigateTo({
				url: '/pages/login/register'
			})
		},
		showAgreement() {
			uni.showModal({
				title: '用户协议',
				content: '这里是用户协议内容...',
				showCancel: false
			})
		},
		showPrivacy() {
			uni.showModal({
				title: '隐私政策',
				content: '这里是隐私政策内容...',
				showCancel: false
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.login-container {
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 100rpx 50rpx;
}

.login-header {
	text-align: center;
	margin-bottom: 80rpx;
	
	.logo {
		width: 160rpx;
		height: 160rpx;
		border-radius: 50%;
		background: #fff;
		margin-bottom: 30rpx;
	}
	
	.title {
		display: block;
		font-size: 48rpx;
		font-weight: bold;
		color: #fff;
		margin-bottom: 16rpx;
	}
	
	.subtitle {
		font-size: 28rpx;
		color: rgba(255, 255, 255, 0.8);
	}
}

.login-form {
	background: #fff;
	border-radius: 20rpx;
	padding: 60rpx 40rpx;
	margin-bottom: 40rpx;
}

.form-item {
	display: flex;
	align-items: center;
	padding: 30rpx 0;
	border-bottom: 1rpx solid #eee;
	
	.iconfont {
		font-size: 40rpx;
		color: #999;
		margin-right: 20rpx;
	}
	
	input {
		flex: 1;
		font-size: 32rpx;
	}
	
	.toggle-password {
		color: #999;
		font-size: 36rpx;
	}
}

.forgot-password {
	text-align: right;
	padding: 30rpx 0;
	
	text {
		color: #666;
		font-size: 26rpx;
	}
}

.login-btn {
	width: 100%;
	height: 90rpx;
	line-height: 90rpx;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: #fff;
	font-size: 32rpx;
	border-radius: 45rpx;
	margin: 40rpx 0;
	
	&[disabled] {
		background: #ccc;
		color: #fff;
	}
}

.register-link {
	text-align: center;
	padding: 20rpx 0;
	
	text {
		color: #666;
		font-size: 28rpx;
	}
	
	.link {
		color: #667eea;
		margin-left: 10rpx;
	}
}

.agreement {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-wrap: wrap;
	padding: 20rpx;
	background: rgba(255, 255, 255, 0.2);
	border-radius: 10rpx;
	
	text, label {
		color: #fff;
		font-size: 24rpx;
	}
	
	.link {
		color: #ffd700;
		margin: 0 5rpx;
	}
	
	checkbox {
		transform: scale(0.7);
	}
}
</style>
