<template>
	<view class="search-container">
		<view class="search-header">
			<view class="search-box">
				<text class="iconfont icon-search"></text>
				<input 
					type="text" 
					v-model="keyword" 
					placeholder="搜索任务" 
					@confirm="handleSearch"
					confirm-type="search"
				/>
				<text class="iconfont icon-close" v-if="keyword" @click="clearKeyword"></text>
			</view>
			<text class="cancel-btn" @click="goBack">取消</text>
		</view>
		
		<view class="search-history" v-if="historyList.length > 0">
			<view class="section-header">
				<text class="title">搜索历史</text>
				<text class="clear" @click="clearHistory">清空</text>
			</view>
			<view class="history-tags">
				<text 
					class="tag" 
					v-for="(item, index) in historyList" 
					:key="index"
					@click="searchByHistory(item)"
				>{{ item }}</text>
			</view>
		</view>
		
		<view class="hot-search">
			<view class="section-header">
				<text class="title">热门搜索</text>
			</view>
			<view class="hot-tags">
				<text class="tag" @click="searchByHistory('注册')">注册任务</text>
				<text class="tag" @click="searchByHistory('下载')">下载任务</text>
				<text class="tag" @click="searchByHistory('关注')">关注任务</text>
				<text class="tag" @click="searchByHistory('问卷')">问卷调查</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			keyword: '',
			historyList: []
		}
	},
	onLoad() {
		this.loadHistory()
	},
	methods: {
		loadHistory() {
			const history = uni.getStorageSync('search_history') || []
			this.historyList = history
		},
		handleSearch() {
			if (!this.keyword.trim()) return
			
			this.saveHistory(this.keyword)
			uni.navigateTo({
				url: `/pages/task/list?keyword=${encodeURIComponent(this.keyword)}`
			})
		},
		searchByHistory(keyword) {
			this.keyword = keyword
			this.handleSearch()
		},
		saveHistory(keyword) {
			let history = uni.getStorageSync('search_history') || []
			history = history.filter(item => item !== keyword)
			history.unshift(keyword)
			if (history.length > 10) history = history.slice(0, 10)
			uni.setStorageSync('search_history', history)
		},
		clearHistory() {
			uni.removeStorageSync('search_history')
			this.historyList = []
		},
		clearKeyword() {
			this.keyword = ''
		},
		goBack() {
			uni.navigateBack()
		}
	}
}
</script>

<style lang="scss" scoped>
.search-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.search-header {
	display: flex;
	align-items: center;
	padding: 20rpx 30rpx;
	background: #fff;
	
	.search-box {
		flex: 1;
		display: flex;
		align-items: center;
		height: 70rpx;
		padding: 0 20rpx;
		background: #f5f5f5;
		border-radius: 35rpx;
		
		.iconfont {
			color: #999;
			font-size: 32rpx;
		}
		
		input {
			flex: 1;
			margin: 0 15rpx;
			font-size: 28rpx;
		}
	}
	
	.cancel-btn {
		margin-left: 20rpx;
		font-size: 28rpx;
		color: #666;
	}
}

.search-history, .hot-search {
	margin-top: 20rpx;
	padding: 30rpx;
	background: #fff;
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
		
		.title {
			font-size: 30rpx;
			font-weight: bold;
		}
		
		.clear {
			font-size: 26rpx;
			color: #999;
		}
	}
	
	.history-tags, .hot-tags {
		display: flex;
		flex-wrap: wrap;
		
		.tag {
			padding: 12rpx 24rpx;
			margin: 10rpx 20rpx 10rpx 0;
			background: #f5f5f5;
			border-radius: 30rpx;
			font-size: 26rpx;
			color: #666;
		}
	}
}
</style>
