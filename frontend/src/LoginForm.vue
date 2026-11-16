<template>
<p>sign up</p>
<input v-model='this.account_id' type="text" placeholder="账号">
<input v-model= 'this.password' type="password" placeholder="密码">
<button type="button" @click="verify_account(account_id, password)">登录</button>
<p>{{ status_message }}</p>
</template>
<script>
export default{
data(){
return{'account_id':'',
       'password': '',
       status_message: ''
}
},

methods:{
async verify_account(account_id, password){
    const login_data={
        account_id:account_id,
        password: password,
        
    }
    try{
    this.status_message= '正在验证账号信息，请稍后...'
    const respone= await fetch('/accounts/login' ,
    {method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(login_data)}
        )
    if(respone.status=== 401){
        this.status_message= '账号或者密码错误，请重新登录'
        return
    }
    if(respone.ok===false){
        this.status_message= '无法验证账号信息,状态码: '+ respone.status    
        return
    }
    this.$emit('login-success')}
    catch{
        this.status_message= '无法验证账号信息，请检查连接'
    }

    
}

}
}
</script>