<template lang="html">
  <div class="cont">
   <div class="mainCont">
     <div class="navbar">
       <nuxt-link class="arrow" to="/main"></nuxt-link>
       <h4></h4>
       <div class="star"></div>
     </div>
     <div class="main">
       <div class="headerBlock">
         <div class="twoInpBlock">
           <input type="text" name="name">
           <input type="text" name="password">
         </div>
         <button type="button" class="but">Прикрепить фотографии</button>
       </div>
       <textarea class="bigInput">
         Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
       </textarea>
       <div class="button_block">
         <button type="button" class="but">Изменить мероприятие</button>
       </div>
     </div>
   </div>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css" scoped>
body{
    max-width: 1500px;
}
.cont{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.mainCont{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1500px;
}
.main{
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin-top: -30px;
}
.headerBlock{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 70%;
  align-items: flex-end;
}
input{
  margin-top: 32px;
  background: #FFFFFF;
  border:none;
  width: 280px;
  height: 50px;
  font-size: 18px;
  padding: 0 20px;
}
.twoInpBlock{
  display: flex;
  flex-direction: column;
  justify-content: space-around;
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
.but{
  border: none;
  border-radius: 12px;
  font-size: 20px;
  margin-top: 20px;
  background-color: white;
  width: 283px;
  height: 60px;
}
.bigInput{
  width: 70%;
  min-height: 400px;
  margin-top: 32px;
  background: #FFFFFF;
  padding: 10px;
  border:none;
}
.button_block{
  width: 70%;
  display: flex;
  justify-content: flex-start;
  margin-bottom: 150px;
}
@media (max-width: 857px) {
  .headerBlock{
    flex-direction: column;
    align-items: center;
    width: 100%;
  }
  .twoInpBlock{
    width: 100%;
  }
  input{
    width: 90%;
  }
  .but{
    width: 200px;
    height: 50px;
  }
  .bigInput{
    width: 90%;
  }
  .button_block{
    width: 100%;
    justify-content: center;
  }
}
</style>
