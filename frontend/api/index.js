export default {
	auth: {
		register(data) {
			return http.post(API_ENDPOINTS.auth.register, data)
		},
		login(data) {
			return http.post(API_ENDPOINTS.auth.login, data)
		},
		refresh(refreshToken) {
			return http.post(API_ENDPOINTS.auth.refresh, { refresh_token: refreshToken })
		},
		logout() {
			return http.post(API_ENDPOINTS.auth.logout)
		}
	},
	user: {
		getProfile() {
			return http.get(API_ENDPOINTS.user.profile)
		},
		updateProfile(data) {
			return http.put(API_ENDPOINTS.user.updateProfile, data)
		},
		changePassword(data) {
			return http.post(API_ENDPOINTS.user.changePassword, data)
		}
	},
	task: {
		getCategories() {
			return http.get(API_ENDPOINTS.task.categories)
		},
		getList(params) {
			return http.get(API_ENDPOINTS.task.list, params)
		},
		getDetail(id) {
			return http.get(API_ENDPOINTS.task.detail(id))
		},
		create(data) {
			return http.post(API_ENDPOINTS.task.create, data)
		},
		accept(id) {
			return http.post(API_ENDPOINTS.task.accept(id))
		},
		submit(id, data) {
			return http.post(API_ENDPOINTS.task.submit(id), data)
		},
		verify(id, data) {
			return http.post(API_ENDPOINTS.task.verify(id), data)
		},
		getMyPublished(params) {
			return http.get(API_ENDPOINTS.task.myPublished, params)
		},
		getMyAccepted(params) {
			return http.get(API_ENDPOINTS.task.myAccepted, params)
		}
	},
	account: {
		getBalance() {
			return http.get(API_ENDPOINTS.account.balance)
		},
		getTransactions(params) {
			return http.get(API_ENDPOINTS.account.transactions, params)
		},
		withdraw(data) {
			return http.post(API_ENDPOINTS.account.withdraw, data)
		},
		getWithdrawals(params) {
			return http.get(API_ENDPOINTS.account.withdrawals, params)
		}
	},
	notification: {
		getList(params) {
			return http.get(API_ENDPOINTS.notification.list, params)
		},
		getUnreadCount() {
			return http.get(API_ENDPOINTS.notification.unreadCount)
		},
		markAsRead(id) {
			return http.post(API_ENDPOINTS.notification.markAsRead(id))
		},
		markAllAsRead() {
			return http.post(API_ENDPOINTS.notification.markAllAsRead)
		}
	},
	system: {
		getConfig() {
			return http.get(API_ENDPOINTS.system.config)
		},
		getBanners() {
			return http.get(API_ENDPOINTS.system.banners)
		},
		getAnnouncements() {
			return http.get(API_ENDPOINTS.system.announcements)
		},
		submitFeedback(data) {
			return http.post(API_ENDPOINTS.system.feedback, data)
		}
	}
}
