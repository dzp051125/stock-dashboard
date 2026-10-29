<template>
  <button @click="load_accounts()">load_accounts</button>
  <AccountSelector  @select-paper="select_account = 'paper'"
                    @select-live="select_account = 'live'"></AccountSelector>
  <div v-if="current_account">
  <DashboardHeader :heading="current_account.name"></DashboardHeader>
  <AccountSummary :account="current_account"
                  :key='current_account.account_id'
                  >
  </AccountSummary>
  <AccountHistory :account ='current_account'
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
  this.load_accounts()
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
  async load_accounts(){
    this.status_message = 'loading demo accounts'
    try{const response = await fetch('/accounts')
    if (response.ok===false){
      this.status_message='response fail'
      return
    }
    const accounts = await response.json()
    if (Array.isArray(accounts)===false){
      this.status_message='Invalid account response.'
      return
    }
    if (accounts.length===0){
      this.status_message= 'No accounts returned.'
      return
    }
    if (accounts.length===1){
      this.status_message= 'Both demo accounts are required.'
      return

    }
    for(const account of accounts){
      console.log(account.account_type)
      if (account.account_type === 'paper'){this.paper_account = account}
      if (account.account_type === 'live'){this.live_account = account}
    }
    this.status_message = 'demo data loaded, no broker connection'
    }
    catch{this.status_message= 'load failed'}
  },


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
