<script lang="ts" setup>
import { userRequest } from 'src/components/userRequest';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const houseDetails = ref({
  name: '',
  password: ''
})
const repeatPassword = ref('')

const error = ref('')
const submitting = ref(false)
const isPwd = ref(true)

function verifyHouseDetails() {
  if (!houseDetails.value.name || !houseDetails.value.password || !repeatPassword.value) {
    error.value = 'All fields are required'
    return
  }
  if (houseDetails.value.password !== repeatPassword.value) {
    error.value = 'Passwords must match'
    return
  }

  userRequest('/household/create', {
    method: 'POST',
    body: JSON.stringify(houseDetails.value)
  }).then(data => {
    if (data.household) {
      router.push('/household').catch(err => console.log(err))
    }

  }).catch(err => console.log(err))

}
</script>
<template>
  <h1 class="text-h5">Create Household</h1>

  <form class="q-gutter-md" @submit.prevent="verifyHouseDetails">
      <q-input required filled v-model="houseDetails.name" label="House name" />

      <q-input v-model="houseDetails.password" filled :type="isPwd ? 'password' : 'text'" label="Password">
          <template v-slot:append>
            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>

        <q-input v-model="repeatPassword" filled type="password" label="Repeat password"/>

        <div v-if="error" class="row items-center q-gutter-md">
          <q-icon style="margin-left: 0" name="warning" color="red" />
          <p style="margin-bottom:0" class="text-red">{{ error }}</p>
        </div>

        <div class="row justify-end q-gutter-md">
          <q-btn
            :to="{name: 'login'}"
            label="Login"
            class="q-mt-md"
          >
          </q-btn>

          <q-btn
            type="submit"
            :loading="submitting"
            label="Save"
            class="q-mt-md"
            color="teal"
          >
          <template v-slot:loading>
            <q-spinner-facebook />
          </template>
        </q-btn>
      </div>
    </form>
</template>