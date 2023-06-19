<template>
    <div ref="trend_container" class="chartContainer" id="chart1"></div>
</template>

<script>

import vegaEmbed from 'vega-embed'

function getDivSize() {
    const container = document.getElementById('trend_box')

    return {
        width: container.offsetWidth,
        height: container.offsetHeight
    }
}

export default {
    
    props: {
        jsonData: {
            type: Object,
            required: true,
        }
    },

    watch: {
        jsonData: {
            deep: true,
            handler(val) {
                if (val) {
                    this.renderChart();
                }
            },
        },
    },

    mounted() {
        window.addEventListener('resize', this.handleResize)
  },

    destroyed() {
        window.removeEventListener('resize', this.handleResize)
  },

    methods: {
        async renderChart() {
            try {
                this.jsonData.autosize = "fit"

                const divSize = getDivSize()
                const result = await vegaEmbed(this.$refs.trend_container, this.jsonData, 
                { width: divSize.width-30, height: divSize.height-10 })
                result.view.resize()
                
                const max = document.getElementById('max')                
                max.innerText = "max: " + this.jsonData['max']
                const min = document.getElementById('min')                
                min.innerText = "min: " + this.jsonData['min']
                const avg = document.getElementById('avg')                
                avg.innerText = "μ: " + this.jsonData['avg']
                const median = document.getElementById('median')                
                median.innerText = "m: " + this.jsonData['median']

            } catch (error) {
                console.error('Failed to render chart:', error)
            }
        },

        handleResize() {
      
           const divSize = getDivSize()

                const result = vegaEmbed(this.$refs.trend_container, this.jsonData, 
                { width: divSize.width-30, height: divSize.height-10 })
        }
    },
    // axios: {
    //     host: "http://10.0.1.47",
    //     port: "30000",
    //     prefix: "/",

    //     proxy: true,

    //     retry: {
    //         retries: 4,
    //         shouldResetTimeout: true, // 재전송 간 타임아웃을 리셋하기
    //         retryDelay: (retry) => {
    //             return retry * 100; // 재전송 횟수 * 0.1초만큼 재전송 시작 시간을 지연시키기
    //         },
    //         retryCondition: (error) => err.response.status === 429, // 서버 혼잡이 일어났을 경우에만 재전송하기
    //     }
    // },

    // proxy: {
    // "/api/": "http://10.0.1.47:30000",
    //"/api2/": "http://api.another-website.com",
    // },

    // async asyncData({ $axios }) {
    //     const { data } = await $axios.get().data;        
    // },

    // async fetch() {
    //     const { data } = await this.$axios.get().data;
    //     this.$axios.get('http://10.0.1.47/');
    // }, 
  
};
</script>

<style>
#chart1 {
    background-image: url("../assets/image/default2.png");
    background-repeat: no-repeat;
    background-position: center;
    flex-grow: 1;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>