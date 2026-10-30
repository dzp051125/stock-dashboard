<template>
<p>{{ account.account_id }}</p>
<p>{{ account.name }}</p>
<p>{{ account.netvalue }}</p>
<p v-if="account.cash !=null">cash:{{ account.cash }}{{account.currency}}</p>
<p>base currency:{{ account.currency }}</p>
<p>source: {{ account.source }}</p>
<p v-if="account.source !=='IBKR'">ai-summary:{{summary}}</p>
</template>
<script>
export default{
props:['account'],
mounted(){if(this.account.source !='IBKR'){
    this.read_summary()}},

data(){
    return{
    summary:'no action'}
},
methods:{
    async read_summary(){
        try{const response= await fetch('/accounts/'+ this.account.account_id + '/account-summary',{method:'POST'})
            if(response.ok===false){
                this.summary='response failed'
                return
            }
            const data= await response.json()
            this.summary= data.summary
        }

        catch{this.summary= 'load failed'}
    }}
}
</script>