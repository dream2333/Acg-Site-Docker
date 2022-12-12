<template>
    <div class="bg">
        <el-card class="card-left">
            <el-result v-if="!logged" icon="warning" title="警告" sub-title="查看内容前请先登录"
                style="top:140px;position:relative">
            </el-result>
            <div v-else>
                <el-upload action="http://localhost:8000/API/user/info/" :show-file-list="false" :headers="headers"
                    name="avatar" :on-success="avatarUploaded">
                    <el-avatar :size="98" :src="circleUrl" style="margin-bottom: 16px;" />
                </el-upload>
                <div style="font-size: x-large;">{{ name }}</div>
                <div class="signature" v-if="!signatureEditing" @click="showSignatureInput">{{ signature ? signature : "这个人很懒，什么都没有留下" }}
                    <el-icon style="margin: 8px;cursor: pointer;" @click="showSignatureInput">
                        <edit />
                    </el-icon>
                </div>
                <el-input v-else ref="signatureInput" v-model="signature" class="signature" size="default"
                    @keyup.enter="signatureInput.$refs.input.blur()" @blur="handleSignatureInputConfirm"
                    maxlength="30" />
                <el-row class="list-user-info">
                    <el-icon style="margin: 8px;">
                        <user />
                    </el-icon>用户组：{{ isSupersuer ? "管理员" : "普通用户" }}
                </el-row>
                <el-row class="list-user-info">
                    <el-icon style="margin: 8px;">
                        <iphone />
                    </el-icon>
                    {{ "电话：" }} <el-button v-if="!phoneEditing" type="text" @click="showPhoneInput">{{
                        phone ? phone : "点击添加电话"
                    }}
                    </el-button>

                    <el-input v-else ref="phoneInput" v-model="phone" style="width: 10rem;" size="small"
                        @keyup.enter="phoneInput.$refs.input.blur()" @blur="handlePhoneInputConfirm"
                        oninput="value=value.replace(/[^\d]/g,'')" maxlength="11"></el-input>
                </el-row>
                <el-row class="list-user-info">
                    <el-icon style="margin: 8px;">
                        <message />
                    </el-icon>{{ "邮箱：" }}
                    <el-button v-if="!emailEditing" type="text" @click="showEmailInput">{{ email ? email : "未设定邮箱" }}
                    </el-button>
                    <el-input v-else ref="emailInput" v-model="email" style="width: 10rem;" size="small"
                        @keyup.enter="emailInput.$refs.input.blur()" @blur="handleEmailInputConfirm" maxlength="30">
                    </el-input>
                </el-row>
                <el-row class="list-user-info">
                    <el-icon style="margin: 8px;">
                        <cloudy />
                    </el-icon>{{ "上次登录：" + lastLogin }}
                </el-row>
                <el-row class="list-user-info">
                    <el-icon style="margin: 8px;">
                        <cloudy />
                    </el-icon>{{ "创建时间：" + dateJoined }}
                </el-row>
                <el-divider />
                <el-row class="list-user-info">标签：</el-row>
                <el-row class="list-user-info">
                    <dynamic-tags :tags="tags" />
                </el-row>
            </div>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { Iphone, User, Message, Cloudy, Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { getUserInfo, updateUserInfo } from '../api';

const headers = {
    Authorization: 'Token ' + localStorage.getItem('ACCESS_TOKEN')
}
const circleUrl = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')
const name = ref("")
const signature = ref("")
const phone = ref("")
const email = ref("")
const logged = ref(false)
const isSupersuer = ref(false)
const lastLogin = ref("")
const dateJoined = ref("")
const phoneEditing = ref(false)
const phoneInput = ref()
const signatureEditing = ref(false)
const signatureInput = ref()
const emailEditing = ref(false)
const emailInput = ref()
const tags = ref("")

function timeFormat(arg: string) {
    return arg.substring(0, 16).replace("T", " ")
}
function avatarUploaded() {
    window.location.reload()
}
//获取个人信息
getUserInfo().then((res) => {
    console.log(res.data)
    logged.value = true
    circleUrl.value = res.data.avatar
    email.value = res.data.email
    name.value = res.data.username
    isSupersuer.value = res.data.is_superuser
    phone.value = res.data.mobile
    lastLogin.value = timeFormat(res.data.last_login)
    dateJoined.value = timeFormat(res.data.date_joined)
    signature.value = res.data.signature
    tags.value = res.data.tags
}).catch((e)=>{
    console.log(e)
})
let phoneNumberTemp = ""
let emailTemp = ""
let signatureTemp = ""
function showPhoneInput() {
    phoneEditing.value = true
    phoneNumberTemp = phone.value
    nextTick(() => {
        phoneInput.value!.input!.focus()
    })
}
function showEmailInput() {
    emailEditing.value = true
    emailTemp = email.value
    nextTick(() => {
        emailInput.value!.input!.focus()
    })
}
function showSignatureInput() {
    signatureEditing.value = true
    signatureTemp = signature.value
    nextTick(() => {
        signatureInput.value!.input!.focus()
    })
}
//点击文字变为输入框后，失去焦点的操作
function handlePhoneInputConfirm() {
    if (phone.value.length != 11) {
        ElMessage({
            message: "电话格式不正确",
            type: "error",
            offset: 40
        });
        phone.value = phoneNumberTemp
    }
    if (phone.value == phoneNumberTemp) {
        phoneEditing.value = false
        return
    }
    updateUserInfo({ mobile: phone.value }).then((res) => {
        if (res.data.status == 0) {
            phone.value = phoneNumberTemp
            ElMessage({
                message: "更改信息错误",
                type: "error",
                offset: 40
            });
        } else {
            ElMessage({
                message: "更改电话号码成功",
                type: "success",
                offset: 40
            });
        }
    }).catch((e) => {
        console.log(e)
    }).finally(() => {
        phoneEditing.value = false
    })

}

//点击文字变为输入框后，失去焦点的操作
function handleEmailInputConfirm() {
    let emailReg = /^\w{3,}(\.\w+)*@[A-z0-9]+(\.[A-z]{2,5}){1,2}$/;
    let res = emailReg.test(email.value);
    if (!res) {
        email.value = emailTemp
        ElMessage({
            message: "邮箱格式不正确",
            type: "error",
            offset: 40
        });
    }
    if (email.value == emailTemp) {
        emailEditing.value = false
        return
    }
    updateUserInfo({ email: email.value }).then((res) => {
        if (res.data.status == 0) {
            email.value = emailTemp
            ElMessage({
                message: "更改信息错误",
                type: "error",
                offset: 40
            });
        } else {
            ElMessage({
                message: "更改邮箱成功",
                type: "success",
                offset: 40
            });
        }
    }).catch((e) => {
        console.log(e)
    }).finally(() => {
        emailEditing.value = false
    })

}
function handleSignatureInputConfirm() {
    if (signature.value == signatureTemp) {
        signatureEditing.value = false
        return
    }
    updateUserInfo({ signature: signature.value }).then((res) => {
        if (res.data.status == 0) {
            signature.value = signatureTemp
            ElMessage({
                message: "更改信息错误",
                type: "error",
                offset: 40
            });
        } else {
            ElMessage({
                message: "更改签名档成功",
                type: "success",
                offset: 40
            });
        }
    }).catch((e) => {
        console.log(e)
    }).finally(() => {
        signatureEditing.value = false
    })

}

</script>

<style scoped>
.bg {
    height: 100%;
    position: fixed;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.card-left {
    border-radius: 20px;
    height: 60%;
    width: 20%;
    min-height: 500px;
    min-width: 400px;
    line-height: 32px;
    padding: 32px 16px 24px 16px;
    justify-content: center;
}

.list-user-info {
    font-size: middle;
    font-weight: lighter;
    align-items: baseline;
}

.signature {
    font-size: middle;
    font-weight: lighter;
    margin-bottom: 16px;
    cursor: pointer;
}
</style>