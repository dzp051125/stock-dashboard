<template>
<p>{{ account.account_id }}</p>
<p>{{ account.name }}</p>
<p>{{ account.as_of }}</p>
<p>{{ account.netvalue }}</p>
<p>{{ account.currency }}</p>
</template>
<script>
export default{
props:['account'],

}

</script>