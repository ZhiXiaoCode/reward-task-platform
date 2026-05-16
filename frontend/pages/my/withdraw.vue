<template>
	<view class="withdraw-container">
		<!-- 可提现余额 -->
		<view class="balance-section">
			<text class="label">可提现余额</text>
			<text class="balance">¥{{ balance }}</text>
		</view>

		<!-- 提现金额 -->
		<view class="form-section">
			<view class="form-label">提现金额</view>
			<view class="amount-input">
				<text class="currency">¥</text>
				<input 
					type="digit" 
					v-model="amount" 
					placeholder="请输入提现金额"
					class="input"
					@input="onAmountChange"
				/>
			</view>
			<view class="quick-amounts">
				<view 
					class="quick-item" 
					v-for="n in [50, 100, 200, 500]"
					:key="n"
					:class="{active: amount == n}"
					@click="amount = n"
				>
					{{ n }}元
				</view>
			</view>
		</view>

		<!-- 提现方式 -->
		<view class="form-section">
			<view class="form-label">提现方式</view>
			<radio-group @change="onPaymentMethodChange">
				<view class="payment-method">
					<view class="method-info">
						<text class="iconfont icon-wechat"></text>
						<text class="method-name">微信</text>
					</view>
					<radio value="wechat" :checked="paymentMethod === 'wechat'" color="#07c160"/>
				</view>
				<view class="payment-method">
					<view class="method-info">
						<text class="iconfont icon-alipay"></text>
						<text class="method-name">支付宝</text>
					</view>
					<radio value="alipay" :checked="paymentMethod === 'alipay'" color="#1677ff"/>
				</view>
			</radio-group>
		</view>

		<!-- 账户信息 -->
		<view class="form-section">
			<view class="form-label">账户信息</view>
			<input 
				type="text" 
				v-model="accountInfo" 
				placeholder="请输入微信/支付宝账号"
				class="form-input"
			/>
		</view>

		<!-- 提示 -->
		<view class="tips-section">
			<view class="tips-title">提现说明</view>
			<view class="tips-item">1. 最低提现金额为1元</view>
			<view class="tips-item">2. 提现申请提交后，1-3个工作日到账</view>
			<view class="tips-item">3. 每个账户每天最多提现3次</view>
		</view>

		<!-- 提交按钮 -->
		<button class="submit-btn" @click="handleSubmit" :disabled="!canSubmit">
			立即提现
		</button>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			balance: 0,
			amount: '',
			paymentMethod: 'wechat',
			accountInfo: ''
		}
	},
	computed: {
		canSubmit() {
			return parseFloat(this.amount) >= 1 && 
			       parseFloat(this.amount) <= this.balance &&
			       this.accountInfo.trim().length > 0
		}
	},
	onShow() {
		this.loadBalance()
	},
	methods: {
		async loadBalance() {
			try {
				const res = await api.account.getBalance()
				if (res.code === 1) {
					this.balance = res.data.balance
				}
			} catch (e) {
				console.error('获取余额失败:', e)
			}
		},
		onAmountChange(e) {
			this.amount = e.detail.value
		},
		onPaymentMethodChange(e) {
			this.paymentMethod = e.detail.value
		},
		async handleSubmit() {
			if (!this.canSubmit) {
				if (parseFloat(this.amount) < 1) {
					uni.showToast({ title: '最低提现金额为1元', icon: 'none' })
				} else if (parseFloat(this.amount) > this.balance) {
					uni.showToast({ title: '余额不足', icon: 'none' })
				} else if (!this.accountInfo.trim()) {
					uni.showToast({ title: '请输入账户信息', icon: 'none' })
				}
				return
			}

			try {
				uni.showLoading({ title: '提交中...' })
				const res = await api.account.withdraw({
					amount: parseFloat(this.amount),
					payment_method: this.paymentMethod,
					account_info: this.accountInfo
				})
				
				if (res.code === 1) {
					uni.showToast({
						title: '提现申请已提交',
						icon: 'success'
					})
					setTimeout(() => {
						uni.navigateBack()
					}, 1500)
				}
			} catch (e) {
				console.error('提现失败:', e)
			} finally {
				uni.hideLoading()
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.withdraw-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding: 20rpx;
}

.balance-section {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 40rpx;
	text-align: center;
	border-radius: 16rpx;
	margin-bottom: 20rpx;
	
	.label {
		display: block;
		font-size: 28rpx;
		color: rgba(255, 255, 255, 0.8);
		margin-bottom: 16rpx;
	}
	
	.balance {
		font-size: 64rpx;
		font-weight: bold;
		color: #fff;
	}
}

.form-section {
	background: #fff;
	padding: 30rpx;
	border-radius: 16rpx;
	margin-bottom: 20rpx;
	
	.form-label {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
	}
	
	.amount-input {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
		
		.currency {
			font-size: 48rpx;
			font-weight: bold;
			color: #333;
			margin-right: 16rpx;
		}
		
		.input {
			flex: 1;
			font-size: 40rpx;
			font-weight: bold;
		}
	}
	
	.quick-amounts {
		display: flex;
		gap: 20rpx;
		
		.quick-item {
			padding: 12rpx 30rpx;
			border: 1rpx solid #ddd;
			border-radius: 8rpx;
			font-size: 26rpx;
			color: #666;
			
			&.active {
				background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
				color: #fff;
				border-color: transparent;
			}
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
	
	radio-group {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.payment-method {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx;
		border: 1rpx solid #ddd;
		border-radius: 12rpx;
		
		.method-info {
			display: flex;
			align-items: center;
			
			.iconfont {
				font-size: 48rpx;
				margin-right: 16rpx;
				
				&.icon-wechat { color: #07c160; }
				&.icon-alipay { color: #1677ff; }
			}
			
			.method-name {
				font-size: 28rpx;
				color: #333;
			}
		}
	}
}

.tips-section {
	background: #fff9e6;
	padding: 30rpx;
	border-radius: 16rpx;
	margin-bottom: 30rpx;
	
	.tips-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #faad14;
		margin-bottom: 16rpx;
	}
	
	.tips-item {
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
