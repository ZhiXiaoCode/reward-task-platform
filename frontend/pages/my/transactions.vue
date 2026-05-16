<template>
	<view class="transactions-container">
		<!-- 筛选标签 -->
		<view class="filter-bar">
			<view 
				class="filter-item" 
				:class="{active: filterType === ''}"
				@click="changeFilter('')"
			>
				全部
			</view>
			<view 
				class="filter-item" 
				:class="{active: filterType === 'income'}"
				@click="changeFilter('income')"
			>
				收入
			</view>
			<view 
				class="filter-item" 
				:class="{active: filterType === 'expense'}"
				@click="changeFilter('expense')"
			>
				支出
			</view>
			<view 
				class="filter-item" 
				:class="{active: filterType === 'withdraw'}"
				@click="changeFilter('withdraw')"
			>
				提现
			</view>
		</view>

		<!-- 交易列表 -->
		<scroll-view class="list-scroll" scroll-y @scrolltolower="loadMore">
			<view class="transaction-list">
				<view 
					class="transaction-item" 
					v-for="item in transactions" 
					:key="item.id"
				>
					<view class="transaction-info">
						<text class="transaction-type">{{ getTypeText(item.type) }}</text>
						<text class="transaction-desc">{{ item.description }}</text>
						<text class="transaction-time">{{ formatDateTime(item.created_at) }}</text>
					</view>
					<text class="transaction-amount" :class="item.amount > 0 ? 'income' : 'expense'">
						{{ item.amount > 0 ? '+' : '' }}{{ item.amount }}
					</text>
				</view>
			</view>

			<view class="loading-more" v-if="loading">
				<text>加载中...</text>
			</view>
			<view class="no-more" v-if="!hasMore && transactions.length > 0">
				<text>没有更多了</text>
			</view>
			<view class="empty-state" v-if="!loading && transactions.length === 0">
				<text class="empty-text">暂无交易记录</text>
			</view>
		</scroll-view>
	</view>
</template>

<script>
import api from '@/api/index.js'

export default {
	data() {
		return {
			transactions: [],
			filterType: '',
			page: 1,
			pageSize: 20,
			hasMore: true,
			loading: false
		}
	},
	onLoad() {
		this.loadTransactions()
	},
	methods: {
		async loadTransactions() {
			if (this.loading) return
			
			try {
				this.loading = true
				const params = {
					page: this.page,
					page_size: this.pageSize
				}
				if (this.filterType) {
					params.transaction_type = this.filterType
				}
				
				const res = await api.account.getTransactions(params)
				if (res.code === 1) {
					if (this.page === 1) {
						this.transactions = res.data.items || []
					} else {
						this.transactions = [...this.transactions, ...(res.data.items || [])]
					}
					this.hasMore = res.data.items && res.data.items.length >= this.pageSize
				}
			} catch (e) {
				console.error('获取交易记录失败:', e)
			} finally {
				this.loading = false
			}
		},
		loadMore() {
			if (this.hasMore && !this.loading) {
				this.page++
				this.loadTransactions()
			}
		},
		changeFilter(type) {
			this.filterType = type
			this.page = 1
			this.hasMore = true
			this.loadTransactions()
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
		formatDateTime(dateStr) {
			if (!dateStr) return ''
			const date = new Date(dateStr)
			return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
		}
	}
}
</script>

<style lang="scss" scoped>
.transactions-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.filter-bar {
	display: flex;
	background: #fff;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #eee;
	
	.filter-item {
		flex: 1;
		text-align: center;
		font-size: 28rpx;
		color: #666;
		padding: 16rpx 0;
		
		&.active {
			color: #667eea;
			font-weight: bold;
		}
	}
}

.list-scroll {
	height: calc(100vh - 100rpx);
}

.transaction-list {
	padding: 20rpx;
}

.transaction-item {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	background: #fff;
	padding: 30rpx;
	border-radius: 16rpx;
	margin-bottom: 20rpx;
	
	.transaction-info {
		flex: 1;
		margin-right: 20rpx;
		
		.transaction-type {
			display: block;
			font-size: 28rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 8rpx;
		}
		
		.transaction-desc {
			display: block;
			font-size: 24rpx;
			color: #999;
			margin-bottom: 8rpx;
		}
		
		.transaction-time {
			font-size: 22rpx;
			color: #ccc;
		}
	}
	
	.transaction-amount {
		font-size: 36rpx;
		font-weight: bold;
		
		&.income {
			color: #52c41a;
		}
		
		&.expense {
			color: #333;
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
	justify-content: center;
	padding: 100rpx 0;
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}
</style>
