<template>
  <div class="contents-container"> 
    <div class="row">
      <div class = "chart-box" id = 'trend_box'>
        <TrendPage :jsonData="trend_data" ref="trend_child"/>
      </div>


      <div class = "chart-box" id = 'scatter_box'>
        <ScatterPlotPage :jsonData="scatter_plot_data" ref="scatter_plot_child"/>
      </div>


    </div>
    <div class="row">
      <div class = "chart-box" id = 'cpk_box'>
        <CpkPage :jsonData="cpk_data" ref="cpk_child"/>
      </div>


      <div class = "chart-box" id = 'spc_box'>
        <SpcPage :jsonData="spc_data" ref="spc_child"/>
      </div>


    </div>
          
    <form>
      <input type="datetime-local" name="start_date" v-model="start_date" style="width: 90px;">
      <input type="datetime-local" name="end_date" v-model="end_date" style="width: 90px;">

      <select name="label" v-model="label">
        <option value="mixa_pasteur_temp">mixa_pasteur_temp</option>
        <option value="mixb_pasteur_temp">mixb_pasteur_temp</option>
      </select>
    </form>
    <button @click="createAllChart">Create</button>
    <button @click="downloadAllChartInfo">Download</button>

          <p id="max"> Max: </p> 
          <p id="min"> Min: </p> 
          <p id="avg"> μ: </p> 
          <p id="median"> m: </p> 
          <p id="sigma"> σ: </p> 
          <p id="cp"> cp: </p> 
          <p id="cpk"> cpk: </p>


  </div>
</template>


<script>

import TrendPage from '../components/TrendPage.vue'
import ScatterPlotPage from '../components/ScatterPlotPage.vue'
import CpkPage from '../components/CpkPage.vue'
import SpcPage from '../components/SpcPage.vue'

// async function asyncPromiseAll() {
//       const promises = [
//         createTrend(),
//         createScatterPlot(),
//         createCpCpk(),
//         createSpc(),
//       ]

//       try {
//         const results = await Promise.all(promises)
//         console.log(results)

//       } catch (error) {
//         console.error(error)
//       }
//     }

export default {
  components: { TrendPage, ScatterPlotPage,  CpkPage, SpcPage},

  layout : 'default',

  data() {
    return {
      start_date: "2020-03-05T10:30", // 시작 날짜 데이터
      end_date: "2020-04-05T10:30", // 종료 날짜 데이터

      label:"mixa_pasteur_temp",

      max:"",
      min:"",
      avg:"",
      median:"",
      sigma:"",
      cp:"",
      cpk:"",

      trend_data: {},
      scatter_plot_data: {},
      cpk_data: {},
      spc_data: {}
    };
  },

  methods: {
    downloadAllChartInfo (event) {
      event.preventDefault();

      var start = this.start_date
      var end = this.end_date
      var lab = this.label

      this.start_date = this.start_date.replace('T', ' ').concat(':00')
      this.end_date = this.end_date.replace('T', ' ').concat(':00')
      
      var url = "/api/download?start_date=" + this.start_date + 
      "&end_date=" + this.end_date + "&label=" + this.label

        window.open(url, "_blank")  

        this.start_date = start
        this.end_date = end
        this.label = lab
    },

    createAllChart (event) {
      // eslint-disable-next-line no-console
      console.log('event occur !!')
      event.preventDefault();

      var start = this.start_date
      var end = this.end_date
      var lab = this.label

      this.start_date = this.start_date.replace('T', ' ').concat(':00')
      this.end_date = this.end_date.replace('T', ' ').concat(':00')
      
      this.$axios.get('/api/vision/trend', {
        params: { start_date: this.start_date, 
                  end_date: this.end_date, 
                  y_label: this.label },
        
      }).then((response_trend) => {

        this.trend_data= response_trend.data

    }).catch((error) => {
      console.error('Failed to fetch data:', error)
    })



      this.$axios.get('/api/vision/scatter_plot', {
        params: { start_date: this.start_date, end_date: this.end_date },
        
      }).then((response_scatter_plot) => {

        this.scatter_plot_data = response_scatter_plot.data

    }).catch((error) => {
      console.error('Failed to fetch data:', error)
    })



      this.$axios.get('/api/vision/cpk', {
        params: { start_date: this.start_date, 
                  end_date: this.end_date,
                  label: this.label},
        
      }).then((response_cpk) => {

        this.cpk_data = response_cpk.data

    }).catch((error) => {
      console.error('Failed to fetch data:', error)
    })



      this.$axios.get('/api/vision/spc', {
        params: { start_date: this.start_date, end_date: this.end_date, label: this.label },
        
      }).then((response_spc) => {

        this.spc_data = response_spc.data

    }).catch((error) => {
      console.error('Failed to fetch data:', error)
    })

    this.start_date = start
    this.end_date = end
    this.label = lab
    },

  }
}

</script>

<style>

.contents-container {
  background-color: rgba(255, 255, 255, 0.5);
  display:flex;
  position: absolute;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  width:70%;
  height:80%;
  flex-wrap: wrap;
  flex-grow: 1;
}

.row {
  display: flex;
  flex-wrap: nowrap;
  margin-bottom: 0;
  background-color:#11064d;
  width: 100%;
  height: 50%;
}

.chart-box {
  flex-grow: 1;
  position: relative;
  flex-basis: 50%;
  width: 43%; 
  height: 90%;
  margin: 10px;
  background-color:#ffffff;
  background-size:cover;
  background-position: center;
  overflow: hidden;
}

#__nuxt, #__layout {
  width: 100%;
  height: 100%;
}

form {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
  }

  input[type="datetime-local"],
  select {
    margin-right: 5px;
  }

p {
  color:#ffffff;
  margin-left:15px;

  left: 0px;
}

button {
  margin-left: 10px;
}
</style>

