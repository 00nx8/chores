<script lang="ts" setup>
import { defineProps } from 'vue';

// display multiple errors at the same time
const props = defineProps<{
    errors: Array<string>
}>()

</script>

<template>
    <section>
        <h4>Error: </h4>
        <ul>
            <li v-for="error in props.errors">{{ error }}</li>
        </ul>
    </section>

</template>

<style scoped>
    * {
        color: red;
    }
</style>