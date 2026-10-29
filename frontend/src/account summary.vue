<template>
<p>{{ account.account_id }}</p>
<p>{{ account.name }}</p>
<p>as  of: {{ account.as_of }}</p>
<p>{{ account.netvalue }}</p>
<p>{{ account.currency }}</p>
<p>received at: {{ account.received_at }}</p>
<p>source: {{ account.source }}</p>
<p>ai-summary:{{summary}}</p>
</template>
<script>
export default{
props:['account'],
mounted(){this.read_summary()},

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