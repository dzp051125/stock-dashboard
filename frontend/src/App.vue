<template>
  <button @click="load_paper()">refresh</button>
  <AccountSelector  @select-paper="select_account = 'paper'"
                    @select-live="select_account = 'live'"></AccountSelector>
  <div v-if="current_account">
  <DashboardHeader :heading="current_account.name"></DashboardHeader>
  <AccountSummary :account="current_account"
                  :key='current_account.account_id'
                  >
  </AccountSummary>
  <AccountHistory v-if="current_account.source!=='IBKR'"
                  :account ='current_account'
                  :key=" current_account.account_id"></AccountHistory>
  <HoldingsList :positions="current_account.holding"></HoldingsList>
  </div>

  <p v-if="!paper_account && !live_account">No account data loaded.</p>
  <StatusMessage :message="status_message"></StatusMessage>
</template>
<script>
import DashboardHeader from './DashboardHeader.vue';
import AccountSummary from './account summary.vue';
import AccountSelector from './AccountSelector.vue';
import HoldingsList from './HoldingsList.vue';
import StatusMessage from './StatusMessage.vue';
import AccountHistory from './AccountHistory.vue';
export default{
components :{
  DashboardHeader: DashboardHeader,
  AccountSummary:AccountSummary,
  AccountSelector: AccountSelector,
  HoldingsList: HoldingsList,
  StatusMessage: StatusMessage,
  AccountHistory: AccountHistory
},
mounted(){
  this.load_paper()
  this.refresh_time= window.setInterval(
    this.load_paper,
    30000
  )
},
beforeUnmount(){
   window.clearInterval(this.refresh_time)
},
computed :{
  current_account(){
    if (this.select_account === 'paper'){
      return this.paper_account
    }
    return this.live_account
  }
},
methods:{
  
  async load_paper(){
    if (this.is_loading) {
  return
}
    this.is_loading = true
    if(this.paper_account === null)
    {this.status_message = '加载账户......'}
    if(this.paper_account){
      this.status_message= '正在刷新'
    }
    try{
      const response= await fetch('/accounts/paper')
      if(response.ok===false){
        if(this.paper_account === null)
        {this.status_message = 'Loading failed. Please check the connection.'}
        if(this.paper_account){
        this.status_message= 'Refresh failed. Showing previously loaded data.'
       }
        return
      }
      const account= await response.json()
      this.paper_account= account
      this.status_message = '账户数据将在30s后刷新'
    }
    catch{if(this.paper_account === null)
        {this.status_message = 'Loading failed. Please check the connection.'}
        if(this.paper_account){
        this.status_message= 'Refresh failed. Showing previously loaded data.'
      }}
    finally{this.is_loading= false}}
    


},

data(){
  return{
    select_account: 'paper',
    status_message: 'Waiting to load account data.',
    paper_account: null,
    live_account: null,
    is_loading: false,
    refresh_time: null
  }

}


}









</script>
