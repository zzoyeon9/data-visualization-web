<template>
    <div ref="spc_container" class="chartContainer" id="chart2"></div>
</template>

<script>

import vegaEmbed from 'vega-embed'

function getDivSize() {
    const container = document.getElementById('spc_box')

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

                const result = await vegaEmbed(this.$refs.spc_container, this.jsonData, 
                { width: divSize.width-20, height: divSize.height-5})

                result.view.resize()

            } catch (error) {
                console.error('Failed to render chart:', error)
            }
        },

        handleResize() {
      
           const divSize = getDivSize()

                const result = vegaEmbed(this.$refs.spc_container, this.jsonData, 
                { width: divSize.width-20, height: divSize.height-5})
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
#chart2 {
    background-image: url("../assets/image/default4.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 50% 80%;
    flex-grow: 1;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>