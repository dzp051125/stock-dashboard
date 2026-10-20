<template>
<button @click="$emit('select-paper')">paper</button>
<button @click="$emit('select-live')">live</button>
</template>
<script>
export default{
    emits: ['select-paper','select-live'],
}
</script>