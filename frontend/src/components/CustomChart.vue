<script setup lang="ts">
import { onMounted, ref } from 'vue';

const props = defineProps(['chores'])

const chartBody = ref()

const chartHeight = props.chores.length + 1

// TODO:
// you have to edit marking as done so it marks completion time.
// get the results from the table for it for the last week


onMounted(() => {
    
})
</script>

<template>
    <section class="container">
        <h2>Chart</h2>
        <section ref="chartBody" class="chartBody">

            <hr class="side">
            <hr class="bottom">
        </section>

    </section>
</template>

<style scoped>
.container {
    width: 100%;
    background-color: grey;
}

.chartBody {
    position: relative;
    display: grid;

    min-height: 1rem;
    height: 10rem;
    max-height: 10rem;

    grid-template-rows: 1fr;
    grid-template-columns: 1fr;
}

</style>