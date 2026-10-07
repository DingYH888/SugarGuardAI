<template>
  <v-chart :option="chartOption" autoresize style="height: 350px" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  MarkLineComponent,
  DataZoomComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getBloodSugarChartOption } from '../utils/charts'
import type { BloodSugar } from '../types'

use([LineChart, GridComponent, TooltipComponent, MarkLineComponent, DataZoomComponent, CanvasRenderer])

const props = defineProps<{ records: BloodSugar[] }>()

const chartOption = computed(() => {
  const sorted = [...props.records].sort(
    (a, b) => new Date(a.measured_at).getTime() - new Date(b.measured_at).getTime(),
  )
  return getBloodSugarChartOption({
    times: sorted.map((r) =>
      new Date(r.measured_at).toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      }),
    ),
    values: sorted.map((r) => r.value),
  })
})
</script>
