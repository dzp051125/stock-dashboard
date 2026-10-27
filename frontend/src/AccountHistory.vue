<template>
<h2>history: {{ account.name }}</h2>
<p>{{ history_message }}</p>
<ul>
    <li v-for= 'snapshot in snapshots':key= 'snapshot.as_of'>
    {{ snapshot.as_of }} - {{ snapshot.netvalue }} {{ account.currency }}
    <span v-if='snapshot.note'>note: {{ snapshot.note }}</span>
    <span v-else>note: no note</span>
    <button v-if="!snapshot.note" type="button" @click="start_edit(snapshot)">add note</button>
    <button v-else type="button" @click="start_edit(snapshot)">edit note</button>
    <button v-if="snapshot.note" type="button" @click="delete_note(snapshot)">delete note</button>
    <div v-if="editing_snapshot_id === snapshot.snapshot_id">
      <textarea v-model="note_draft"></textarea>
      <button type="button" @click="save_note(snapshot)">save</button>
      <button type="button" @click="editing_snapshot_id= null">cancel</button>
    </div>
    </li>
</ul>
</template>
<script>
export default{
props:['account'],
data(){
    return{
        snapshots: [],
        history_message: 'history not loaded',
        editing_snapshot_id: null,
        note_draft:''
    }

},
mounted(){
    this.load_snapshots()
},
methods:
{ start_edit(snapshot){
  this.editing_snapshot_id= snapshot.snapshot_id
  this.note_draft= snapshot.note ||''
},
  async save_note(snapshot){
  try{
    const response= await fetch('/accounts/' + this.account.account_id + '/snapshots/'+
    snapshot.snapshot_id +'/note',{method: 'PUT', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({content: this.note_draft})})
    if (response.ok === false){
      this.history_message= 'save failed'

      return
    }
    this.editing_snapshot_id= null
    await this.load_snapshots()}
  catch{
    this.history_message = 'save failed'
}



  },
  async delete_note(snapshot){
     try {
        const response = await fetch(
            '/accounts/' + this.account.account_id + '/snapshots/' + snapshot.snapshot_id + '/note',
            { method: 'DELETE' }
        )
        if (response.ok === false) {
            this.history_message = 'delete failed'
            return
        }
        if (this.editing_snapshot_id === snapshot.snapshot_id) {
            this.editing_snapshot_id = null
        }
        await this.load_snapshots()
    } catch {
        this.history_message = 'delete failed'
    }


  },
  async load_snapshots(){
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
