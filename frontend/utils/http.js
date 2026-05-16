/**
 * HTTP请求工具 - 完整版
 */

import CryptoJS from '@/utils/crypto.js'
import API_ENDPOINTS from '@/config/api.config.js'

const STORAGE_KEY = {
	ACCESS_TOKEN: 'access_token',
	REFRESH_TOKEN: 'refresh_token',
	USER_INFO: 'user_info'
}

const getToken = () => {
	const encrypted = uni.getStorageSync(STORAGE_KEY.ACCESS_TOKEN)
	if (!encrypted) return ''
	try {
		return CryptoJS.decrypt(encrypted) || ''
	} catch (e) {
		console.error('Token解密失败:', e)
		return ''
	}
}

const setToken = (token) => {
	if (!token) return
	const encrypted = CryptoJS.encrypt(token)
	uni.setStorageSync(STORAGE_KEY.ACCESS_TOKEN, encrypted)
}

const setRefreshToken = (token) => {
	if (!token) return
	const encrypted = CryptoJS.encrypt(token)
	uni.setStorageSync(STORAGE_KEY.REFRESH_TOKEN, encrypted)
}

const clearToken = () => {
	uni.removeStorageSync(STORAGE_KEY.ACCESS_TOKEN)
	uni.removeStorageSync(STORAGE_KEY.REFRESH_TOKEN)
	uni.removeStorageSync(STORAGE_KEY.USER_INFO)
}

const getRefreshToken = () => {
	const encrypted = uni.getStorageSync(STORAGE_KEY.REFRESH_TOKEN)
	if (!encrypted) return ''
	try {
		return CryptoJS.decrypt(encrypted) || ''
	} catch (e) {
		return ''
	}
}

let isRefreshing = false
let refreshQueue = []

const processQueue = (error, token = null) => {
	refreshQueue.forEach(promise => {
		if (error) {
			promise.reject(error)
		} else {
			promise.resolve(token)
		}
	})
	refreshQueue = []
}

const refreshToken = () => {
	return new Promise((resolve, reject) => {
		const refresh_token = getRefreshToken()
		if (!refresh_token) {
			reject(new Error('No refresh token'))
			return
		}

		uni.request({
			url: API_ENDPOINTS.auth.refresh,
			method: 'POST',
			data: { refresh_token },
			success: (res) => {
				if (res.data.code === 1) {
					const { access_token, refresh_token: newRefreshToken } = res.data.data
					setToken(access_token)
					setRefreshToken(newRefreshToken)
					resolve(access_token)
				} else {
					clearToken()
					reject(new Error('Refresh failed'))
				}
			},
			fail: (err) => {
				reject(err)
			}
		})
	})
}

const request = (options) => {
	const {
		url,
		method = 'GET',
		data = {},
		header = {},
		loading = true,
		autoAuth = true
	} = options

	if (loading) {
		uni.showLoading({ title: '加载中...', mask: true })
	}

	return new Promise((resolve, reject) => {
		const token = getToken()
		const headers = {
			'Content-Type': 'application/json',
			...header
		}

		if (token && autoAuth) {
			headers['Authorization'] = `Bearer ${token}`
		}

		const requestOptions = {
			url,
			method,
			data,
			header: headers,
			success: (res) => {
				if (loading) {
					uni.hideLoading()
				}

				if (res.statusCode === 200) {
					const response = res.data
					
					if (response.code === 1) {
						resolve(response)
					} else if (response.code === 0) {
						uni.showToast({
							title: response.msg || '操作失败',
							icon: 'none',
							duration: 2000
						})
						reject(response)
					} else if (response.code === 401) {
						if (autoAuth && !isRefreshing) {
							isRefreshing = true
							refreshToken()
								.then(newToken => {
									isRefreshing = false
									processQueue(null, newToken)
									const newHeaders = { ...headers, 'Authorization': `Bearer ${newToken}` }
									uni.request({
										url, method, data, header: newHeaders,
										success: (res) => resolve(res.data),
										fail: reject
									})
								})
								.catch(err => {
									isRefreshing = false
									processQueue(err, null)
									clearToken()
									uni.reLaunch({ url: '/pages/login/login' })
									reject(err)
								})
						} else {
							return new Promise((resolve, reject) => {
								refreshQueue.push({ resolve, reject })
							}).then(() => {
								const newToken = getToken()
								const newHeaders = { ...headers, 'Authorization': `Bearer ${newToken}` }
								uni.request({
									url, method, data, header: newHeaders,
									success: (res) => resolve(res.data),
									fail: reject
								})
							})
						}
					} else {
						reject(response)
					}
				} else if (res.statusCode === 401) {
					if (autoAuth) {
						clearToken()
						uni.showToast({ title: '登录已过期，请重新登录', icon: 'none' })
						setTimeout(() => {
							uni.reLaunch({ url: '/pages/login/login' })
						}, 1500)
					}
					reject(res.data)
				} else if (res.statusCode >= 500) {
					uni.showToast({
						title: '服务器错误，请稍后重试',
						icon: 'none',
						duration: 2000
					})
					reject(res.data)
				} else {
					uni.showToast({
						title: '请求失败',
						icon: 'none',
						duration: 2000
					})
					reject(res.data)
				}
			},
			fail: (err) => {
				if (loading) {
					uni.hideLoading()
				}
				uni.showToast({
					title: '网络连接失败',
					icon: 'none',
					duration: 2000
				})
				reject(err)
			}
		}

		uni.request(requestOptions)
	})
}

const http = {
	get: (url, data, options = {}) => {
		return request({
			url,
			method: 'GET',
			data,
			...options
		})
	},
	post: (url, data, options = {}) => {
		return request({
			url,
			method: 'POST',
			data,
			...options
		})
	},
	put: (url, data, options = {}) => {
		return request({
			url,
			method: 'PUT',
			data,
			...options
		})
	},
	delete: (url, data, options = {}) => {
		return request({
			url,
			method: 'DELETE',
			data,
			...options
		})
	},
	upload: (url, filePath, formData = {}, options = {}) => {
		return new Promise((resolve, reject) => {
			if (options.loading !== false) {
				uni.showLoading({ title: '上传中...', mask: true })
			}

			const token = getToken()
			const header = {
				'Authorization': token ? `Bearer ${token}` : '',
				...options.header
			}

			uni.uploadFile({
				url,
				filePath,
				name: options.name || 'file',
				formData,
				header,
				success: (res) => {
					if (options.loading !== false) {
						uni.hideLoading()
					}
					const data = JSON.parse(res.data)
					if (data.code === 1) {
						resolve(data)
					} else {
						uni.showToast({ title: data.msg || '上传失败', icon: 'none' })
						reject(data)
					}
				},
				fail: (err) => {
					if (options.loading !== false) {
						uni.hideLoading()
					}
					uni.showToast({ title: '上传失败', icon: 'none' })
					reject(err)
				}
			})
		})
	}
}

export {
	http,
	API_ENDPOINTS,
	STORAGE_KEY,
	setToken,
	setRefreshToken,
	clearToken,
	getToken,
	getRefreshToken
}
