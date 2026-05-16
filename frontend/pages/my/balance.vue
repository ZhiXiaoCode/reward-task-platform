<template>
	<view class="balance-container">
		<!-- 余额卡片 -->
		<view class="balance-card">
			<text class="balance-label">账户余额（元）</text>
			<text class="balance-value">¥{{ balance }}</text>
			<view class="balance-buttons">
				<button class="btn recharge" @click="goToRecharge">充值</button>
				<button class="btn withdraw" @click="goToWithdraw">提现</button>
			</view>
		</view>

		<!-- 统计信息 -->
		<view class="stats-section">
			<view class="stat-item">
				<text class="stat-value">{{ stats.total_income }}</text>
				<text class="stat-label">累计收入</text>
			</view>
			<view class="stat-divider"></view>
			<view class="stat-item">
				<text class="stat-value">{{ stats.total_withdraw }}</text>
				<text class="stat-label">累计提现</text>
			</view>
		</view>

		<!-- 交易记录 -->
		<view class="transactions-section">
			<view class="section-header">
				<text class="section-title">交易记录</text>
				<text class="more" @click="goToTransactions">查看全部 ></text>
			</view>
			
			<view class="transaction-list">
				<view 
					class="transaction-item" 
					v-for="item in recentTransactions" 
					:key="item.id"
				>
					<view class="transaction-info">
						<text class="transaction-type">{{ getTypeText(item.type) }}</text>
						<text class="transaction-time">{{ formatTime(item.created_at) }}</text>
					</view>
					<text class="transaction-amount" :class="item.amount > 0 ? 'income' : 'expense'">
						{{ item.amount > 0 ? '+' : '' }}{{ item.amount }}
					</text>
				</view>
				
				<view class="empty-state" v-if="recentTransactions.length === 0">
					<text>暂无交易记录</text>
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
			balance: 0,
			stats: {
				total_income: 0,
				total_withdraw: 0
			},
			recentTransactions: []
		}
	},
	onShow() {
		this.loadBalance()
		this.loadRecentTransactions()
	},
	methods: {
		async loadBalance() {
			try {
				const res = await api.account.getBalance()
				if (res.code === 1) {
					this.balance = res.data.balance
					this.stats = res.data
				}
			} catch (e) {
				console.error('获取余额失败:', e)
			}
		},
		async loadRecentTransactions() {
			try {
				const res = await api.account.getTransactions({
					page: 1,
					page_size: 5
				})
				if (res.code === 1) {
					this.recentTransactions = res.data.items || []
				}
			} catch (e) {
				console.error('获取交易记录失败:', e)
			}
		},
		getTypeText(type) {
			const typeMap = {
				'income': '任务奖励',
				'expense': '任务支出',
				'withdraw': '提现',
				'deposit': '充值'
			}
			return typeMap[type] || type
		},
		formatTime(timeStr) {
			if (!timeStr) return ''
			const date = new Date(timeStr)
			return `${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
		},
		goToRecharge() {
			uni.showToast({
				title: '充值功能开发中',
				icon: 'none'
			})
		},
		goToWithdraw() {
			uni.navigateTo({
				url: '/pages/my/withdraw'
			})
		},
		goToTransactions() {
			uni.navigateTo({
				url: '/pages/my/transactions'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.balance-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.balance-card {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 60rpx 40rpx;
	text-align: center;
	
	.balance-label {
		display: block;
		font-size: 28rpx;
		color: rgba(255, 255, 255, 0.8);
		margin-bottom: 20rpx;
	}
	
	.balance-value {
		display: block;
		font-size: 72rpx;
		font-weight: bold;
		color: #fff;
		margin-bottom: 40rpx;
	}
	
	.balance-buttons {
		display: flex;
		gap: 30rpx;
		justify-content: center;
		
		.btn {
			width: 200rpx;
			height: 80rpx;
			line-height: 80rpx;
			font-size: 30rpx;
			border-radius: 40rpx;
			border: none;
			
			&.recharge {
				background: #fff;
				color: #667eea;
			}
			
			&.withdraw {
				background: transparent;
				border: 2rpx solid #fff;
				color: #fff;
			}
		}
	}
}

.stats-section {
	display: flex;
	background: #fff;
	margin: 20rpx;
	padding: 30rpx;
	border-radius: 16rpx;
	
	.stat-item {
		flex: 1;
		text-align: center;
		
		.stat-value {
			display: block;
			font-size: 40rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 10rpx;
		}
		
		.stat-label {
			font-size: 26rpx;
			color: #999;
		}
	}
	
	.stat-divider {
		width: 1rpx;
		background: #eee;
		margin: 0 30rpx;
	}
}

.transactions-section {
	margin: 20rpx;
	background: #fff;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
		
		.section-title {
			font-size: 30rpx;
			font-weight: bold;
			color: #333;
		}
		
		.more {
			font-size: 26rpx;
			color: #999;
		}
	}
	
	.transaction-list {
		.transaction-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 20rpx 0;
			border-bottom: 1rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.transaction-info {
				display: flex;
				flex-direction: column;
				
				.transaction-type {
					font-size: 28rpx;
					color: #333;
					margin-bottom: 8rpx;
				}
				
				.transaction-time {
					font-size: 24rpx;
					color: #999;
				}
			}
			
			.transaction-amount {
				font-size: 32rpx;
				font-weight: bold;
				
				&.income {
					color: #52c41a;
				}
				
				&.expense {
					color: #ff4d4f;
				}
			}
		}
		
		.empty-state {
			text-align: center;
			padding: 40rpx;
			color: #999;
			font-size: 26rpx;
		}
	}
}
</style>
