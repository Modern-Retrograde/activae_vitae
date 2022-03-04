<template lang="html">
  <div class="container">
    <h2 style="text-align:center">Добро пожаловать на Activae Vitae! <br>Заполните все поля, чтобы зарегистрировать <br> новый аккаунт</h2>
    <input type="text" name="name" placeholder="Фамилия Имя Отчество">
    <input type="text" name="password" placeholder="Пароль">
    <input type="text" name="password" placeholder="Повторите пароль">
    <input type="text" name="Email" placeholder="Электронная почта">
    <input type="text" name="name" placeholder="Занимаемая должность">
    <nuxt-link to="/login" class="in">Войти</nuxt-link>
    <button type="button" name="button">Зарегистрироваться</button>
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
  width: 100%;
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
