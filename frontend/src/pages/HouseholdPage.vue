<script lang='ts' setup>
import { userRequest } from 'src/components/userRequest';
import { ref } from 'vue'

import GetAHouse from 'src/components/GetAHouse.vue';

const hasHousehold = ref(true)

userRequest('/user/household', {
  method: 'GET',
}).then(data => {
  if (!data.household) {
    console.log('homeless')
  }
  hasHousehold.value = false
})

</script>

<template>
  <h1>Household</h1>
  <section v-if="hasHousehold">
    <p>youre not homeless, grats</p>
  </section>
  <section v-else>
    <GetAHouse />
  </section>
</template>