import axios from 'axios';

/* It's creating a new axios instance with a baseURL. */
const axiosAPI = axios.create({
    baseURL: "https://api.cryptflixinvest.com/api/bob/",
    headers: {
        "Content-Type": "application/json"
    },
    withCredentials: true,
    timeout: 40000
})

/**
 * It's a function that takes in a method, url, request, and headers, and returns a promise that
 * resolves to the data from the response, or rejects with the error.
 * @param {string} method - The HTTP method to use for the request.
 * @param {string} url - The URL of the API request.
 * @param {any} request - the request body
 * @param {any} headers - any = {}
 * @returns The return value is a promise.
 */
const apiRequest = (method: string, url: string, request: any) => {

    //using the axios instance to perform the request that received from each http method
    return axiosAPI({
        method: method,
        url: url,
        data: request
    }).then(res => {
        return Promise.resolve(res.data);
    })
        .catch(err => {
            return Promise.reject(err);
        });
};

/**
 * Post is a function that takes a url and a request and returns an apiRequest with the method post,
 * the url, and the request.
 * @param {string} url - The URL to make the request to.
 * @param {any} request - the request object
 */
const post = (url: string, request: any) => apiRequest("post", url, request);

/**
 * It takes a url and a request object, and returns a promise that resolves to the response from the
 * server
 * @param {string} url - The URL to make the request to.
 * @param {any} request - The request object that is passed to the API.
 */
const get = (url: string, request: any) => apiRequest("get", url, request);

/* It's creating an object with the post and get functions. */
const API = {
    post,
    get
}

export default API;