<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { userRequest } from './userRequest';

const props = defineProps(['chores'])

const chartBody = ref()
const chartHeight = props.chores.length + 1

const chartTextLeft = 'Chores done'
const chartTextBottom = 'Date'


console.log(props.chores)



</script>

<template>
    <section class="container">
        <h2>Chart</h2>
        <section ref="chartBody" class="chartBody">
            
            <div class="labelLeft">
                {{ chartTextLeft }}
            </div>
            <div class="labelBottom">
                {{ chartTextBottom }}
            </div>
            <div class="borders">
                <hr class="side">
                <hr class="bottom">
            </div>
        </section>

    </section>
</template>

<style scoped>
.container {
    width: 100%;
    /* background-color: grey; */
}
.borders { 
    position: absolute;
    top:0;
    bottom: 0;
    height:10rem;
    width: 100%;
}
.labelBottom {
    position: absolute;
    bottom: -1.5rem;
    left: 0;
}
.labelLeft {
    position: absolute;
    bottom: 0;
    left: -1.5rem;
    display: flex;
    align-items: center;
    writing-mode: sideways-lr;
}

.bottom {   
    display:block;
    width: 100%;
    height: 1px;
    border: none;
    background-color: white;
}


.side {
    display:block;
    height: 100%;
    width: 1px;
    border: none;
    background-color: white;
}

.chartBody {
    position: relative;
    display: grid;
    margin: 1rem;
    min-height: 1rem;
    height: 10rem;
    max-height: 10rem;

}

</style>