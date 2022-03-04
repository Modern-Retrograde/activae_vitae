<template lang="html">
  <div class="cont">
    <div class="navbar">
      <nuxt-link class="arrow" to="/main"></nuxt-link>
      <h4></h4>
      <div class="star"></div>
    </div>
    <div class="main">
      <div class="profile">
        <div class="avatar"></div>
        <h2 class="name">Иван стас стасов</h2>
      </div>
      <div class="buttons">
        <button>Создать мероприятие</button>
        <button>Cменить аккаунт</button>
      </div>
      <div class="myEvents">
        <h2>Мои события</h2>
      </div>
    </div>
  </div>
</template>

<script>
export default {
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
.profile{
  display: flex;
  flex-direction: column;
  align-items:center;
}
.avatar{
  width: 300px;
  height: 300px;
  border: 2px solid black;
  border-radius: 200px;
}
.name{
  margin-top: 20px;
}
.buttons{
  display: flex;
  flex-direction: row;
  align-items: center;
}
button{
  border: none;
  border-radius: 12px;
  font-size: 20px;
  margin-top: 20px;
  background-color: white;
  width: 283px;
  height: 60px;
  margin: 10px;
}
.myEvents{
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}
@media (max-width: 675px) {
  .buttons{
    flex-direction: column;
    align-items: center;
  }
}
</style>
