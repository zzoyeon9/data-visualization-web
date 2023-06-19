<template>
<div class="container">
  <header class="header">
    <title> Data Visualization Web Solution </title>
      <h1> 식품 살균 공정 관리 차트 데이터 현황</h1>
  </header>
      <nuxt />
</div>
</template>

<style>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  position: relative;
  background-image: url('../assets/image/main_background.jpg');
  background-size: cover;
}

.header {
  background-color: #000000;
  justify-content: center;
  position: absolute;
  top: 0px;
  color : white;
  text-align: center;
  width: 100%;

  /* 헤더 스타일링 추가 */
}


html, body {
  width:100%;
  height: 100%; /* 부모 요소의 크기 설정 */
  margin: 0;
  padding: 0;
  position:relative;
  background-size:cover;
  background-position: center;
  overflow: hidden;
}
</style>