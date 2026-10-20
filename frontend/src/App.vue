<template>
  <AccountSelector  @select-paper="select_account = 'paper'"
                    @select-live="select_account = 'live'"></AccountSelector>
  <div v-if="select_account ==='paper'">
  <DashboardHeader :heading="paper_account.name"></DashboardHeader>
  <AccountSummary :account="paper_account"
                  @rename="paper_account.name = 'updated account'">
  </AccountSummary>
  <HoldingsList :positions="paper_account.holding"></HoldingsList>
  </div>
  <div v-if="select_account === 'live'">
  <DashboardHeader :heading="live_account.name"></DashboardHeader>
  <AccountSummary :account="live_account"
                  @rename="live_account.name = 'updated account'">
  </AccountSummary>
  <HoldingsList :positions="live_account.holding"></HoldingsList>
  </div>
  <StatusMessage :message="status_message"></StatusMessage>
</template>
<script>
import DashboardHeader from './DashboardHeader.vue';
import AccountSummary from './account summary.vue';
import AccountSelector from './AccountSelector.vue';
import HoldingsList from './HoldingsList.vue';
import StatusMessage from './StatusMessage.vue';
export default{
components :{
  DashboardHeader: DashboardHeader,
  AccountSummary:AccountSummary,
  AccountSelector: AccountSelector,
  HoldingsList: HoldingsList,
  StatusMessage: StatusMessage
},

data(){
  return{
    select_account: 'paper',
    status_message: 'Demo data only. No broker connection.',
    "paper_account": {
    account_id: 'demo_paper',
    account_type: 'paper',
    base_currency: 'usd',
    source: 'demo',
    as_of: '2026-10-20T20:00:00+08:00',
    received_at: '2026-10-20T20:01:00+08:00',
    "name" : "paper account",
    "netvalue": '15000.00',
    'currency': 'usd',
    'holding': [
      {'symbol': 'tsm', 'quantity':'3',},
      {'symbol': 'googl', 'quantity': '3'}
    ]
  },
    "live_account": {
    account_id: 'demo_live',
    account_type: 'live',
    base_currency: 'usd',
    source: 'demo',
    as_of: '2026-10-20T20:00:00+08:00',
    received_at: '2026-10-20T20:01:00+08:00',
    "name" : "live account",
    "netvalue": '14000.00',
    'currency': 'usd',
    'holding': [
      {'symbol': 'tsm', 'quantity':'3',},
      {'symbol': 'avgo', 'quantity': '3'}
    ]
  }
  }
}


}









</script>






