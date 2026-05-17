const BASE_URL = 'https://reward-task-platform-production.up.railway.app/api'

const API_ENDPOINTS = {
	auth: {
		register: `${BASE_URL}/auth/register`,
		login: `${BASE_URL}/auth/login`,
		refresh: `${BASE_URL}/auth/refresh`,
		logout: `${BASE_URL}/auth/logout`
	},
	user: {
		profile: `${BASE_URL}/user/profile`,
		updateProfile: `${BASE_URL}/user/profile`,
		changePassword: `${BASE_URL}/user/password`
	},
	task: {
		categories: `${BASE_URL}/tasks/categories`,
		list: `${BASE_URL}/tasks`,
		detail: (id) => `${BASE_URL}/tasks/${id}`,
		create: `${BASE_URL}/tasks`,
		accept: (id) => `${BASE_URL}/tasks/${id}/accept`,
		submit: (id) => `${BASE_URL}/tasks/${id}/submit`,
		verify: (id) => `${BASE_URL}/tasks/${id}/verify`,
		myPublished: `${BASE_URL}/tasks/my/published`,
		myAccepted: `${BASE_URL}/tasks/my/accepted`
	},
	account: {
		balance: `${BASE_URL}/account/balance`,
		transactions: `${BASE_URL}/account/transactions`,
		withdraw: `${BASE_URL}/account/withdraw`,
		withdrawals: `${BASE_URL}/account/withdrawals`
	},
	notification: {
		list: `${BASE_URL}/notifications`,
		unreadCount: `${BASE_URL}/notifications/unread-count`,
		markAsRead: (id) => `${BASE_URL}/notifications/${id}/read`,
		markAllAsRead: `${BASE_URL}/notifications/read-all`
	},
	system: {
		config: `${BASE_URL}/system/config`,
		banners: `${BASE_URL}/system/banners`,
		announcements: `${BASE_URL}/system/announcements`,
		feedback: `${BASE_URL}/system/feedback`
	}
}

export default API_ENDPOINTS

