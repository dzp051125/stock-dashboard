<template>
<p>{{ account.account_id }}</p>
<p>{{ account.name }}</p>
<p>as  of: {{ account.as_of }}</p>
<p>{{ account.netvalue }}</p>
<p>{{ account.currency }}</p>
<p>received at: {{ account.received_at }}</p>
<p>source: {{ account.source }}</p>
</template>
<script>
export default{
props:['account'],

}

</script>