import type { EChartsOption } from 'echarts'

export function getBloodSugarChartOption(data: {
  times: string[]
  values: number[]
}): EChartsOption {
  return {
    title: { text: '血糖趋势图', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: data.times },
    yAxis: {
      type: 'value',
      name: 'mmol/L',
      min: 2,
      max: 16,
    },
    series: [
      {
        name: '血糖值',
        type: 'line',
        data: data.values,
        smooth: true,
        markLine: {
          data: [
            { yAxis: 3.9, lineStyle: { color: '#E6A23C' }, label: { formatter: '低血糖 3.9' } },
            { yAxis: 7.0, lineStyle: { color: '#67C23A' }, label: { formatter: '目标上限 7.0' } },
            { yAxis: 10.0, lineStyle: { color: '#F56C6C' }, label: { formatter: '高血糖 10.0' } },
          ],
        },
        areaStyle: { opacity: 0.1 },
      },
    ],
    dataZoom: [{ type: 'inside' }],
  }
}

export function getHealthScoreOption(score: number): EChartsOption {
  return {
    series: [
      {
        type: 'gauge',
        startAngle: 200,
        endAngle: -20,
        min: 0,
        max: 100,
        splitNumber: 5,
        itemStyle: { color: score >= 80 ? '#67C23A' : score >= 60 ? '#E6A23C' : '#F56C6C' },
        progress: { show: true, width: 18 },
        pointer: { show: false },
        axisLine: { lineStyle: { width: 18, color: [[1, '#E5E9F2']] } },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        detail: {
          valueAnimation: true,
          offsetCenter: [0, '0%'],
          fontSize: 36,
          formatter: '{value}分',
        },
        data: [{ value: score }],
      },
    ],
  }
}
