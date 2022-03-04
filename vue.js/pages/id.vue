<template lang="html">
  <div class="cont">
    <div class="navbar">
      <nuxt-link class="arrow" to="/main"></nuxt-link>
      <h4>Ну какой-то ивент</h4>
      <div class="star"></div>
    </div>
    <div class="main">
      <div class="buttons">
        <button type="button" name="button" class="but" v-if="one" @click="memory()">Напомнить о событии за день до начала</button>
        <button type="button" name="button" class="but" v-if="two" @click="feedback()">Оставить отзыв</button>
        <button type="button" name="button" class="but" v-if="three" @click="change()">Изменить событие</button>
        <button type="button" name="button" class="but" v-if="four" @click="feedbacks()">Отзывы</button>
      </div>
      <div class="text">
         <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
         <p class="time"> {{ ranDate }} </p>
         <p>Форма проведения: {{ och }}</p>
         <div class="sl">
           <Slider />
         </div>
      </div>
    </div>
  </div>
</template>

<script>
import Slider from '@/components/Slider.vue'
import array from '@/components/array.js'
export default {
  data(){
    return{
      array:array,
      ranDate: "",
      och:"",
      one: true,
      two: true,
      three: false,
      four: false
    }
  },
  components:{
    Slider
  },
  mounted(){
    let self = this
    function randomDate(date1, date2){
    function randomValueBetween(min, max) {
      return Math.random() * (max - min) + min;
    }
    var date1 = date1 || '01-01-1970'
    var date2 = date2 || new Date().toLocaleDateString()
    date1 = new Date(date1).getTime()
    date2 = new Date(date2).getTime()
    if( date1>date2){
        return new Date(randomValueBetween(date2,date1)).toLocaleDateString()
    } else{
        return new Date(randomValueBetween(date1, date2)).toLocaleDateString()

     }
    }
    function ranProv() {
      let ran = Math.floor(Math.random() * 101)
      if(ran > 50){
        self.och = "Очное"
      }
      else {
        self.och = "Заочное"
      }
    }
    ranProv();
    this.ranDate = randomDate('02/13/2013', '01/01/2000');
  }

}
</script>

<style lang="css" scoped>
body{
    max-width: 1500px;
    margin: 100px;
}
.cont{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.navbar{
  margin-top: 20px;
  height: 50px;
  width: 95%;
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
  background: url("@/assets/star.png");
  background-size: cover;
  width: 25px;
  height: 25px;
}
h4{
  margin-top: 10px;
}
.buttons{
  display: flex;
  flex-direction: column;
}
.main{
  display: flex;
  flex-direction: row;
  width: 95%;

}
.but{
  border: none;
  border-radius: 12px;
  font-size: 20px;
  margin-top: 20px;
  background-color: white;
  width: 283px;
  height: 85px;
}
.text{
  margin-left: 20px;
  margin-top: 20px;
  font-size: 25px;
  display: flex;
  flex-direction:column;
  align-items:flex-start;
}
.time{
  margin-top: 10px;
}
.sl{
  width: 100%;
  height: 300px;
  max-width: 500px;
}
@media (max-width: 720px) {
  .main{
    flex-direction: column;
    align-items: center;
  }
  .but{
    width: 100%;
    height: 60px;
    font-size: 15px;
  }
}
@media (max-width: 420px) {
  h4{
    font-size: 18px;
  }
  .text{
    font-size: 16px;
    margin-left: 0px;
    width: 100%;
  }
}
</style>
