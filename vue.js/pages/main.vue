<template lang="html">
  <div class="container">
    <Navbar @toggle="hoh" @hool="kok" />
   <div class="menu">
     <div class="main_menu" v-if="calen">
       <div class="cale"><span>Календарь событий</span></div>
       <div class="cale_main"></div>
       <button @click="link()" class="cale" style="margin-top:20px"><span>Сохраненные события</span></button>
     </div>
     <div class="main_menu" v-if="filter">
       <div class="cale"><span>Сортировка</span></div>
       <div class="filter_main" >
        <h5>Паралелль</h5>
        <div v-for="item in 5" :key="item.id" style="display:flex;align-items:center;margin-top:5px">
          <input type="checkbox" style="margin-right:20px" class="check">{{ item + 6 }}ые классы
        </div>
       </div>
       <button @click="link" class="cale" style="margin-top:20px"><span>Пойск</span></button>
     </div>
   </div>
   <div class="row row-cols-1 row-cols-md-3 g-4 mt-10" style="max-width:1300px">
     <div v-for="item in array" :key="item.id">
       <div class="col">
        <div class="card" style="cursor:pointer;z-index:1" @click.prevent="openUser(item)">
         <div class="card-img-top">
             <h5 class="card-title">{{ item.zag }}</h5>
         </div>
         <div class="card-body">
           <p class="card-text">{{ item.text }}</p>
           <div class="icon" @click="okay()">
             <div :id="item.id" class="norm" width="20px" v-bind:class="{ ok: gog }">
           </div>

         </div>
        </div>
      </div>
     </div>
   </div>
   </div>
  </div>
</template>

<script>
import array from '@/components/array.js'
import Navbar from '@/components/Navbar.vue'
export default {
  data () {
    return{
      array: array,
      gog: false,
      calen: false,
      filter: false,
    }
  },
  components:{
    Navbar
  },
  methods:{
    okay(){
      let i = event.target.id;
      let elem = document.getElementById(i);
      if(this.array[i].state == false){
        elem.classList.add('ok');
        this.array[i].state = true
      }
      else{
        elem.classList.remove('ok');
        this.array[i].state = false;
      }

    },
    hoh(){
      if(this.filter == true){
        this.filter = false;
        this.calen = !this.calen;
      }
      else {
        this.calen = !this.calen;
      }
    },
    kok(){
      if (this.calen == true) {
        this.calen = false;
        this.filter = !this.filter;
      }
      else {
        this.filter = !this.filter;
      }
    },
    openUser(item) {
      this.$router.push('/id')
    },
  }
}
</script>

<style lang="css" scoped>
body{
  width: 100%;
  height: 100%;
  background-color: #E2E9FF;
  font-family: Neucha;
  font-size: calc( (100vw - 480px)/(1280 - 480) * (24 - 16) + 16px);
  max-width: 1500px;
}
.container{
  max-width: 100%;
  display: flex;
  flex-direction: column;
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
}
.row{
  width: 90%;
  margin-top:20px;
}
.norm{
  background: url('@/assets/star.png');
  width: 20px;
  height: 20px;
  background-size: cover;
  z-index: 2;
}
.ok{
  background: url('@/assets/starF.png');
  width: 20px;
  height: 20px;
  background-size: cover;
  z-index: 2;
}
.icon{
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  z-index: 4;
}
.menu{
  width: 100%;
  display: flex;
  justify-content: flex-start;
  position: relative;
}
.main_menu{
  background: #C6D4FF;
  border: 1px solid #616161;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  z-index: 10;
  margin-top: -10px
}
.cale{
  width: auto;
  border-radius: 10px;
  border: 2px solid black;
  width: 250px;
  height: 35px;
  background-color: white;
  margin-bottom: 0px;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content:center;
  padding: 0px 3px;
}
.cale_main{
  width: 250px;
  height: 250px;
  background-color: white;
  margin-top: 20px;
  border: 1px solid black;
}
span{
  margin-top: 2px;
}
.filter_main{
  width: 100%;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.check{
  width: 20px;
  height: 20px;
  margin-top: -5px;
  border-radius: 0px;
  border: 1px solid black;
}
@media (max-width: 650px) {
  .row{
    margin-top: -10px;
  }
}
</style>
