<script lang="ts" setup></script>

<template>
  <section class="column justify-center items-center">

    <h1 class="text-h5 text-center">You're not a part of any household...</h1>

    <div class="row justify-center q-gutter-md items-center">
      <section class="column items-center justify-center">
        <h2 class="text-h6">Create a household</h2>
        <q-btn :to="{name: 'createHouse'}" color="primary">Create</q-btn>
      </section>
      <section class="column items-center justify-center">
        <h2 class="text-h6">Or join an existing one</h2>
        <q-btn :to="{name: 'joinHouse'}" color="secondary">Join</q-btn>
      </section>
    </div>
  </section>

</template>