<template>
<ul>
    <li v-for="position in positions">
        {{ position.symbol }} - {{ position.quantity }}
    </li>
</ul>
</template>
<script>
export default{
props:['positions']}
</script>