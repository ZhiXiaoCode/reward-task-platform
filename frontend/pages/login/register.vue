<template>
	<view class="register-container">
		<view class="register-header">
			<text class="title">注册账号</text>
			<text class="subtitle">加入我们，开始赚钱之旅</text>
		</view>

		<view class="register-form">
			<view class="form-item">
				<text class="label">手机号</text>
				<input 
					type="number" 
					v-model="formData.phone" 
					placeholder="请输入手机号"
					maxlength="11"
				/>
			</view>

			<view class="form-item">
				<text class="label">验证码</text>
				<input 
					type="number" 
					v-model="formData.code" 
					placeholder="请输入验证码"
					maxlength="6"
				/>
				<button 
					class="send-code-btn" 
					:disabled="countdown > 0"
					@click="sendCode"
				>
					{{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
				</button>
			</view>

			<view class="form-item">
				<text class="label">设置密码</text>
				<input 
					:type="showPassword ? 'text' : 'password'"
					v-model="formData.password" 
					placeholder="请设置6-20位密码"
					minlength="6"
					maxlength="20"
				/>
			</view>

			<view class="form-item">
				<text class="label">确认密码</text>
				<input 
					:type="showPassword ? 'text' : 'password'"
					v-model="formData.confirmPassword" 
					placeholder="请再次输入密码"
				/>
			</view>

			<button 
				class="register-btn" 
				:disabled="!canRegister"
				@click="handleRegister"
			>
				立即注册
			</button>

			<view class="login-link">
				<text>已有账号？</text>
				<text class="link" @click="goToLogin">立即登录</text>
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
				code: '',
				password: '',
				confirmPassword: ''
			},
			showPassword: false,
			agreed: false,
			countdown: 0
		}
	},
	computed: {
		canRegister() {
			return this.formData.phone.length === 11 && 
			       this.formData.code.length === 6 &&
			       this.formData.password.length >= 6 &&
			       this.formData.password === this.formData.confirmPassword &&
			       this.agreed
		}
	},
	methods: {
		async sendCode() {
			if (this.formData.phone.length !== 11) {
				uni.showToast({
					title: '请输入正确的手机号',
					icon: 'none'
				})
				return
			}

			this.countdown = 60
			const timer = setInterval(() => {
				this.countdown--
				if (this.countdown <= 0) {
					clearInterval(timer)
				}
			}, 1000)

			uni.showToast({
				title: '验证码已发送',
				icon: 'success'
			})
		},
		async handleRegister() {
			if (!this.canRegister) {
				if (this.formData.password !== this.formData.confirmPassword) {
					uni.showToast({
						title: '两次密码不一致',
						icon: 'none'
					})
				} else {
					uni.showToast({
						title: '请填写完整信息',
						icon: 'none'
					})
				}
				return
			}

			try {
				const res = await api.auth.register({
					phone: this.formData.phone,
					password: this.formData.password
				})
				
				if (res.code === 1) {
					setToken(res.data.access_token)
					uni.setStorageSync('user_info', res.data.user)
					
					uni.showToast({
						title: '注册成功',
						icon: 'success'
					})
					
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1500)
				}
			} catch (e) {
				console.error('注册失败:', e)
			}
		},
		onAgreementChange(e) {
			this.agreed = e.detail.value.length > 0
		},
		goToLogin() {
			uni.navigateBack()
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
.register-container {
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 100rpx 50rpx;
}

.register-header {
	text-align: center;
	margin-bottom: 60rpx;
	
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

.register-form {
	background: #fff;
	border-radius: 20rpx;
	padding: 60rpx 40rpx;
	margin-bottom: 40rpx;
}

.form-item {
	margin-bottom: 40rpx;
	
	.label {
		display: block;
		font-size: 28rpx;
		color: #666;
		margin-bottom: 16rpx;
	}
	
	input {
		width: 100%;
		height: 80rpx;
		padding: 0 20rpx;
		border: 1rpx solid #ddd;
		border-radius: 10rpx;
		font-size: 30rpx;
	}
	
	.send-code-btn {
		position: absolute;
		right: 10rpx;
		top: 50%;
		transform: translateY(-50%);
		padding: 10rpx 20rpx;
		background: #667eea;
		color: #fff;
		font-size: 24rpx;
		border-radius: 8rpx;
		
		&[disabled] {
			background: #ccc;
		}
	}
}

.register-btn {
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

.login-link {
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
