import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { ElMessage, } from 'element-plus';


export class Request {
    public static axiosInstance: AxiosInstance;

    // constructor() {
    //     // 创建axios实例
    //     this.axiosInstance = axios.create({timeout: 1000 * 12});
    //     // 初始化拦截器
    //     this.initInterceptors();
    // }

    public static init() {
        // 创建axios实例
        this.axiosInstance = axios.create({
            baseURL: location.origin,
            timeout: 6000,
        });
        this.axiosInstance.defaults.withCredentials = true
        // 初始化拦截器
        this.initInterceptors();
        return axios;
    }

    // 为了让http.ts中获取初始化好的axios实例
    // public getInterceptors() {
    //     return this.axiosInstance;
    // }



    // 初始化拦截器
    public static initInterceptors() {
        // 设置post请求头
        axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';

        /**
         * 请求拦截器
         * 每次请求前，如果存在token则在请求头中携带token
         */
        this.axiosInstance.interceptors.request.use(
            (config: AxiosRequestConfig) => {

                // 登录流程控制中，根据本地是否存在token判断用户的登录情况
                // 但是即使token存在，也有可能token是过期的，所以在每次的请求头中携带token
                // 后台根据携带的token判断用户的登录情况，并返回给我们对应的状态码
                // if (config.headers.isJwt) {

                const token = localStorage.getItem('ACCESS_TOKEN');
                if (token) {
                    config.headers!.Authorization = 'Token ' + token;
                }
                return config
            },
            (error: any) => {
                console.log(error);
            },
        );


        // 响应拦截器
        this.axiosInstance.interceptors.response.use(
            // 请求成功
            (response: AxiosResponse) => {
                // if (res.headers.authorization) {
                //     localStorage.setItem('id_token', res.headers.authorization);
                // } else {
                //     if (res.data && res.data.token) {
                //         localStorage.setItem('id_token', res.data.token);
                //     }
                // }

                if (response.status === 200) {
                    // return Promise.resolve(response.data);
                    return response;
                } else {
                    Request.errorHandle(response);
                    // return Promise.reject(response.data);
                    return response;
                }
            },
            // 请求失败
            (error: any) => {
                const { response } = error;
                if (response) {
                    // 请求已发出，但是不在2xx的范围
                    Request.errorHandle(response);
                    return Promise.reject(response.data);
                } else {
                    // 处理断网的情况
                    // eg:请求超时或断网时，更新state的network状态
                    // network状态在app.vue中控制着一个全局的断网提示组件的显示隐藏
                    // 关于断网组件中的刷新重新获取数据，会在断网组件中说明
                    ElMessage({ message: '网络异常', type: "error", offset: 40 });
                }
            });
    }


    /**
     * http握手错误
     * @param res 响应回调,根据不同响应进行不同操作
     */
    private static errorHandle(res: any) {
        // 状态码判断
        switch (res.status) {
            case 401:
                break;
            case 403:
                break;
            case 404:
                ElMessage({ message: '请求的资源不存在', type: "warning", offset: 40 });
                break;
            default:
                ElMessage({ message: '连接错误', type: "error", offset: 40 });
        }
    }


}