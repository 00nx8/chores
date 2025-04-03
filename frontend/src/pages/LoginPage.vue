<script lang="ts" setup>
import { ref } from 'vue';
import { userRequest } from 'src/components/userRequest';
import { Cookies } from 'quasar';
import { useRouter } from 'vue-router';

const router = useRouter()

const isPwd = ref(true)
const submitting = ref(false)
const error = ref('')

const username = ref('')
const password = ref('')

function verifyLoginDetails() {
  submitting.value = true

  if (!username.value || !password.value) {
    error.value = 'Username and password are required'
    submitting.value = false
    return
  }

  userRequest('/login', {
    method: 'POST',
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  }).then(res => {
    if (res.token) {
      Cookies.set('token', res.token)
      localStorage.setItem('username', username.value)
      router.push('/household').catch(err => console.log(err))
    }
  }).catch(err => error.value = err.message)
  submitting.value = false
}

</script>

<template>
  <section style="height: 100dvh" class="column justify-center items-center">
    <h1 style="margin: 0">login</h1>

    <form class="q-gutter-md" @submit.prevent="verifyLoginDetails">
      <q-input filled v-model="username" label="Username" />
      <q-input label="Password"  v-model="password" filled :type="isPwd ? 'password' : 'text'">
          <template v-slot:append>
            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>
        <div v-if="error" class="row items-center q-gutter-md">
          <q-icon style="margin-left: 0" name="warning" color="red" />
          <p style="margin-bottom:0" class="text-red">{{ error }}</p>
        </div>

        <div class="row justify-end q-gutter-md">
          <q-btn
            :to="{name: 'register'}"
            label="Register"
            class="q-mt-md"

          >
          </q-btn>

          <q-btn
            type="submit"
            :loading="submitting"
            label="Log in"
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