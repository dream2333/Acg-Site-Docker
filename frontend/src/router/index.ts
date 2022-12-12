import { createRouter, createWebHistory,createWebHashHistory } from "vue-router";
import AppAboutVue from "../components/AppAbout.vue";
import VideoViewVue from "../components/video/VideoView.vue";
import VideoListViewVue from "../components/home/VideoListView.vue";
import HistoryViewVue from "../components/home/HistoryView.vue";
import HomeViewVue from "../components/Home/HomeView.vue";
import HomePageVue from "../views/HomePage.vue";
import MessageBoardVue from "../views/MessageBoard.vue";
import UserInfoPageVue from "../views/UserInfoPage.vue";
import VideoLikedListViewVue from "../components/home/VideoLikedListView.vue";
import ArticleViewVue from "../components/home/ArticleView.vue";
import SearchPageVue from "../views/SearchPage.vue";
const routes = [
  {
    path: "/",
    name: "index",
    component: HomePageVue,
    meta: {
      title: "首页",
    },
    children: [
      {
        path: "/home",
        name: "home",
        component: HomeViewVue,
      },
      {
        path: "/videoList",
        name: "videoList",
        component: VideoListViewVue,
        meta: { keepAlive: true },
      },
      {
        path: "/like",
        name: "like",
        component: VideoLikedListViewVue,
      },
      {
        path: "/video/:id",
        name: "video",
        component: VideoViewVue,
      },
      {
        path: "/article/:id",
        name: "article",
        component: ArticleViewVue,
      },
      {
        path: "/search/:str?",
        name: "search",
        component: SearchPageVue,
      },
      {
        path: "/history",
        name: "history",
        component: HistoryViewVue,
      }
    ],
  },
  {
    path: "/msgboard",
    name: "msgboard",
    component: MessageBoardVue,
    meta: {
      title: "留言板",
    },
  },
  {
    path: "/userinfo",
    name: "userinfo",
    component: UserInfoPageVue,
    meta: {
      title: "个人信息",
    },
  },
  {
    path: "/about",
    name: "about",
    component: AppAboutVue,
    meta: {
      title: "关于",
    },
  },
  {
    path: "",
    redirect: "/home",
  },
];
export const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});
