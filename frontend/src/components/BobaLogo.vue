<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 48 48"
    :width="size"
    :height="size"
    fill="none"
    aria-hidden="true"
  >
    <defs>
      <mask :id="maskId">
        <rect x="0" y="0" width="100%" height="100%" fill="white" />
        <path d="M 21 19 L 43 19 L 39 44 L 25 44 Z" fill="black" />
        <line x1="36" y1="6" x2="31.5" y2="40" stroke="black" stroke-width="4" stroke-linecap="round" />
      </mask>

      <g :id="cupId" stroke="#111111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="11" y1="8" x2="15" y2="40" />
        <circle cx="5" cy="16" r="4" />
        <path d="M 5 12 L 5 20 M 1 16 L 9 16" />
        <path d="M 4 21 L 24 25" />
        <path d="M 6 21.5 L 10 40 C 10.2 41 11 42 12 42 L 18 42 C 19 42 19.8 41 20 40 L 22.5 24.5" />
        <rect x="10" y="27" width="4" height="4" rx="0.5" transform="rotate(15, 12, 29)" />
        <rect x="15" y="34" width="4" height="4" rx="0.5" transform="rotate(-15, 17, 36)" />
      </g>
    </defs>

    <use :href="`#${cupId}`" opacity="0.25" />
    <use :href="`#${cupId}`" :mask="`url(#${maskId})`" />

    <g stroke="#111111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <line x1="36" y1="6" x2="31.5" y2="40" />

      <rect x="22" y="20" width="20" height="3" rx="1" />
      <path d="M 24 23 L 26.5 40 C 26.7 41 27.5 42 28.5 42 L 35.5 42 C 36.5 42 37.3 41 37.5 40 L 40 23" />
      <path d="M 24.5 28 Q 32 31 39.5 28" />

      <circle cx="29" cy="38" r="1.5" fill="#111111" stroke="none" />
      <circle cx="34" cy="38" r="1.5" fill="#111111" stroke="none" />
      <circle cx="31.5" cy="35" r="1.5" fill="#111111" stroke="none" />
      <circle cx="27.5" cy="34" r="1.5" fill="#111111" stroke="none" />
      <circle cx="35" cy="34" r="1.5" fill="#111111" stroke="none" />

      <path d="M 42 4 Q 42 9 37 9 Q 42 9 42 14 Q 42 9 47 9 Q 42 9 42 4 Z" fill="#111111" stroke="none" />
    </g>
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: [Number, String],
    default: 24
  }
})

const seed = Math.random().toString(36).slice(2, 9)
const maskId = computed(() => `boba-mask-${seed}`)
const cupId = computed(() => `lemonade-cup-${seed}`)
</script>
