<template>
<p>接收时间: {{ account.as_of }}</p>
<p>账户编号：{{ account.account_id }}</p>
<p>账户名称：{{ account.name }}</p>
<p>账户净值：{{ account.netvalue }} {{ account.currency }}</p>
<p>当日盈亏：{{ account.daily_pnl }} {{ account.currency }}</p>
<p>未实现盈亏：{{ account.unrealized_pnl }} {{ account.currency }}</p>
<p>已实现盈亏：{{ account.realized_pnl }} {{ account.currency }}</p>
<p>股票持仓总市值：{{ account.stock_market_value }} {{ account.currency }}</p>
<p>购买力：{{ account.buying_power }} {{ account.currency }}</p>
<p v-if="account.cash !=null">现金余额：{{ account.cash }} {{ account.currency }}</p>
<p>基础币种：{{ account.currency }}</p>
<p>数据来源：{{ account.source }}</p>

<p v-if="account.source !=='IBKR'">AI 总结：{{ summary }}</p>
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