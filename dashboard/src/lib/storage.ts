/**
 * It takes a string as an argument and returns the value of the key in localStorage
 * @param {string} key - string - The key of the item you want to get from localStorage
 * @returns The value of the key in localStorage.
 */
export function getStorage(key: string) {
	return JSON.parse(localStorage.getItem(key)!);
}

/**
 * It takes a string as an argument and returns the value of the key in sessionStorage
 * @param {string} key - string - The key of the item you want to get from sessionStorage
 * @returns The value of the key in sessionStorage.
 */
export function getSession(key: string) {
	return JSON.parse(sessionStorage.getItem(key)!);
}

/**
 * This function sets a cookie with the name, value, and expiration time specified by the user.
 * @param {string} name - The name of the cookie.
 * @param {string} cookie - string - The cookie value
 * @param {number} expires - number - The amount of time in milliseconds that the cookie will last.
 * @param {string} [path='/'] - The path of the cookie.
 * @param {string} [sameSite=Strict] - 'Strict'
 * @param {string} [domain] - The domain of the cookie.
 */
export function setCookie(
	name: string,
	cookie: string,
	expires: number,
	path: string = '/',
	sameSite: string = 'Strict',
	domain: string = ''
) {
	function encode({ s }: { s: string }): string {
		return encodeURIComponent(s);
	}

	function stringifyCookieValue({ value }: { value: string }): string {
		return encode({ s: value });
	}

	function time(minutes: number, seconds: number, milliseconds: number): Date {
		var date = new Date();
		date.setTime(date.getTime() + 1 * 30 * 24 * minutes * seconds * milliseconds);
		return date;
	}

	document.cookie = [
		encode({ s: `${name}` }),
		'=',
		stringifyCookieValue({ value: `${cookie}` }),
		'; expires=' + time(60, 60, expires).toUTCString(),
		'; path=' + `${path}`,
		'; domain=' + `${domain}`,
		'; secure=' + true,
		'; sameSite=' + `${sameSite}`
	].join('');
}

/**
 * This function takes a key and a value, and sets the value in localStorage with the key.
 * @param {string} key - string - The key to store the value under
 * @param {any} value - any
 */
export function setStorage(key: string, value: any) {
	localStorage.setItem(key, JSON.stringify(value));
}

/**
 * It takes a string as an argument, and returns a string or undefined.
 * @param {string} name - The name of the cookie you want to get.
 * @returns A function that returns a string or undefined.
 */
export function getCookie(name: string): string | undefined {
	function getCookie(cookiename: any): string | undefined {
		const name = `${cookiename}=`;
		const decoded = decodeURIComponent(document.cookie);
		const arr = decoded.split('; ');
		let res;
		arr.forEach((val) => {
			if (val.indexOf(name) === 0) res = val.substring(name.length);
		});
		return res;
	}
	var cookie = getCookie(name);
	return cookie;
}

/**
 * Delete the localstorage infomation
 * @param key - string
 */
export var deleteStorage = async (key: string): Promise<void> => {
	localStorage.removeItem(key);
};

/**
 * This function takes a key and a value, and sets the value in session storage.
 * @param {string} key - The key to store the value under.
 * @param {any} value - any
 */
export function setSession(key: string, value: any) {
	sessionStorage.setItem(key, JSON.stringify(value));
}

/**
 * Delete the sessionstorage infomation
 * @param key - string
 */
export var deleteSession = async (key: string): Promise<void> => {
	sessionStorage.removeItem(key);
};

