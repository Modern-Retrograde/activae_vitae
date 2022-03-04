<template lang="html">
  <div class="main">
  <div class="avBlock">
    <div class="avatar top"></div>
  </div>
    <div class="cont">
      <div class="icons">
        <img @click="ActionName()" src="@/assets/cale.svg" width="60px" style="cursor:pointer">
        <img @click="kek()" src="@/assets/sort.svg" class="icon" width="60px" style="cursor:pointer">
      </div>
      <form>
       <input type="text" placeholder="Пойск события.." id="before" >
       <a href="#" style="text-decoration:none;color:black;z-index:2;  margin-left:-50px;">
         <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
         </svg>
       </a>
      </form>
      <div class="icons lo">
        <button type="button" name="button" style="margin-right:20px;">Зарегистрироваться</button>
      </div>
      <div class="avatar bot"></div>
    </div>
  </div>
</template>

<script>
export default {
  methods:{
    ActionName(){
      this.$emit('toggle');
    },
    kek(){
      this.$emit('hool')
    },
  }
}
</script>

<style lang="css" scoped>
.avBlock{
  width: 100%;
  display: flex;
  justify-content: end;
}
.top{
  display: none;
}
.main{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.cont{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100px;
  border-bottom: 1px solid #000000;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
input{
  position: relative;
  background: #FFFFFF;
  border:none;
  width: 95%;
  height: 49.81px;
  font-size: 18px;
  padding: 0 20px;
  z-index: 1;
}
form{
  flex-grow: 4;
  display: flex;
  flex-direction: row;
  justify-content:center;
  align-items: center;
}
a{
  position: relative;
}
.icon{
  margin-left: 15px;
}
.icons{
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-basis: 10%;
}
button{
  width: 250px;
  height: 50px;
  border: none;
  background-color: white;
  font-size: 20px;
  border-radius: 12px;
}
.avatar{
  width: 60px;
  height: 60px;
  border-radius: 50px;
  border: 2px solid black;
}
@media (max-width: 1000px) {
  input{
    width: 85%;
  }
  button{
    width: 200px;
  }
}
@media (max-width: 762px) {
  input{
    width: 90%;
  }
  button{
    display: none;
  }
  .lo{
    display: none;
  }
}
@media (max-width: 450px) {
  .icon{
    display: none;
  }
  .bot{
    margin-top: -170px;
    display: none;
  }
  input{
    width: 95%;
    height: 35px;
    font-size: 13px;
    margin-top: 3px;
  }
  svg{
    width: 20px;
    height: 20px;
    margin-top: 5px;
    margin-left: 20px;
  }
  img{
    width: 40px;
  }
  .container{
    height: 70px;
    margin-top: -20px;
  }
  .main{
    height: 70px;
  }
  .top{
    display: block;
    width: 40px;
    height: 40px;
  }
  .avBlock{
    width: 100%;
    height: 60px;
    display: flex;
    justify-content: end;
    margin-top: -45px;
  }
}

</style>
