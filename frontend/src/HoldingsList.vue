<template>
<ul>
    <li v-for="position in positions">
        <div v-for="(value,field) in position":key='field'>
            {{ field }}:{{ value }}
        </div>
        
    </li>
</ul>
</template>
<script>
export default{
props:['positions']}
</script>