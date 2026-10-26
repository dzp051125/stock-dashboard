<template>
<h2>history: {{ account.name }}</h2>
<p>{{ history_message }}</p>
<ul>
    <li v-for= 'snapshot in snapshots':key= 'snapshot.as_of'>
    {{ snapshot.as_of }} - {{ snapshot.netvalue }} {{ account.currency }}
    </li>

</ul>
</template>
<script>
export default{
props:['account'],
data(){
    return{
        snapshots: [],
        history_message: 'history not loaded'
    }

},
mounted(){
    this.load_snapshots()
},
methods: {async load_snapshots(){
    this.history_message = 'loading history'
    try{const response = await fetch('/accounts/' + this.account.account_id +'/snapshots')
      if (response.ok ===false){
        this.history_message = 'load failed'
        return
      }
      const snapshots = await response.json()
      if (Array.isArray(snapshots)=== false){
        this.history_message= 'invalid records'
        return
      }
      this.snapshots = snapshots
      if (snapshots.length === 0){
        this.history_message = 'no records returned'
        return
      }
      this.history_message= 'loaded success'
    }
    catch{this.history_message = 'load failed'}


  }
}

}

</script>