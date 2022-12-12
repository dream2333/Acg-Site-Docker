import { Request } from "./utils/request";
//用户注册
export function register(parameter: any) {
  return Request.axiosInstance({
    url: "API/user/register/",
    method: "post",
    data: parameter,
  });
}
//用户登录
export function login(parameter: any) {
  return Request.axiosInstance({
    url: "API/user/login/",
    method: "post",
    data: parameter,
  });
}
//用户注销
export function logout() {
  return Request.axiosInstance({
    url: "API/user/logout/",
    method: "get",
  });
}
//获取用户信息
export function getUserInfo() {
  return Request.axiosInstance({
    url: "API/user/info/",
    method: "get",
  });
}
//更新用户信息
export function updateUserInfo(parameter: any) {
  return Request.axiosInstance({
    url: "API/user/info/",
    method: "post",
    data: parameter,
  });
}
//获取所有留言板内容
export function getAllMessage() {
  return Request.axiosInstance({
    url: "API/message/list/",
    method: "get",
  });
}
//获取当前用户留言板内容
export function getMyMessage() {
  return Request.axiosInstance({
    url: "API/message/my/",
    method: "get",
  });
}

//获取评论内容
export function getComment(link_to: number) {
  return Request.axiosInstance({
    url: "API/video/" + link_to.toString() + "/comment/",
    method: "get",
  });
}

//上传留言板内容
export function leaveMessage(parameter: any) {
  return Request.axiosInstance({
    url: "API/message/my/",
    method: "post",
    data: parameter,
  });
}
//上传评论内容
export function leaveComment(parameter: any) {
  return Request.axiosInstance({
    url: "API/video/comment/",
    method: "post",
    data: parameter,
  });
}

//获取视频详细信息
export function getVideoInfo(index: Number) {
  return Request.axiosInstance({
    url: "API/video/" + index.toString() + "/",
    method: "get",
  });
}

//获取视频列表
export function getVideoList(page: Number, ordering: string) {
  return Request.axiosInstance({
    url: "/API/video/list?page=" + page.toString() + "&ordering=" + ordering,
    method: "get",
  });
}

//添加视频到喜欢列表
export function likeVideo(video_id: Number) {
  return Request.axiosInstance({
    url: "API/video/like/" + video_id.toString() + "/",
    method: "get",
  });
}

//获取喜欢列表
export function getLikedList() {
  return Request.axiosInstance({
    url: "API/video/like/list/",
    method: "get",
  });
}

//从喜欢列表移除视频
export function removeLiked(video_id: Number) {
  return Request.axiosInstance({
    url: "API/video/like/remove/" + video_id.toString() + "/",
    method: "get",
  });
}
//获取菜单数据
export function getMenu() {
  return Request.axiosInstance({
    url: "API/homemenu",
    method: "get",
  });
}
//获取文章
export function getArticle(index: number) {
  return Request.axiosInstance({
    url: "API/article/" + index.toString() + "/",
    method: "get",
  });
}

//获取文章列表
export function getArticleList() {
  return Request.axiosInstance({
    url: "API/article/list/?ordering=-timestamp",
    method: "get",
  });
}

//搜索视频
export function videoSearch(query: string, page: number) {
  return Request.axiosInstance({
    url: "/API/video/search/?query=" + query + "&page="+page.toString() ,
    method: "get",
  });
}
