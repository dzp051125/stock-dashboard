<template>
<ul>
    <li v-for="position in positions">
        <div v-for="(value,field) in position":key='field'>
            {{ field }}:
            <span v-if="value=== null">暂无数据</span>
            <span v-else>{{ value }}</span>
        </div>
        
    </li>
</ul>
</template>
<script>
export default{
props:['positions']}
</script>