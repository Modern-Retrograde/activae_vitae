<template lang="html">
  <div class="cont">
    <div class="navbar">
      <nuxt-link class="arrow" to="/main"></nuxt-link>
      <h4>Событие</h4>
      <div class="star"></div>
    </div>
    <div class="main" style="max-width:1300px">
      <div class="diagram">
        <img src="@/assets/diagram.png" width="60%">
        <h4>70% понравилось<br>30% не понравилось</h4>
      </div>
      <div class="mb-3">
        <div v-for="item in joy" :key="item.id">
          <div class="col">
           <div class="card" style="cursor:pointer;z-index:1">
            <div class="card-img-top"></div>
            <div class="card-body">
              <p class="card-text">Дата: {{item.date}}</p>
              <p class="card-text">{{ item.text }}</p>
            </div>
          </div>
         </div>
        </div>
       </div>
     </div>
  </div>
</template>

<script>
export default {
  data(){
    return{
      joy:[
        {
          id:0,
          text: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt u',
          date: '21.03.2021'
        },
        {
          id:1,
          text: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt u',
          date: '09.06.2021'
        },
        {
          id:2,
          text: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt u',
          date: '27.12.2021'
        },
      ]
    }
  }
}
</script>

<style lang="css" scoped>
.cont{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.navbar{
  margin-top: 20px;
  height: 50px;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.arrow{
  background: url("@/assets/arrow.svg");
  background-size: cover;
  width: 50px;
  height: 25px;
}
.star{
  background: none;
  background-size: cover;
  width: 25px;
  height: 25px;
}
h4{
  margin-top: 10px;
}
.main{
  display: flex;
  flex-direction: row;
  width: 90%;
}
.diagram{
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  align-items: center;
}
.card-img-top{
  width: 100%;
  height: 30px;
  background: #9FB7FF;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
h5{
  display: flex;
  align-items: center;
  margin-top: 10px;
}
.card{
  background-color: #C6D4FF;
  margin-top: 30px;
}
@media (max-width: 600px) {
 .main{
   flex-direction: column;
   align-items:center;
 }
}
</style>
