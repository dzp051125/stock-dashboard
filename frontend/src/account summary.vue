<template>
<p>{{ account.name }}</p>
<p>{{ account.netvalue }}</p>
<p>{{ account.currency }}</p>
<button @click="$emit('rename')">change account name</button>
</template>
<script>
export default{
props:['account'],
emits:['rename']

}

</script>