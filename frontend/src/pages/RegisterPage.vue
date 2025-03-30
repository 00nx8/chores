<script lang="ts" setup>
import { userRequest } from 'src/components/userRequest';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Notify } from 'quasar';

const router = useRouter()

const isPwd = ref(true)
const submitting = ref(false)

const error = ref('')

const username = ref('')
const password = ref('')
const repeatPassword = ref('')

function verifyLoginDetails() {
  if (
    !username.value ||
    !password.value ||
    !repeatPassword.value
  ) {
    error.value = 'Fille out all fields'
    return
  }
  if (password.value !== repeatPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  userRequest('/register', {
    method:"POST",
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  })
  .then(res => {
    if (res.status == 'ok') {
      Notify.create({message: "Successfully registered"})
      router.push('/login').catch(err => console.log(err))
    }
  })
  .catch( err => console.log(err) )
}

// build login endpoint in api
// build register endpoint in api

</script>

<template>
  <section style="height: 100dvh" class="column justify-center items-center">
    <h1 style="margin: 0">register</h1>

    <form class="q-gutter-md" @submit.prevent="verifyLoginDetails">
      <q-input required filled v-model="username" label="Username" />
      <q-input v-model="password" filled :type="isPwd ? 'password' : 'text'" label="Password">
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
  </section>

</template>