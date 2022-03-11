<template lang="html">
  <div class="container">
    <h2 style="text-align:center">Добро пожаловать на Activae Vitae! <br><br> Войдите пожалуйста в ваш аккаунт</h2>
    <input type="text" name="name" placeholder="Логин">
    <input type="text" name="password" placeholder="Пароль">
    <nuxt-link to="/" class="in">Зарегистрироваться</nuxt-link>
    <button type="button" name="button">Войти</button>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css">
.container{
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 99px;
  font-weight: 400;
}
input{
  margin-top: 32px;
  background: #FFFFFF;
  border:none;
  width: 387px;
  height: 49.81px;
  font-size: 18px;
  padding: 0 20px;
}
.in{
  margin-top:37px;
  text-decoration:none;
  color:black;
  font-size:22px
}
button{
  width: 283px;
  height: 85px;
  border: none;
  background-color: white;
  font-size: 25px;
  margin-top: 19px;
  border-radius: 12px;
  margin-bottom: 161px;
}
@media (max-width: 600px) {
  .container{
    width: 100%;
    margin-top: 40px;
  }
}
@media (max-width: 420px) {
  h2{
    font-size: 20px;
  }
  input{
    width: 300px;
    height: 40px;
  }
  button{
    width: 200px;
    height: 40px;
    border: none;
    font-size: 20px;
  }
}
</style>
