<template>
<img src = "../../assets/image/scatter-plot.PNG">
</template>
<script>

export default {
    axios: {
        host: "http://10.0.1.47",
        port: "30000",
        prefix: "/",

        proxy: true,

        retry: {
            retries: 4,
            shouldResetTimeout: true, // 재전송 간 타임아웃을 리셋하기
            retryDelay: (retry) => {
                return retry * 100; // 재전송 횟수 * 0.1초만큼 재전송 시작 시간을 지연시키기
            },
            retryCondition: (error) => err.response.status === 429, // 서버 혼잡이 일어났을 경우에만 재전송하기
        }
    },

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

</style>