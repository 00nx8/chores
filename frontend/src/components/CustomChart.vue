<script setup lang="ts">

const props = defineProps(['chores', 'title', 'tagLeft', 'tagBottom'])

const chartTextLeft = props.tagLeft
const chartTextBottom = props.tagBottom

function shortenArrayBySize(array: any[], size: number): [any[], number] {
    // Will attempt to make a given array into length of size.
    // elimninating entries from 0 -> lenght - size
    // RETURNS : array, number of items removed.
    const excess = -(size - array.length) 

    if (excess) {
        array.splice(0, excess)
    }
    return [array, excess]
}


const displayedMonths = new Map()
// chores is a list of objects with information about when a chore was done. 
// this adds up how many chores were done in a given month
props.chores.forEach(chore => {
    const dateObj = new Date(chore.done_on)

    const monthNumber = (dateObj.getMonth() + 1).toString().padStart(2, '0')

    if (displayedMonths.has(monthNumber)) {
        displayedMonths.set(monthNumber, displayedMonths.get(monthNumber) + 1) 
    } else {
        displayedMonths.set(monthNumber, 1)
    }
})

// gets the highest amount in the dataset
const maxCount = Math.max(...Array.from(displayedMonths.values()))
// generates a list from 1 to the highest amount
let countRange = Array.from({ length: maxCount }, (_, i) => maxCount - i).reverse()

// if the number keys generated is higher then the allowed amount, it removes the excess from low->high
const MAX_DISPLAYED_KEYS = 8
let [keys, excess]: [number[], number] = shortenArrayBySize(countRange, MAX_DISPLAYED_KEYS)

// used to determine the height of bars/position of keys on the chart.
const CHART_HEIGHT = 10
const scale = CHART_HEIGHT / countRange.length
// [(height, displayedValue, month)]


let calculatedHeightValues = []
const lowestKey = keys[0]

// calculates the height of each bar in the barchart based on how many keys were removed
// checks for edge cases where the currentValue is lower than the lowest key.
// In which case 1 is assigned for the height.

displayedMonths.forEach((currentValue, key) => {
    let height = currentValue;
    if (excess > 0) {
        console.log(excess)
        height = currentValue - excess
    }

    if (currentValue < lowestKey) {
        height = 1;
    }

    calculatedHeightValues.push([
        height || currentValue,
        currentValue,
        key,
    ]);
});

const MAX_ALLOWED_BARS = 10

let [displayedHeightValues, overflow] = shortenArrayBySize(calculatedHeightValues, MAX_ALLOWED_BARS)

// TODO
// if the value in the month is lower than the excess i.e val - excess = <0 then the height will be determined with a negative integer.
// this leads to some funy graphs where 2 is higher than 7
// also if the value displayed on theg graph is lower than the lowest number displayed, how should it be done ?
// In either cases, their value to be dispayed with will be set to 1.
console.log(displayedHeightValues)
</script>

<template>
    <section class="container">
        <h2>{{props.title}}</h2>  
        <section class="chartBody">
            <div class="bars">
                <div 
                    v-for="[height, displayedValue, month], i in displayedHeightValues"
                    :style="{left: `${i * 1.75}rem`, height: `${height * scale}rem`}"
                    class="bar"
                    :key=i>
                    <p class="month">{{ month }}</p>
                    <p>{{ displayedValue }}</p>
                </div>
                <!-- <div
                    v-for="(month, i) in Object.keys(displayedMonths)"
                    class="bar"
                    :style="{left: `${i * 2}rem`, height: `${(displayedMonths[month] - -excess) * scale}rem`}"
                 >{{displayedMonths[month]}}</div> -->
            </div>
            <div>
                <div class="labelLeft">
                    {{ chartTextLeft }}
                </div>
            </div>
            <div class="keys">
                <p 
                    :key="i" v-for="val, i in countRange"
                    :style="{position: 'absolute', bottom: `${i * scale}rem`}"
                >{{ val }}</p>
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
.keys {
    position: absolute;
    bottom: 0;
    left: -1rem;
    height: 100%;
    width: 1rem;
}
.bars  {
    position: relative;
    height: 10rem;
}
.bar {
    position: absolute;
    bottom: 0;
    height: 9rem;
    max-height: 9rem;
    background-color: red;
    width: 1.2rem;
    min-height: .5rem;
}
.bar > P {
    color: white;
    line-height: .8rem;

}
.bar > p.month {
    position: absolute;
    bottom: -1rem;
}
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
    bottom: -2.5rem;
    left: 0;
}
.labelLeft {
    position: absolute;
    bottom: 0;
    left: -2.5rem;
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
    margin: 1rem;
    min-height: 1rem;
    height: 10rem;
    max-height: 10rem;

}

</style>