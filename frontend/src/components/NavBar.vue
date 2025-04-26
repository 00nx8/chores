<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>
<template>
    <nav>
        <RouterLink :to="{name: 'profile'}">
           Profile
        </RouterLink>
        <RouterLink :to="{name: 'household'}">
           Household
        </RouterLink>
        <RouterLink to="/">
           PlaceHolder
        </RouterLink>
    </nav>
</template>

<style scoped>
nav {
    background-color: rgba(128, 128, 128, 0.075);
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100dvw;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}
</style>