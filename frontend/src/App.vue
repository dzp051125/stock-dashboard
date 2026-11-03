<template>
  <button @click="load_paper()">refresh</button>
  <AccountSelector  @select-paper="select_account = 'paper'"
                    @select-live="select_account = 'live'"></AccountSelector>
  <StockSearch></StockSearch>
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
import StockSearch from './StockSearch.vue';
export default{
components :{
  DashboardHeader: DashboardHeader,
  AccountSummary:AccountSummary,
  AccountSelector: AccountSelector,
  HoldingsList: HoldingsList,
  StatusMessage: StatusMessage,
  AccountHistory: AccountHistory,
  StockSearch:StockSearch
},
mounted(){
  this.load_paper()
  this.refresh_time= window.setInterval(
    this.load_paper,
    1000
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
  
  async load_paper() {
    if (this.is_loading) {
      return
    }
    this.is_loading = true
    if (this.paper_account === null) {
      this.status_message = '正在读取后台缓存……'
    }
    try {
      const response = await fetch('/accounts/paper', { cache: 'no-store' })
      if (response.ok === false) {
        this.status_message = this.paper_account
          ? '无法读取后台缓存，暂时显示上次数据。'
          : '无法读取后台缓存，请检查连接或登录状态。'
        return
      }
      const data = await response.json()
      if (!data || typeof data !== 'object' || !('account' in data)) {
        this.status_message = '后台返回的数据格式不正确。'
        return
      }
      if (data.account !== null) {
        this.paper_account = data.account
      }
      if (data.last_error) {
        this.status_message = this.paper_account
          ? 'Gateway 更新失败，暂时显示上次成功数据；后台会继续重试。'
          : '暂时无法取得账户数据，后台会继续重试。'
      } else if (data.is_updating) {
        this.status_message = this.paper_account
          ? '后台正在更新 Gateway 数据，当前显示上次成功数据。'
          : '后台正在读取 Gateway，等待首次数据……'
      } else if (data.account === null) {
        this.status_message = this.paper_account
          ? '后台正在重新准备数据，暂时显示上次数据。'
          : '后台尚未取得账户数据。'
      } else {
        this.status_message = '已显示后台最新缓存；网页每秒检查，Gateway 读取完成后间隔 30 秒更新。'
      }
    } catch {
      this.status_message = this.paper_account
        ? '网络连接失败，暂时显示上次成功数据。'
        : '网络连接失败，请检查网站连接。'
    } finally {
      this.is_loading = false
    }
  }
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
