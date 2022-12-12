FROM nginx:alpine

ENV TimeZone=Asia/Shanghai 

# # 用本地的nginx配置文件覆盖镜像的Nginx配置
COPY dist /web/dist
COPY default.conf /etc/nginx/conf.d/default.conf