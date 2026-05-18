<template>
	<view class="messages-container">
		<view class="message-list" v-if="messages.length > 0">
			<view 
				class="message-item" 
				v-for="item in messages" 
				:key="item.id"
				@click="goToDetail(item)"
			>
				<view class="message-header">
					<text class="title">{{ item.title }}</text>
					<text class="time">{{ item.time }}</text>
				</view>
				<text class="content">{{ item.content }}</text>
				<view class="unread-dot" v-if="!item.is_read"></view>
			</view>
		</view>
		
		<view class="empty-state" v-else>
			<text class="iconfont icon-message"></text>
			<text>暂无消息</text>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			messages: []
		}
	},
	onLoad() {
		this.loadMessages()
	},
	methods: {
		async loadMessages() {
			// TODO: 从API加载消息
			this.messages = [
				{
					id: 1,
					title: '系统通知',
					content: '欢迎使用悬赏任务平台！',
					time: '2024-01-01',
					is_read: false
				}
			]
		},
		goToDetail(item) {
			uni.navigateTo({
				url: `/pages/my/notifications`
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.messages-container {
	min-height: 100vh;
	background: #f5f5f5;
}

.message-list {
	padding: 20rpx;
	
	.message-item {
		position: relative;
		padding: 30rpx;
		background: #fff;
		border-radius: 16rpx;
		margin-bottom: 20rpx;
		
		.message-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 16rpx;
			
			.title {
				font-size: 30rpx;
				font-weight: bold;
			}
			
			.time {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.content {
			font-size: 26rpx;
			color: #666;
			line-height: 1.5;
		}
		
		.unread-dot {
			position: absolute;
			top: 30rpx;
			right: 30rpx;
			width: 16rpx;
			height: 16rpx;
			background: #ff4d4f;
			border-radius: 50%;
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 200rpx 0;
	
	.iconfont {
		font-size: 100rpx;
		color: #ddd;
		margin-bottom: 30rpx;
	}
	
	text {
		color: #999;
		font-size: 28rpx;
	}
}
</style>
