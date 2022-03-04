<template lang="html">
  <div class="cont">
    <div class="navbar">
      <nuxt-link class="arrow" to="/main"></nuxt-link>
      <h4>Мои события</h4>
      <div class="star"></div>
    </div>
    <div class="row row-cols-1 row-cols-md-3 g-4 mt-10" style="max-width:1300px">
      <div v-for="item in array" :key="item.id">
        <div class="col">
         <div class="card" style="cursor:pointer;z-index:1">
          <div class="card-img-top" @click.prevent="openUser(item)">
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
export default {
  data(){
    return{
      array:[
        {
          id:0,
          zag: "Даотфварщафщвр",
          text: "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        },
        {
          id:1,
          zag: "Замоскворецкая линия",
          text: "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        },
        {
          id:2,
          zag: "Арбатско-Покровская линия",
          text: "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
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
</style>
