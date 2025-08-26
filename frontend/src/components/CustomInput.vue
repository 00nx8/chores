<script lang="ts" setup>
import { ref } from 'vue';
// send input value to parent container
const emit = defineEmits(["update:modelValue"])
function updateValue (e: Event) {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}

const props = defineProps<{
  type: string
  name: string
}>()

const inputValue = ref('')

</script>

<template>
  <label>
    {{ name }}
    <input 
      v-model="inputValue" 
      @input="updateValue"
      :type="props.type" />
  </label>

</template>
