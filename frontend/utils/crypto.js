/**
 * 加密工具 - 增强版
 */

const SECRET_KEY = 'reward_task_secure_2024_v3'

const CryptoJS = {
	_Base64: (function() {
		const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
		
		return {
			encode: function(input) {
				if (!input) return ''
				let output = ''
				let bytes
				
				if (typeof input === 'string') {
					const encoder = new TextEncoder()
					bytes = Array.from(encoder.encode(input))
				} else if (input instanceof Uint8Array) {
					bytes = Array.from(input)
				} else {
					return ''
				}
				
				for (let i = 0; i < bytes.length; i += 3) {
					const byte1 = bytes[i]
					const byte2 = bytes[i + 1] || 0
					const byte3 = bytes[i + 2] || 0
					
					const enc1 = byte1 >> 2
					const enc2 = ((byte1 & 3) << 4) | (byte2 >> 4)
					const enc3 = ((byte2 & 15) << 2) | (byte3 >> 6)
					const enc4 = byte3 & 63
					
					if (bytes[i + 1] === undefined) {
						output += chars.charAt(enc1) + chars.charAt(enc2) + '=='
					} else if (bytes[i + 2] === undefined) {
						output += chars.charAt(enc1) + chars.charAt(enc2) + chars.charAt(enc3) + '='
					} else {
						output += chars.charAt(enc1) + chars.charAt(enc2) + chars.charAt(enc3) + chars.charAt(enc4)
					}
				}
				return output
			},
			
			decode: function(input) {
				if (!input) return ''
				try {
					let output = ''
					const bytes = []
					input = input.replace(/[^A-Za-z0-9+/=]/g, '')
					
					for (let i = 0; i < input.length; i += 4) {
						const enc1 = chars.indexOf(input[i])
						const enc2 = chars.indexOf(input[i + 1])
						const enc3 = chars.indexOf(input[i + 2])
						const enc4 = chars.indexOf(input[i + 3])
						
						if (enc1 === -1 || enc2 === -1) return ''
						
						bytes.push((enc1 << 2) | (enc2 >> 4))
						if (enc3 !== -1 && input[i + 2] !== '=') {
							bytes.push(((enc2 & 15) << 4) | (enc3 >> 2))
						}
						if (enc4 !== -1 && input[i + 3] !== '=') {
							bytes.push(((enc3 & 3) << 6) | enc4)
						}
					}
					
					const decoder = new TextDecoder()
					return decoder.decode(new Uint8Array(bytes))
				} catch (e) {
					return ''
				}
			}
		}
	})(),
	
	_xor: function(str, key) {
		if (!str || !key) return ''
		let result = ''
		for (let i = 0; i < str.length; i++) {
			result += String.fromCharCode(str.charCodeAt(i) ^ key.charCodeAt(i % key.length))
		}
		return result
	},
	
	encrypt: function(data) {
		try {
			const str = typeof data === 'string' ? data : JSON.stringify(data)
			const step1 = this._xor(str, SECRET_KEY)
			return this._Base64.encode(step1)
		} catch (e) {
			console.error('加密失败:', e)
			return ''
		}
	},
	
	decrypt: function(encrypted) {
		try {
			if (!encrypted) return ''
			const step1 = this._Base64.decode(encrypted)
			return this._xor(step1, SECRET_KEY)
		} catch (e) {
			console.error('解密失败:', e)
			return ''
		}
	},
	
	md5: function(str) {
		function safeAdd(x, y) {
			const lsw = (x & 0xffff) + (y & 0xffff)
			const msw = (x >> 16) + (y >> 16) + (lsw >> 16)
			return (msw << 16) | (lsw & 0xffff)
		}
		
		function bitRotateLeft(num, cnt) {
			return (num << cnt) | (num >>> (32 - cnt))
		}
		
		function md5cmn(q, a, b, x, s, t) {
			return safeAdd(bitRotateLeft(safeAdd(safeAdd(a, q), safeAdd(x, t)), s), b)
		}
		
		function md5ff(a, b, c, d, x, s, t) {
			return md5cmn((b & c) | ((~b) & d), a, b, x, s, t)
		}
		
		function md5gg(a, b, c, d, x, s, t) {
			return md5cmn((b & d) | (c & (~d)), a, b, x, s, t)
		}
		
		function md5hh(a, b, c, d, x, s, t) {
			return md5cmn(b ^ c ^ d, a, b, x, s, t)
		}
		
		function md5ii(a, b, c, d, x, s, t) {
			return md5cmn(c ^ (b | (~d)), a, b, x, s, t)
		}
		
		const x = []
		str = unescape(encodeURIComponent(str))
		
		for (let i = 0; i < str.length * 8; i += 8) {
			x[i >> 5] |= (str.charCodeAt(i / 8) & 0xff) << i % 32
		}
		
		x[str.length >> 5] |= 0x80 << (str.length % 32)
		x[(((str.length + 64) >>> 9) << 4) + 14] = str.length * 8
		
		let a = 1732584193, b = -271733879, c = -1732584194, d = 271733878
		
		for (let i = 0; i < x.length; i += 16) {
			const olda = a, oldb = b, oldc = c, oldd = d
			
			a = md5ff(a, b, c, d, x[i], 7, -680876936)
			d = md5ff(d, a, b, c, x[i + 1], 12, -389564586)
			c = md5ff(c, d, a, b, x[i + 2], 17, 606105819)
			b = md5ff(b, c, d, a, x[i + 3], 22, -1044525330)
			a = md5ff(a, b, c, d, x[i + 4], 7, -176418897)
			d = md5ff(d, a, b, c, x[i + 5], 12, 1200080426)
			c = md5ff(c, d, a, b, x[i + 6], 17, -1473231341)
			b = md5ff(b, c, d, a, x[i + 7], 22, -45705983)
			a = md5ff(a, b, c, d, x[i + 8], 7, 1770035416)
			d = md5ff(d, a, b, c, x[i + 9], 12, -1958414417)
			c = md5ff(c, d, a, b, x[i + 10], 17, -42063)
			b = md5ff(b, c, d, a, x[i + 11], 22, -1990404162)
			a = md5ff(a, b, c, d, x[i + 12], 7, 1804603682)
			d = md5ff(d, a, b, c, x[i + 13], 12, -40341101)
			c = md5ff(c, d, a, b, x[i + 14], 17, -1502002290)
			b = md5ff(b, c, d, a, x[i + 15], 22, 1236535329)
			
			a = md5gg(a, b, c, d, x[i + 1], 5, -165796510)
			d = md5gg(d, a, b, c, x[i + 6], 9, -1069501632)
			c = md5gg(c, d, a, b, x[i + 11], 14, 643717713)
			b = md5gg(b, c, d, a, x[i], 20, -373897302)
			a = md5gg(a, b, c, d, x[i + 5], 5, -701558691)
			d = md5gg(d, a, b, c, x[i + 10], 9, 38016083)
			c = md5gg(c, d, a, b, x[i + 15], 14, -660478335)
			b = md5gg(b, c, d, a, x[i + 4], 20, -405537848)
			a = md5gg(a, b, c, d, x[i + 9], 5, 568446438)
			d = md5gg(d, a, b, c, x[i + 14], 9, -1019803690)
			c = md5gg(c, d, a, b, x[i + 3], 14, -187363961)
			b = md5gg(b, c, d, a, x[i + 8], 20, 1163531501)
			a = md5gg(a, b, c, d, x[i + 13], 5, -1444681467)
			d = md5gg(d, a, b, c, x[i + 2], 9, -51403784)
			c = md5gg(c, d, a, b, x[i + 7], 14, 1735328473)
			b = md5gg(b, c, d, a, x[i + 12], 20, -1926607734)
			
			a = md5hh(a, b, c, d, x[i + 5], 4, -378558)
			d = md5hh(d, a, b, c, x[i + 8], 11, -2022574463)
			c = md5hh(c, d, a, b, x[i + 11], 16, 1839030562)
			b = md5hh(b, c, d, a, x[i + 14], 23, -35309556)
			a = md5hh(a, b, c, d, x[i + 1], 4, -1530992060)
			d = md5hh(d, a, b, c, x[i + 4], 11, 1272893353)
			c = md5hh(c, d, a, b, x[i + 7], 16, -155497632)
			b = md5hh(b, c, d, a, x[i + 10], 23, -1094730640)
			a = md5hh(a, b, c, d, x[i + 13], 4, 681279174)
			d = md5hh(d, a, b, c, x[i], 11, -358537222)
			c = md5hh(c, d, a, b, x[i + 3], 16, -722521979)
			b = md5hh(b, c, d, a, x[i + 6], 23, 76029189)
			a = md5hh(a, b, c, d, x[i + 9], 4, -640364487)
			d = md5hh(d, a, b, c, x[i + 12], 11, -421815835)
			c = md5hh(c, d, a, b, x[i + 15], 16, 530742520)
			b = md5hh(b, c, d, a, x[i + 2], 23, -995338651)
			
			a = md5ii(a, b, c, d, x[i], 6, -198630844)
			d = md5ii(d, a, b, c, x[i + 7], 10, 1126891415)
			c = md5ii(c, d, a, b, x[i + 14], 15, -1416354905)
			b = md5ii(b, c, d, a, x[i + 5], 21, -57434055)
			a = md5ii(a, b, c, d, x[i + 12], 6, 1700485571)
			d = md5ii(d, a, b, c, x[i + 3], 10, -1894986606)
			c = md5ii(c, d, a, b, x[i + 10], 15, -1051523)
			b = md5ii(b, c, d, a, x[i + 1], 21, -2054922799)
			a = md5ii(a, b, c, d, x[i + 8], 6, 1873313359)
			d = md5ii(d, a, b, c, x[i + 15], 10, -30611744)
			c = md5ii(c, d, a, b, x[i + 6], 15, -1560198380)
			b = md5ii(b, c, d, a, x[i + 13], 21, 1309151649)
			a = md5ii(a, b, c, d, x[i + 4], 6, -145523070)
			d = md5ii(d, a, b, c, x[i + 11], 10, -1120210379)
			c = md5ii(c, d, a, b, x[i + 2], 15, 718787259)
			b = md5ii(b, c, d, a, x[i + 9], 21, -343485551)
			
			a = safeAdd(a, olda)
			b = safeAdd(b, oldb)
			c = safeAdd(c, oldc)
			d = safeAdd(d, oldd)
		}
		
		const hex = (n) => {
			let s = ''
			for (let i = 0; i < 4; i++) {
				s += ((n >>> (i * 8)) & 255).toString(16).padStart(2, '0')
			}
			return s
		}
		
		return hex(a) + hex(b) + hex(c) + hex(d)
	}
}

export default CryptoJS
