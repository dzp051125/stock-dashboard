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
    const respone= await fetch('/accounts/login' ,
    {method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(login_data)}
        )
    if(respone.ok===false){
        const error= await respone.json()
        this.status_message= error.detail
        return
    }
    this.$emit('login-success')
    
}

}
}
</script>