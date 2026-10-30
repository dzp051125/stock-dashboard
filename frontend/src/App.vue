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
    this.status_message = 'loading  paper account'
    try{
      const response= await fetch('/accounts/paper')
      if(response.ok===false){
        this.status_message='paper response falied'
        return
      }
      const account= await response.json()
      this.paper_account= account
      this.status_message = 'Paper account loaded.'
    }
    catch{this.status_message= 'paper account load failed'}
  }


},

data(){
  return{
    select_account: 'paper',
    status_message: 'Demo data only. No broker connection.',
    paper_account: null,
    live_account: null
  }

}


}









</script>
