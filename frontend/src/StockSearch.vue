<template>
<p>搜索:</p>
<input v-model="symbol" placeholder='请输入股票代码' @keyup.enter="load_quote()">
<button :disabled="is_quote_loading"  type="button" @click="load_quote()">{{ is_quote_loading?'查询中...':'查询' }}</button>
<p>{{ quote_message }}</p>
<p v-if="quote">{{ quote.symbol }}-{{ quote.price }}</p>
<p v-if="quote">{{ market_data_label }}</p>
</template>
<script>
export default{
data(){
    return{symbol:'',
           quote:null,
           quote_message:'',
           is_quote_loading: false

    }

},
computed:{
    market_data_label(){
        if (this.quote === null) {
  return ''
}
    if(this.quote.market_data_type===1){
        return'实时行情'
    }
    if(this.quote.market_data_type===2){
        return'冻结行情'
    }
    if(this.quote.market_data_type===3){
        return'延迟行情'
    }
    if(this.quote.market_data_type===4){
        return'延迟冻结行情'
    }return '未知行情类型'
    
}},
methods:{
async load_quote(){
    if(this.is_quote_loading){
        return
    }
    this.quote= null
    this.quote_message= '正在查询'
    this.symbol= this.symbol.trim()
    if(this.symbol=== ''){
        this.quote_message= '请输入股票代码'
        return
    }
    this.is_quote_loading= true
    try{
    const response= await fetch('/stock/'+ this.symbol + '/search')
    if (response.ok=== false){
        const error= await response.json()
        this.quote_message= error.detail
        return
    }
    this.quote= await response.json()
    this.quote_message= '查询成功'}
    catch{this.quote_message = '请检查连接'}
    finally{this.is_quote_loading= false}
}   

}

}

</script>
