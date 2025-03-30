<script lang='ts' setup>
import { userRequest } from 'src/components/userRequest';
import { useRouter } from 'vue-router';

const router = useRouter()

userRequest('/user/household', {
  method: 'GET',
}).then(data => {
  if (!data.household) {
    router.push('/household/create')
  }
})

</script>

<template>
  <h1>Household</h1>

</template>