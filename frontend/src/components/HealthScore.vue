<template>
  <v-chart :option="chartOption" autoresize style="height: 250px" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { GaugeChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { getHealthScoreOption } from '../utils/charts'

use([GaugeChart, CanvasRenderer])

const props = defineProps<{ score: number }>()
const chartOption = computed(() => getHealthScoreOption(props.score))
</script>
