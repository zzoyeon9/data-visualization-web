<template>
    <div ref="scatter_container" class="chartContainer" id="chart4"></div>
</template>

<script>

import vegaEmbed from 'vega-embed'

function getDivSize() {
    const container = document.getElementById('scatter_box')

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

                const result = await vegaEmbed(this.$refs.scatter_container, this.jsonData, 
                { width: divSize.width-15, height: divSize.height-10 })

                result.view.resize()

            } catch (error) {
                console.error('Failed to render chart:', error)
            }
        },

        handleResize() {
      
           const divSize = getDivSize()

                const result = vegaEmbed(this.$refs.scatter_container, this.jsonData, 
                { width: divSize.width-15, height: divSize.height-10 })
        }
    },
  
};
</script>

<style>
#chart4 {
    background-image: url("../assets/image/default1.png");

    background-repeat: no-repeat;
    background-position: center;
    overflow: hidden;
    flex-grow: 1;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>