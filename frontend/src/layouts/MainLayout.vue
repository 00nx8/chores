<script setup lang="ts">
</script>


<template>
  <q-layout view="hHh lpR fFf">

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar class="justify-center">
        <q-tabs align="center" class="q-mb-none q-pt-none q-gutter-none">
          <q-route-tab to="/" label="One" />
          <q-route-tab to="/" label="Two" />
          <q-route-tab to="/" label="Three" />
        </q-tabs>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

